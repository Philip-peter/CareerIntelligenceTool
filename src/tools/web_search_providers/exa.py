import asyncio
import json
import os
import sys

from exa_py import AsyncExa

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

from config import cfg  # noqa: E402
from src.tools.web_search_providers import basewebsearchprovider  # noqa: E402


class ExaWebSearchTool(basewebsearchprovider.BaseWebSearchProvider):
    def __init__(self) -> None:
        super().__init__()

        # initialize exa
        self.exa_async_client = AsyncExa(api_key=cfg.EXA_API_KEY)

    async def search(
        self,
        query: str,
    ):

        # set async ratelimit thresold
        search_ratelimit = asyncio.Semaphore(cfg.WEB_SEARCH_RATE_LIMIT)

        async with search_ratelimit:
            try:
                response = await self.exa_async_client.search(
                    query=query,
                    type="auto",  # instant, fast, auto, deep-lite, deep, deep-reasoning
                    category="company",  # company, research paper, news, personal site, financial report, people
                    num_results=cfg.WEB_SEARCH_MAX_RESULT,
                    moderation=True,
                )

                # convert exa serachresponse object to dict
                response_dict = json.loads(
                    json.dumps(response, default=lambda o: o.__dict__)
                )

                relevant_result = ", ".join(
                    [r.get("text") for r in response_dict["results"]]
                )

                return relevant_result

            except Exception as e:
                print(f"Encountered error during web search: \n[exa tool] -> {e}")
                return "No search results"
