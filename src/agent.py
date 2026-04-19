import os
import sys
from typing import cast

from langchain_core.runnables import RunnableConfig
from langgraph.graph import START, StateGraph  # END

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

from config import cfg  # noqa: E402
from src.applicant_profile import my_applicant_profile  # noqa: E402
from src.nodes import (  # noqa: E402
    company_profile,
    finance,
    industry,
    job,
    job_scanner,
    leadership,
    report,
    router,
    workforce,
)
from src.state import State  # noqa: E402
from src.utils.llm_summarizer import LlmSummarizer  # noqa: E402
from src.utils.tavily import TavilyResearchTool  # noqa: E402


class Workflow:
    def __init__(self) -> None:

        # initiate tavily research tool
        self.tavily_research_tool = TavilyResearchTool()

        # initiate llm summarizer tool
        self.llm_summarizer_tool = LlmSummarizer()

        # initiate nodes
        self.industry_obj = industry.Industry()
        self.leadership_obj = leadership.Leadership()
        self.workforce_obj = workforce.Workforce()
        self.finance_obj = finance.FinancialData()
        self.report_obj = report.GenerateReport()
        self.router_obj = router.Router()
        self.company_profile_obj = company_profile.CompanyProfile()
        self.job_scanner_obj = job_scanner.JobScanner()
        self.job_obj = job.Job()

        # workflow
        workflow = StateGraph(State)

        # add nodes
        workflow.add_node(
            "job_scanner",
            self.job_scanner_obj.fetch_dummy_jobs,
        )
        workflow.add_node(
            "router_agent",
            self.router_obj.process_jobs,
        )
        workflow.add_node(
            "job_profile_agent",
            self.job_obj.run_research,
        )
        workflow.add_node(
            "company_profile_agent",
            self.company_profile_obj.run_research,
        )
        workflow.add_node(
            "industry_agent",
            self.industry_obj.run_research,
        )
        workflow.add_node(
            "finance_agent",
            self.finance_obj.run_research,
        )
        workflow.add_node(
            "leadership_agent",
            self.leadership_obj.run_research,
        )
        workflow.add_node(
            "workforce_agent",
            self.workforce_obj.run_research,
        )
        workflow.add_node(
            "reporting_agent",
            self.report_obj.run,
        )

        # add edges
        workflow.add_edge(START, "job_scanner")
        workflow.add_edge("job_scanner", "router_agent")
        workflow.add_conditional_edges("router_agent", self.router_obj.process_jobs)

        # compile agent
        self.agent = workflow.compile()

    def run(self):
        # init applicant profile
        # TODO: Add persist where we check if applicant profile already exist before init
        candidate_profile = my_applicant_profile.init_candidate_profile()

        # set initial state
        initial_state = cast(
            State,
            {
                "applicant_profile": candidate_profile,
                "raw_jobs": [],
                "job_queue": [],
                "agent_analysis": [],
                "final_report": "",
            },
        )

        # set runnable config
        config = cast(
            RunnableConfig,
            {
                "configurable": {
                    "shared_config": cfg,
                    "web_research_tool": self.tavily_research_tool,
                    "llm_summarizer": self.llm_summarizer_tool,
                }
            },
        )

        # invoke agent
        return self.agent.ainvoke(input=initial_state, config=config)
