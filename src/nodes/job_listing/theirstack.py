import os
import sys

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../../"))
sys.path.append(root_dir)

from config import cfg  # noqa: E402

from . import job_provider_interface  # noqa: E402


class TheirStack(job_provider_interface.JobProviderInterface):
    def __init__(self) -> None:
        super().__init__()
        self.api_key = cfg.THEIRSTACK_API_KEY
        self.api_url = cfg.THEIRSTACK_API_URL
        self.preferred_jobs = [
            "security engineer",
            # "detection and response",
            # "cloud security",
            # "infrastructure security",
            # "security analyst",
            # "detection and response",
        ]
        self.preferred_location = [
            # "US",
            "CA",
            # "GB",
        ]
        # self.job_seniority = [
        #     "staff",
        #     "senior",
        #     "mid-level",
        # ]
        # self.minimum_salary = 120000
        self.preferred_job_board = ["linkedin.com"]
        self.preferred_employment_status = [
            "full_time",
            "part_time",
            "temporary",
            "contract",
        ]

    def fetch_jobs(self):
        payload = {
            "page": 0,  # research how to use pagination
            "limit": 1,  # theirstack max limit < -- currently experimental
            "job_title_or": self.preferred_jobs,
            "job_country_code_or": self.preferred_location,
            "posted_at_max_age_days": 30,
            # "job_seniority_or": self.job_seniority,
            # "min_salary_usd": self.minimum_salary,
            "url_domain_or": self.preferred_job_board,
            "employment_statuses_or": self.preferred_employment_status,
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        try:
            response = requests.request(
                method="POST",
                url=self.api_url,
                json=payload,
                headers=headers,
                verify=False,
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Encountered error during 'fetch_jobs' operation. Error: {e}")


theirstack_provider = TheirStack()
