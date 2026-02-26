import os
import sys

from langchain_core.runnables import RunnableConfig

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

from src.state import State  # noqa: E402


class CompanyGrounding:
    @staticmethod
    def queries_template(company_name):
        pass

    async def research_company(self, state: State, config: RunnableConfig):
        web_research_tool = config.get("configurable", {}).get("web_research_tool")
        if not web_research_tool:
            raise ValueError("web search tool is not configured")

        query = ""
        company_url = state["job_posting_link"]

        # extract company details
        company_details = await web_research_tool.extract(
            query=query, research_urls=company_url
        )

        return company_details
