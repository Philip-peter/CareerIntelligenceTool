import os
import sys

from langchain_core.runnables import RunnableConfig

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

from src.models import TargetJobDetails  # noqa: E402
from src.nodes.job_listing.theirstack import theirstack_provider  # noqa: E402
from src.state import State  # noqa: E402


class JobPostingResearch:
    async def fetch_recent_jobs(self, state: State, config: RunnableConfig):
        # fetch recent jobs
        recent_jobs = theirstack_provider.fetch_jobs()
        result = {"job_posting_raw": recent_jobs}
        return {"raw_research": result}

    async def normalize_job(self, state: State, config: RunnableConfig):
        # normalize jobs
        normalized_jobs = theirstack_provider.normalize_jobs()
        return {"job_posting_details": normalized_jobs}
