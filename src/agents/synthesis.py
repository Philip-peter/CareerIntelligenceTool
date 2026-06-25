import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

from src.models import JobSwitchRecommendationModel  # noqa: E402
from src.prompts import synthesis_prompts  # noqa: E402

# import simulated analysis data for demo
from src.simulated_applicant_data import simulated_current_employer  # noqa: E402
from src.state import State  # noqa: E402
from src.tools import TOOLS_REGISTRY  # noqa: E402


class SynthesisAgent:
    def __init__(self) -> None:
        # initiate tools
        self.llm_tool = TOOLS_REGISTRY["llm_tool"]

    async def synthesize(self, state: State):
        synthesis_results = []

        # system prompt
        system_prompt = synthesis_prompts.SYNTHESIS_SYSTEM_PROMPT

        # Unpack the aggregated research per job
        for job_analysis in state["aggregated_analysis"]:
            for job_id, job_data in job_analysis.items():
                # extract prospect company profile
                prospect_company_profile = {
                    "job_title": job_data.get("job", {}).get(
                        "job_title", "Not Available"
                    ),
                    "job_posting_link": job_data.get("job", {}).get(
                        "job_posting_link", "Not Available"
                    ),
                    "job_description": job_data.get("job", {}).get(
                        "job_description", "Not Available"
                    ),
                    "job_salary": job_data.get("job", {}).get(
                        "job_salary", "Not Available"
                    ),
                    "job_hiring_team": job_data.get("job", {}).get(
                        "job_hiring_team", "Not Available"
                    ),
                    "company_name": job_data.get("company", {}).get(
                        "company_name", "Not Available"
                    ),
                    "company_industry": job_data.get("company", {}).get(
                        "company_industry", "Not Available"
                    ),
                    "company_official_url": job_data.get("company", {}).get(
                        "company_official_url", "Not Available"
                    ),
                    "company_linkedin_url": job_data.get("company", {}).get(
                        "company_linkedin_url", "Not Available"
                    ),
                }

                # user prompt
                user_prompt = synthesis_prompts.build_synthesis_user_prompt(
                    current_employer_analysis=simulated_current_employer,
                    prospect_employer_analysis=job_data,
                )

                llm_response = await self.llm_tool.run_with_schema(
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                    output_schema=JobSwitchRecommendationModel,
                )

                synthesis_results.append(
                    {
                        "job_id": job_id,
                        "current_company_profile": simulated_current_employer,
                        "prospect_company_profile": prospect_company_profile,
                        "recommendation": llm_response.model_dump(),
                    }
                )

        return {"synthesis_results": synthesis_results}
