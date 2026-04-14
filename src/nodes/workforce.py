import asyncio
import os
import sys
from typing import Any, Dict

from langchain_core.runnables import RunnableConfig

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

from src.models import WorkforceContextModels  # noqa: E402
from src.state import State  # noqa: E402


class Workforce:
    def _generate_queries_template(self, grounding_data):
        name = grounding_data["company_name"]
        domain = grounding_data["company_domain"]
        industry = grounding_data["company_industry"]

        # Clean domain for site filtering
        clean_domain = (
            domain.replace("https://", "").replace("http://", "").split("/")[0]
            if domain
            else ""
        )

        return [
            {
                "topic": "layoff_history",
                # Focuses on news and layoff trackers like 'layoffs.fyi' or 'Warn Act' notices
                "query": f'"{name}" (layoff OR "headcount reduction" OR "RIF" OR "restructuring") 2024..2026',
            },
            {
                "topic": "hiring_trends",
                # site: search on their careers page and LinkedIn to gauge growth velocity
                "query": f'site:{clean_domain}/careers OR site:linkedin.com/jobs "{name}" "hiring" expansion',
            },
            {
                "topic": "executive_turnover",
                # Targeting press releases and professional news regarding C-suite exits
                "query": f'"{name}" "executive departure" OR "resignation" (CFO OR CTO OR COO OR CMO) 2025 2026',
            },
            {
                "topic": "employee_sentiments",
                # Forcing exact matches on review platforms for current sentiment
                "query": f'site:glassdoor.com OR site:indeed.com "{name}" "reviews" "CEO approval" 2025 2026',
            },
            {
                "topic": "labor_disputes",
                # Helpful for industrial/workforce grounding: unions and legal friction
                "query": f'"{name}" {industry} "union" OR "strike" OR "labor dispute" OR "unfair labor practice"',
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

    async def run_research(self, inputs: Dict, state: State, config: RunnableConfig):

        # distpatch_job from router agent
        dispatch_job = inputs["job"]

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
        ### ROLE
        You are a Corporate Intelligence Analyst specializing in organizational health and workforce dynamics. Your goal is to synthesize raw web search data into structured insights.

        ### ANALYTICAL GUIDELINES
        1. **Identify Patterns:** Don't just list events; identify trends (e.g., "multiple rounds of layoffs" vs "a single restructuring").
        2. **Contextualize Signals:** Label findings as "stability signals," "risk signals," or "growth signals" based on the provided examples.
        3. **Handle Missing Data:** Use exactly "No data available" if the search results do not provide enough information for a specific field.
        4. **Source Integrity:** Prioritize information from the last 2-3 years as specified in the schema.

        ### OUTPUT REQUIREMENT
        Return a single JSON object that strictly follows the provided schema. Do not include markdown formatting or conversational text outside the JSON.
        """

        user_prompt = f"""
        ### TASK
        Analyze the provided web search results to populate the Workforce Context Model for the target company: : {grounding.get("company_name")}

        ### Schema Fields to Populate:
        1. layoff_history: Freq/scale of layoffs (e.g., 'Meta conducted multiple large layoffs in 2022-2023')
        2. hiring_trends: Expansion vs. freeze signals (e.g., 'Rapid AI hiring surge at NVIDIA')
        3. executive_turnover: Stability of CFO/CTO/COO (e.g., 'Multiple CFO changes in 2 years - risk signal')
        4. employee_sentiments: Glassdoor/public sentiment (e.g., 'Low morale complaints during restructuring')

        ### Raw Search Results:
        {web_research}
        """

        llm_response = await llm_analyzer_tool.run(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            output_schema=WorkforceContextModels,
        )

        formatted_results = {
            "job_id": job.get("job_id"),
            "agent_type": "workforce",
            "data": llm_response.model_dump(),
        }

        # wrap formatted_result in list for applying reducer in agent_analysis state
        return {"agent_analysis": [formatted_results]}
