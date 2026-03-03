import os
import sys
from datetime import datetime

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_dir)

from src.state import State  # noqa: E402


class GenerateReport:
    def __init__(self) -> None:
        pass

    def summarize(self, state: State):
        # summarize report
        summary = f"""
        # Target Company: {state["target_company"]}
        ---

        ### Job Details
        **Job Title:**
        **Job Description:**
        **Minimum Qualifications:**
        **Preferred Qualifications:**
        **Skills and Experience:**
        **Benefits:**
        **Salary:**

        ---
        *Report generated on: {datetime.now().strftime("%Y-%m-%d")}*
        """

        return {"final_report": summary}
