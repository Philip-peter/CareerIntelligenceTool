import os
import sys
from operator import or_
from typing import Annotated, Dict, List, TypedDict

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

from src.models import (  # noqa: E402
    ApplicantModel,
    FinancialContextModels,
    IndustryContextModels,
    JobPostingModel,
    JobRoleContextModels,
    LeadershipContextModels,
    TargetJobDetails,
    WorkforceContextModels,
)


class State(TypedDict):
    applicant_profile: ApplicantModel
    job_queue: ""
    raw_research: Annotated[Dict, or_]
    industry_research: IndustryContextModels
    finance_research: FinancialContextModels
    workforce_research: WorkforceContextModels
    leadership_research: LeadershipContextModels
    final_report: str
    # --------------------------------------
    target_company: str
    target_company_url: str
    job_posting_details: TargetJobDetails
    job_role_research: JobRoleContextModels
