import os
import sys
from typing import Dict

from langchain_core.runnables import RunnableConfig

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

# from src.models import JobRoleContextModels  # noqa: E402
from src.state import State  # noqa: E402


class Job:
    def run_research(self, inputs: Dict, state: State, config: RunnableConfig):

        # distpatch_job from router agent
        dispatch_job = inputs["job"]

        # extract grounding and job data from supervisor Send payload
        job = dispatch_job["job_data"]
        # grounding = dispatch_job["grounding_data"]

        # TO DO: Need to modify
        job_profile = {
            "job_title": job.get("job_title", "Not Available"),
            "job_posting_link": job.get("job_posting_link", "Not Available"),
        }

        formatted_results = {
            "job_id": job.get("job_id"),
            "agent_type": "job",
            "data": job_profile,
        }

        return {"agent_analysis": [formatted_results]}
