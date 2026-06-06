from search_queries.registry import QueryEntry

STRATEGIC_DIRECTION_QUERIES: list[QueryEntry] = [
    QueryEntry(
        id="direction_earnings_call_forward_guidance",
        agent="direction",
        topic="earnings_call_forward_guidance",
        template=(
            '"{name}" site:{clean_domain} OR "earnings call" OR "earnings call transcript" '
            '"forward-looking" OR "guidance" OR "outlook" OR "we expect" '
            'OR "next quarter" OR "full year" OR "fiscal year" '
            '"2025" OR "2026" '
            "site:seekingalpha.com OR site:fool.com OR site:bloomberg.com"
        ),
        purpose=(
            "Extract official financial guidance from earnings call transcripts — the richest "
            "source of unfiltered forward-looking statements. Raised guidance signals growth "
            "and hiring ahead; withdrawn or lowered guidance typically precedes cost-cutting."
        ),
        # primary_sources=["seekingalpha.com", "fool.com", "bloomberg.com"],
        # signal_type="financial",
        # job_applicant_relevance=9,
        # tags=["direction", "earnings", "guidance", "outlook", "forward_looking"],
    ),
    QueryEntry(
        id="direction_ceo_earnings_call_statements",
        agent="direction",
        topic="ceo_strategic_narrative",
        template=(
            '"{name}" CEO "prepared remarks" OR "opening statement" '
            'OR "I am pleased to report" OR "our strategy" OR "we are focused on" '
            'OR "key priorities" OR "in the coming year" OR "we remain committed to" '
            '"earnings" "2025" OR "2026" '
            "site:seekingalpha.com OR site:fool.com OR site:sec.gov"
        ),
        purpose=(
            "Target the CEO's prepared remarks specifically — the opening statement of an "
            "earnings call is where strategic direction is declared most explicitly. "
            "Distinguish concrete commitments from aspirational language."
        ),
        # primary_sources=["seekingalpha.com", "fool.com", "sec.gov"],
        # signal_type="behavioral",
        # job_applicant_relevance=9,
        # tags=["direction", "ceo", "strategy", "narrative", "earnings", "prepared_remarks"],
    ),
    QueryEntry(
        id="direction_analyst_qa_from_earnings",
        agent="direction",
        topic="analyst_pressure_points",
        template=(
            '"{name}" "earnings call" "question and answer" OR "Q&A" OR "analyst question" '
            '"concerns" OR "headwinds" OR "risk" OR "slowdown" OR "competition" '
            'OR "when do you expect" OR "can you elaborate" '
            '"2025" OR "2026" '
            "site:seekingalpha.com OR site:fool.com"
        ),
        purpose=(
            "Surface the Q&A section of earnings calls where analysts pressure-test "
            "management's claims. This is where risks the CEO won't volunteer are exposed — "
            "analysts ask the uncomfortable questions in the public record."
        ),
        # primary_sources=["seekingalpha.com", "fool.com"],
        # signal_type="factual",
        # job_applicant_relevance=8,
        # tags=["direction", "analyst", "risk", "earnings", "qa", "pressure_points"],
    ),
    QueryEntry(
        id="direction_investor_day_strategic_targets",
        agent="direction",
        topic="investor_day_long_term_targets",
        template=(
            '"{name}" site:{clean_domain} OR "investor day" OR "analyst day" '
            'OR "capital markets day" OR "long-term targets" OR "three year plan" '
            'OR "five year plan" OR "strategic plan" OR "we intend to" '
            '"2024" OR "2025" OR "2026" '
            "site:{clean_domain} OR site:seekingalpha.com OR site:bloomberg.com"
        ),
        purpose=(
            "Extract multi-year revenue targets, product roadmaps, and workforce plans from "
            "investor day presentations — the longest-horizon forward statements management "
            "makes publicly. No investor day in 2+ years is itself a stagnation signal."
        ),
        # primary_sources=["company_domain", "seekingalpha.com", "bloomberg.com"],
        # signal_type="factual",
        # job_applicant_relevance=8,
        # tags=["direction", "investor_day", "targets", "long_term", "strategy", "roadmap"],
    ),
    QueryEntry(
        id="direction_recent_capital_investments",
        agent="direction",
        topic="recent_capital_investments",
        template=(
            '"{name}" site:{clean_domain} OR "capital investment" OR "R&D spending" '
            'OR "new facility" OR "data center" OR "infrastructure investment" '
            'OR "capex" OR "we are building" OR "expanding capacity" '
            '"2024" OR "2025" OR "2026" '
            "site:bloomberg.com OR site:wsj.com OR site:reuters.com"
        ),
        purpose=(
            "Identify where capital is being deployed — new facilities, R&D spend, and "
            "capex are leading indicators of where headcount and career opportunities will "
            "grow. Companies invest ahead of hiring."
        ),
        # primary_sources=["bloomberg.com", "wsj.com", "reuters.com"],
        # signal_type="financial",
        # job_applicant_relevance=8,
        # tags=["direction", "capex", "investment", "growth", "infrastructure", "rd"],
    ),
    QueryEntry(
        id="direction_hiring_signals",
        agent="direction",
        topic="hiring_signals",
        template=(
            '"{name}" site:{clean_domain} OR "we are hiring" OR "join our team" '
            'OR "new roles" OR "open positions" OR "rapidly growing team" '
            'OR "AI engineer" OR "data scientist" OR "product manager" '
            'OR "expanding our" OR "building out" '
            "site:linkedin.com OR site:builtin.com OR site:levels.fyi"
        ),
        purpose=(
            "Assess the composition of active job postings — the types of roles a company "
            "is hiring for reveals strategic direction more honestly than any press release. "
            "Flag whether hiring is concentrated in growth areas or limited to backfill."
        ),
        # primary_sources=["linkedin.com", "builtin.com", "levels.fyi"],
        # signal_type="factual",
        # job_applicant_relevance=10,
        # tags=["direction", "hiring", "roles", "growth", "strategy", "composition"],
    ),
    QueryEntry(
        id="direction_strategic_alliances_and_partnerships",
        agent="direction",
        topic="strategic_alliances_and_partnerships",
        template=(
            '"{name}" site:{clean_domain} OR "strategic partnership" OR "strategic alliance" '
            'OR "joint venture" OR "collaboration agreement" OR "signed agreement with" '
            'OR "partnered with" OR "expanded partnership" '
            '"2024" OR "2025" OR "2026" '
            "site:prnewswire.com OR site:businesswire.com OR site:bloomberg.com"
        ),
        purpose=(
            "Document new partnerships and alliances to understand which ecosystems the "
            "company is aligning with and which capabilities it is choosing to build "
            "externally rather than internally."
        ),
        # primary_sources=["prnewswire.com", "businesswire.com", "bloomberg.com"],
        # signal_type="factual",
        # job_applicant_relevance=7,
        # tags=["direction", "partnerships", "alliances", "ecosystem", "joint_venture"],
    ),
    QueryEntry(
        id="direction_mergers_and_acquisitions",
        agent="direction",
        topic="mergers_and_acquisitions",
        template=(
            '"{name}" site:{clean_domain} OR "acquisition" OR "acquired" OR "merger" '
            'OR "acquires" OR "to be acquired" OR "definitive agreement" '
            'OR "completed acquisition" OR "purchase price" '
            '"2024" OR "2025" OR "2026" '
            "site:sec.gov OR site:bloomberg.com OR site:wsj.com OR site:reuters.com"
        ),
        purpose=(
            "Document completed and announced M&A activity. Assess integration risk for "
            "new hires joining during post-merger periods and flag if the company itself "
            "is a rumored or confirmed acquisition target."
        ),
        # primary_sources=["sec.gov", "bloomberg.com", "wsj.com", "reuters.com"],
        # signal_type="factual",
        # job_applicant_relevance=8,
        # tags=["direction", "ma", "acquisition", "merger", "integration", "risk"],
    ),
    QueryEntry(
        id="direction_new_products_and_ventures",
        agent="direction",
        topic="new_products_and_ventures",
        template=(
            '"{name}" site:{clean_domain} OR "launched" OR "new product" OR "new service" '
            'OR "entering the market" OR "new business unit" OR "new division" '
            'OR "product announcement" OR "generally available" OR "beta launch" '
            '"2024" OR "2025" OR "2026" '
            "site:{clean_domain} OR site:techcrunch.com OR site:venturebeat.com"
        ),
        purpose=(
            "Identify new product launches and business line entries to reveal where future "
            "headcount investment will be concentrated. New ventures signal which teams "
            "are being built and which are in maintenance mode."
        ),
        # primary_sources=["company_domain", "techcrunch.com", "venturebeat.com"],
        # signal_type="factual",
        # job_applicant_relevance=8,
        # tags=["direction", "products", "launches", "ventures", "innovation", "new_business"],
    ),
    QueryEntry(
        id="direction_market_and_geographic_expansion",
        agent="direction",
        topic="market_and_geographic_expansion",
        template=(
            '"{name}" site:{clean_domain} OR "expansion" OR "entering" OR "new market" '
            'OR "international growth" OR "new region" OR "opened office" '
            'OR "APAC" OR "EMEA" OR "Latin America" OR "new vertical" '
            '"2024" OR "2025" OR "2026" '
            "site:{clean_domain} OR site:bloomberg.com OR site:businessinsider.com"
        ),
        purpose=(
            "Assess geographic and vertical expansion plans. Flag whether expansion is "
            "backed by signed contracts and concrete hiring plans or is aspirational "
            "language only — weight signed contracts significantly higher."
        ),
        # primary_sources=["company_domain", "bloomberg.com", "businessinsider.com"],
        # signal_type="factual",
        # job_applicant_relevance=7,
        # tags=["direction", "expansion", "geographic", "international", "markets", "apac", "emea"],
    ),
    QueryEntry(
        id="direction_ai_and_technology_roadmap",
        agent="direction",
        topic="ai_and_technology_roadmap",
        template=(
            '"{name}" site:{clean_domain} OR "AI roadmap" OR "technology investment" '
            'OR "AI strategy" OR "machine learning" OR "generative AI" OR "AI agents" '
            'OR "platform modernization" OR "tech stack" OR "engineering investment" '
            '"2024" OR "2025" OR "2026" '
            "site:{clean_domain} OR site:techcrunch.com OR site:wired.com "
            "OR site:venturebeat.com"
        ),
        purpose=(
            "Assess AI and technology investment direction and its role implications. "
            "Distinguish between AI building new product capabilities vs. AI being used "
            "internally to reduce headcount. Directly flag automation risk to the "
            "candidate's target role where possible."
        ),
        # primary_sources=["company_domain", "techcrunch.com", "wired.com", "venturebeat.com"],
        # signal_type="factual",
        # job_applicant_relevance=9,
        # tags=["direction", "ai", "technology", "roadmap", "automation", "genai"],
    ),
    QueryEntry(
        id="direction_government_and_enterprise_contracts",
        agent="direction",
        topic="government_and_enterprise_contracts",
        template=(
            '"{name}" site:{clean_domain} OR "contract win" OR "government contract" '
            'OR "enterprise deal" OR "multi-year agreement" OR "awarded contract" '
            'OR "selected by" OR "chosen as" OR "signed deal" '
            '"2024" OR "2025" OR "2026" '
            "site:{clean_domain} OR site:prnewswire.com OR site:govwin.com "
            "OR site:bloomberg.com"
        ),
        purpose=(
            "Document large contract wins as leading indicators of near-term hiring surges. "
            "Delivery headcount typically grows within 90 days of a major contract award — "
            "contract win velocity is the most reliable near-term hiring signal."
        ),
        # primary_sources=["company_domain", "prnewswire.com", "govwin.com", "bloomberg.com"],
        # signal_type="factual",
        # job_applicant_relevance=8,
        # tags=["direction", "contracts", "government", "enterprise", "hiring", "revenue"],
    ),
    QueryEntry(
        id="direction_divestitures_and_business_exits",
        agent="direction",
        topic="divestitures_and_business_exits",
        template=(
            '"{name}" site:{clean_domain} OR "divested" OR "sold off" OR "exiting" '
            'OR "discontinued" OR "wind down" OR "spinning off" OR "carve out" '
            'OR "strategic review" OR "non-core assets" '
            '"2024" OR "2025" OR "2026" '
            "site:sec.gov OR site:wsj.com OR site:bloomberg.com OR site:reuters.com"
        ),
        purpose=(
            "Identify divisions, product lines, or markets being exited. Divestitures "
            "signal where the company is pulling investment and cutting headcount — "
            "candidates joining a divested or exiting unit face elevated redundancy risk."
        ),
        # primary_sources=["sec.gov", "wsj.com", "bloomberg.com", "reuters.com"],
        # signal_type="factual",
        # job_applicant_relevance=9,
        # tags=["direction", "divestiture", "exit", "restructuring", "risk", "wind_down"],
    ),
]
