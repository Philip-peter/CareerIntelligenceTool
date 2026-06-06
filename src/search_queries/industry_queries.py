from search_queries.registry import QueryEntry

INDUSTRY_QUERIES: list[QueryEntry] = [
    QueryEntry(
        id="industry_cyclic_or_defensive",
        agent="industry",
        topic="cyclic_or_defensive",
        template=(
            '"{name}" {industry} "economic downturn" OR "recession" OR "slowdown" '
            '"layoffs" OR "hiring freeze" OR "budget cuts" OR "workforce impact" '
            "site:{clean_domain} OR site:bloomberg.com OR site:wsj.com"
        ),
        purpose=(
            "Determine whether the industry is cyclical or defensive and what that means "
            "for workforce stability during economic downturns. Focus on whether downturns "
            "historically trigger layoffs and hiring freezes in this sector — not stock "
            "defensiveness, which is an investor signal irrelevant to job applicants."
        ),
        # primary_sources=["company_domain", "bloomberg.com", "wsj.com"],
        # signal_type="factual",
        # job_applicant_relevance=8,
        # tags=["industry", "cyclical", "defensive", "recession", "stability", "workforce"],
    ),
    QueryEntry(
        id="industry_regulatory_environment",
        agent="industry",
        topic="regulatory_environment",
        template=(
            'site:sec.gov "{name}" "risk factors" "regulatory" OR "compliance" '
            'OR "government oversight" "operations" OR "workforce" '
            'OR "business continuity" OR "license" OR "penalty"'
        ),
        purpose=(
            "Identify regulatory oversight and its implications for company operations, "
            "workforce stability, and risk of forced restructuring or shutdown. SEC 10-K "
            "Risk Factors sections use this language verbatim — making SEC the most "
            "reliable source for regulatory risk disclosure."
        ),
        # primary_sources=["sec.gov"],
        # signal_type="factual",
        # job_applicant_relevance=7,
        # tags=["industry", "regulatory", "compliance", "risk", "sec", "10k", "government"],
    ),
    QueryEntry(
        id="industry_ai_disruption",
        agent="industry",
        topic="ai_disruption",
        template=(
            '"{name}" {industry} "AI" OR "automation" OR "artificial intelligence" '
            '"job displacement" OR "workforce reduction" OR "replacing roles" '
            'OR "productivity gains" OR "AI strategy" OR "AI investment" '
            "site:{clean_domain} OR site:techcrunch.com OR site:wired.com"
        ),
        purpose=(
            "Assess whether AI is a structural threat to roles in this industry or a "
            "growth driver creating new opportunities. Broadened beyond the company domain "
            "to capture industry-wide automation and job displacement signals — not just "
            "what the company says about its own AI strategy."
        ),
        # primary_sources=["company_domain", "techcrunch.com", "wired.com"],
        # signal_type="factual",
        # job_applicant_relevance=9,
        # tags=["industry", "ai", "automation", "disruption", "displacement", "productivity"],
    ),
    QueryEntry(
        id="industry_competition",
        agent="industry",
        topic="competition",
        template=(
            '"{name}" {industry} competitors "market share" OR "market position" '
            'OR "competitive advantage" "losing ground" OR "dominant player" '
            'OR "industry leader" OR "threat from" '
            "site:{clean_domain} OR site:bloomberg.com OR site:businessinsider.com"
        ),
        purpose=(
            "Assess the competitive landscape as a proxy for employer stability. Intense "
            "competition with margin pressure often precedes cost-cutting and layoffs. "
            "A durable market position signals a more stable employer. Reframed away from "
            "investor metrics like pricing power and switching costs."
        ),
        # primary_sources=["company_domain", "bloomberg.com", "businessinsider.com"],
        # signal_type="factual",
        # job_applicant_relevance=7,
        # tags=["industry", "competition", "market_share", "stability", "competitive_advantage"],
    ),
    QueryEntry(
        id="industry_growth_trajectory",
        agent="industry",
        topic="industry_growth_trajectory",
        template=(
            '{industry} "industry growth" OR "market size" OR "market forecast" '
            'OR "sector outlook" "hiring trends" OR "talent demand" '
            'OR "expanding" OR "declining" OR "headcount growth" '
            "site:bloomberg.com OR site:mckinsey.com OR site:forrester.com "
            "OR site:gartner.com"
        ),
        purpose=(
            "Determine whether the industry is expanding or contracting and what that "
            "implies for long-term hiring outlook and job security. Analyst and research "
            "firm sources are prioritized over news — Gartner, McKinsey, and Forrester "
            "produce the most reliable sector growth forecasts."
        ),
        # primary_sources=["bloomberg.com", "mckinsey.com", "forrester.com", "gartner.com"],
        # signal_type="factual",
        # job_applicant_relevance=9,
        # tags=["industry", "growth", "outlook", "forecast", "talent_demand", "trajectory"],
    ),
    QueryEntry(
        id="industry_consolidation_and_ma_risk",
        agent="industry",
        topic="consolidation_and_ma_risk",
        template=(
            '"{name}" {industry} "merger" OR "acquisition" OR "consolidation" OR "buyout" '
            '"job cuts" OR "integration" OR "redundancies" OR "acquired by" '
            'OR "merger impact employees" '
            "site:{clean_domain} OR site:wsj.com OR site:reuters.com OR site:bloomberg.com"
        ),
        purpose=(
            "Assess M&A activity in the industry as a job security risk. Post-merger "
            "integration frequently leads to redundancies and culture disruption — "
            "a candidate joining during active integration faces elevated uncertainty "
            "around team structure, reporting lines, and role continuity."
        ),
        # primary_sources=["wsj.com", "reuters.com", "bloomberg.com", "company_domain"],
        # signal_type="factual",
        # job_applicant_relevance=8,
        # tags=["industry", "ma", "consolidation", "acquisition", "redundancy", "integration"],
    ),
    QueryEntry(
        id="industry_offshoring_and_automation_risk",
        agent="industry",
        topic="offshoring_and_automation_risk",
        template=(
            '"{name}" {industry} "offshoring" OR "outsourcing" OR "automation" '
            'OR "nearshoring" "role elimination" OR "cost reduction" '
            'OR "moving jobs" OR "replacing workers" '
            "site:{clean_domain} OR site:techcrunch.com OR site:businessinsider.com"
        ),
        purpose=(
            "Identify whether roles in this industry are at structural risk of being "
            "offshored, outsourced, or automated independently of this company's specific "
            "performance. Structural role risk exists at the industry level and affects "
            "the candidate regardless of which employer they join."
        ),
        # primary_sources=["company_domain", "techcrunch.com", "businessinsider.com"],
        # signal_type="factual",
        # job_applicant_relevance=9,
        # tags=["industry", "offshoring", "outsourcing", "automation", "nearshoring", "risk"],
    ),
]
