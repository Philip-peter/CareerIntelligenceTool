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

        summary = f"""# TARGET COMPANY: {state["target_company"]}
        ====================================================================================

        ### COMPANY PROFILE
        * **Industry:** {state["target_company_profile"].industry}
        * **Core Product/Service:** {state["target_company_profile"].core_product_service}
        * **Company Type:** {state["target_company_profile"].company_type}
        * **Company Maturity:** {state["target_company_profile"].company_maturity}
        * **Primary Revenue Model:** {state["target_company_profile"].primary_revenue_model}

        ====================================================================================

        ### JOB DETAILS
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

        ====================================================================================

        ### INDUSTRY ANALYSIS
        * **Cyclic or Defensive:** {state["industry_research"].cyclic_or_defensive}
        * **AI destruption:** {state["industry_research"].ai_distruption}
        * **Competition:** {state["industry_research"].competition}
        * **Regulatory environment:** {state["industry_research"].regulatory_environment}

        ====================================================================================

        ### LEADERSHIP ANALYSIS
        * **CEO Tenure:** {state["leadership_research"].ceo_tenure}
        * **Founder Involvement:** {state["leadership_research"].founder_involvement}
        * **Strategic Pivots:** {state["leadership_research"].strategic_pivots}
        * **Insider Behavior:** {state["leadership_research"].insider_behavior}

        ====================================================================================

        ### WORKFORCE ANALYSIS
        * **Layoff History:** {state["workforce_research"].layoff_history}
        * **Hiring Trends:** {state["workforce_research"].hiring_trends}
        * **Executive Turnover:** {state["workforce_research"].executive_turnover}
        * **Employee Sentiments:** {state["workforce_research"].employee_sentiments}

        ====================================================================================

        *Report generated on: {datetime.now().strftime("%Y-%m-%d")}*"""

        return {"final_report": textwrap.dedent(summary).strip()}
