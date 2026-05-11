import os
import sys

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
            "salary_expectations": 140000.0,
            "desired_work_location": {
                "country": "Canada",
                "city_state": "Ontario",
            },
            "desired_employment_status": "fulltime",
            "desired_work_arrangement": "remote",
            "career_switch_motivation": "compensation",
        }

        return UserProfileModels(**applicant_profile), UserPreferenceModel(
            **applicant_preferences
        )

    def init_candidate_profile(self):
        """Capture users input and returns user profile and preference objects"""
        current_company = input("CURRENT COMPANY: ")
        current_company_official_url = input("CURRENT COMPANY URL: ")
        current_company_linkedin_url = input("CURRENT COMPANY LINKEDIN: ")
        salary_expectations = float(input("SALARY EXPECTATION [hint: float]: "))
        desired_work_country = input("DESIRED LOCATION [hint: country]: ")
        desired_work_city_state = input("DESIRED LOCATION [hint: city/state]: ")
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
            "salary_expectations": salary_expectations,
            "desired_work_location": {
                "country": desired_work_country,
                "city_state": desired_work_city_state,
            },
            "desired_employment_status": desired_employment_status,
            "desired_work_arrangement": desired_work_arrangement,
            "career_switch_motivation": career_switch_motivation,
        }

        return UserProfileModels(**applicant_profile), UserPreferenceModel(
            **applicant_preferences
        )


# applicant profile instance
my_applicant_data = ApplicantData()
