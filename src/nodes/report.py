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
            pass

        summary = f"""
        ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        JOB ID: {final_analysis}
        ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        *Report generated on: {datetime.now().strftime("%Y-%m-%d")}*"""

        return {"final_report": textwrap.dedent(summary).strip()}
