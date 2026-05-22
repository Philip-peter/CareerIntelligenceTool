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

        for job_analysis in final_analysis:
            recommendation = job_analysis.get("recommendation", {})
            formatted_report = f"""
            ---

            # Job Analysis Report
            **Job ID:** `{job_analysis["job_id"]}`

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

        # summary = ""
        # final_analysis = state.get("aggregated_analysis", "No report generated")

        # for report in final_analysis:
        #     for j_id, job_data in report.items():
        #         formatted_report = f"""
        #         ---

        #         # Job Analysis Report
        #         **Job ID:** `{j_id}`

        #         ---

        #         ## Job Details
        #         | Field | Details |
        #         |---|---|
        #         | **Title** | {job_data.get("job", {}).get("job_title", "No Data Available")} |
        #         | **Posting** | {job_data.get("job", {}).get("job_posting_link", "No Data Available")} |

        #         ## Company Details
        #         **Company Name: {job_data.get("company", {}).get("company_name", "No Data Available")}
        #         **Industry: {job_data.get("company", {}).get("company_industry", "No Data Available")}
        #         **Company Official Site: {job_data.get("company", {}).get("company_official_url", "No Data Available")}
        #         **Company LinkedIn Site: {job_data.get("company", {}).get("company_linkedin_url", "No Data Available")}

        #         ---

        #         ## Leadership Analysis

        #         **1. CEO Tenure**
        #         {job_data.get("leadership", {}).get("ceo_tenure", "No Data Available")}

        #         **2. Founder Involvement**
        #         {job_data.get("leadership", {}).get("founder_involvement", "No Data Available")}

        #         **3. Strategic Pivots**
        #         {job_data.get("leadership", {}).get("strategic_pivots", "No Data Available")}

        #         **4. Executive Reputation**
        #         {job_data.get("leadership", {}).get("executive_reputation", "No Data Available")}

        #         **5. Leadership Stability**
        #         {job_data.get("leadership", {}).get("leadership_stability", "No Data Available")}

        #         **6. Employee Treatment During Hardship**
        #         {job_data.get("leadership", {}).get("employee_treatment_during_hardship", "No Data Available")}

        #         **7. Management Style and Culture**
        #         {job_data.get("leadership", {}).get("management_style_and_culture", "No Data Available")}

        #         **8. Vision and Communication Clarity**
        #         {job_data.get("leadership", {}).get("vision_and_communication_clarity", "No Data Available")}

        #         **9. DEI and Values Commitment**
        #         {job_data.get("leadership", {}).get("dei_and_values_commitment", "No Data Available")}

        #         **10. Employee Development Investment**
        #         {job_data.get("leadership", {}).get("employee_development_investment", "No Data Available")}

        #         ---

        #         ## Industry Analysis

        #         **1. Cyclic or Defensive**
        #         {job_data.get("industry", {}).get("cyclic_or_defensive", "No Data Available")}

        #         **2. Regulatory Environment**
        #         {job_data.get("industry", {}).get("regulatory_environment", "No Data Available")}

        #         **3. AI Disruption**
        #         {job_data.get("industry", {}).get("ai_distruption", "No Data Available")}

        #         **4. Competition**
        #         {job_data.get("industry", {}).get("competition", "No Data Available")}

        #         **5. Industry Growth Trajectory**
        #         {job_data.get("industry", {}).get("industry_growth_trajectory", "No Data Available")}

        #         **6. Consolidation and MA Risk**
        #         {job_data.get("industry", {}).get("consolidation_and_ma_risk", "No Data Available")}

        #         **7. Offshore and Automation Risk**
        #         {job_data.get("industry", {}).get("offshoring_and_automation_risk", "No Data Available")}

        #         ---

        #         ## Financial Analysis

        #         **1. Revenue Growth**
        #         {job_data.get("finance", {}).get("revenue_growth", "No Data Available")}

        #         **2. Debt**
        #         {job_data.get("finance", {}).get("debt", "No Data Available")}

        #         **3. Cash Flow**
        #         {job_data.get("finance", {}).get("cash_flow", "No Data Available")}

        #         **4. Revenue Concentration**
        #         {job_data.get("finance", {}).get("revenue_concentration", "No Data Available")}

        #         **5. Investor Sentiment**
        #         {job_data.get("finance", {}).get("investor_sentiment", "No Data Available")}

        #         **6. Funding and Runway**
        #         {job_data.get("finance", {}).get("funding_and_runway", "No Data Available")}

        #         **7. Financial Distress Signals**
        #         {job_data.get("finance", {}).get("financial_distress_signals", "No Data Available")}

        #         ---

        #         ## Workforce Analysis

        #         **1. Layoff History**
        #         {job_data.get("workforce", {}).get("layoff_history", "No Data Available")}

        #         **2. Hiring Trends**
        #         {job_data.get("workforce", {}).get("hiring_trends", "No Data Available")}

        #         **3. Executive Turnover**
        #         {job_data.get("workforce", {}).get("executive_turnover", "No Data Available")}

        #         **4. Employee Sentiment**
        #         {job_data.get("workforce", {}).get("employee_sentiments", "No Data Available")}

        #         **5. Labor Disputes**
        #         {job_data.get("workforce", {}).get("labor_disputes", "No Data Available")}

        #         **6. Remote and Flexibility Policy**
        #         {job_data.get("workforce", {}).get("remote_and_flexibility_policy", "No Data Available")}

        #         **7. Compensation and Benefits**
        #         {job_data.get("workforce", {}).get("compensation_and_benefits", "No Data Available")}

        #         **8. Headcount Trajectory**
        #         {job_data.get("workforce", {}).get("headcount_trajectory", "No Data Available")}

        #         **9. Employee Tenure and Retention**
        #         {job_data.get("workforce", {}).get("employee_tenure_and_retention", "No Data Available")}

        #         ---

        #         *Report generated: {datetime.now().strftime("%Y-%m-%d")}*

        #         """

        #         summary += formatted_report

        return {"final_report": textwrap.dedent(summary).strip()}
