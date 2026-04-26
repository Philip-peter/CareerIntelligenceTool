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
        final_analysis = state.get("aggregated_analysis", "No report generated")

        for report in final_analysis:
            for j_id, job_data in report.items():
                formatted_report = f"""
                ---

                # Job Analysis Report
                **Job ID:** `{j_id}`

                ---

                ## Job Details
                | Field | Details |
                |---|---|
                | **Title** | {job_data.get("job", {}).get("job_title", "N/A")} |
                | **Posting** | {job_data.get("job", {}).get("job_posting_link", "N/A")} |

                ---

                ## Leadership Analysis

                **1. CEO Tenure**
                {job_data.get("leadership", {}).get("ceo_tenure", "N/A")}

                **2. Founder Involvement**
                {job_data.get("leadership", {}).get("founder_involvement", "N/A")}

                **3. Insider Behavior**
                {job_data.get("leadership", {}).get("insider_behavior", "N/A")}

                **4. Executive Reputation**
                {job_data.get("leadership", {}).get("executive_reputation", "N/A")}

                ---

                ## Industry Analysis

                **1. Cyclic or Defensive**
                {job_data.get("industry", {}).get("cyclic_or_defensive", "N/A")}

                **2. Regulatory Environment**
                {job_data.get("industry", {}).get("regulatory_environment", "N/A")}

                **3. AI Disruption**
                {job_data.get("industry", {}).get("ai_distruption", "N/A")}

                **4. Competition**
                {job_data.get("industry", {}).get("competition", "N/A")}

                ---

                ## Financial Analysis

                **1. Revenue Growth**
                {job_data.get("finance", {}).get("revenue_growth", "N/A")}

                **2. Debt**
                {job_data.get("finance", {}).get("debt", "N/A")}

                **3. Cash Flow**
                {job_data.get("finance", {}).get("cash_flow", "N/A")}

                **4. Revenue Concentration**
                {job_data.get("finance", {}).get("revenue_concentration", "N/A")}

                **5. Investor Sentiment**
                {job_data.get("finance", {}).get("investor_sentiment", "N/A")}

                ---

                ## Workforce Analysis

                **1. Layoff History**
                {job_data.get("workforce", {}).get("layoff_history", "N/A")}

                **2. Hiring Trends**
                {job_data.get("workforce", {}).get("hiring_trends", "N/A")}

                **3. Executive Turnover**
                {job_data.get("workforce", {}).get("executive_turnover", "N/A")}

                **4. Employee Sentiment**
                {job_data.get("workforce", {}).get("employee_sentiments", "N/A")}

                **5. Labor Disputes**
                {job_data.get("workforce", {}).get("labor_disputes", "N/A")}

                ---

                *Report generated: {datetime.now().strftime("%Y-%m-%d")}*

                """

                summary += formatted_report

        return {"final_report": textwrap.dedent(summary).strip()}
