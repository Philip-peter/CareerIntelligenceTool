import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../../"))
sys.path.append(root_dir)

from src.tools.job_search_providers import theirstack  # noqa: E402

__all__ = ["theirstack"]
