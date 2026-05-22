import operator
import os
import sys
from typing import Annotated, Any, Dict, List, TypedDict

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

from src.models import JobPostingModel  # noqa: E402


# Sub Agent State
class SubAgentState(TypedDict):
    job: Dict


# Overall State
class State(TypedDict):
    applicant_profile: dict
    applicant_preference: dict
    raw_jobs: List
    job_queue: List[JobPostingModel]
    agent_analysis: Annotated[List[Dict[str, Any]], operator.add]
    aggregated_analysis: Annotated[List[Dict[str, Any]], operator.add]
    synthesis_results: Annotated[List[Dict[str, Any]], operator.add]
    final_report: str
