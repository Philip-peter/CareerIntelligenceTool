import os
import sys
from datetime import datetime

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_dir)

from src.state import State  # noqa: E402


class GenerateReport:
    def __init__(self) -> None:
        pass

    def run(self, state: State):
        # summarize report
        summary = f"""
        # Target Company: {state["target_company"]}
        ---

        ### Job Details
        **Job Title:** {state["job_posting_details"].job_title}
        **Job Description:** {state["job_posting_details"].job_description}
        **Minimum Qualifications:** {state["job_posting_details"].minimum_qualifications}
        **Preferred Qualifications:** {state["job_posting_details"].preferred_qualifications}
        **Skills and Experience:** {state["job_posting_details"].skills_experience}
        **Benefits:** {state["job_posting_details"].benefits}
        **Salary:** {state["job_posting_details"].salary}

        ---

        ### Company Profile
        **Job Profile:** {state["target_company_profile"]}

        ---

        *Report generated on: {datetime.now().strftime("%Y-%m-%d")}*
        """

        return {"final_report": summary}
