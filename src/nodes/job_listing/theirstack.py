import os
import sys

import requests

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../../"))
sys.path.append(root_dir)

from job_provider_interface import JobProviderInterface  # noqa: E402

from config import cfg  # noqa: E402


class TheirStack(JobProviderInterface):
    def __init__(self) -> None:
        super().__init__()
        self.api_key = cfg.THEIRSTACK_API_KEY
        self.api_url = cfg.THEIRSTACK_API_URL

    def fetch_jobs(self):
        body = """{
          "page": 0,
          "limit": 25,
          "job_country_code_or": [
            "US"
          ],
          "posted_at_max_age_days": 7
        }"""

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        try:
            response = requests.request(
                method="POST",
                url=self.api_url,
                data=body,
                headers=headers,
                verify=False,
            )
            response.raise_for_status()
            return
        except Exception as e:
            print(f"Encountered error during 'fetch_jobs' operation. Error: {e}")
