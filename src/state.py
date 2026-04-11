import operator
import os
import sys
from operator import or_
from typing import Annotated, Dict, List, TypedDict

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

from src.models import (  # noqa: E402
    # ApplicantModel,
    # FinancialContextModels,
    # IndustryContextModels,
    JobPostingModel,
    # JobRoleContextModels,
    # LeadershipContextModels,
    # WorkforceContextModels,
)


class State(TypedDict):
    # applicant_profile: ApplicantModel
    job_queue: List[JobPostingModel]
    raw_research: Annotated[Dict, or_]
    agent_analysis: Annotated[
        List[Dict], operator.add
    ]  # sample: [{job_id:"", "job_title":"", "industry_analysis":"", "finance_analysis":""}]
    # industry_research: IndustryContextModels
    # finance_research: FinancialContextModels
    # workforce_research: WorkforceContextModels
    # leadership_research: LeadershipContextModels
    # final_report: str
