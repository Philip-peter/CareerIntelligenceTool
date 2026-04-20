import os
import sys

from langchain_core.runnables import RunnableConfig

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

# from src.models import TargetJobDetails  # noqa: E402
from src.models import JobPostingModel  # noqa: E402
from src.nodes.job_listing.theirstack import theirstack_provider  # noqa: E402
from src.state import State  # noqa: E402


class JobScanner:
    # async def fetch_dummy_jobs(self, state: State):

    #     # mock api response
    #     mock_api_response = [
    #         {
    #             "id": 657542775,
    #             "job_title": "Security Engineer (Bangkok Based, Relocation Support)",
    #             "url": "https://ca.linkedin.com/jobs/view/security-engineer-bangkok-based-relocation-support-at-agoda-4376307656",
    #             "date_posted": "2026-04-05",
    #             "has_blurred_data": False,
    #             "company": "Agoda",
    #             "location": "Toronto, Ontario",
    #             "state_code": "ON",
    #             "latitude": 43.70643,
    #             "longitude": -79.39864,
    #             "remote": False,
    #             "hybrid": False,
    #             "country": "Canada",
    #             "country_code": "CA",
    #             "seniority": "mid_level",
    #             "company_domain": "careersatagoda.com",
    #             "employment_statuses": ["full_time"],
    #             "technology_slugs": [
    #                 "amazon-web-services",
    #                 "google-cloud-platform",
    #                 "terraform",
    #                 "kubernetes",
    #                 "golang",
    #                 "typescript",
    #             ],
    #             "description": "**About Agoda**\nAt Agoda, we bridge the world through travel...",
    #             "company_object": {
    #                 "id": "C5sZVlVBHF5TNbFoUy0KibuRpW8hRGPTLOx3F13wnAbefzqmxetCKWLRg35EosiU",
    #                 "name": "Agoda",
    #                 "domain": "careersatagoda.com",
    #                 "industry": "Software Development",
    #                 "employee_count": 11183,
    #                 "url": "https://careersatagoda.com",
    #                 "linkedin_url": "https://www.linkedin.com/company/agoda/",
    #                 "is_recruiting_agency": False,
    #                 "technology_slugs": ["python", "react", "kubernetes", "terraform"],
    #             },
    #             "locations": [
    #                 {
    #                     "id": 6167865,
    #                     "name": "Toronto",
    #                     "state": "Ontario",
    #                     "country_name": "Canada",
    #                 }
    #             ],
    #         },
    #         # 2. Nexus Tech (Mock Startup)
    #         {
    #             "id": 700123456,
    #             "job_title": "Senior Backend Engineer (Python/FastAPI)",
    #             "url": "https://www.linkedin.com/jobs/view/senior-backend-engineer-at-nexus-tech-700123456",
    #             "date_posted": "2026-04-06",
    #             "has_blurred_data": False,
    #             "company": "Nexus Tech",
    #             "location": "San Francisco, California",
    #             "state_code": "CA",
    #             "latitude": 37.7749,
    #             "longitude": -122.4194,
    #             "remote": True,
    #             "hybrid": False,
    #             "min_annual_salary": 160000,
    #             "max_annual_salary": 210000,
    #             "salary_currency": "USD",
    #             "country": "USA",
    #             "country_code": "US",
    #             "seniority": "senior_level",
    #             "company_domain": "nexustech.io",
    #             "employment_statuses": ["full_time"],
    #             "technology_slugs": [
    #                 "python",
    #                 "fastapi",
    #                 "postgresql",
    #                 "docker",
    #                 "aws",
    #             ],
    #             "description": "**About Nexus Tech**\nNexus Tech is a leading fintech startup...",
    #             "company_object": {
    #                 "id": "NEXUS123456789",
    #                 "name": "Nexus Tech Inc.",
    #                 "domain": "nexustech.io",
    #                 "industry": "Financial Services",
    #                 "employee_count": 150,
    #                 "yc_batch": "W18",
    #                 "total_funding_usd": 45000000,
    #                 "is_recruiting_agency": False,
    #             },
    #             "locations": [
    #                 {
    #                     "id": 5391959,
    #                     "name": "San Francisco",
    #                     "state": "California",
    #                     "country_name": "United States",
    #                 }
    #             ],
    #         },
    #         # 3. Anthropic (Real Company Mock)
    #         {
    #             "id": 998877665,
    #             "job_title": "Member of Technical Staff - AI Safety & Alignment",
    #             "url": "https://www.linkedin.com/jobs/view/mts-ai-safety-at-anthropic-998877665",
    #             "date_posted": "2026-04-07",
    #             "has_blurred_data": False,
    #             "company": "Anthropic",
    #             "location": "San Francisco, California",
    #             "state_code": "CA",
    #             "latitude": 37.77493,
    #             "longitude": -122.41942,
    #             "remote": False,
    #             "hybrid": True,
    #             "min_annual_salary": 250000,
    #             "max_annual_salary": 450000,
    #             "salary_currency": "USD",
    #             "country": "United States",
    #             "country_code": "US",
    #             "seniority": "senior_level",
    #             "company_domain": "anthropic.com",
    #             "employment_statuses": ["full_time"],
    #             "technology_slugs": [
    #                 "python",
    #                 "pytorch",
    #                 "jax",
    #                 "rust",
    #                 "kubernetes",
    #                 "aws",
    #             ],
    #             "description": "**About Anthropic**\nAnthropic is an AI safety and research company...",
    #             "company_object": {
    #                 "id": "ANT-55667788",
    #                 "name": "Anthropic",
    #                 "domain": "anthropic.com",
    #                 "industry": "Artificial Intelligence",
    #                 "employee_count": 500,
    #                 "total_funding_usd": 7300000000,
    #                 "linkedin_url": "https://www.linkedin.com/company/anthropicresearch/",
    #                 "is_recruiting_agency": False,
    #                 "funding_stage": "Series C",
    #             },
    #             "locations": [
    #                 {
    #                     "id": 5391959,
    #                     "name": "San Francisco",
    #                     "state": "California",
    #                     "country_name": "United States",
    #                 }
    #             ],
    #         },
    #     ]

    #     # store in state
    #     result = {"job_posting_raw": mock_api_response}
    #     return {"raw_research": result}

    async def fetch_recent_jobs(self, state: State, config: RunnableConfig):
        # fetch recent jobs
        recent_jobs = theirstack_provider.fetch_jobs()

        if not recent_jobs:
            print("No recent jobs found")
            # return empty list
            return {"raw_research": {"job_posting_raw": []}}

        result = recent_jobs.get("data", [])
        return {"raw_jobs": result}

    async def normalize_job(self, state: State, config: RunnableConfig):
        list_of_jobs = []
        recent_jobs = state.get("raw_jobs", [])

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
