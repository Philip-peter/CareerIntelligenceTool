from typing import Any, Literal, Optional, Union

from pydantic import BaseModel, Field, field_validator


# model for the candidate
class ApplicantModel(BaseModel):
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


class JobPostingModel(BaseModel):
    # --- MANDATORY FIELDS ---
    job_title: str = Field(
        ..., description="The official title of the position. REQUIRED."
    )
    job_posting_link: str = Field(
        ..., description="The direct URL to the job advertisement. REQUIRED."
    )
    job_description: str = Field(
        ..., description="The full text content of the job posting. REQUIRED."
    )

    # --- OPTIONAL FIELDS ---
    employment_statuses: Any = Field(default="No data available")
    job_city: Optional[str] = Field(default="No data available")
    job_state: Optional[str] = Field(default="No data available")
    country: Optional[str] = Field(default="No data available")
    salary: Optional[Union[str, int, float]] = Field(default="No data available")
    minimum_salary: Optional[Union[str, int, float]] = Field(
        default="No data available"
    )
    company: Optional[str] = Field(default="No data available")
    company_founded_year: Optional[Union[int, str]] = Field(default="No data available")
    company_name: Optional[str] = Field(default="No data available")
    company_domain: Optional[str] = Field(default="No data available")
    company_url: Optional[str] = Field(default="No data available")
    company_linkedin_url: Optional[str] = Field(default="No data available")
    company_industry: Optional[str] = Field(default="No data available")
    company_employee_count: Optional[Union[int, str]] = Field(
        default="No data available"
    )
    company_num_jobs: Optional[Union[int, str]] = Field(default="No data available")
    publicly_traded_symbol: Optional[str] = Field(default="No data available")
    yc_batch: Optional[str] = Field(default="No data available")
    total_funding_usd: Optional[Union[float, int, str]] = Field(
        default="No data available"
    )
    last_funding_round_date: Optional[str] = Field(default="No data available")
    last_funding_round_amount_readable: Optional[str] = Field(
        default="No data available"
    )
    hiring_team: Any = Field(default="No data available")
    is_recruiting_agency: Optional[Union[bool, str]] = Field(
        default="No data available"
    )

    # --- MAGIC CONVERSION ---
    @field_validator("*", mode="before")
    @classmethod
    def convert_none_to_default(cls, v: Any, info):
        # If the field is not mandatory and the value is None, return the default string
        if v is None:
            return "No data available"

        # If it's a boolean string "True"/"False"
        # only if the field is expected to be a string
        if (
            isinstance(v, bool)
            and cls.model_fields[info.field_name].annotation == Optional[str]
        ):
            return str(v)

        return v

    class Config:
        # Automatically convert numbers to string
        coerce_numbers_to_str = True


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

    investor_sentiment: str = Field(
        default="No data available",
        description="Analyze management's outlook from earnings calls and investor presentations. "
        "Include key themes from quarterly results and how the market/investors are reacting to "
        "recent financial guidance. Examples: Management raising full-year guidance (bullish); "
        "Investor concerns over slowing growth in a core segment; Heavy emphasis on 'efficiency' "
        "in latest investor deck.",
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

    labor_disputes: str = Field(
        default="No data available",
        description="Detail any significant labor issues, including unionization efforts, "
        "strikes, or legal friction related to unfair labor practices. "
        "Examples: Ongoing UAW strike activity (operational risk); "
        "Successful unionization votes at retail locations; "
        "No history of labor disputes or union presence.",
    )


class LeadershipContextModels(BaseModel):
    ceo_tenure: str = Field(
        default="No data available",
        description=(
            "State how long the current CEO has served and assess their impact on employees — "
            "not just business performance. Look for reorganizations, layoffs, or culture shifts that "
            "occurred under their leadership. "
            "Examples: CEO drove stable headcount growth and avoided mass layoffs during downturns (positive); "
            "Three major reorgs in four years with high attrition following each (negative signal for stability)."
        ),
    )
    founder_involvement: str = Field(
        default="No data available",
        description=(
            "Describe whether founders remain involved in leadership and assess the cultural effect of "
            "their presence or absence — not their ownership stake. "
            "Founder involvement can mean strong mission alignment or an unpredictable 'founder mode' environment. "
            "Examples: Founder stepped back into advisory role, enabling professional management to scale culture; "
            "Founder still controls day-to-day decisions, creating bottlenecks and inconsistent employee experience."
        ),
    )
    strategic_pivots: str = Field(
        default="No data available",
        description=(
            "Identify major business model shifts and evaluate their workforce consequences. "
            "Did pivots lead to layoffs, new career opportunities, or signal reactive vs. visionary leadership? "
            "Examples: Pivot into new product line created 200 new engineering roles (positive for applicants); "
            "Abandoned core product after failed expansion, resulting in 30% headcount reduction (risk signal)."
        ),
    )
    executive_reputation: str = Field(
        default="No data available",
        description=(
            "Assess the public and employee-facing reputation of the executive team. "
            "Include Glassdoor and Blind approval ratings, employee sentiment, management controversies, "
            "and any notable awards or public criticism. "
            "Examples: CEO maintains 85% Glassdoor approval with consistent positive reviews on transparency; "
            "Executive team publicly criticized for poor communication during restructuring."
        ),
    )
    leadership_stability: str = Field(
        default="No data available",
        description=(
            "Assess C-suite and senior leadership turnover across roles (CEO, CTO, CFO, CPO, CHRO). "
            "High churn in VP/Director layers is a major red flag for job applicants. "
            "Examples: Stable leadership team with less than 10% annual attrition (positive signal); "
            "Three CHROs in two years (instability signal for culture and HR practices)."
        ),
    )
    employee_treatment_during_hardship: str = Field(
        default="No data available",
        description=(
            "Evaluate how leadership has handled workforce reductions, restructurings, or downturns. "
            "Assess whether layoffs were handled transparently and humanely (severance, notice, support). "
            "Examples: Leadership provided 6-month severance and outplacement support (positive); "
            "Employees terminated via email with no severance (negative signal for leadership character)."
        ),
    )
    management_style_and_culture: str = Field(
        default="No data available",
        description=(
            "Characterize the leadership's management philosophy and its downstream effect on culture. "
            "Is it top-down and command-control, or collaborative and empowering? "
            "Look for signals of psychological safety, micromanagement, or autonomy. "
            "Examples: Leaders publicly promote internal mobility and employee development; "
            "Culture described as fear-based in Glassdoor reviews referencing executive behavior."
        ),
    )
    vision_and_communication_clarity: str = Field(
        default="No data available",
        description=(
            "Assess whether leadership communicates a clear, consistent strategic direction to employees. "
            "Look for evidence of regular all-hands meetings, transparent roadmaps, and honest messaging. "
            "Examples: CEO hosts monthly town halls and publishes internal strategy memos (positive); "
            "Employees report being blindsided by major announcements (negative signal)."
        ),
    )
    dei_and_values_commitment: str = Field(
        default="No data available",
        description=(
            "Evaluate leadership's demonstrated commitment to diversity, equity, and inclusion — "
            "not just stated values, but measurable actions (representation in leadership, pay equity audits, ERGs). "
            "Note any public controversies or rollbacks. "
            "Examples: Executive team reflects diverse backgrounds, company publishes annual pay equity report; "
            "Leadership rolled back DEI programs under pressure with no explanation."
        ),
    )
    employee_development_investment: str = Field(
        default="No data available",
        description=(
            "Determine whether leadership actively invests in employee growth through L&D budgets, "
            "mentorship programs, internal promotions, and career pathing. "
            "Examples: Company promotes 70% of senior roles internally (strong signal for growth); "
            "No formal L&D budget, high attrition among high performers."
        ),
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
