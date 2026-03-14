import asyncio
import copy
import os
import sys
from typing import Any, Dict, List

from langchain_core.runnables import RunnableConfig

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

from src.models import LeadershipContextModels  # noqa: E402
from src.state import State  # noqa: E402


class Leadership:
    def __init__(self) -> None:
        pass

    @staticmethod
    def queries_template(company_name):
        return [
            {
                "topic": "ceo_tenure",
                "query": f"[{company_name}] CEO tenure performance track record earnings call transcripts leadership stability sentiment",
            },
            {
                "topic": "founder_involvement",
                "query": f"[{company_name}] founder role board involvement ownership stake voting power dual-class stock structure",
            },
            {
                "topic": "strategic_pivots",
                "query": f"[{company_name}] major business model shifts restructuring history failed expansion exit core products strategy evolution",
            },
            {
                "topic": "insider_behavior",
                "query": f"[{company_name}] SEC Form 4 insider buying selling trends executive share ownership compensation alignment",
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

        result = {"leadership_research_raw": researched_data_by_topic}

        return {"raw_research": result}

    async def run_llm_analysis(self, state: State, config: RunnableConfig):

        llm_analyzer_tool = config.get("configurable", {}).get("llm_summarizer")
        if not llm_analyzer_tool:
            raise ValueError("llm analyzer tool is not configured")

        system_prompt = """
        ### ROLE
        You are a Senior Equity Research Analyst specializing in corporate governance and leadership transitions. Your task is to extract structured leadership insights from provided web search results.

        ### OBJECTIVE
        Analyze the provided text to populate a specific JSON schema. You must maintain high analytical standards, distinguishing between factual data (e.g., tenure years) and market signals (e.g., performance trends).

        ### EXTRACTION RULES
        1.  **Strict Schema Adherence:** Your output must be a single JSON object matching the requested schema exactly.
        2.  **No Data Handling:** If search results do not contain information for a specific field, use the default value: "No data available".
        3.  **Synthesize, Don't Just Copy:** Combine information from multiple search snippets to provide a comprehensive summary for each field.
        4.  **Tone:** Professional, objective, and data-driven.

        ### OUTPUT FORMAT
        Provide only the raw JSON. Do not include conversational filler, markdown code blocks (unless specified), or explanations outside of the JSON structure.
        """

        user_prompt = f"""
        ### Task
        Analyze the following search results for the company: {state["target_company"]}
        Extract leadership context for the company into the JSON format specified by the LeadershipContextModels schema.

        ### Schema Fields to Populate:
        1. **ceo_tenure**: State tenure length and performance impact (improvement/decline).
        2. **founder_involvement**: Describe current roles (leadership/board) and ownership stake.
        3. **strategic_pivots**: Identify major business model shifts and their outcomes.
        4. **insider_behavior**: Analyze recent stock buying/selling trends and executive ownership.

        ### Raw Search Results:
        {state["raw_research"].get("industry_research_raw")}
        """

        llm_response = await llm_analyzer_tool.run(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            output_schema=LeadershipContextModels,
        )

        return {"leadership_research": llm_response}
