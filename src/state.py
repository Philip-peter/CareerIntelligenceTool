import os
import sys
from typing import TypedDict

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

from src.models import (  # noqa: E402
    CandidateModel,
    FinancialContextModels,
    IndustryContextModels,
    JobRoleContextModels,
    LeadershipContextModels,
    WorkforceContextModels,
)


class State(TypedDict):
    candidate: CandidateModel
    target_company: str
    job_posting_link: str
    industry_research: IndustryContextModels
    finance_research: FinancialContextModels
    workforce_research: WorkforceContextModels
    leadership_research: LeadershipContextModels
    job_role_research: JobRoleContextModels
    final_report: str
