import asyncio
import os
import sys
from typing import Any, Dict

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

from src.models import FinancialContextModels  # noqa: E402
from src.prompts import finance_prompts  # noqa: E402
from src.search_queries import QUERY_REGISTRY  # noqa: E402
from src.search_queries.registry import render_queries  # noqa: E402
from src.state import SubAgentState  # noqa: E402
from src.tools import TOOLS_REGISTRY  # noqa: E402


class FinancialData:
    def __init__(self) -> None:
        # initiate tools
        self.web_search_tool = TOOLS_REGISTRY["web_search_tool"]
        self.llm_tool = TOOLS_REGISTRY["llm_tool"]

    async def _run_web_research(self, grounding_data) -> Dict[str, Any]:

        # generate web search query for finance agent from query registry
        working_queries = render_queries(
            agent="finance", grounding=grounding_data, registry=QUERY_REGISTRY
        )

        async def process_query(item: Dict[str, Any]):
            """Utility function for performing web search for each query"""
            query = item.get("query")
            # search
            web_search = await self.web_search_tool.search(query=query)
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

    async def run_research(self, state: SubAgentState):

        # distpatch job data from router agent
        dispatch_job = state["job"]
        job_info = dispatch_job["job_data"]
        grounding = dispatch_job["grounding_data"]

        web_research = await self._run_web_research(grounding_data=grounding)

        system_prompt = finance_prompts.FINANCE_SYSTEM_PROMPT

        user_prompt = finance_prompts.build_finance_user_prompt(
            grounding=grounding, job_info=job_info, web_research=web_research
        )

        llm_response = await self.llm_tool.run_with_schema(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            output_schema=FinancialContextModels,
        )

        # validate pydantic model
        validated_llm_response = FinancialContextModels.model_validate(llm_response)

        formatted_results = {
            "job_id": job_info.get("job_id"),
            "agent_type": "finance",
            "data": validated_llm_response.model_dump(),
        }

        # wrap formatted_result in list for applying reducer in agent_analysis state
        return {"agent_analysis": [formatted_results]}
