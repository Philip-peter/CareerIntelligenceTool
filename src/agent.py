import os
import sys
from typing import cast

from langchain_core.runnables import RunnableConfig
from langgraph.graph import END, START, StateGraph

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

from config import cfg  # noqa: E402
from src.agents import (  # noqa: E402
    aggregator,
    company_profile,
    finance,
    industry,
    job,
    job_scanner,
    leadership,
    report,
    router,
    strategic_direction,
    synthesis,
    workforce,
)
from src.applicant_data import my_applicant_data  # noqa: E402
from src.state import State  # noqa: E402


class Workflow:
    def __init__(self) -> None:

        # # initiate tavily research tool
        # self.tavily_research_tool = TavilyResearchTool()

        # # initiate llm summarizer tool
        # self.llm_summarizer_tool = LlmSummarizer()

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
        self.aggregator_obj = aggregator.Aggregator()
        self.synthesis_obj = synthesis.SynthesisAgent()
        self.company_direction_obj = strategic_direction.StrategicDirection()

        # workflow
        workflow = StateGraph(State)

        # add nodes
        workflow.add_node(
            "job_scanner",
            self.job_scanner_obj.fetch_recent_jobs,
        )
        workflow.add_node(
            "normalize_jobs",
            self.job_scanner_obj.normalize_job,
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
        workflow.add_node(
            "aggregator_agent",
            self.aggregator_obj.aggregate_analysis_result,
        )
        workflow.add_node(
            "synthesis_agent",
            self.synthesis_obj.synthesize,
        )
        workflow.add_node(
            "company_direction_agent",
            self.company_direction_obj.run_research,
        )

        # add edges
        workflow.add_edge(START, "job_scanner")
        workflow.add_edge("job_scanner", "normalize_jobs")
        workflow.add_conditional_edges(
            "normalize_jobs",
            self.router_obj.process_jobs,
            [
                "job_profile_agent",
                "company_profile_agent",
                "industry_agent",
                "finance_agent",
                "leadership_agent",
                "workforce_agent",
                "company_direction_agent",
            ],
        )
        workflow.add_edge("job_profile_agent", "aggregator_agent")
        workflow.add_edge("company_profile_agent", "aggregator_agent")
        workflow.add_edge("industry_agent", "aggregator_agent")
        workflow.add_edge("finance_agent", "aggregator_agent")
        workflow.add_edge("leadership_agent", "aggregator_agent")
        workflow.add_edge("workforce_agent", "aggregator_agent")
        workflow.add_edge("company_direction_agent", "aggregator_agent")
        workflow.add_edge("aggregator_agent", "synthesis_agent")
        workflow.add_edge("synthesis_agent", "reporting_agent")
        workflow.add_edge("reporting_agent", END)

        # compile agent
        self.agent = workflow.compile()

    def run(self):
        # init applicant preference
        # my_app_profile, my_app_preference = my_applicant_profile.init_candidate_profile()

        # use synthetic user preferences fot testing
        my_app_profile, my_app_preference = my_applicant_data.dummy_user_preferences()

        # set initial state
        initial_state = cast(
            State,
            {
                "applicant_profile": my_app_profile,
                "applicant_preference": my_app_preference,
                "raw_jobs": [],
                "job_queue": [],
                "agent_analysis": [],
                "aggregated_analysis": [],
                "synthesis_results": [],
                "final_report": "",
            },
        )

        # set runnable config
        config = cast(
            RunnableConfig,
            {
                "configurable": {
                    "shared_config": cfg,
                }
            },
        )

        # invoke agent
        return self.agent.ainvoke(input=initial_state, config=config)
