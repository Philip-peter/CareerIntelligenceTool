INDUSTRY_SYSTEM_PROMPT = """
### ROLE
You are a Senior Talent Market Intelligence Analyst specializing in industry risk assessment
for job seekers evaluating career moves.

### STRATEGIC OBJECTIVE
Synthesize raw web research and company grounding into a structured industry profile that helps
a prospective employee understand the structural forces shaping their potential employer's sector.
The goal is not financial analysis — it is career risk and opportunity assessment.

### ANALYTICAL FRAMEWORK:
1. **Contextual Filtering**: Use the 'TARGET ENTITY' details to ensure all research findings
are scoped to the correct industry and sector. Discard results that belong to adjacent or
unrelated industries (e.g., distinguish 'Cloud Infrastructure' from 'Enterprise SaaS' if applicable).

2. **Job-Applicant Lens**: Every finding should be interpreted through the question:
"What does this mean for someone working here?" Translate industry dynamics into
workforce implications — hiring trends, layoff risk, role stability, and career ceiling.

3. **Role Relevance**: Where possible, relate industry forces to the specific job title provided
in the JOB CONTEXT. A regulatory shift may affect a compliance role differently than an engineering role.

4. **AI and Automation**: Assess whether AI represents a structural threat to roles in this
industry or a tailwind creating new opportunities. Distinguish between AI augmenting workers
and AI eliminating job categories outright.

5. **Source Conflicts**: If sources disagree on market outlook or competitive position,
default to the most recent and reputable source. Flag the disagreement in your output.

6. **Strict JSON**: Respond ONLY with the raw JSON object. No preamble, no markdown, no explanation.
"""


def build_industry_anchor(grounding: dict, job_ctx: dict) -> str:
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
    - Purpose: Assess industry-level forces that affect job security, career growth,
    and employer stability for a candidate considering this role.
    """


def build_industry_user_prompt(
    grounding: dict, job_info: dict, web_research: dict
) -> str:
    industry_anchor = build_industry_anchor(grounding=grounding, job_ctx=job_info)
    return f"""
    ### Company & Industry Grounding:
    {industry_anchor}

    ### Web Research Results:
    {web_research}

    ### Analysis Task:
    Perform an industry analysis for {grounding.get("company_name")} in the {grounding.get("company_industry")} sector.
    Evaluate all findings through the lens of a job applicant considering a {job_info.get("job_title")} role.

    Populate ALL fields of the IndustryContextModels schema:

    1. **cyclic_or_defensive**: Is this industry cyclical or defensive? What happens to headcount
    and hiring in this sector during economic downturns? Cite historical patterns where available.

    2. **regulatory_environment**: What regulatory bodies govern this industry? How does compliance
    burden affect company operations, workforce stability, and risk of forced restructuring or shutdown?

    3. **ai_disruption**: Is AI a threat to roles in this industry or a growth driver creating new ones?
    Distinguish between automation of specific tasks vs. elimination of entire job categories.
    Relate findings to the {job_info.get("job_title")} role where possible.

    4. **competition**: How competitive is this industry and what does that mean for the company's
    stability as an employer? Does the company hold a durable market position or is it fighting
    for survival in a commoditized market?

    5. **industry_growth_trajectory**: Is the industry expanding or contracting? What does the
    talent demand outlook look like — are companies in this sector actively hiring or reducing headcount?

    6. **consolidation_and_ma_risk**: How active is M&A in this industry? Is the company a likely
    acquisition target or acquirer, and what would that mean for employees in terms of redundancies
    or culture disruption?

    7. **offshoring_and_automation_risk**: Are roles in this industry structurally at risk of being
    offshored, outsourced, or automated — independent of this company's specific performance?

    Return ONLY a JSON object. Use "No data available" for any fields where research is insufficient.
    """
