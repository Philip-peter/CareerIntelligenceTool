from __future__ import annotations

from enum import Enum
from typing import Any, List, Optional, Union

from pydantic import BaseModel, Field, field_validator

# ---------------------------------------------------------------------------
# BaseModel for User Preference
# ---------------------------------------------------------------------------

# Enums for user profile


class EmploymentStatus(str, Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"


class WorkArrangement(str, Enum):
    REMOTE = "remote"
    HYBRID = "hybrid"
    ON_SITE = "on_site"


class SwitchMotivation(str, Enum):
    COMPENSATION = "compensation"  # primarily chasing higher pay
    GROWTH = "growth"  # next level, new skills
    STABILITY = "stability"  # escaping uncertainty
    WORK_LIFE_BALANCE = "work_life_balance"  # reclaiming personal time
    IMPACT = "impact"  # meaningful work
    PRESTIGE = "prestige"  # brand name, title


# Sub Models


class Location(str, Enum):
    US = "US"
    CA = "CA"
    GB = "GB"


# Main Class for User Preferences


class UserPreferenceModel(BaseModel):
    preferred_job_roles: List[str] = Field(..., description="Desired job roles")
    # salary_expectations: float = Field(
    #     ..., description="Salary expectations and currency"
    # )
    desired_work_location: List[Location] = Field(
        ..., description="Preferred job location"
    )
    desired_employment_status: List[EmploymentStatus] = Field(
        ..., description="Desired employment type"
    )
    desired_work_arrangement: WorkArrangement = Field(
        ..., description="Remote, hybrid, or on-site preference"
    )
    career_switch_motivation: SwitchMotivation = Field(
        ..., description="The primary driver for the candidate's next move"
    )


# ---------------------------------------------------------------------------
# BaseModel for User Profile
# ---------------------------------------------------------------------------


class UserProfileModels(BaseModel):
    current_company: str = Field(
        ...,
        description="The name of the candidate's current employer",
        examples=["Google", "Amazon"],
    )
    current_company_official_url: str = Field(
        ...,
        description="The official url of the candidate's current employer",
        examples=["https://www.dayforce.com/ca"],
    )
    current_company_linkedin_url: Optional[str] = Field(
        ...,
        description="The official linkedin page of the candidate's current employer",
        examples=["https://linkedin.com/company/dayforce/"],
    )


# ---------------------------------------------------------------------------
# BaseModel for Job Posting
# ---------------------------------------------------------------------------
#
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
        description=(
            "Assess whether the industry is cyclical or defensive and what that means for workforce stability. "
            "Focus on whether economic downturns historically trigger layoffs, hiring freezes, or budget cuts "
            "in this sector — not stock defensiveness. "
            "Examples: Automotive (cyclical, mass layoffs common during recessions); "
            "Healthcare (defensive, headcount largely stable during downturns); "
            "SaaS (mixed — SMB-facing contracts churn, enterprise tends to hold)."
        ),
    )
    regulatory_environment: str = Field(
        default="No data available",
        description=(
            "Describe the level of regulatory oversight and its implications for company operations, "
            "workforce stability, and business continuity. Flag whether regulatory risk could lead to "
            "operational disruptions, fines, license loss, or forced restructuring that affects employees. "
            "Examples: Banks like JPMorgan Chase (heavy compliance burden, but regulation adds operational stability); "
            "Crypto firms (high regulatory uncertainty, risk of forced shutdowns); "
            "Software startups (low regulatory burden, faster operational agility)."
        ),
    )
    ai_disruption: str = Field(
        default="No data available",
        description=(
            "Assess whether AI and automation represent a threat or tailwind to roles and job stability "
            "within this industry. Distinguish between AI augmenting workers vs. eliminating roles outright. "
            "Include both company-specific AI strategy and industry-wide displacement signals. "
            "Examples: Legal document review (high displacement risk from AI); "
            "NVIDIA (AI is a growth tailwind creating new roles); "
            "Traditional consulting (partial automation of analytical tasks, senior roles less affected)."
        ),
    )
    competition: str = Field(
        default="No data available",
        description=(
            "Describe the competitive landscape and assess what it means for the company's stability "
            "and longevity as an employer. Intense competition with margin pressure often precedes "
            "cost-cutting and layoffs. A strong moat signals a more durable employer. "
            "Examples: Airlines (high competition, low margins, frequent workforce reductions); "
            "Visa (dominant market position, strong moat, stable employer); "
            "ASML (near-monopoly in EUV lithography, highly stable with strong hiring demand)."
        ),
    )
    industry_growth_trajectory: str = Field(
        default="No data available",
        description=(
            "Evaluate whether the industry is expanding or contracting and what that implies for "
            "hiring outlook, career growth potential, and long-term job security. "
            "Reference market size forecasts, talent demand trends, and sector analyst outlooks. "
            "Examples: Cybersecurity (high growth, strong talent demand, low layoff risk); "
            "Print media (structural decline, shrinking headcount industry-wide); "
            "Cloud infrastructure (rapid expansion with sustained hiring across all levels)."
        ),
    )
    consolidation_and_ma_risk: str = Field(
        default="No data available",
        description=(
            "Assess the level of M&A activity in the industry and the risk it poses to employees "
            "through redundancies, culture disruption, or post-merger integration layoffs. "
            "Flag whether the company itself is a likely acquisition target or acquirer. "
            "Examples: Regional banks (high consolidation risk, frequent post-merger layoffs); "
            "Enterprise software (active M&A market, acquired companies often see role redundancies); "
            "Mature telecom (high consolidation history with significant workforce reductions post-merger)."
        ),
    )
    offshoring_and_automation_risk: str = Field(
        default="No data available",
        description=(
            "Identify whether roles in this industry are at structural risk of being moved offshore, "
            "outsourced, or eliminated through automation — independent of company-specific performance. "
            "Examples: Customer support roles in SaaS (high offshoring and automation risk); "
            "Semiconductor engineering (low offshoring risk due to IP sensitivity and specialized talent); "
            "Back-office finance and accounting (moderate risk from RPA and offshore shared services)."
        ),
    )


