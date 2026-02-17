# import asyncio

import os
import sys
from typing import Any, Dict, List, Literal

from tavily import AsyncTavilyClient

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

from config import cfg  # noqa: E402


class TavilyResearchTool:
    def __init__(self) -> None:
        # initiate tavily client
        self.tavily_async_client = AsyncTavilyClient(api_key=cfg.TAVILY_API_KEY)

    async def search(
        self,
        query,
        topic: Literal["news", "general", "finance"] = "general",
        include_raw_content: bool = False,
        include_answer: bool = False,
        search_depth: Literal["basic", "advanced", "fast", "ultra-fast"] = "basic",
        max_results: int = cfg.TAVILY_SEARCH_MAX_RESULT,
        include_domains: List[str] = [],
    ) -> List[Dict[str, Any]]:
        try:
            response = await self.tavily_async_client.search(
                query=query,
                search_depth=search_depth,
                topic=topic,
                include_answer=include_answer,
                include_raw_content=include_raw_content,
                max_results=max_results,
                include_domains=include_domains,
            )

            # filter relevance based on content score
            relevant_result = [res for res in response["result"] if res["score"] >= 0.6]

            # select response with highest relevant score only if relevant_result is empty
            if len(relevant_result) == 0:
                max_score = 0.0
                for res in response["result"]:
                    if res["score"] >= max_score:
                        max_score = res["score"]
                        relevant_result = [res]

            return relevant_result
        except Exception as e:
            print(f"Encountered error during taviliy search: {e}")
            return []

    async def extract(
        self,
        query,
        research_urls: List[str] = [],
        extract_depth: Literal["basic", "advanced"] = "basic",
        chunks_per_source: int = cfg.TAVILY_METHOD_CHUNK_SIZE,
    ) -> List[Dict[str, Any]]:
        try:
            response = await self.tavily_async_client.extract(
                urls=research_urls,
                query=query,
                extract_depth=extract_depth,
                chunks_per_source=chunks_per_source,
            )
            return response["results"]
        except Exception as e:
            print(f"Encountered error during taviliy search: {e}")
            return []
