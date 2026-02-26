import copy
import os
import sys

from langchain_core.runnables import RunnableConfig

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

from src.state import State  # noqa: E402


class CompanyGrounding:
    def __init__(self):
        pass

    @staticmethod
    def queries_template(company_name):
        return f"Find comprehensive company profile for [{company_name}] including official website, industry classification and core business overview."

    async def research_company(self, state: State, config: RunnableConfig):
        working_query = copy.deepcopy(
            self.queries_template(company_name=state["target_company"])
        )
        web_research_tool = config.get("configurable", {}).get("web_research_tool")
        if not web_research_tool:
            raise ValueError("web search tool is not configured")

        # extract company details
        company_details = await web_research_tool.extract(
            query=working_query, research_urls=state["job_posting_link"]
        )

        return {"target_company_profile": company_details}
