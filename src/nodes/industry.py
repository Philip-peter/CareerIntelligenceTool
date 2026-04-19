import asyncio
import os
import sys
from typing import Any, Dict

from langchain_core.runnables import RunnableConfig

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

from src.models import IndustryContextModels  # noqa: E402
from src.state import SubAgentState  # noqa: E402


class Industry:
    def _generate_queries_template(self, grounding_data):
        name = grounding_data["company_name"]
        domain = grounding_data["company_domain"]
        industry = grounding_data["company_industry"]

        # Clean domain (remove http/www)
        clean_domain = (
            domain.replace("https://", "").replace("http://", "").split("/")[0]
        )

        return [
            {
                "topic": "cyclic_or_defensive",
                # We add the industry to the query to help the search engine contextualize the 'cyclical' nature
                "query": f'"{name}" {industry} analyst commentary "cyclical or defensive" recession sensitivity operating margin',
            },
            {
                "topic": "regulatory_environment",
                # Still using site:sec.gov but adding the specific company name for 10-K extraction
                "query": f'site:sec.gov "{name}" regulatory risks risk factors compliance "government oversight"',
            },
            {
                "topic": "ai_disruption",
                # Prioritize the official domain to see what THEY say about AI vs what news says
                "query": f'site:{clean_domain} AI integration strategy R&D spending "AI capex"',
            },
            {
                "topic": "competition",
                # Search for the company name and industry keywords specifically focused on pricing power
                "query": f'"{name}" {industry} "gross margin trend" competitors pricing power switching costs',
            },
        ]

    async def _run_web_research(
        self, grounding_data, web_research_tool
    ) -> Dict[str, Any]:

        # generate web search query
        working_queries = self._generate_queries_template(grounding_data=grounding_data)

        async def process_query(item: Dict[str, Any]):
            query = item.get("query")
            # search
            web_search = await web_research_tool.search(query=query, topic="general")
            item["researched_data"] = web_search
            return item

        task = [process_query(q) for q in working_queries]
        all_processed_task = await asyncio.gather(*task, return_exceptions=True)

        researched_data_by_topic = {
            r["topic"]: r["researched_data"]
            for r in all_processed_task
            if not isinstance(r, (Exception, BaseException))
        }

        return researched_data_by_topic

    async def run_research(self, state: SubAgentState, config: RunnableConfig):

        # distpatch_job from router agent
        dispatch_job = state["job"]

        # extract grounding and job data from supervisor Send payload
        job = dispatch_job["job_data"]
        grounding = dispatch_job["grounding_data"]

        # initiate web search tool
        web_research_tool = config.get("configurable", {}).get("web_research_tool")
        if not web_research_tool:
            raise ValueError("web search tool is not configured")

        # run web search
        web_research = self._run_web_research(
            grounding_data=grounding, web_research_tool=web_research_tool
        )

        # initiate llm analysis
        llm_analyzer_tool = config.get("configurable", {}).get("llm_summarizer")
        if not llm_analyzer_tool:
            raise ValueError("llm analyzer tool is not configured")

        system_prompt = """
        You are a Senior Equity Research Analyst specializing in industrial organization and strategic moat analysis. Your task is to synthesize raw web search data into a structured industry profile.

        ### Guidelines:
        - **Evidence-Based:** Base every claim on the provided search results. If the data is conflicting, highlight the consensus.
        - **Specifics Over Generalities:** Use concrete examples (e.g., mention specific regulators like the FDA or specific competitors like ASML).
        - **Nuance:** Distinguish between "cyclical" and "defensive" by referencing historical performance during downturns if available.
        - **Strict Output:** You must output valid JSON that conforms to the provided schema. Do not include introductory text or conversational filler.
        """

        user_prompt = f"""
        ### Task
        Analyze the following search results for the company: {grounding.get("company_name")}.
        Extract and synthesize information into the JSON format specified by the IndustryContextModels schema.

        ### Schema Fields to Populate:
        1. **cyclic_or_defensive**: Classify the industry type and cite recession performance.
        2. **regulatory_environment**: Detail oversight levels, compliance costs, and specific agencies.
        3. **ai_distruption**: Evaluate AI as a threat (headwind) or opportunity (tailwind).
        4. **competition**: Map the landscape, including market share, moats, and key rivals.

        ### Raw Search Results:
        {web_research}

        ### Response Format:
        Return ONLY a JSON object. If information for a field is entirely missing from the text, use the default: "No data available".
        """

        llm_response = await llm_analyzer_tool.run(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            output_schema=IndustryContextModels,
        )

        formatted_results = {
            "job_id": job.get("job_id"),
            "agent_type": "industry",
            "data": llm_response.model_dump(),
        }

        # wrap formatted_result in list for applying reducer in agent_analysis state
        return {"agent_analysis": [formatted_results]}
