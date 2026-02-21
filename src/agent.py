import os
import sys
from typing import cast

from langchain_core.runnables import RunnableConfig
from langgraph.graph import END, START, StateGraph

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

from config import cfg  # noqa: E402
from src.models import (  # noqa: E402
    CandidateModel,
    FinancialContextModels,
    IndustryContextModels,
    JobRoleContextModels,
    LeadershipContextModels,
    WorkforceContextModels,
)
from src.nodes import (  # noqa: E402
    # finance,
    industry,
    # jobrole,
    leadership,
    report,
    # workforce,
)
from src.state import State  # noqa: E402
from src.utils.tavily import TavilyResearchTool  # noqa: E402


class Workflow:
    def __init__(self) -> None:

        # initiate tavily research tool
        self.tavily_research_tool = TavilyResearchTool()

        # initiate nodes
        self.industry_obj = industry.Industry()
        self.leadership_obj = leadership.Leadership()
        self.report_obj = report.GenerateReport()

        # workflow
        workflow = StateGraph(State)

        # add nodes
        workflow.add_node("industry_researcher", self.industry_obj.run_research)
        workflow.add_node("leadership_researcher", self.leadership_obj.run_research)
        workflow.add_node("report_generator", self.report_obj.summarize)

        # add edges
        workflow.add_edge(START, "industry_researcher")
        workflow.add_edge(START, "leadership_researcher")
        workflow.add_edge("industry_researcher", "report_generator")
        workflow.add_edge("leadership_researcher", "report_generator")
        workflow.add_edge("report_generator", END)

        # compile agent
        self.agent = workflow.compile()

    def run(self, target_company: str):

        if not target_company:
            raise ValueError("Target Company not configured")

        # set initial state
        initial_state = cast(
            State,
            {
                "candidate": CandidateModel,
                "target_company": target_company,
                "job_posting_link": str,
                "industry_research": IndustryContextModels,
                "finance_research": FinancialContextModels,
                "workforce_research": WorkforceContextModels,
                "leadership_research": LeadershipContextModels,
                "job_role_research": JobRoleContextModels,
                "final_report": str,
            },
        )

        # initial_state = cast(State, {"target_company": target_company})

        # set runnable config
        config = cast(
            RunnableConfig,
            {
                "configurable": {
                    "shared_config": cfg,
                    "web_research_tool": self.tavily_research_tool,
                }
            },
        )

        # invoke agent
        return self.agent.ainvoke(input=initial_state, config=config)
