import os
import sys
from typing import TypedDict

from langgraph.graph import END, START, StateGraph

# from langgraph.graph.message import add_messages
from config import cfg
from models import (
    CandidateModel,
    FinancialContextModels,
    IndustryContextModels,
    JobRoleContextModels,
    LeadershipContextModels,
    WorkforceContextModels,
)
from utils.tavily import TavilyResearchTool

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

from src.nodes import finance, industry, jobrole, leadership, workforce  # noqa: E402


class State(TypedDict):
    candidate: CandidateModel
    target_company: str
    job_posting_link: str
    industry_research: IndustryContextModels
    finance_research: FinancialContextModels
    workforce_research: WorkforceContextModels
    leadership_research: LeadershipContextModels
    job_role_research: JobRoleContextModels


class Workflow:
    def __init__(self) -> None:

        # initiate tavily research tool
        self.tavily_research_tool = TavilyResearchTool()

        # initiate nodes
        self.industry_obj = industry.Industry()
        self.leadership_obj = leadership.Leadership()

        # workflow
        workflow = StateGraph(State)

        # add nodes
        workflow.add_node("industry_researcher", self.industry_obj.run_research)
        workflow.add_node("leadership_researcher", self.leadership_obj.run_research)

        # add edges

        # compile agent
        self.agent = workflow.compile()

    def run(self):

        # set input
        input = {}

        # set runnable config
        config = {
            "configurable": {
                "shared_config": cfg,
                "web_research_tool": self.tavily_research_tool,
            }
        }

        # invoke agent
        self.agent.invoke(input=input, config=config)
