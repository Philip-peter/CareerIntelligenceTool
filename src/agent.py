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
    CompanyProfileModel,
    #     CandidateModel,
    FinancialContextModels,
    IndustryContextModels,
    #     JobRoleContextModels,
    LeadershipContextModels,
    TargetJobDetails,
    WorkforceContextModels,
)
from src.nodes import (  # noqa: E402
    company_profile,
    finance,
    industry,
    job_posting_analysis,
    # jobrole,
    leadership,
    report,
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
        self.job_posting_analysis_obj = job_posting_analysis.JobPostingAnalysis()
        self.company_profile = company_profile.CompanyProfile()

        # workflow
        workflow = StateGraph(State)

        # add nodes
        workflow.add_node(
            "job_posting_web_search", self.job_posting_analysis_obj.extract_job
        )
        workflow.add_node(
            "job_posting_llm_analysis", self.job_posting_analysis_obj.analyze_job
        )
        workflow.add_node(
            "company_profile_web_search", self.company_profile.run_research
        )
        workflow.add_node(
            "company_profile_llm_analysis", self.company_profile.run_llm_analysis
        )
        workflow.add_node("industry_web_search", self.industry_obj.run_research)
        workflow.add_node("industry_llm_analysis", self.industry_obj.run_llm_analysis)
        workflow.add_node("finance_web_search", self.finance_obj.run_research)
        workflow.add_node("finance_llm_analysis", self.finance_obj.run_llm_analysis)
        workflow.add_node("workforce_web_search", self.workforce_obj.run_research)
        workflow.add_node("workforce_llm_analysis", self.workforce_obj.run_llm_analysis)
        workflow.add_node("leadership_web_search", self.leadership_obj.run_research)
        workflow.add_node(
            "leadership_llm_analysis", self.leadership_obj.run_llm_analysis
        )
        workflow.add_node("report_generator", self.report_obj.run)

        # add edges
        workflow.add_edge(START, "job_posting_web_search")
        workflow.add_edge(START, "company_profile_web_search")
        workflow.add_edge(START, "industry_web_search")
        workflow.add_edge(START, "leadership_web_search")
        workflow.add_edge(START, "workforce_web_search")
        workflow.add_edge("job_posting_web_search", "job_posting_llm_analysis")
        workflow.add_edge("job_posting_llm_analysis", "report_generator")
        workflow.add_edge("company_profile_web_search", "company_profile_llm_analysis")
        workflow.add_edge("company_profile_llm_analysis", "report_generator")
        workflow.add_edge("industry_web_search", "industry_llm_analysis")
        workflow.add_edge("industry_llm_analysis", "report_generator")
        workflow.add_edge("leadership_web_search", "leadership_llm_analysis")
        workflow.add_edge("leadership_llm_analysis", "report_generator")
        workflow.add_edge("workforce_web_search", "workforce_llm_analysis")
        workflow.add_edge("workforce_llm_analysis", "report_generator")
        workflow.add_edge("finance_web_search", "finance_llm_analysis")
        workflow.add_edge("finance_llm_analysis", "report_generator")
        workflow.add_edge("report_generator", END)

        # compile agent
        self.agent = workflow.compile()

    def run(
        self,
        job_link,
        target_company,
        # current_company,
        # currently_employed,
        # current_role,
        # current_job_tenure,
        # risk_tolerance,
        # career_stage,
        # career_priority,
    ):
        # initiate candidate
        # candidate = CandidateModel(
        #     currently_employed=currently_employed,
        #     current_role=current_role,
        #     current_company=current_company,
        #     current_job_tenure=current_job_tenure,
        #     risk_tolerance=risk_tolerance,
        #     career_stage=career_stage,
        #     career_priority=career_priority,
        # )

        # set initial state
        initial_state = cast(
            State,
            {
                # "candidate": candidate,
                "target_company": target_company,
                "target_company_profile": CompanyProfileModel(),
                "raw_research": {},
                "job_posting_link": job_link,
                "job_posting_details": TargetJobDetails(),
                "industry_research": IndustryContextModels(),
                "finance_research": FinancialContextModels(),
                "workforce_research": WorkforceContextModels(),
                "leadership_research": LeadershipContextModels(),
                # "job_role_research": JobRoleContextModels(),
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
