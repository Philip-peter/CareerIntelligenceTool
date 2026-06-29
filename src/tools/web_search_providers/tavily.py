import asyncio
import os
import sys
from typing import Any, Dict, List, Literal, Union

from tavily import AsyncTavilyClient

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

from config import cfg  # noqa: E402
from src.tools.web_search_providers import basewebsearchprovider  # noqa: E402


class TavilyResearchTool(basewebsearchprovider.BaseWebSearchProvider):
    def __init__(self) -> None:
        # async tavily client
        self.tavily_async_client = AsyncTavilyClient(api_key=cfg.TAVILY_API_KEY)

    async def search(self, query) -> str:
        # set async ratelimit thresold
        search_ratelimit = asyncio.Semaphore(cfg.WEB_SEARCH_RATE_LIMIT)

        # search
        async with search_ratelimit:
            try:
                response = await self.tavily_async_client.search(
                    query=query,
                    search_depth="basic",  # options: basic, advanced, fast, ultra-fast
                    topic="general",  # options: news, general, finance
                    max_results=cfg.WEB_SEARCH_MAX_RESULT,
                )

                relevant_result = ", ".join(
                    [r.get("content") for r in response["results"]]
                )
                return relevant_result

            except Exception as e:
                print(f"Encountered error during web search: \n[tavily tool] -> {e}")
                return "No search results"

    async def extract(
        self,
        query,
        research_urls: Union[str, List[str]],
        extract_depth: Literal["basic", "advanced"] = "advanced",
        chunks_per_source: int = cfg.TAVILY_CHUNK_SIZE,
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
            print(f"Encountered error during taviliy extract: {e}")
            return []

    async def crawl(self, url: str, instructions: str) -> List[Dict[str, Any]]:
        try:
            response = await self.tavily_async_client.crawl(
                url=url,
                instructions=instructions,
                chunks_per_source=cfg.TAVILY_CHUNK_SIZE,
            )
            return response["results"]
        except Exception as e:
            print(f"Encountered error during taviliy crawl: {e}")
            return []
