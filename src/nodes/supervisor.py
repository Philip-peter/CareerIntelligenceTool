import os
import sys

from langgraph.constants import Send

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

from src.state import State  # noqa: E402


class Supervisor:
    def process_jobs(self, state: State):
        sends = []

        job_queue = state["job_queue"]

        for job in job_queue:
            sends.append(Send("industry_web_search", {"job": job}))
            sends.append(Send("leadership_web_search", {"job": job}))
            sends.append(Send("workforce_web_search", {"job": job}))
            sends.append(Send("finance_web_search", {"job": job}))
        return sends
