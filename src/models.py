from typing import Literal, Optional, Self

from pydantic import BaseModel, Field, model_validator


# model for the candidate
class CandidateModel(BaseModel):
    currently_employed: bool = Field(
        ..., description="Whether the candidate is currently working"
    )
    current_company: Optional[str] = Field(
        description="The name of the candidate's current employer",
        examples=["Google", "Amazon"],
    )
    current_role: Optional[str] = Field(description="Current job title")
    current_job_tenure: Optional[float] = Field(
        ge=0, description="Number of years in the current position"
    )
    risk_tolerance: Literal[1, 2, 3, 4, 5] = Field(
        ..., description="Scale of 1 (low) to 5 (high) for risk appetite"
    )
    career_stage: Literal["early", "mid", "senior"] = Field(
        ..., description="The candidate's current professional seniority level"
    )
    career_priority: Literal["compensation", "stability"] = Field(
        ..., description="The primary driver for the candidate's next move"
    )

    @model_validator(mode="after")
    def check_employment_details(self) -> Self:
        if self.currently_employed and not all(
            [self.current_company, self.current_role, self.current_job_tenure]
        ):
            raise ValueError(
                "Encountered Error: Incomplete employment details, complete current_company, current_role and current_job_tenure"
            )
        if not self.currently_employed:
            self.current_company = None
            self.current_role = None
            self.current_job_tenure = None
        return self


# models for the research context
class IndustryContextModels(BaseModel):
    cyclic_or_defensive: str = Field(
        default="No data available",
        description="Classify whether the company operates in a cyclical industry (sensitive to economic cycles) or defensive industry (stable during recessions). "
        "Include historical recession performance if available. "
        "Examples: Automotive like Ford Motor Company (cyclical, demand drops in recessions); "
        "Consumer staples like Procter & Gamble (defensive, steady demand).",
    )

    regulatory_environment: str = Field(
        default="No data available",
        description="Describe the level of regulatory oversight affecting the company and industry. "
        "Include required approvals, compliance costs, and exposure to policy changes. "
        "Examples: Banks like JPMorgan Chase (high capital requirements, stress tests); "
        "Pharma like Pfizer (FDA approvals required); "
        "Software startups (typically low regulatory burden).",
    )

    ai_distruption: str = Field(
        default="No data available",
        description="Assess whether AI is a threat or tailwind to the company’s business model. "
        "Specify if AI could automate core services or drive new revenue. "
        "Examples: Chegg (at risk due to AI homework tools); "
        "NVIDIA (benefits from AI chip demand); "
        "Traditional consulting firms (partial automation risk).",
    )

    competition: str = Field(
        default="No data available",
        description="Describe the competitive landscape including main competitors, market share concentration, barriers to entry, and pricing power. "
        "Examples: Airlines like Delta Air Lines (high competition, low margins); "
        "Visa (strong moat, network effects); "
        "ASML (near monopoly in EUV lithography).",
    )


class FinancialContextModels(BaseModel):
    revenue_growth: str = Field(
        default="No data available",
        description="Summarize historical revenue growth trends (3–5 year CAGR if possible). "
        "Note acceleration or deceleration. "
        "Examples: High-growth SaaS (20–40% CAGR); "
        "Mature utilities (2–5% growth); "
        "Declining retailers with negative YoY revenue.",
    )

    profitability: str = Field(
        default="No data available",
        description="Describe profit margins (gross, operating, net) and trend direction. "
        "Examples: Apple (high gross margins, strong profitability); "
        "Early-stage startup (negative net income but improving margins); "
        "Retail grocery (thin margins).",
    )

    debt: str = Field(
        default="No data available",
        description="Assess leverage levels including debt-to-equity or debt-to-EBITDA where available. "
        "Note refinancing risk. "
        "Examples: Capital-intensive telecom with high debt; "
        "Asset-light SaaS with minimal debt.",
    )

    cash_flow: str = Field(
        default="No data available",
        description="Describe operating and free cash flow stability. "
        "Indicate whether the company generates consistent positive cash flow or burns cash. "
        "Examples: Microsoft generates strong free cash flow; "
        "Venture-backed startup burning cash with limited runway.",
    )

    revenue_concentration: str = Field(
        default="No data available",
        description="Assess dependency on a small number of customers, products, or regions. "
        "Examples: A company deriving 40% of revenue from one client (high concentration risk); "
        "Diversified multinational with broad customer base (low concentration risk).",
    )


class WorkforceContextModels(BaseModel):
    layoff_history: str = Field(
        default="No data available",
        description="Describe major layoffs in the past 2–3 years including frequency and scale. "
        "Examples: Meta Platforms conducted multiple large layoffs in 2022–2023; "
        "Stable mid-sized firm with no recent workforce reductions.",
    )

    hiring_trends: str = Field(
        default="No data available",
        description="Assess whether the company is expanding headcount or freezing hiring. "
        "Include signals like aggressive LinkedIn recruiting or job posting declines. "
        "Examples: Rapid AI hiring surge at NVIDIA; "
        "Hiring freeze after cost-cutting measures.",
    )

    executive_turnover: str = Field(
        default="No data available",
        description="Evaluate stability of leadership team (CFO, CTO, COO turnover). "
        "Frequent departures may signal instability. "
        "Examples: Multiple CFO changes in 2 years (risk signal); "
        "Long-tenured executive team (stability signal).",
    )

    employee_sentiments: str = Field(
        default="No data available",
        description="Summarize employee satisfaction from public sources like Glassdoor. "
        "Include CEO approval rating if available. "
        "Examples: High CEO approval at Microsoft; "
        "Low morale complaints during restructuring phases.",
    )


class LeadershipContextModels(BaseModel):
    ceo_tenure: str = Field(
        default="No data available",
        description="State how long the current CEO has served and whether performance improved or declined under their leadership. "
        "Examples: Satya Nadella at Microsoft (long tenure, successful transformation); "
        "Frequent CEO turnover at struggling companies.",
    )

    founder_involvement: str = Field(
        default="No data available",
        description="Describe whether founders remain involved in leadership or board roles and their ownership stake. "
        "Examples: Mark Zuckerberg at Meta Platforms (founder-led); "
        "Founder exited with no operational involvement.",
    )

    strategic_pivots: str = Field(
        default="No data available",
        description="Identify major business model shifts and evaluate their outcomes. "
        "Examples: Netflix pivot from DVD rentals to streaming (successful); "
        "Company abandoning core product after failed expansion.",
    )

    insider_behavior: str = Field(
        default="No data available",
        description="Analyze insider stock buying/selling trends and executive ownership levels. "
        "Examples: Significant insider buying during downturn (confidence signal); "
        "Heavy executive selling amid declining performance (risk signal).",
    )


class JobRoleContextModels(BaseModel):
    core_or_experiemental: str = Field(
        default="No data available",
        description="Determine whether the role supports the company’s primary revenue driver (core) or a new/experimental initiative. "
        "Examples: Cloud engineering at Microsoft (core); "
        "Metaverse R&D at Meta during early build phase (experimental).",
    )

    revenue_generating_or_cost_center: str = Field(
        default="No data available",
        description="Classify whether the role directly generates revenue (sales, product tied to revenue) or supports operations (HR, internal IT). "
        "Revenue-generating roles often have higher strategic priority.",
    )

    automation_exposure: str = Field(
        default="No data available",
        description="Assess likelihood that the role could be automated or augmented by AI. "
        "Examples: Routine data entry (high automation risk); "
        "Complex AI systems engineering (low automation risk).",
    )
