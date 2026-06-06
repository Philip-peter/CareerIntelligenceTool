# queries/leadership_queries.py

from search_queries.registry import QueryEntry

LEADERSHIP_QUERIES: list[QueryEntry] = [
    QueryEntry(
        id="leadership_ceo_tenure",
        agent="leadership",
        topic="ceo_tenure",
        template=(
            '"{name}" site:{clean_domain} OR CEO tenure leadership '
            '"reorganization" OR "layoffs" OR "culture shift" '
            '"since joining" OR "under his leadership" OR "under her leadership" employees'
        ),
        purpose=(
            "Identify how long the current CEO has served and what workforce consequences "
            "occurred under their tenure — reorgs, layoffs, and culture shifts are the "
            "most relevant signals for a prospective employee, not financial performance."
        ),
        # primary_sources=["company_domain", "bloomberg.com", "wsj.com"],
        # signal_type="factual",
        # job_applicant_relevance=8,
        # tags=["leadership", "ceo", "tenure", "stability", "reorg", "layoffs"],
    ),
    QueryEntry(
        id="leadership_founder_involvement",
        agent="leadership",
        topic="founder_involvement",
        template=(
            '"{name}" site:{clean_domain} OR founder "founder-led" OR "founder mode" '
            'OR "founder vision" company culture employees '
            '"day-to-day" OR "still involved" OR "stepped back"'
        ),
        purpose=(
            "Determine whether founders remain active in leadership and assess the cultural "
            "effect of their presence or absence on employee experience. Founder involvement "
            "can mean strong mission alignment or an unpredictable founder mode environment."
        ),
        # primary_sources=["company_domain", "techcrunch.com", "businessinsider.com"],
        # signal_type="behavioral",
        # job_applicant_relevance=6,
        # tags=["leadership", "founder", "culture", "founder_mode", "mission"],
    ),
    QueryEntry(
        id="leadership_strategic_pivots",
        agent="leadership",
        topic="strategic_pivots",
        template=(
            '"{name}" site:{clean_domain} OR "strategic pivot" OR "business transformation" '
            'OR "restructuring" employees "job cuts" OR "new direction" '
            'OR "career opportunities" OR "headcount"'
        ),
        purpose=(
            "Identify major business model shifts and assess their workforce consequences. "
            "Did pivots create new roles or trigger headcount reductions? Reframed away "
            "from investor outcome framing toward employee impact framing."
        ),
        # primary_sources=["company_domain", "bloomberg.com", "techcrunch.com"],
        # signal_type="factual",
        # job_applicant_relevance=7,
        # tags=["leadership", "strategy", "pivots", "transformation", "headcount", "restructuring"],
    ),
    QueryEntry(
        id="leadership_executive_reputation",
        agent="leadership",
        topic="executive_reputation",
        template=(
            '"{name}" site:{clean_domain} OR CEO "Glassdoor" OR "Blind" OR "employee reviews" '
            '"approval rating" OR "leadership style" OR "management controversy" '
            'OR "executive criticism"'
        ),
        purpose=(
            "Assess public and employee-facing reputation of the executive team through "
            "approval ratings, employee review platforms, and any notable controversies. "
            "Glassdoor and Blind are weighted most heavily as they reflect direct employee "
            "experience rather than curated press coverage."
        ),
        # primary_sources=["glassdoor.com", "teamblind.com", "company_domain"],
        # signal_type="sentiment",
        # job_applicant_relevance=9,
        # tags=["leadership", "reputation", "glassdoor", "blind", "approval", "controversy"],
    ),
    QueryEntry(
        id="leadership_stability",
        agent="leadership",
        topic="leadership_stability",
        template=(
            '"{name}" site:{clean_domain} OR "chief" OR "VP" OR "vice president" '
            '"departed" OR "resigned" OR "appointed" OR "replaced" '
            '"executive turnover" OR "leadership changes" '
            "site:businessinsider.com OR site:wsj.com OR site:bloomberg.com"
        ),
        purpose=(
            "Assess C-suite and VP-level turnover patterns across key roles — CEO, CTO, "
            "CFO, CPO, CHRO. High churn is a major red flag for prospective employees "
            "and often signals deeper cultural or strategic instability."
        ),
        # primary_sources=["businessinsider.com", "wsj.com", "bloomberg.com"],
        # signal_type="factual",
        # job_applicant_relevance=9,
        # tags=["leadership", "stability", "turnover", "csuite", "vp", "departure"],
    ),
    QueryEntry(
        id="leadership_employee_treatment_during_hardship",
        agent="leadership",
        topic="employee_treatment_during_hardship",
        template=(
            '"{name}" site:{clean_domain} OR layoffs OR "workforce reduction" '
            'OR "restructuring" "severance" OR "notice period" '
            'OR "how it was handled" OR "employees react" '
            "site:techcrunch.com OR site:businessinsider.com OR site:glassdoor.com"
        ),
        purpose=(
            "Evaluate how leadership handled layoffs and restructurings — transparency, "
            "severance quality, and employee communication are the strongest proxies for "
            "leadership character. How a company treats people on the way out reveals "
            "how it treats people on the way in."
        ),
        # primary_sources=["techcrunch.com", "businessinsider.com", "glassdoor.com"],
        # signal_type="behavioral",
        # job_applicant_relevance=10,
        # tags=["leadership", "layoffs", "severance", "hardship", "transparency", "character"],
    ),
    QueryEntry(
        id="leadership_management_style_and_culture",
        agent="leadership",
        topic="management_style_and_culture",
        template=(
            '"{name}" site:{clean_domain} OR "management style" OR "work culture" '
            'OR "micromanagement" OR "psychological safety" OR "toxic culture" '
            'OR "employee autonomy" '
            "site:glassdoor.com OR site:teamblind.com OR site:reddit.com"
        ),
        purpose=(
            "Characterize the leadership management philosophy and its downstream effect "
            "on culture. Employee-sourced platforms are weighted most heavily here — "
            "Glassdoor, Blind, and Reddit surface unfiltered signals of psychological "
            "safety, micromanagement, and autonomy that official sources conceal."
        ),
        # primary_sources=["glassdoor.com", "teamblind.com", "reddit.com"],
        # signal_type="sentiment",
        # job_applicant_relevance=10,
        # tags=["leadership", "culture", "management", "psychological_safety", "micromanagement", "autonomy"],
    ),
    QueryEntry(
        id="leadership_vision_and_communication_clarity",
        agent="leadership",
        topic="vision_and_communication_clarity",
        template=(
            '"{name}" site:{clean_domain} OR CEO "all-hands" OR "town hall" '
            'OR "internal memo" OR "strategic vision" "employees" '
            '"communication" OR "transparency" OR "roadmap" OR "blindsided"'
        ),
        purpose=(
            "Assess whether leadership communicates a clear, consistent direction to "
            "employees. Employees being blindsided by major announcements is a strong "
            "negative signal. Town halls and internal memos are the best evidence of "
            "genuine transparency."
        ),
        # primary_sources=["company_domain", "glassdoor.com", "businessinsider.com"],
        # signal_type="behavioral",
        # job_applicant_relevance=8,
        # tags=["leadership", "communication", "transparency", "vision", "town_hall", "roadmap"],
    ),
    QueryEntry(
        id="leadership_dei_and_values_commitment",
        agent="leadership",
        topic="dei_and_values_commitment",
        template=(
            '"{name}" site:{clean_domain} OR "diversity" OR "DEI" OR "inclusion" '
            '"pay equity" OR "representation" OR "ERG" OR "diversity report" '
            'OR "DEI rollback" OR "diversity controversy" '
            "site:{clean_domain} OR site:builtin.com"
        ),
        purpose=(
            "Evaluate leadership's demonstrated DEI commitment through measurable actions "
            "rather than stated values. Rollbacks and controversies are equally important "
            "to surface as positive programs — they reveal the gap between stated and "
            "real values."
        ),
        # primary_sources=["company_domain", "builtin.com"],
        # signal_type="behavioral",
        # job_applicant_relevance=7,
        # tags=["leadership", "dei", "diversity", "inclusion", "values", "pay_equity", "erg"],
    ),
    QueryEntry(
        id="leadership_employee_development_investment",
        agent="leadership",
        topic="employee_development_investment",
        template=(
            '"{name}" site:{clean_domain} OR "employee development" '
            'OR "learning and development" OR "internal promotions" OR "career growth" '
            'OR "mentorship" OR "tuition reimbursement" OR "L&D budget" '
            "site:{clean_domain} OR site:glassdoor.com"
        ),
        purpose=(
            "Determine whether leadership actively invests in employee growth through L&D, "
            "mentorship programs, and internal promotion rates. Internal promotion rate "
            "is the single strongest signal that a company grows people rather than "
            "just hiring externally for every senior role."
        ),
        # primary_sources=["company_domain", "glassdoor.com"],
        # signal_type="behavioral",
        # job_applicant_relevance=8,
        # tags=["leadership", "development", "learning", "mentorship", "promotions", "career_growth"],
    ),
]
