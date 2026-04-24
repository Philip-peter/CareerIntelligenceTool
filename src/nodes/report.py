import os
import sys
import textwrap
from datetime import datetime

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_dir)


from src.state import State  # noqa: E402


class GenerateReport:
    def run(self, state: State):

        final_analysis = state.get("agent_analysis", "No report generated")

        summary = f"""
        ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        {final_analysis}
        ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        *Report generated on: {datetime.now().strftime("%Y-%m-%d")}*"""

        return {"final_report": textwrap.dedent(summary).strip()}
