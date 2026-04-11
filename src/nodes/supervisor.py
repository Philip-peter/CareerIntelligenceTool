import hashlib
import os
import sys

from langgraph.constants import Send

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

from src.state import State  # noqa: E402


class Supervisor:
    @staticmethod
    def _generate_job_id(company_name, job_title):
        """Generates a deterministic ID based on company and title."""
        input_string = f"{company_name}-{job_title}".lower().replace(" ", "")
        # Returns the first 12 characters of a SHA-256 hash
        return hashlib.sha256(input_string.encode()).hexdigest()[:12]

    def process_jobs(self, state: State):
        sends = []

        # fetch job_queue
        job_queue = state["job_queue"]

        for job in job_queue:
            # generate job id
            job_id = self._generate_job_id(
                company_name=job.company_name, job_title=job.job_title
            )

            # set dispatch job
            dispatch_job = {
                "job_data": {
                    "job_id": job_id,
                    "job_title": job.job_title,
                    "job_posting_link": job.job_posting_link,
                    "job_description": job.job_description,
                },
                "grounding_data": {
                    "company_name": job.company_name,
                    "company_domain": job.company_domain,
                    "company_official_url": job.company_url,
                    "company_linkedin_url": job.company_linkedin_url,
                    "company_industry": job.company_industry,
                },
            }

            # update the node names after refactoring the nodes
            # sends.append(Send("industry_web_search", {"job": dispatch_job}))
            # sends.append(Send("leadership_web_search", {"job": dispatch_job}))
            # sends.append(Send("workforce_web_search", {"job": dispatch_job}))
            # sends.append(Send("finance_web_search", {"job": dispatch_job}))
        return sends
