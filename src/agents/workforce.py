import asyncio
import os
import sys
from typing import Any, Dict

from langchain_core.runnables import RunnableConfig

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

from src.models import WorkforceContextModels  # noqa: E402
from src.prompts import workforce_prompts  # noqa: E402
from src.search_queries import WORKFORCE_QUERIES  # noqa: E402
from src.search_queries.registry import render_queries  # noqa: E402
from src.state import SubAgentState  # noqa: E402
from src.tools import web_research_tool  # noqa: E402
from src.tools.llm_providers import llm_tool  # noqa: E402


class Workforce:
    async def _run_web_research(self, grounding_data) -> Dict[str, Any]:

        # generate web search query
        working_queries = render_queries(
            agent="workforce", grounding=grounding_data, registry=WORKFORCE_QUERIES
        )

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

        # dispatch_job from router agent
        dispatch_job = state["job"]

        # extract grounding and job data
        job_info = dispatch_job["job_data"]
        grounding = dispatch_job["grounding_data"]

        # run web search (awaiting to fix the RuntimeWarning)
        web_research = await self._run_web_research(grounding_data=grounding)

        system_prompt = workforce_prompts.WORKFORCE_SYSTEM_PROMPT

        user_prompt = workforce_prompts.build_workforce_user_prompt(
            grounding=grounding, job_info=job_info, web_research=web_research
        )

        llm_response = await llm_tool.run_with_schema(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            output_schema=WorkforceContextModels,
        )

        # validate pydantic model
        validated_llm_response = WorkforceContextModels.model_validate(llm_response)

        formatted_results = {
            "job_id": job_info.get("job_id"),
            "agent_type": "workforce",
            "data": validated_llm_response.model_dump(),
        }

        # wrap formatted_result in list for applying reducer in agent_analysis state
        return {"agent_analysis": [formatted_results]}
