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
            "occurred under their tenure — reorgs, layoffs, culture shifts."
        ),
        # primary_sources=["company_domain", "bloomberg.com", "wsj.com"],
        # signal_type="factual",
        # job_applicant_relevance=8,
        # tags=["leadership", "ceo", "stability", "tenure"],
    ),
    # ... rest of leadership queries
]
