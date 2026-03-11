import os
import sys
import textwrap
from datetime import datetime

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_dir)


from src.state import State  # noqa: E402


class GenerateReport:
    def __init__(self) -> None:
        pass

    def run(self, state: State):

        summary = f"""# Target Company: {state["target_company"]}
        ---

        ### Company Profile
        * **Industry:** {state["target_company_profile"].industry}
        * **Core Product/Service:** {state["target_company_profile"].core_product_service}
        * **Company Type:** {state["target_company_profile"].company_type}
        * **Company Maturity:** {state["target_company_profile"].company_maturity}
        * **Primary Revenue Model:** {state["target_company_profile"].primary_revenue_model}

        ---

        ### Job Details
        * **Job Title:** {state["job_posting_details"].job_title}
        * **Salary:** {state["job_posting_details"].salary}

        **Description:**
        {state["job_posting_details"].job_description}

        **Minimum Qualifications:**
        {state["job_posting_details"].minimum_qualifications}

        **Preferred Qualifications:**
        {state["job_posting_details"].preferred_qualifications}

        **Skills and Experience:**
        {state["job_posting_details"].skills_experience}

        **Benefits:**
        {state["job_posting_details"].benefits.replace(";", "\n* ")}

        ---

        ### Industry Analysis
        * **Industry:** {state["industry_research"]}

        ---

        *Report generated on: {datetime.now().strftime("%Y-%m-%d")}*"""

        # ###########################################################################

        # summary_debug = f"""# Target Company: {state["target_company"]}
        # ---

        # ### Company Profile
        # * **Industry:** {state["target_company_profile"]}

        # ---

        # ### Job Details
        # * **Job Title:** {state["job_posting_details"].job_title}
        # * **Salary:** {state["job_posting_details"].salary}

        # **Description:**
        # {state["job_posting_details"].job_description}

        # **Minimum Qualifications:**
        # {state["job_posting_details"].minimum_qualifications}

        # **Preferred Qualifications:**
        # {state["job_posting_details"].preferred_qualifications}

        # **Skills and Experience:**
        # {state["job_posting_details"].skills_experience}

        # **Benefits:**
        # {state["job_posting_details"].benefits.replace(";", "\n* ")}

        # ---

        # ### Industry Analysis
        # * **Industry:** {state["industry_research"]}

        # ---

        # *Report generated on: {datetime.now().strftime("%Y-%m-%d")}*"""

        return {"final_report": textwrap.dedent(summary).strip()}
