import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../../../"))
sys.path.append(root_dir)

from src.tools.job_search_providers import theirstack  # noqa: E402
from src.tools.llm_providers import llm_factory  # noqa: E402
from src.tools.web_search_providers import web_tool_factory  # noqa: E402

# initialize tools
job_search_tool = theirstack.TheirStack()
web_search_tool = web_tool_factory.WebSearchFactory.create_web_tool()
llm_tool = llm_factory.LlmFactory.create_llm()

# tool registry
TOOLS_REGISTRY = {
    "job_search_tool": job_search_tool,
    "web_search_tool": web_search_tool,
    "llm_tool": llm_tool,
}