class FinancialContextModels(BaseModel):
    revenue_growth: str = Field(
        default="No data available",
        description=(
            "Summarize revenue growth trends over the past 2-3 years and what the trajectory signals "
            "for the company's long-term viability as an employer. Accelerating growth suggests hiring "
            "demand; decelerating or negative growth often precedes cost-cutting and layoffs. "
            "Examples: Consistent 25%+ YoY revenue growth with expanding customer base "
            "(strong employer stability signal); Revenue declining 3 years consecutively in core segment "
            "(elevated layoff and restructuring risk)."
        ),
    )
    profitability: str = Field(
        default="No data available",
        description=(
            "Describe gross, operating, and net margin trends and what they reveal about the company's "
            "financial sustainability as an employer. Sustained losses or margin compression often "
            "trigger cost reduction programs that affect headcount and compensation. "
            "Examples: Improving operating margins with clear path to profitability "
            "(financial health improving, lower workforce risk); Widening operating losses with no "
            "stated path to profitability (elevated risk of cost-cutting measures affecting employees)."
        ),
    )
    debt: str = Field(
        default="No data available",
        description=(
            "Assess leverage levels and refinancing risk. High debt burdens constrain a company's "
            "ability to invest in headcount, compensation, and benefits — and can force restructuring "
            "if refinancing conditions deteriorate. Reference credit ratings where available. "
            "Examples: Manageable debt-to-EBITDA of 1.5x with investment-grade credit rating "
            "(low financial stress signal); Highly leveraged at 6x EBITDA with covenant pressures "
            "and recent credit downgrade (elevated restructuring and layoff risk)."
        ),
    )
    cash_flow: str = Field(
        default="No data available",
        description=(
            "Describe operating and free cash flow stability and what it means for the company's "
            "ability to sustain payroll, benefits, and investment in people. For private companies, "
            "assess burn rate and estimated cash runway. A company burning cash without a clear "
            "path to positive FCF is a materially higher employment risk. "
            "Examples: Consistent positive free cash flow funding organic growth and employee programs "
            "(strong stability signal); Monthly burn rate of $8M with 10 months of runway and no "
            "funding round announced (high employment risk for prospective hires)."
        ),
    )
    revenue_concentration: str = Field(
        default="No data available",
        description=(
            "Assess dependency on a small number of customers, products, or geographies. "
            "High concentration means a single contract loss or regional downturn can trigger "
            "rapid workforce reductions — a material risk for any new hire. "
            "Examples: 45% of revenue from a single enterprise customer with contract up for renewal "
            "(high concentration risk, significant job security exposure); Diversified revenue across "
            "500+ customers with no single customer exceeding 3% of revenue (low concentration risk)."
        ),
    )
    investor_sentiment: str = Field(
        default="No data available",
        description=(
            "Summarize the outlook from earnings calls, investor presentations, and analyst commentary. "
            "Translate investor signals into workforce implications — raised guidance suggests growth "
            "and hiring; emphasis on 'efficiency' or 'right-sizing' in IR decks is a layoff precursor. "
            "Weight analyst views alongside management commentary to counterbalance optimistic IR framing. "
            "Examples: Management raising full-year guidance with analysts confirming positive outlook "
            "(bullish signal for hiring and stability); Investor deck heavily emphasizing cost discipline "
            "and operational efficiency following a revenue miss (likely precursor to headcount reduction)."
        ),
    )
    funding_and_runway: str = Field(
        default="No data available",
        description=(
            "For private, pre-IPO, or venture-backed companies, assess the most recent funding round, "
            "total capital raised, estimated burn rate, and cash runway. A strong role at an underfunded "
            "company is a high employment risk. For public companies, note whether the balance sheet "
            "is self-sustaining or reliant on debt and equity issuance. "
            "Examples: Series B company with $40M raised, 18-month runway, and active Series C process "
            "(moderate risk — dependent on successful fundraise); Bootstrapped and profitable with no "
            "external funding dependency (strong stability signal for private employer)."
        ),
    )
    financial_distress_signals: str = Field(
        default="No data available",
        description=(
            "Identify the earliest warning indicators of financial distress that may not surface in "
            "standard revenue or margin analysis. Look for going concern warnings in SEC filings, "
            "covenant breaches, credit downgrades, deferred vendor payments, or bankruptcy filings. "
            "These signals typically precede mass layoffs by 6-12 months. "
            "Examples: Auditor issued going concern warning in most recent 10-K filing "
            "(critical risk signal — imminent financial instability); No distress signals detected "
            "across SEC filings, credit ratings, and news sources (clean financial health signal)."
        ),
    )


