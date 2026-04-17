import operator
import os
import sys
from typing import Annotated, Dict, List, TypedDict

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

from src.models import (  # noqa: E402
    # ApplicantModel,
    JobPostingModel,
)


class State(TypedDict):
    # applicant_profile: ApplicantModel
    raw_jobs: List
    job_queue: List[JobPostingModel]
    agent_analysis: Annotated[List[Dict], operator.add]
    # final_report: str
