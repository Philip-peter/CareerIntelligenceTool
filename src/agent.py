import os
import sys
from typing import cast

from langchain_core.runnables import RunnableConfig
from langgraph.graph import END, START, StateGraph

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

from config import cfg  # noqa: E402
from src.applicant_profile import my_applicant_profile  # noqa: E402
from src.models import (  # noqa: E402
    FinancialContextModels,
    IndustryContextModels,
    #     JobPostingModel,
    #     JobRoleContextModels,
    LeadershipContextModels,
    WorkforceContextModels,
)
from src.nodes import (  # noqa: E402
    # finance,
    # industry,
    job_posting_researcher,
    supervisor,
    # jobrole,
    # leadership,
    # report,
    # workforce,
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
        # self.industry_obj = industry.Industry()
        # self.leadership_obj = leadership.Leadership()
        # self.workforce_obj = workforce.Workforce()
        # self.finance_obj = finance.FinancialData()
        # self.report_obj = report.GenerateReport()
        self.job_posting_obj = job_posting_researcher.JobPostingResearch()
        self.supervisor_obj = supervisor.Supervisor()

        # workflow
        workflow = StateGraph(State)

        # add nodes
        workflow.add_node(
            "job_posting_fetch_dummy_jobs",
            self.job_posting_obj.fetch_dummy_jobs,
        )
        # workflow.add_node(
        #     "job_posting_fetch_recent_jobs",
        #     self.job_posting_obj.fetch_recent_jobs,
        # )
        workflow.add_node(
            "job_posting_normalize_jobs", self.job_posting_obj.normalize_job
        )
        # workflow.add_node(
        #     "supervisor_process_jobs", self.supervisor_obj.process_jobs
        # )
        # workflow.add_node("industry_web_search", self.industry_obj.run_research)
        # workflow.add_node("industry_llm_analysis", self.industry_obj.run_llm_analysis)
        # workflow.add_node("finance_web_search", self.finance_obj.run_research)
        # workflow.add_node("finance_llm_analysis", self.finance_obj.run_llm_analysis)
        # workflow.add_node("workforce_web_search", self.workforce_obj.run_research)
        # workflow.add_node("workforce_llm_analysis", self.workforce_obj.run_llm_analysis)
        # workflow.add_node("leadership_web_search", self.leadership_obj.run_research)
        # workflow.add_node(
        #     "leadership_llm_analysis", self.leadership_obj.run_llm_analysis
        # )
        # workflow.add_node("report_generator", self.report_obj.run)

        # add edges
        # workflow.add_edge(START, "job_posting_fetch_recent_jobs")
        workflow.add_edge(START, "job_posting_fetch_dummy_jobs")

        workflow.add_edge("job_posting_fetch_dummy_jobs", "job_posting_normalize_jobs")
        workflow.add_conditional_edges(
            "job_posting_normalize_jobs",
            self.supervisor_obj.process_jobs,
            [
                "industry_web_search",
                "leadership_web_search",
                "workforce_web_search",
                "finance_web_search",
            ],
        )
        # workflow.add_edge("job_posting_fetch_recent_jobs", "job_posting_normalize_jobs")

        # workflow.add_edge("job_posting_normalize_jobs", "industry_web_search")
        # workflow.add_edge("industry_web_search", "industry_llm_analysis")
        # workflow.add_edge("industry_llm_analysis", "report_generator")

        # workflow.add_edge("job_posting_normalize_jobs", "leadership_web_search")
        # workflow.add_edge("leadership_web_search", "leadership_llm_analysis")
        # workflow.add_edge("leadership_llm_analysis", "report_generator")

        # workflow.add_edge("job_posting_normalize_jobs", "workforce_web_search")
        # workflow.add_edge("workforce_web_search", "workforce_llm_analysis")
        # workflow.add_edge("workforce_llm_analysis", "report_generator")

        # workflow.add_edge("job_posting_normalize_jobs", "finance_web_search")
        # workflow.add_edge("finance_web_search", "finance_llm_analysis")
        # workflow.add_edge("finance_llm_analysis", "report_generator")

        # workflow.add_edge("report_generator", END)

        # compile agent
        self.agent = workflow.compile()

    def run(self):
        # init applicant profile
        # TODO: Add persist where we check if applicant profile already exist before init
        # candidate_profile = my_applicant_profile.init_candidate_profile()

        # set initial state
        initial_state = cast(
            State,
            {
                # "applicant_profile": candidate_profile,
                "job_queue": [],
                "raw_research": {},
                "agent_analysis": [],
                # "industry_research": IndustryContextModels(),
                # "finance_research": FinancialContextModels(),
                # "workforce_research": WorkforceContextModels(),
                # "leadership_research": LeadershipContextModels(),
                # "job_role_research": JobRoleContextModels(),
                # "final_report": "",
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