class WorkforceContextModels(BaseModel):
    layoff_history: str = Field(
        default="No data available",
        description=(
            "Describe major layoff events in the past 2-3 years including frequency, scale, and how "
            "they were handled. Cross-reference layoffs.fyi, WARN Act notices, and news coverage. "
            "Focus on what the pattern reveals about the company's workforce stability. "
            "Examples: Meta conducted multiple large layoffs in 2022-2023 but provided strong severance "
            "and outplacement support (scale risk, handled humanely); "
            "No layoff history in the past 3 years despite industry-wide reductions (strong stability signal)."
        ),
    )
    hiring_trends: str = Field(
        default="No data available",
        description=(
            "Assess whether the company is actively growing headcount or contracting. "
            "Look for signals like surge in open roles, hiring announcements, or conversely "
            "hiring freezes and paused recruitment. Distinguish between targeted hiring "
            "in specific functions vs. broad expansion. "
            "Examples: Aggressive AI and engineering hiring across all levels (growth signal); "
            "Job postings declined 60% YoY with freeze announced in Q1 (contraction signal)."
        ),
    )
    mid_management_turnover: str = Field(
        default="No data available",
        description=(
            "Assess churn at the director and VP level — the management layer a new hire would "
            "most directly report into. High mid-management turnover is a stronger day-to-day risk "
            "signal than C-suite changes, which are tracked separately in the leadership profile. "
            "Sources include LinkedIn departures, Glassdoor reviews mentioning manager changes, "
            "and Blind discussions. "
            "Examples: High director-level attrition with frequent team restructuring (instability signal); "
            "Stable mid-management tenure averaging 4+ years (positive signal for new hires)."
        ),
    )
    employee_sentiments: str = Field(
        default="No data available",
        description=(
            "Summarize employee satisfaction from platforms including Glassdoor, Blind, Fishbowl, "
            "and Indeed. Include CEO approval rating, overall company rating, and recurring themes "
            "in reviews — both positive and negative. Weight recent reviews more heavily. "
            "Examples: 4.2 Glassdoor rating with 85% CEO approval and consistent praise for work-life "
            "balance (strong signal); Low morale reviews citing poor communication and lack of direction "
            "spiking after restructuring announcement (negative signal)."
        ),
    )
    labor_disputes: str = Field(
        default="No data available",
        description=(
            "Detail any significant labor issues including unionization efforts, strikes, NLRB filings, "
            "wrongful termination suits, or class action complaints from employees. "
            "Flag whether disputes are isolated incidents or part of a broader pattern. "
            "Examples: Active NLRB unfair labor practice filing with ongoing union organizing drive "
            "(material risk signal); No history of labor disputes or union activity across all locations "
            "(stable signal)."
        ),
    )
    remote_and_flexibility_policy: str = Field(
        default="No data available",
        description=(
            "Describe the company's current remote, hybrid, or in-office policy and any recent changes. "
            "Flag return-to-office mandates as these frequently trigger voluntary attrition spikes. "
            "Note whether policy varies by role, team, or location. "
            "Examples: Fully remote with no RTO mandate announced (positive for flexibility-seeking candidates); "
            "Enforced 5-day RTO policy implemented in 2025 following prior hybrid arrangement "
            "(high voluntary attrition risk, negative signal for remote-preferring candidates)."
        ),
    )
    compensation_and_benefits: str = Field(
        default="No data available",
        description=(
            "Assess salary competitiveness, total compensation structure, and benefits quality "
            "relative to industry peers. Include equity (RSU, options), 401k matching, health coverage, "
            "and any notable perks or reductions. Cross-reference Glassdoor, Blind, and levels.fyi. "
            "Examples: Top-of-market total compensation with strong RSU grants and full health coverage "
            "(strong signal for attraction and retention); Below-market base salary with no equity "
            "and benefits cuts announced in 2025 (switching risk signal)."
        ),
    )
    headcount_trajectory: str = Field(
        default="No data available",
        description=(
            "Evaluate the overall workforce size trend over the past 2-3 years — distinct from "
            "specific layoff events. A company can avoid formal layoffs while quietly shrinking "
            "through attrition and hiring freezes. Look for headcount data from macrotrends, "
            "annual reports, or LinkedIn employee count changes. "
            "Examples: Workforce grew from 8,000 to 12,000 employees over 3 years (strong growth signal); "
            "Headcount declined 25% over 2 years via attrition without formal layoff announcements "
            "(stealth contraction signal)."
        ),
    )
    employee_tenure_and_retention: str = Field(
        default="No data available",
        description=(
            "Assess average employee tenure and retention signals from LinkedIn data, Glassdoor reviews, "
            "and Blind discussions. High turnover relative to industry peers is one of the strongest "
            "red flags for a prospective employee regardless of stated cause. "
            "Examples: Average tenure of 4.5 years with high internal promotion rate "
            "(strong retention signal); Average tenure under 18 months with Glassdoor reviews "
            "citing burnout and poor management (high-risk signal for a new hire)."
        ),
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
