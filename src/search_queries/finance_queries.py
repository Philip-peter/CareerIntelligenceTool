import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

from src.search_queries.registry import QueryEntry  # noqa: E402

FINANCE_QUERIES: list[QueryEntry] = [
    QueryEntry(
        id="finance_revenue_growth",
        agent="finance",
        topic="revenue_growth",
        template=(
            '"{name}" site:{clean_domain} OR site:sec.gov '
            '"revenue growth" OR "annual revenue" OR "revenue trend" '
            '"2023" OR "2024" OR "2025" "year over year" OR "YoY" OR "CAGR" '
            '"growing" OR "declining" OR "flat revenue"'
        ),
        purpose=(
            "Summarize revenue growth trajectory and translate it into workforce stability "
            "signals. Accelerating growth suggests hiring demand; decelerating or negative "
            "growth often precedes cost-cutting and layoffs. IR domain and SEC filings are "
            "the most reliable sources for revenue tables."
        ),
        # primary_sources=["sec.gov", "company_domain", "bloomberg.com"],
        # signal_type="financial",
        # job_applicant_relevance=8,
        # tags=["finance", "revenue", "growth", "yoy", "cagr", "stability"],
    ),
    QueryEntry(
        id="finance_profitability",
        agent="finance",
        topic="profitability",
        template=(
            '"{name}" site:{clean_domain} OR site:sec.gov {industry} '
            '"gross margin" OR "operating margin" OR "net margin" OR "EBITDA" '
            '"2024" OR "2025" "profitable" OR "profitability" '
            'OR "operating loss" OR "path to profitability"'
        ),
        purpose=(
            "Assess margin trends and financial sustainability as an employer. Sustained "
            "losses or margin compression often trigger cost reduction programs that affect "
            "headcount and compensation. Path to profitability language signals a company "
            "still burning cash."
        ),
        # primary_sources=["sec.gov", "company_domain", "seekingalpha.com"],
        # signal_type="financial",
        # job_applicant_relevance=7,
        # tags=["finance", "profitability", "margins", "ebitda", "operating_loss"],
    ),
    QueryEntry(
        id="finance_debt",
        agent="finance",
        topic="debt",
        template=(
            '"{name}" site:{clean_domain} OR site:sec.gov '
            '"debt-to-equity" OR "debt-to-EBITDA" OR "total liabilities" OR "long-term debt" '
            '"credit rating" OR "leverage" OR "covenant" OR "refinancing" '
            "site:moodys.com OR site:spglobal.com OR site:fitchratings.com"
        ),
        purpose=(
            "Assess leverage levels and refinancing risk. High debt burdens constrain "
            "investment in headcount, compensation, and benefits — and can force "
            "restructuring if refinancing conditions deteriorate. Credit agency sources "
            "are more reliable than news for current ratings."
        ),
        # primary_sources=["sec.gov", "moodys.com", "spglobal.com", "fitchratings.com"],
        # signal_type="financial",
        # job_applicant_relevance=7,
        # tags=["finance", "debt", "leverage", "credit", "covenant", "refinancing"],
    ),
    QueryEntry(
        id="finance_cash_flow",
        agent="finance",
        topic="cash_flow",
        template=(
            '"{name}" site:{clean_domain} OR site:sec.gov '
            '"cash flow from operations" OR "free cash flow" OR "FCF" '
            '"capital expenditures" OR "burn rate" OR "cash runway" OR "cash position" '
            '"2024" OR "2025"'
        ),
        purpose=(
            "Assess cash flow stability and ability to sustain payroll, benefits, and "
            "people investment. Burn rate and runway are the most job-applicant-relevant "
            "financial signals — especially for private or pre-profitability employers. "
            "Statement of Cash Flows in SEC filings is the primary source."
        ),
        # primary_sources=["sec.gov", "company_domain", "bloomberg.com"],
        # signal_type="financial",
        # job_applicant_relevance=9,
        # tags=["finance", "cashflow", "fcf", "burn_rate", "runway", "operations"],
    ),
    QueryEntry(
        id="finance_revenue_concentration",
        agent="finance",
        topic="revenue_concentration",
        template=(
            '"{name}" site:{clean_domain} OR site:sec.gov '
            '"revenue concentration" OR "customer concentration" OR "major customers" '
            '"percent of total revenue" OR "accounts for" OR "single customer" '
            'OR "top 10 customers"'
        ),
        purpose=(
            "Assess single-customer or single-product revenue dependency. High concentration "
            "means one contract loss can trigger rapid workforce reductions. This language "
            "appears verbatim in 10-K Risk Factors and Notes to Financial Statements — "
            "SEC is the most reliable source."
        ),
        # primary_sources=["sec.gov", "company_domain"],
        # signal_type="financial",
        # job_applicant_relevance=8,
        # tags=["finance", "concentration", "customer_risk", "revenue", "10k", "risk_factors"],
    ),
    QueryEntry(
        id="finance_investor_sentiment",
        agent="finance",
        topic="investor_sentiment",
        template=(
            '"{name}" site:{clean_domain} OR "investor presentation" OR "earnings release" '
            'OR "analyst rating" OR "price target" OR "outlook" OR "guidance" '
            '"2024" OR "2025" OR "2026" '
            "site:seekingalpha.com OR site:bloomberg.com OR site:wsj.com"
        ),
        purpose=(
            "Translate investor and analyst signals into workforce implications. Emphasis "
            "on efficiency or right-sizing in IR decks is a layoff precursor. Analyst "
            "sources are included alongside official IR to counterbalance optimistic "
            "management framing."
        ),
        # primary_sources=["seekingalpha.com", "bloomberg.com", "wsj.com", "company_domain"],
        # signal_type="financial",
        # job_applicant_relevance=7,
        # tags=["finance", "investor", "sentiment", "guidance", "analyst", "outlook"],
    ),
    QueryEntry(
        id="finance_funding_and_runway",
        agent="finance",
        topic="funding_and_runway",
        template=(
            '"{name}" site:{clean_domain} '
            '"funding round" OR "Series A" OR "Series B" OR "venture capital" OR "raised" '
            'OR "runway" OR "cash reserves" OR "burn rate" OR "IPO" OR "pre-IPO" '
            "site:crunchbase.com OR site:techcrunch.com OR site:bloomberg.com"
        ),
        purpose=(
            "For private, pre-IPO, or venture-backed employers, assess funding stage, "
            "total capital raised, burn rate, and cash runway. A strong role at an "
            "underfunded company is a high employment risk. Crunchbase is the primary "
            "source for private company funding data."
        ),
        # primary_sources=["crunchbase.com", "techcrunch.com", "bloomberg.com", "company_domain"],
        # signal_type="financial",
        # job_applicant_relevance=10,
        # tags=["finance", "funding", "runway", "startup", "venture", "series", "ipo"],
    ),
    QueryEntry(
        id="finance_financial_distress_signals",
        agent="finance",
        topic="financial_distress_signals",
        template=(
            '"{name}" site:{clean_domain} OR site:sec.gov '
            '"going concern" OR "covenant breach" OR "credit downgrade" OR "missed payment" '
            'OR "debt restructuring" OR "bankruptcy" OR "financial difficulty" '
            'OR "liquidity risk" '
            "site:bloomberg.com OR site:wsj.com OR site:reuters.com"
        ),
        purpose=(
            "Identify the earliest warning indicators of financial distress that will not "
            "surface in standard revenue or margin queries. Going concern warnings in SEC "
            "filings typically precede mass layoffs by 6-12 months — the highest urgency "
            "signal in the entire finance agent."
        ),
        # primary_sources=["sec.gov", "bloomberg.com", "wsj.com", "reuters.com"],
        # signal_type="financial",
        # job_applicant_relevance=10,
        # tags=["finance", "distress", "going_concern", "bankruptcy", "covenant", "liquidity"],
    ),
]
