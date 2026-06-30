import os
import sys

import httpx

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../../"))
sys.path.append(root_dir)

from config import cfg  # noqa: E402

from . import job_provider_interface  # noqa: E402


class TheirStack(job_provider_interface.JobProviderInterface):
    def __init__(self) -> None:
        super().__init__()

        # theirstack credentials
        self.api_key = cfg.THEIRSTACK_API_KEY
        self.api_url = cfg.THEIRSTACK_API_URL

    async def fetch_jobs(self, user_preferences: dict):

        # initiate user preferences
        preferred_jobs = user_preferences.get("preferred_job_roles")
        preferred_location = user_preferences.get("desired_work_location")
        # self.minimum_salary = user_preferences.get("salary_expectations")
        preferred_job_board = ["linkedin.com"]
        preferred_employment_status = user_preferences.get("desired_employment_status")

        payload = {
            "page": 0,  # research how to use pagination
            "limit": 1,  # theirstack max limit < -- currently experimental
            "job_title_or": preferred_jobs,
            "job_country_code_or": preferred_location,
            "posted_at_max_age_days": 60,
            # "min_salary_usd": self.minimum_salary,
            "url_domain_or": preferred_job_board,
            "employment_statuses_or": preferred_employment_status,
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        async with httpx.AsyncClient(verify=False, headers=headers) as client:
            try:
                response = await client.post(url=self.api_url, json=payload)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                # Catches server errors (4xx, 5xx) specifically
                print(
                    f"API returned error status: {e.response.status_code} during 'fetch_jobs'"
                )
                # return {}
            except httpx.RequestError as e:
                # Catches network failures, connection timeouts, DNS issues
                print(
                    f"Network error occurred while reaching {e.request.url} during 'fetch_jobs'"
                )
                # return {}
