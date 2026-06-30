import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../../../"))
sys.path.append(root_dir)

from src.tools.web_search_providers import web_tool_factory  # noqa: E402

__all__ = ["web_tool_factory"]
