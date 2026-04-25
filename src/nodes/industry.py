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
        # Dispatch job from router agent
        dispatch_job = state["job"]

        # Extract grounding and job data
        job_info = dispatch_job["job_data"]
        grounding = dispatch_job["grounding_data"]

        # Tool initialization
        web_research_tool = config.get("configurable", {}).get("web_research_tool")
        llm_analyzer_tool = config.get("configurable", {}).get("llm_summarizer")

        if not web_research_tool or not llm_analyzer_tool:
            raise ValueError("Required tools (search or llm) are not configured")

        # Run web search
        web_research = await self._run_web_research(
            grounding_data=grounding, web_research_tool=web_research_tool
        )

        # Anchor Context: Define the Company Sector and Niche
        industry_anchor = f"""
        TARGET ENTITY:
        - Company: {grounding.get("company_name")}
        - Reported Industry: {grounding.get("company_industry")}
        - Domain: {grounding.get("company_domain")}

        JOB CONTEXT:
        - Position: {job_info.get("job_title")}
        - Context: Analyzing industry forces relevant to this role.
        """

        system_prompt = """
        You are a Senior Equity Research Analyst specializing in Industrial Organization and Strategic Moat Analysis.
        Your task is to synthesize raw web search data and company grounding into a structured industry profile.

        ### Strategic Framework:
        1. **Contextual Filtering**: Use the 'TARGET ENTITY' details to ensure search results are relevant to the specific sector (e.g., distinguish between 'Cloud Computing' and 'Enterprise Software' if applicable).
        2. **Moat Assessment**: Look for evidence of high switching costs, network effects, or cost advantages.
        3. **AI Impact**: Categorize AI as a structural shift. Is it an existential threat to the current business model or a margin-expanding tool?
        4. **Consensus & Conflict**: If different sources disagree on market share or regulatory outlook, provide the most reputable or consensus-based view.
        """

        user_prompt = f"""
        ### Company & Industry Grounding:
        {industry_anchor}

        ### Web Research Results:
        {web_research}

        ### Analysis Task:
        Perform a deep-dive industry analysis for {grounding.get("company_name")} based on the research results.
        Populate the IndustryContextModels schema focusing on:

        1. **cyclic_or_defensive**: Classify the industry type and cite historical performance during economic cycles.
        2. **regulatory_environment**: Identify specific oversight agencies (e.g., FTC, SEC, GDPR) and compliance burdens.
        3. **ai_distruption**: Evaluate AI as a headwind (threat) or tailwind (opportunity).
        4. **competition**: Map the landscape, identify key rivals, and describe the 'moat' (competitive advantage).

        Return ONLY a JSON object. Use "No data available" if the research is insufficient.
        """

        # Run llm analysis
        llm_response = await llm_analyzer_tool.run(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            output_schema=IndustryContextModels,
        )

        formatted_results = {
            "job_id": job_info.get("job_id"),
            "agent_type": "industry",
            "data": llm_response.model_dump(),
        }

        return {"agent_analysis": [formatted_results]}
