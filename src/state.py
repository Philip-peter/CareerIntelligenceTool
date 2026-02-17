from typing import Annotated, List, TypedDict

from langgraph.graph import END, START, StateGraph

# from langgraph.graph.message import add_messages
from candidate_input import Candidate, TargetCompany
from config import cfg
from models import Research
from utils.tavily import TavilyResearchTool


class State(TypedDict):
    # messages: Annotated[list, add_messages]
    candidate: Candidate
    target_company: TargetCompany
    research: Research


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
