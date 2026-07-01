import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

from src.models import JobPostingModel  # noqa: E402
from src.state import State  # noqa: E402
from src.tools import TOOLS_REGISTRY  # noqa: E402


class JobScanner:
    def __init__(self) -> None:
        # initiate tools
        self.job_search_tool = TOOLS_REGISTRY["job_search_tool"]

    async def fetch_recent_jobs(self, state: State):

        # load user preference from state
        user_preferences = state["applicant_preference"]

        # fetch recent jobs
        recent_jobs = await self.job_search_tool.fetch_jobs(
            user_preferences=user_preferences
        )

        if not recent_jobs:
            print("No recent jobs found")
            # return empty list
            return {"raw_research": {"job_posting_raw": []}}

        result = recent_jobs.get("data")
        return {"raw_jobs": result}

    async def check_job_results(self, state: State):
        recent_jobs = state.get("raw_jobs")
        if not recent_jobs:
            return "stop_flow"
        return "continue_to_next_agent"

    async def normalize_job(self, state: State):
        list_of_jobs = []
        recent_jobs = state.get("raw_jobs")

        if not recent_jobs:
            raise ValueError("No jobs found, halt further processing")

        for job in recent_jobs:
            extracted_jobs_fields = {}

            extracted_jobs_fields["job_title"] = job.get("job_title", "")
            extracted_jobs_fields["job_posting_link"] = job.get("url", "")
            extracted_jobs_fields["company"] = job.get("company", "")
            extracted_jobs_fields["job_city"] = job.get("location", "")
            extracted_jobs_fields["job_state"] = job.get("state_code", "")
            extracted_jobs_fields["country"] = job.get("country", "")
            extracted_jobs_fields["salary"] = job.get("salary_string", "")
            extracted_jobs_fields["minimum_salary"] = job.get(
                "min_annual_salary_usd", ""
            )
            extracted_jobs_fields["company_domain"] = job.get("company_domain", "")
            extracted_jobs_fields["hiring_team"] = job.get("hiring_team", [])
            extracted_jobs_fields["employment_statuses"] = job.get(
                "employment_statuses", []
            )
            extracted_jobs_fields["job_description"] = job.get("description", "")
            extracted_jobs_fields["company_name"] = job.get("company_object", {}).get(
                "name", ""
            )
            extracted_jobs_fields["company_industry"] = job.get(
                "company_object", {}
            ).get("industry", "")
            extracted_jobs_fields["company_employee_count"] = job.get(
                "company_object", {}
            ).get("employee_count", "")
            extracted_jobs_fields["company_num_jobs"] = job.get(
                "company_object", {}
            ).get("num_jobs", "")
            extracted_jobs_fields["company_url"] = job.get("company_object", {}).get(
                "url", ""
            )
            extracted_jobs_fields["company_linkedin_url"] = job.get(
                "company_object", {}
            ).get("linkedin_url", "")
            extracted_jobs_fields["is_recruiting_agency"] = job.get(
                "company_object", {}
            ).get("is_recruiting_agency", "")
            extracted_jobs_fields["company_founded_year"] = job.get(
                "company_object", {}
            ).get("founded_year", "")
            extracted_jobs_fields["publicly_traded_symbol"] = job.get(
                "company_object", {}
            ).get("publicly_traded_symbol", "")
            extracted_jobs_fields["yc_batch"] = job.get("company_object", {}).get(
                "yc_batch", ""
            )
            extracted_jobs_fields["total_funding_usd"] = job.get(
                "company_object", {}
            ).get("total_funding_usd", "")
            extracted_jobs_fields["last_funding_round_date"] = job.get(
                "company_object", {}
            ).get("last_funding_round_date", "")
            extracted_jobs_fields["last_funding_round_amount_readable"] = job.get(
                "company_object", {}
            ).get("last_funding_round_amount_readable", "")

            # create JobPostingModel instance
            job_data = JobPostingModel(**extracted_jobs_fields)

            # append to list_of_jobs
            list_of_jobs.append(job_data)

        return {"job_queue": list_of_jobs}
