import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

from src.search_queries.registry import QueryEntry  # noqa: E402

WORKFORCE_QUERIES: list[QueryEntry] = [
    QueryEntry(
        id="workforce_layoff_history",
        agent="workforce",
        topic="layoff_history",
        template=(
            '"{name}" site:{clean_domain} OR "layoff" OR "headcount reduction" '
            'OR "RIF" OR "restructuring" '
            '"2024" OR "2025" OR "2026" '
            "site:layoffs.fyi OR site:techcrunch.com OR site:businessinsider.com "
            "OR site:warn-tracker.com"
        ),
        purpose=(
            "Document major layoff events in the past 2-3 years including frequency, "
            "scale, and how they were handled. Layoffs.fyi and WARN Act tracker are the "
            "most reliable sources — they surface events that companies do not proactively "
            "publicize. Recurring layoffs even after profitable quarters are a strong "
            "employer risk signal."
        ),
        # primary_sources=["layoffs.fyi", "warn-tracker.com", "techcrunch.com", "businessinsider.com"],
        # signal_type="factual",
        # job_applicant_relevance=10,
        # tags=["workforce", "layoffs", "rif", "restructuring", "stability", "warn_act"],
    ),
    QueryEntry(
        id="workforce_hiring_trends",
        agent="workforce",
        topic="hiring_trends",
        template=(
            '"{name}" site:{clean_domain} OR "hiring" OR "open roles" '
            'OR "headcount growth" OR "expansion" '
            '"actively recruiting" OR "talent acquisition" OR "hiring freeze" '
            'OR "paused hiring" '
            "site:builtin.com OR site:techcrunch.com OR site:businessinsider.com"
        ),
        purpose=(
            "Assess whether the company is actively growing headcount or contracting. "
            "Replaced unreliable path-level and LinkedIn site filtering with hiring signal "
            "keywords from news sources. Distinguish broad expansion from targeted hiring "
            "in specific functions and flag any announced hiring freezes."
        ),
        # primary_sources=["builtin.com", "techcrunch.com", "businessinsider.com", "company_domain"],
        # signal_type="factual",
        # job_applicant_relevance=9,
        # tags=["workforce", "hiring", "growth", "expansion", "freeze", "talent_acquisition"],
    ),
    QueryEntry(
        id="workforce_mid_management_turnover",
        agent="workforce",
        topic="mid_management_turnover",
        template=(
            '"{name}" site:{clean_domain} OR "director" OR "VP" '
            'OR "vice president" OR "senior manager" '
            '"left" OR "departed" OR "resigned" OR "laid off" '
            "site:linkedin.com OR site:glassdoor.com OR site:teamblind.com"
        ),
        purpose=(
            "Assess churn at the director and VP level — the management layer a new hire "
            "would most directly report into. Differentiated from the leadership agent's "
            "stability query which targets C-suite. High mid-management churn is a stronger "
            "day-to-day risk signal for a new hire than executive departures."
        ),
        # primary_sources=["linkedin.com", "glassdoor.com", "teamblind.com"],
        # signal_type="factual",
        # job_applicant_relevance=9,
        # tags=["workforce", "management", "turnover", "directors", "vp", "churn"],
    ),
    QueryEntry(
        id="workforce_employee_sentiments",
        agent="workforce",
        topic="employee_sentiments",
        template=(
            '"{name}" site:{clean_domain} OR "employee reviews" OR "work culture" '
            'OR "CEO approval" "pros and cons" OR "recommend to a friend" '
            'OR "employee experience" '
            "site:glassdoor.com OR site:teamblind.com OR site:fishbowlapp.com "
            "OR site:indeed.com"
        ),
        purpose=(
            "Summarize employee satisfaction across multiple platforms. Fishbowl and Blind "
            "are added alongside Glassdoor and Indeed to capture a broader cross-section "
            "of unfiltered employee voice. Weight reviews from the past 12 months most "
            "heavily — sentiment can shift rapidly after restructuring events."
        ),
        # primary_sources=["glassdoor.com", "teamblind.com", "fishbowlapp.com", "indeed.com"],
        # signal_type="sentiment",
        # job_applicant_relevance=10,
        # tags=["workforce", "sentiment", "glassdoor", "blind", "culture", "reviews", "approval"],
    ),
    QueryEntry(
        id="workforce_labor_disputes",
        agent="workforce",
        topic="labor_disputes",
        template=(
            '"{name}" site:{clean_domain} OR "union" OR "strike" OR "labor dispute" '
            'OR "unfair labor practice" OR "NLRB" OR "wrongful termination" '
            'OR "class action employees" '
            "site:nlrb.gov OR site:reuters.com OR site:bloomberg.com"
        ),
        purpose=(
            "Identify NLRB filings, union organizing activity, strikes, and wrongful "
            "termination suits. Expanded beyond active strikes to include NLRB filings "
            "and class actions which are more discoverable and often surface earlier "
            "than public labor disputes. Flag whether disputes are isolated or a pattern."
        ),
        # primary_sources=["nlrb.gov", "reuters.com", "bloomberg.com"],
        # signal_type="factual",
        # job_applicant_relevance=7,
        # tags=["workforce", "labor", "union", "nlrb", "strike", "wrongful_termination", "class_action"],
    ),
    QueryEntry(
        id="workforce_remote_and_flexibility_policy",
        agent="workforce",
        topic="remote_and_flexibility_policy",
        template=(
            '"{name}" site:{clean_domain} OR "remote work" OR "hybrid policy" '
            'OR "return to office" OR "RTO mandate" OR "work from home" '
            'OR "flexible work" OR "in-office requirement" '
            "site:glassdoor.com OR site:techcrunch.com OR site:businessinsider.com"
        ),
        purpose=(
            "Describe the current remote, hybrid, or in-office policy and flag any recent "
            "RTO mandates. Return-to-office mandates correlate strongly with voluntary "
            "attrition spikes and are a top decision factor for candidates — especially "
            "those relocating or currently remote."
        ),
        # primary_sources=["glassdoor.com", "techcrunch.com", "businessinsider.com", "company_domain"],
        # signal_type="factual",
        # job_applicant_relevance=9,
        # tags=["workforce", "remote", "hybrid", "rto", "flexibility", "work_from_home"],
    ),
    QueryEntry(
        id="workforce_compensation_and_benefits",
        agent="workforce",
        topic="compensation_and_benefits",
        template=(
            '"{name}" site:{clean_domain} OR "salary" OR "compensation" '
            'OR "total compensation" OR "benefits" OR "equity" OR "RSU" '
            'OR "401k" OR "health insurance" OR "pay transparency" '
            "site:glassdoor.com OR site:levels.fyi OR site:teamblind.com "
            "OR site:reddit.com"
        ),
        purpose=(
            "Assess salary competitiveness, total compensation structure, and benefits "
            "quality relative to industry peers. Levels.fyi is the most reliable source "
            "for verified compensation data in tech — weighted above Glassdoor for "
            "engineering and product roles. Cross-reference Blind and Reddit for candid "
            "compensation discussions."
        ),
        # primary_sources=["levels.fyi", "glassdoor.com", "teamblind.com", "reddit.com"],
        # signal_type="sentiment",
        # job_applicant_relevance=10,
        # tags=["workforce", "compensation", "salary", "benefits", "equity", "rsu", "401k"],
    ),
    QueryEntry(
        id="workforce_headcount_trajectory",
        agent="workforce",
        topic="headcount_trajectory",
        template=(
            '"{name}" site:{clean_domain} OR "headcount" OR "total employees" '
            'OR "workforce size" OR "growing team" OR "shrinking" '
            'OR "hiring slowdown" OR "attrition" '
            "site:macrotrends.net OR site:businessinsider.com OR site:bloomberg.com"
        ),
        purpose=(
            "Evaluate overall workforce size trend over 2-3 years independent of specific "
            "layoff events. A company can shrink quietly through attrition and hiring "
            "freezes without formal announcements. Macrotrends is the best source for "
            "historical headcount data on public companies."
        ),
        # primary_sources=["macrotrends.net", "businessinsider.com", "bloomberg.com"],
        # signal_type="factual",
        # job_applicant_relevance=8,
        # tags=["workforce", "headcount", "trajectory", "attrition", "growth", "contraction"],
    ),
    QueryEntry(
        id="workforce_employee_tenure_and_retention",
        agent="workforce",
        topic="employee_tenure_and_retention",
        template=(
            '"{name}" site:{clean_domain} OR "employee tenure" OR "average tenure" '
            'OR "retention rate" OR "high turnover" OR "employees leave" '
            'OR "attrition rate" OR "revolving door" '
            "site:glassdoor.com OR site:linkedin.com OR site:teamblind.com"
        ),
        purpose=(
            "Assess average employee tenure and retention signals. High turnover relative "
            "to industry peers is one of the strongest employer red flags regardless of "
            "stated cause. LinkedIn tenure data and Glassdoor reviews mentioning frequent "
            "departures are the most reliable signals for this field."
        ),
        # primary_sources=["glassdoor.com", "linkedin.com", "teamblind.com"],
        # signal_type="sentiment",
        # job_applicant_relevance=9,
        # tags=["workforce", "tenure", "retention", "attrition", "turnover", "revolving_door"],
    ),
]
