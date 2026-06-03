import os
import sys

import httpx

# import requests
# import urllib3

# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../../"))
sys.path.append(root_dir)

from config import cfg  # noqa: E402

from . import job_provider_interface  # noqa: E402


class TheirStack(job_provider_interface.JobProviderInterface):
    def __init__(self, user_preferences: dict) -> None:
        super().__init__()
        self.api_key = cfg.THEIRSTACK_API_KEY
        self.api_url = cfg.THEIRSTACK_API_URL
        self.preferred_jobs = user_preferences.get("preferred_job_roles")
        self.preferred_location = user_preferences.get("desired_work_location")
        # self.minimum_salary = user_preferences.get("salary_expectations")
        self.preferred_job_board = ["linkedin.com"]
        self.preferred_employment_status = user_preferences.get(
            "desired_employment_status"
        )

    async def fetch_jobs(self):
        payload = {
            "page": 0,  # research how to use pagination
            "limit": 1,  # theirstack max limit < -- currently experimental
            "job_title_or": self.preferred_jobs,
            "job_country_code_or": self.preferred_location,
            "posted_at_max_age_days": 30,
            # "min_salary_usd": self.minimum_salary,
            "url_domain_or": self.preferred_job_board,
            "employment_statuses_or": self.preferred_employment_status,
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

        # try:
        #     response = requests.request(
        #         method="POST",
        #         url=self.api_url,
        #         json=payload,
        #         headers=headers,
        #         verify=False,
        #     )
        #     response.raise_for_status()
        #     return response.json()
        # except Exception as e:
        #     print(f"Encountered error during 'fetch_jobs' operation. \nError: {e}")
