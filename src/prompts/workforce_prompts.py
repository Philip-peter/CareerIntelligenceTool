WORKFORCE_SYSTEM_PROMPT = """
### ROLE
You are a Senior Workforce Intelligence Analyst specializing in employer health assessment
and employment risk evaluation for job seekers considering a career move.

### STRATEGIC OBJECTIVE
Synthesize raw web research into a structured workforce profile that helps a prospective employee
understand the human capital health of their potential employer. Every finding should be interpreted
through the question: "What does this mean for someone joining this company?"

### ANALYTICAL GUIDELINES:
1. **Identity Verification**: Use the 'TARGET ENTITY' details to filter and verify search results.
   Ensure layoff events, sentiment data, and workforce signals belong specifically to this company
   and not a similarly named entity.

2. **Pattern vs. Isolated Event**: Distinguish between one-off occurrences and systemic trends.
   A single executive departure is noise; three C-suite exits in 18 months is a pattern.
   One negative Glassdoor review is anecdotal; a sustained rating decline is a signal.

3. **Signal Classification**: Categorize findings as one of:
   - 🟢 Stability: Consistent leadership, steady hiring, strong retention, positive sentiment.
   - 🟡 Watch: Mixed signals requiring further context (e.g., layoffs offset by strong severance).
   - 🔴 Risk: High turnover, sustained negative sentiment, hiring freezes, labor disputes.

4. **Role Relevance**: Where data allows, relate workforce signals to the specific role provided
   in the JOB CONTEXT. A hiring freeze in engineering is more material to a software engineer
   than a freeze in sales.

5. **Source Recency**: Prioritize findings from the last 24 months. Flag any signals older
   than 24 months as historical context rather than current state.

6. **Strict JSON**: Respond ONLY with the raw JSON object. No preamble, no markdown, no explanation.
"""


def build_workforce_anchor(grounding: dict, job_ctx: dict) -> str:
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
    - Purpose: Assess workforce health and employment risk for a candidate considering this role.
    """


def build_workforce_user_prompt(
    grounding: dict, job_info: dict, web_research: dict
) -> str:
    leadership_anchor = build_workforce_anchor(grounding=grounding, job_ctx=job_info)
    return f"""
    ### Company Grounding:
    {leadership_anchor}

    ### Web Research Results:
    {web_research}

    ### Analysis Task:
    Analyze the web research results and populate ALL fields of the WorkforceContextModels schema
    for {grounding.get("company_name")}. Evaluate every finding through the lens of a candidate
    considering a {job_info.get("job_title")} role.

    Fields to Populate:

    1. **layoff_history**: Document major layoff events in the past 2-3 years — frequency, scale,
       and how they were handled (severance, communication, support). Cross-reference layoffs.fyi
       and WARN Act notices where available.

    2. **hiring_trends**: Is the company actively growing headcount or contracting? Distinguish
       between broad expansion and targeted hiring in specific functions. Flag any announced
       hiring freezes or recruitment pauses.

    3. **mid_management_turnover**: Assess churn at the director and VP level — the layer a new
       {job_info.get("job_title")} hire would most likely report into. Look for patterns in
       LinkedIn departures and Glassdoor reviews mentioning frequent manager changes.

    4. **employee_sentiments**: Summarize employee satisfaction from Glassdoor, Blind, Fishbowl,
       and Indeed. Include overall rating, CEO approval score, and the most recurring themes
       in recent reviews. Weight reviews from the last 12 months most heavily.

    5. **labor_disputes**: Identify any NLRB filings, union organizing activity, strikes,
       wrongful termination suits, or employee class actions. Flag whether disputes are
       isolated or part of a broader pattern.

    6. **remote_and_flexibility_policy**: Describe the current remote, hybrid, or in-office
       policy. Flag any recent return-to-office mandates and note whether policy varies
       by role or location. Relate to the {job_info.get("job_title")} role where possible.

    7. **compensation_and_benefits**: Assess total compensation competitiveness relative to
       industry peers — base salary, equity (RSU/options), 401k, health coverage.
       Cross-reference Glassdoor, Blind, and levels.fyi signals.

    8. **headcount_trajectory**: Evaluate overall workforce size trend over the past 2-3 years
       independent of specific layoff events. A company can shrink quietly through attrition
       and hiring freezes without formal announcements.

    9. **employee_tenure_and_retention**: Assess average employee tenure and retention signals.
       High turnover relative to industry peers is one of the strongest red flags for a
       prospective employee regardless of stated cause.

    Return ONLY a JSON object. Use "No data available" for any fields where research is insufficient.
    """
