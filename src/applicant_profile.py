import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(root_dir)

from src.models import UserPreference  # noqa: E402


class ApplicantProfile:
    def dummy_user_preferences(self):
        """Synthetic user preferences for testing"""
        user_preferences = {
            "current_company": "Dayforce",
            "salary_expectations": 140000.0,
            "desired_work_location": {
                "country": "Canada",
                "city_state": "Ontario",
            },
            "desired_employment_status": "fulltime",
            "desired_work_arrangement": "remote",
            "career_switch_motivation": "compensation",
        }

        return UserPreference(**user_preferences)

    def init_candidate_profile(self):
        """Capture users preference"""
        current_company = input("CURRENT COMPANY: ")
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

        applicant_data = {
            "current_company": current_company,
            "salary_expectations": salary_expectations,
            "desired_work_location": {
                "country": desired_work_country,
                "city_state": desired_work_city_state,
            },
            "desired_employment_status": desired_employment_status,
            "desired_work_arrangement": desired_work_arrangement,
            "career_switch_motivation": career_switch_motivation,
        }

        return UserPreference(**applicant_data)

    def update_candidate_profile(self):
        pass


# applicant profile instance
my_applicant_profile = ApplicantProfile()
