import asyncio
import copy
import os
import sys
from typing import Any, Dict, List

from langchain_core.runnables import RunnableConfig

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

from src.models import WorkforceContextModels  # noqa: E402
from src.state import State  # noqa: E402


class Workforce:
    def __init__(self) -> None:
        pass

    @staticmethod
    def queries_template(company_name):
        return [
            {
                "topic": "layoff_history",
                "query": f"{company_name} layoffs headcount reduction 2024 2025 2026 history",
            },
            {
                "topic": "hiring_trends",
                "query": f"{company_name} hiring trends job openings expansion or hiring freeze 2026",
            },
            {
                "topic": "executive_turnover",
                "query": f"{company_name} executive departures turnover CFO CTO COO leadership changes",
            },
            {
                "topic": "employee_sentiments",
                "query": f"{company_name} employee reviews glassdoor sentiment CEO approval rating 2026",
            },
        ]

    async def run_research(self, state: State, config: RunnableConfig):
        # make new copy of queries template
        working_queries: List[Dict[str, Any]] = copy.deepcopy(
            self.queries_template(company_name=state["target_company"])
        )
        web_research_tool = config.get("configurable", {}).get("web_research_tool")
        if not web_research_tool:
            raise ValueError("web search tool is not configured")

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

        result = {"workforce_research_raw": researched_data_by_topic}

        return {"raw_research": result}

    async def run_llm_analysis(self, state: State, config: RunnableConfig):

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
        Analyze the provided web search results to populate the Workforce Context Model for the target company.

        ### Schema Fields to Populate:
        1. layoff_history: Freq/scale of layoffs (e.g., 'Meta conducted multiple large layoffs in 2022-2023')
        2. hiring_trends: Expansion vs. freeze signals (e.g., 'Rapid AI hiring surge at NVIDIA')
        3. executive_turnover: Stability of CFO/CTO/COO (e.g., 'Multiple CFO changes in 2 years - risk signal')
        4. employee_sentiments: Glassdoor/public sentiment (e.g., 'Low morale complaints during restructuring')

        ### Raw Search Results:
        {state["raw_research"].get("industry_research_raw")}
        """

        llm_response = await llm_analyzer_tool.run(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            output_schema=WorkforceContextModels,
        )

        return {"workforce_research": llm_response}
