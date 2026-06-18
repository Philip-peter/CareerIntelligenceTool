import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../../../"))
sys.path.append(root_dir)

from src.tools.web_search_providers import tavily  # noqa: E402

# initalize web search tool
web_tool = tavily.TavilyResearchTool()
