LEADERSHIP_SYSTEM_PROMPT = """
### ROLE
You are a Senior Talent Intelligence Analyst specializing in Corporate Leadership Assessment for job seekers.

### STRATEGIC OBJECTIVE
Your goal is to cross-reference 'Internal Grounding' with 'Web Research' to create a high-fidelity leadership
profile from the perspective of a prospective employee — not an investor.
Focus on signals that indicate what it is like to work under this leadership team.

### EXTRACTION & VERIFICATION RULES:
1. **Identity Guardrail**: Use the 'TARGET COMPANY IDENTITY' to verify search results. Only include data
   that clearly belongs to this specific entity (matching domain or industry). Discard results
   that belong to similarly named companies.
2. **Employee Lens**: Prioritize signals that affect day-to-day employee experience — culture,
   communication, stability, growth opportunities, and how leadership behaves under pressure.
3. **Synthesize Signals**: Look for the "why" behind the data. For example, correlate CEO tenure
   with layoff history, or connect executive turnover patterns to Glassdoor sentiment trends.
4. **Source Credibility**: Weight employee-sourced platforms (Glassdoor, Blind, Reddit) heavily
   for culture fields. Use news sources (TechCrunch, Bloomberg, WSJ) for factual events like
   layoffs, leadership departures, and strategic pivots.
5. **Strict JSON**: Respond ONLY with the raw JSON object. No preamble, no markdown, no explanation.
"""


def build_leadership_anchor(grounding: dict, job_ctx: dict) -> str:
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
    """


def build_leadership_user_prompt(
    grounding: dict, job_info: dict, web_research: dict
) -> str:
    leadership_anchor = build_leadership_anchor(grounding=grounding, job_ctx=job_info)
    return f"""
    ### Company Grounding Context:
    {leadership_anchor}

    ### Web Research Results:
    {web_research}

    ### Analysis Task:
    Using the research results above, populate the LeadershipContextModels schema for {grounding.get("company_name")}
    strictly from the perspective of a job applicant evaluating this company.

    Fields to Populate:
    1. **ceo_tenure**: How long the current CEO has served and how their tenure has affected employees —
       include any reorgs, layoffs, or culture shifts that occurred under their watch.

    2. **founder_involvement**: Whether founders remain active in leadership and what effect their
       presence or absence has on company culture and employee experience.

    3. **strategic_pivots**: Major business model shifts under current leadership and their workforce
       consequences — did pivots create opportunities or trigger headcount reductions?

    4. **executive_reputation**: Public and employee-facing reputation of the executive team based on
       Glassdoor ratings, Blind reviews, approval scores, and any notable controversies.

    5. **leadership_stability**: C-suite and VP-level turnover patterns across key roles (CEO, CTO, CFO,
       CPO, CHRO). Flag high churn as a risk signal for prospective employees.

    6. **employee_treatment_during_hardship**: How leadership handled layoffs, restructurings, or downturns —
       assess transparency, severance quality, and communication during difficult periods.

    7. **management_style_and_culture**: Leadership's management philosophy and its effect on culture —
       look for signals of psychological safety, autonomy, micromanagement, or fear-based environments.

    8. **vision_and_communication_clarity**: Whether leadership communicates a clear, consistent direction
       to employees — look for evidence of town halls, internal memos, and whether employees feel informed.

    9. **dei_and_values_commitment**: Leadership's demonstrated commitment to DEI through measurable actions,
       not just stated values — flag rollbacks, controversies, or strong program investment.

    10. **employee_development_investment**: Whether leadership actively invests in employee growth through
        L&D budgets, mentorship, internal promotions, and career pathing programs.

    Return ONLY a JSON object. Use "No data available" for any fields where insufficient evidence exists.
    """
