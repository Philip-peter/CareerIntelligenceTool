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
            "detection and response",
            "cloud security",
            "infrastructure security",
        ]
        self.preferred_location = [
            "CA",
        ]
        self.job_seniority = [
            "staff",
            "senior",
            "mid-level",
        ]
        self.minimum_salary = 120000
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
            "limit": 25,  # theirstack max limit
            "job_title_or": self.preferred_jobs,
            "job_country_code_or": self.preferred_location,
            "posted_at_max_age_days": 7,
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

    def normalize_jobs(self, *raw_jobs):

        normalized_jobs = []

        for job in raw_jobs:
            desired_job_fields = {}

            desired_job_fields["job_title"] = job.get("job_title", "")
            desired_job_fields["job_posting_link"] = job.get("url", "")
            desired_job_fields["company"] = job.get("company", "")
            desired_job_fields["job_city"] = job.get("location", "")
            desired_job_fields["job_state"] = job.get("state_code", "")
            desired_job_fields["country"] = job.get("country", "")
            desired_job_fields["salary"] = job.get("salary_string", "")
            desired_job_fields["minimum_salary"] = job.get("min_annual_salary_usd", "")
            desired_job_fields["company_domain"] = job.get("company_domain", "")
            desired_job_fields["hiring_team"] = job.get("hiring_team", [])
            desired_job_fields["employment_statuses"] = job.get(
                "employment_statuses", []
            )
            desired_job_fields["job_description"] = job.get("description", "")
            desired_job_fields["company_name"] = job.get("company_object", {}).get(
                "name", ""
            )
            desired_job_fields["company_industry"] = job.get("company_object", {}).get(
                "industry", ""
            )
            desired_job_fields["company_employee_count"] = job.get(
                "company_object", {}
            ).get("employee_count", "")
            desired_job_fields["company_num_jobs"] = job.get("company_object", {}).get(
                "num_jobs", ""
            )
            desired_job_fields["company_url"] = job.get("company_object", {}).get(
                "url", ""
            )
            desired_job_fields["company_linkedin_url"] = job.get(
                "company_object", {}
            ).get("linkedin_url", "")
            desired_job_fields["is_recruiting_agency"] = job.get(
                "company_object", {}
            ).get("is_recruiting_agency", "")
            desired_job_fields["company_founded_year"] = job.get(
                "company_object", {}
            ).get("founded_year", "")
            desired_job_fields["publicly_traded_symbol"] = job.get(
                "company_object", {}
            ).get("publicly_traded_symbol", "")
            desired_job_fields["yc_batch"] = job.get("company_object", {}).get(
                "yc_batch", ""
            )
            desired_job_fields["total_funding_usd"] = job.get("company_object", {}).get(
                "total_funding_usd", ""
            )
            desired_job_fields["last_funding_round_date"] = job.get(
                "company_object", {}
            ).get("last_funding_round_date", "")
            desired_job_fields["last_funding_round_amount_readable"] = job.get(
                "company_object", {}
            ).get("last_funding_round_amount_readable", "")

            normalized_jobs.append(desired_job_fields)

            return normalized_jobs


theirstack_provider = TheirStack()
