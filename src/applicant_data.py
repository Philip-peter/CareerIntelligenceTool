import os
import sys
from typing import List

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(root_dir)

from src.models import UserPreferenceModel, UserProfileModels  # noqa: E402


class ApplicantData:
    def dummy_user_preferences(self):
        """Synthetic user profile and preferences for testing"""

        applicant_profile = {
            "current_company": "Dayforce",
            "current_company_official_url": "https://www.dayforce.com/ca",
            "current_company_linkedin_url": "https://linkedin.com/company/dayforce/",
        }

        applicant_preferences = {
            "preferred_job_roles": ["security engineer", "cloud security"],
            # "salary_expectations": 140000.0,
            "desired_work_location": ["US"],
            "desired_employment_status": ["full_time"],
            "desired_work_arrangement": "remote",
            "career_switch_motivation": "compensation",
        }

        # pydantic model validate
        user_profile = UserProfileModels.model_validate(applicant_profile)
        user_preference = UserPreferenceModel.model_validate(applicant_preferences)

        # convert to dict
        user_profile = user_profile.model_dump(mode="json")
        user_preference = user_preference.model_dump(mode="json")

        return user_profile, user_preference

    def init_candidate_profile(self):
        """Capture users input and returns user profile and preference objects"""
        current_company = input("CURRENT COMPANY: ")
        current_company_official_url = input("CURRENT COMPANY URL: ")
        current_company_linkedin_url = input("CURRENT COMPANY LINKEDIN: ")
        preferred_job_roles = input(
            "PREFERRED JOB ROLES [seperate multiple preferred jobs using comma]: "
        )
        salary_expectations = float(input("SALARY EXPECTATION [hint: float]: "))
        desired_work_country = input("DESIRED LOCATION [hint: US, CA, GB]: ")
        desired_employment_status = input(
            "DESIRED EMPLOYMENT STATUS [hint: full_time, part_time, contract]: "
        )
        desired_work_arrangement = input(
            "DESIRED WORK ARRANGEMENT [hint: remote, hybrid]: "
        )
        career_switch_motivation = input(
            "CAREER SWITCH PRIORITY [hint: compensation, growth, stability, work_life_balance, impact, prestige]: "
        )

        applicant_profile = {
            "current_company": current_company,
            "current_company_official_url": current_company_official_url,
            "current_company_linkedin_url": current_company_linkedin_url,
        }

        applicant_preferences = {
            "preferred_job_role": preferred_job_roles.split(
                ","
            ),  # convert comma seperated strings to List[str]
            "salary_expectations": salary_expectations,
            "desired_work_country": List[desired_work_country],  # convert to a list
            "desired_employment_status": List[
                desired_employment_status
            ],  # convert to a list
            "desired_work_arrangement": desired_work_arrangement,
            "career_switch_motivation": career_switch_motivation,
        }

        # pydantic model validate
        user_profile = UserProfileModels.model_validate(applicant_profile)
        user_preference = UserPreferenceModel.model_validate(applicant_preferences)

        # convert to dict
        user_profile = user_profile.model_dump(mode="json")
        user_preference = user_preference.model_dump(mode="json")

        return user_profile, user_preference


# applicant profile instance
my_applicant_data = ApplicantData()
