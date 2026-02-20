from typing import Annotated, List, TypedDict

from langgraph.graph import END, START, StateGraph

# from langgraph.graph.message import add_messages
from candidate_input import Candidate
from config import cfg
from models import (
    FinancialContextModels,
    IndustryContextModels,
    JobRoleContextModels,
    LeadershipContextModels,
    WorkforceContextModels,
)
from utils.tavily import TavilyResearchTool


class State(TypedDict):
    # messages: Annotated[list, add_messages]
    candidate: Candidate
    target_company: str  # update the company name after grounding
    industry_research: IndustryContextModels
    finance_research: FinancialContextModels
    workforce_research: WorkforceContextModels
    leadership_research: LeadershipContextModels
    job_role_research: JobRoleContextModels


class Workflow:
    def __init__(self) -> None:

        # initiate tavily research tool
        self.tavily_research_tool = TavilyResearchTool()

        # workflow
        workflow = StateGraph(State)

        # add nodes

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
