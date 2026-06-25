import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

# from src.models import JobRoleContextModels  # noqa: E402
from src.state import SubAgentState  # noqa: E402


class Job:
    async def run_research(self, state: SubAgentState):

        # distpatch_job from router agent
        dispatch_job = state["job"]

        # extract job data from supervisor Send payload
        job = dispatch_job["job_data"]

        # TO DO: Need to modify
        job_profile = {
            "job_title": job.get("job_title", "Not Available"),
            "job_posting_link": job.get("job_posting_link", "Not Available"),
            "job_description": job.get("job_description", "Not Available"),
            "job_salary": job.get("job_salary", "Not Available"),
            "job_hiring_team": job.get("job_hiring_team", "Not Available"),
        }

        formatted_results = {
            "job_id": job.get("job_id"),
            "agent_type": "job",
            "data": job_profile,
        }

        return {"agent_analysis": [formatted_results]}
