import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(root_dir)

from src.models import ApplicantModel  # noqa: E402


class ApplicantProfile:
    pass

    # TODO: Validate User Input
    # TODO: Execute once and persist data
    def init_candidate_profile(self):
        current_company = input("CURRENT COMPANY: ")
        currently_employed = input("CURRENTLY EMPLOYED: ")
        current_role = input("CURRENT ROLE: ")
        current_job_tenure = input("CURRENT JOB TENURE: ")
        risk_tolerance = int(input("RISK TOLERANCE: "))
        career_stage = input("CAREER STAGE: ")
        career_priority = input("CAREER PRIORITY: ")

        applicant_data = {
            "current_company": current_company,
            "currently_employed": currently_employed,
            "current_role": current_role,
            "current_job_tenure": current_job_tenure,
            "risk_tolerance": risk_tolerance,
            "career_stage": career_stage,
            "career_priority": career_priority,
        }

        return ApplicantModel(**applicant_data)

    def update_candidate_profile(self):
        pass


# applicant profile instance
my_applicant_profile = ApplicantProfile()
