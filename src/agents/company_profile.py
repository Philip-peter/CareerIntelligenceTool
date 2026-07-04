import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

from src.state import SubAgentState  # noqa: E402


class CompanyProfile:
    async def run_research(self, state: SubAgentState):

        # distpatch_job from router agent
        dispatch_job = state["job"]

        # extract grounding and job data from supervisor Send payload
        job = dispatch_job["job_data"]
        grounding = dispatch_job["grounding_data"]

        # TO DO: Need to modify
        company_profile = {
            "company_name": grounding.get("company_name", "Not Available"),
            "company_domain": grounding.get("company_domain", "Not Available"),
            "company_official_url": grounding.get(
                "company_official_url", "Not Available"
            ),
            "company_linkedin_url": grounding.get(
                "company_linkedin_url", "Not Available"
            ),
            "company_industry": grounding.get("company_industry", "Not Available"),
        }

        formatted_results = {
            "job_id": job.get("job_id"),
            "agent_type": "company",
            "data": company_profile,
        }

        return {"agent_analysis": [formatted_results]}
