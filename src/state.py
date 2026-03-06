import os
import sys
from operator import add
from typing import Annotated, Dict, List, TypedDict

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

from src.models import (  # noqa: E402
    CandidateModel,
    FinancialContextModels,
    IndustryContextModels,
    JobRoleContextModels,
    LeadershipContextModels,
    TargetJobDetails,
    WorkforceContextModels,
)


class State(TypedDict):
    candidate: CandidateModel
    target_company: str
    target_company_url: str
    target_company_profile: str
    job_posting_link: str
    raw_research: Annotated[List[Dict[str, str]], add]
    job_posting_details: TargetJobDetails
    job_role_research: JobRoleContextModels
    industry_research: IndustryContextModels
    finance_research: FinancialContextModels
    workforce_research: WorkforceContextModels
    leadership_research: LeadershipContextModels
    final_report: str
