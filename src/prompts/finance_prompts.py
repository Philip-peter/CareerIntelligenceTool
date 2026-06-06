FINANCE_SYSTEM_PROMPT = """
You are a Senior Equity Research Analyst. Your goal is to synthesize internal company
grounding data with external web research to produce a high-fidelity financial profile.

### Strategic Constraints:
1. **Verification**: Use the 'COMPANY IDENTITY' section to verify that the 'Web Research Results'
   actually pertain to the correct entity. Cross-reference domains and industries.
2. **Role Relevance**: Keep the financial analysis relevant to the 'Target Role' context.
3. **Data Integrity**: If search results provide conflicting numbers, prefer data from
   official company domains or reputable financial news outlets.
4. **Strict JSON**: Respond only with the requested JSON schema.
"""


def build_finance_anchor(grounding: dict, job_ctx: dict) -> str:
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


def build_finance_user_prompt(
    grounding: dict, job_info: dict, web_research: dict
) -> str:
    company_anchor = build_finance_anchor(grounding=grounding, job_ctx=job_info)
    return f"""
    ### Internal Grounding Data:
    {company_anchor}

    ### Web Research Results:
    {web_research}

    ### Analysis Task:
    Using the research results above, populate the FinancialContextModels schema for {grounding.get("company_name")}.
    Focus on:
    - Revenue Growth (CAGR)
    - Profitability Margins
    - Debt and Leverage
    - Cash Flow Stability
    - Revenue Concentration
    - Investor Sentiment
    - Funding and Runway
    - Financial Distress Signals

    If no specific financial data was found in the research for a field, return "No data available".
    """
