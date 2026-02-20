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


class Industry:
    def __init__(self) -> None:
        pass

    @staticmethod
    def queries_template(company_name):
        return [
            {
                "topic": "cyclic_or_defensive",
                "query": f"[{company_name}] is it cyclical or defensive analyst commentary recession sensitivity operating margin volatility",
            },
            {
                "topic": "regulatory_environment",
                "query": f"[{company_name}] regulatory risks 10-K risk factors site:sec.gov compliance requirements government oversight industry regulation impact on revenue",
            },
            {
                "topic": "ai_distruption",
                "query": f"[{company_name}] AI integration strategy R&D spending AI capex competitive positioning",
            },
            {
                "topic": "competition",
                "query": f"[{company_name}] gross margin trend vs competitors pricing power switching costs network effects",
            },
        ]

    async def run_research(
        self, state: State, config: RunnableConfig
    ) -> Dict[str, Any]:
        # make new copy of queries template
        working_queries: List[Dict[str, Any]] = copy.deepcopy(
            self.queries_template(company_name=state["target_company"])
        )
        web_research_tool = config.get("configurable", {}).get("web_search_tool")
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
        asyncio.gather(*task)

        new_data = {r["topic"]: r["researched_data"] for r in working_queries}

        updated_industry_research = state["industry_research"].model_copy(
            update=new_data
        )
        return {"industry_research": updated_industry_research}
