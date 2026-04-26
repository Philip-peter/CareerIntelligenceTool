import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

from src.state import State  # noqa: E402


class Aggregator:
    def aggregate_analysis_result(self, state: State):
        grouped_job_analysis = {}

        agent_analysis = state["agent_analysis"]

        for analysis in agent_analysis:
            job_id = analysis["job_id"]
            if job_id not in grouped_job_analysis:
                grouped_job_analysis[job_id] = {}
            grouped_job_analysis[job_id][analysis["agent_type"]] = analysis["data"]

        return {"aggregated_analysis": [grouped_job_analysis]}
