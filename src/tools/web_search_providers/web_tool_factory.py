import os
import sys
from enum import Enum

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

from config import cfg  # noqa: E402
from src.tools.web_search_providers import exa, tavily  # noqa: E402


class WebTool(str, Enum):
    TAVILY = "tavily"
    EXA = "exa"


class WebSearchFactory:
    @staticmethod
    def create_web_tool(web_tool: WebTool | None = None):

        # use global preferred llm provider if None
        provider = web_tool or cfg.PREFERRED_WEB_SEARCH_PROVIDER

        match provider:
            case WebTool.TAVILY:
                return tavily.TavilyResearchTool(api_key=cfg.TAVILY_API_KEY)
            case WebTool.EXA:
                return exa.ExaWebSearchTool(api_key=cfg.EXA_API_KEY)
            case _:
                raise ValueError(f"Unsupported Web Search Provider: {provider}")
