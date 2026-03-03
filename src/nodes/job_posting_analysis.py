import os
import sys

from langchain_core.runnables import RunnableConfig

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

from src.models import TargetJobDetails  # noqa: E402
from src.state import State  # noqa: E402


class JobPostingAnalysis:
    async def extract_job(self, state: State, config: RunnableConfig):

        query = "Identify the job title, job role summary, requirements, qualifications, and company benefits."

        web_research_tool = config.get("configurable", {}).get("web_research_tool")
        if not web_research_tool:
            raise ValueError("web search tool is not configured")

        # extract company details
        extracted_job_details = await web_research_tool.extract(
            query=query, research_urls=state["job_posting_link"]
        )

        return {"job_posting_raw": extracted_job_details[0].get("raw_content", "")}

    async def analyze_job(self, state: State, config: RunnableConfig):

        llm_analyzer_tool = config.get("configurable", {}).get("llm_summarizer")
        if not llm_analyzer_tool:
            raise ValueError("llm analyzer tool is not configured")

        system_prompt = """
        You are an expert HR Data Analyst specializing in structured information extraction. Your task is to parse raw job posting text and map it into a clean, structured format.

        Rules:

        Fidelity: Extract text exactly as it appears; do not summarize unless necessary for clarity.

        Exclusion: If a specific field (like Salary or Benefits) is not mentioned in the text, return 'Not Specified' or null.

        Requirements: Clearly separate 'Minimum Qualifications' from 'Preferred Qualifications' if the text allows.

        Tone: Maintain a professional, objective tone.
        """

        user_prompt = f"""
        Please analyze the job posting below and extract these specific fields:
        - job_title
        - job_description
        - minimum_qualifications
        - preferred_qualifications
        - skills_experience
        - benefits
        - salary (as a number only)

        Job Posting Content:
        {state["job_posting_raw"]}
        """

        llm_response = await llm_analyzer_tool.run(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            output_schema=TargetJobDetails,
        )
        return {"job_posting_details": llm_response}
