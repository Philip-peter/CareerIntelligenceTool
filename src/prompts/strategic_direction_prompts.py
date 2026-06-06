STRATEGIC_DIRECTION_SYSTEM_PROMPT = """
### ROLE
You are a Senior Strategic Intelligence Analyst specializing in corporate direction
assessment for job seekers evaluating the long-term viability and growth trajectory
of a prospective employer.

### STRATEGIC OBJECTIVE
Your goal is to synthesize earnings call transcripts, investor communications, M&A
activity, hiring signals, and strategic announcements into a clear forward-looking
picture of where this company is heading. Every finding must be interpreted through
one lens: "Is this a company worth joining right now, and will it still be a good
employer in 2-3 years?"

### ANALYTICAL FRAMEWORK

1. **Identity Guardrail**: Use the 'TARGET COMPANY IDENTITY' to verify all research
    findings belong to this specific entity. Discard results from similarly named
    companies, subsidiaries, or unrelated entities sharing a common name.

2. **Distinguish Signal from Noise**: Not all announcements are equal. Weight findings
    by credibility and specificity:
    - HIGHEST SIGNAL: Signed contracts, completed acquisitions, concrete hiring numbers,
        official guidance with specific figures.
    - MEDIUM SIGNAL: CEO prepared remarks, investor day targets, partnership announcements
        with named counterparties.
    - LOWEST SIGNAL: Aspirational language without commitments, unnamed "strategic reviews",
        or press releases without financial detail.

3. **Forward vs. Backward Orientation**: This agent is explicitly forward-looking.
    Prioritize findings from the past 12-18 months. Flag anything older than 24 months
    as historical context only. The question is not where the company has been —
    it is where it is going.

4. **Translate to Workforce Implications**: Every strategic finding must be connected
    to a workforce implication for the candidate. A $500M AI investment means nothing
    to a job seeker unless you explain what it means for hiring, role stability, and
    career growth in their specific function.

5. **Role Relevance**: Where data allows, relate strategic direction signals to the
    specific job title provided in the JOB CONTEXT. A divestiture of a professional
    services division is a critical risk for a consultant but irrelevant for an engineer
    joining the product team.

6. **Acquisitions and Integration Risk**: Flag any completed acquisitions from the past
    18 months as potential integration turbulence zones. New hires joining during active
    post-merger integration face elevated uncertainty around team structures, reporting
    lines, and culture.

7. **Absence of Direction is a Signal**: If a company has issued no investor day targets,
    made no significant partnerships or acquisitions, launched no new products, and issued
    vague or withdrawn guidance — treat this as a stagnation signal, not a neutral finding.
    Reflect it in the relevant fields.

8. **Strict JSON**: Respond ONLY with the raw JSON object matching the CompanyDirectionModels
    schema. No preamble, no markdown, no explanation.
"""


def build_strategic_direction_anchor(grounding: dict, job_ctx: dict) -> str:
    return f"""
    TARGET COMPANY IDENTITY:
    - Legal Name: {grounding.get("company_name")}
    - Corporate Domain: {grounding.get("company_domain")}
    - LinkedIn: {grounding.get("company_linkedin_url")}
    - Industry: {grounding.get("company_industry")}
    - Official Website: {grounding.get("company_official_url")}

    JOB CONTEXT:
    - Target Role: {job_ctx.get("job_title")}
    - Role Description: {job_ctx.get("job_description", "")[:500]}...
    - Purpose: Assess the company's strategic direction and forward momentum to determine
    whether this is a growing, stable, or contracting employer over the next 2-3 years.
    """


def build_strategic_direction_user_prompt(
    grounding: dict, job_info: dict, web_research: dict
) -> str:
    strategic_direction_anchor = build_strategic_direction_anchor(
        grounding=grounding, job_ctx=job_info
    )
    return f"""
    ### Company Grounding Context:
    {strategic_direction_anchor}

    ### Web Research Results:
    {web_research}

    ### Analysis Task:
    Using the research results above, populate ALL fields of the CompanyDirectionModels schema
    for {grounding.get("company_name")}. Evaluate every finding through the lens of a candidate
    considering a {job_info.get("job_title")} role and assess whether the company's strategic
    direction represents a growth opportunity or an employment risk.

    Fields to Populate:

    1. **earnings_call_forward_guidance**: What is the most recent official guidance issued
        by management? Are they raising, maintaining, or lowering targets? Translate the
        guidance into a workforce signal — raised guidance suggests investment ahead;
        lowered or withdrawn guidance often precedes cost-cutting.

    2. **ceo_strategic_narrative**: What did the CEO declare as the company's strategic
        priorities in the most recent earnings call prepared remarks? Distinguish between
        concrete commitments and aspirational language. What does the narrative mean for
        someone joining this company today?

    3. **analyst_pressure_points**: What risks and concerns did analysts raise during the
        most recent earnings call Q&A? These are the vulnerabilities management had to
        defend under pressure — surface what the CEO was reluctant to volunteer.

    4. **investor_day_long_term_targets**: What multi-year targets and workforce plans were
        declared at the most recent investor day or capital markets day? If no investor day
        has been held in the past 2 years, flag this as a low visibility signal.

    5. **recent_capital_investments**: What major capital commitments has the company made
        in the past 12-18 months? Where is money being deployed — and what does that mean
        for where headcount will grow?

    6. **hiring_signals**: What types of roles has the company been actively recruiting for
        in the past 3-6 months? What does the composition of open roles reveal about which
        teams are growing and which are being wound down?

    7. **strategic_alliances_and_partnerships**: What significant new partnerships or
        alliances have been announced? What do they signal about which markets and ecosystems
        the company is aligning with?

    8. **mergers_and_acquisitions**: What acquisitions or mergers have been completed or
        announced in the past 12-24 months? Assess integration risk for a new hire and flag
        if the company itself is a rumored acquisition target.

    9. **new_products_and_ventures**: What new products, services, or business lines have
        been launched in the past 12-18 months? Where will future headcount investment
        be concentrated based on these launches?

    10. **market_and_geographic_expansion**: Is the company expanding into new geographies
        or customer verticals? Is the expansion backed by signed contracts and concrete
        hiring plans, or is it aspirational language only?

    11. **ai_and_technology_roadmap**: What is the company's stated AI and technology
        investment direction? Is AI being used to build new capabilities or to reduce
        headcount? Directly flag any automation risk to the {job_info.get("job_title")} role.

    12. **government_and_enterprise_contracts**: What significant contract wins have been
        announced in the past 12-18 months? Large contracts are leading indicators of
        near-term hiring surges in delivery and implementation teams.

    13. **divestitures_and_business_exits**: What divisions, product lines, or markets has
        the company exited or announced plans to exit? Flag any divestiture that could
        affect the {job_info.get("job_title")} role or the team the candidate would be joining.

    Return ONLY a JSON object. Use "No data available" for any fields where research is insufficient.
    """
