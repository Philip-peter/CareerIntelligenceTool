import asyncio
import copy
import os
import sys
from typing import Any, Dict, List

from langchain_core.runnables import RunnableConfig

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

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
            search_result = await web_research_tool.search(query=query, topic="news")
            researched_urls = [r["url"] for r in search_result]
            # extract
            research_data = await web_research_tool.extract(
                query=query, researched_urls=researched_urls
            )
            item["researched_urls"] = researched_urls
            item["researched_data"] = research_data
            return item

        task = [process_query(q) for q in working_queries]
        result = await asyncio.gather(*task, return_exceptions=True)

        new_data = {
            r["topic"]: r["researched_data"]
            for r in result
            if not isinstance(r, (Exception, BaseException))
        }

        updated_leadership_research = state["leadership_research"].model_copy(
            update=new_data
        )
        return {"leadership_research": updated_leadership_research}
