import os
import sys

from langchain_core.runnables import RunnableConfig

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

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

        return {"job_posting_details": extracted_job_details}
