import asyncio
import os
import sys
from typing import Any, Dict

from langchain_core.runnables import RunnableConfig

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

from src.models import IndustryContextModels  # noqa: E402
from src.prompts import industry_prompts  # noqa: E402
from src.search_queries import INDUSTRY_QUERIES  # noqa: E402
from src.search_queries.registry import render_queries  # noqa: E402
from src.state import SubAgentState  # noqa: E402


class Industry:
    async def _run_web_research(
        self, grounding_data, web_research_tool
    ) -> Dict[str, Any]:

        # generate web search query
        working_queries = render_queries(
            agent="industry", grounding=grounding_data, registry=INDUSTRY_QUERIES
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

        system_prompt = industry_prompts.INDUSTRY_SYSTEM_PROMPT

        user_prompt = industry_prompts.build_industry_user_prompt(
            grounding=grounding, job_info=job_info, web_research=web_research
        )

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
