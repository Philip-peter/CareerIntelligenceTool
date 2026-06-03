import os
import sys
import textwrap
from datetime import datetime

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_dir)


from src.state import State  # noqa: E402


class GenerateReport:
    def run(self, state: State):

        summary = ""
        final_analysis = state.get("synthesis_results", "No report generated")

        # TO DO - Removed Job Description, re-evaluate later
        for job_analysis in final_analysis:
            # current_company_profile = job_analysis.get("current_company_profile", {})
            prospect_company_profile = job_analysis.get("prospect_company_profile", {})
            recommendation = job_analysis.get("recommendation", {})

            formatted_report = f"""
            ---

            # Job Analysis Report
            **Job ID:** `{job_analysis["job_id"]}`

            ---

            ## Prospect Job Data

            **Job Title:** {prospect_company_profile.get("job_title")}
            **Job Link:** {prospect_company_profile.get("job_posting_link")}
            **Job Salary:** {prospect_company_profile.get("job_salary")}
            **Job Hiring Team:** {"\n".join(prospect_company_profile.get("job_hiring_team", "No data available"))}

            ---

            ## Prospect Company Profile

            **Company:** {prospect_company_profile.get("company_name")}
            **Company Industry:** {prospect_company_profile.get("company_industry")}
            **Company Website:** {prospect_company_profile.get("company_official_url")}
            **Company LinkedIn:** {prospect_company_profile.get("company_linkedin_url")}

            ---

            ## Category Scorecards

            **Prospect Leadership Analysis Score: {recommendation.get("leadership_score_prospect", "N/A")}::::Current Leadership Analysis Score: {recommendation.get("leadership_score_current", "N/A")}**
            **Prospect Industry Analysis Score: {recommendation.get("industry_score_prospect", "N/A")}::::Current Industry Analysis Score: {recommendation.get("industry_score_current", "N/A")}**
            **Prospect Financial Analysis Score: {recommendation.get("financial_score_prospect", "N/A")}::::Current Leadership Analysis Score: {recommendation.get("financial_score_current", "N/A")}**
            **Prospect Workforce Analysis Score: {recommendation.get("workforce_score_prospect", "N/A")}::::Current Workforce Analysis Score: {recommendation.get("workforce_score_current", "N/A")}**

            ---

            ##Flag Summaries

            **🔴 Red Flags (Prospect)**:
                {"\n".join(recommendation.get("red_flags", "None"))}**
            **🟡 Watch Items (Prospect)**:
                {"\n".join(recommendation.get("watch_items", "None"))}
            **🟢 Green Flags (Prospect)**:
                {"\n".join(recommendation.get("green_flags", "None"))}

            ---

            ##Head-to-Head Comparison

            **{recommendation.get("head_to_head_summary", "None")}**

            ---

            ##Final Recommendation

            **Recommendation:** {recommendation.get("recommendation", "None")}
            **Confidence Level:** {recommendation.get("confidence_level", "None")}
            **Deciding Factor:** {recommendation.get("deciding_factor", "None")}


            ---

            *Report generated: {datetime.now().strftime("%Y-%m-%d")}*

            """

            summary += formatted_report

        return {"final_report": textwrap.dedent(summary).strip()}
