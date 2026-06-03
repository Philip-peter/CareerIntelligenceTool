import asyncio
import os
import sys
from typing import Any, Dict

from langchain_core.runnables import RunnableConfig

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

from src.models import CompanyDirectionModels  # noqa: E402
from src.state import SubAgentState  # noqa: E402


class StrategicDirection:
    async def _generate_queries_template(self, grounding_data):
        name = grounding_data["company_name"]
        domain = grounding_data["company_domain"]
        # linkedin_url = grounding_data.get("company_linkedin_url", "")

        # Clean domain for site filtering
        clean_domain = (
            domain.replace("https://", "").replace("http://", "").split("/")[0]
            if domain
            else ""
        )

        return [
            {
                "topic": "earnings_call_forward_guidance",
                # Earnings call transcripts are the richest source of unfiltered CEO
                # forward-looking statements — Seeking Alpha and Motley Fool publish
                # full transcripts while Bloomberg/WSJ cover key quotes
                "query": f'"{name}" site:{clean_domain} OR "earnings call" OR "earnings call transcript" '
                f'"forward-looking" OR "guidance" OR "outlook" OR "we expect" '
                f'OR "next quarter" OR "full year" OR "fiscal year" '
                f'"2025" OR "2026" '
                f"site:seekingalpha.com OR site:fool.com OR site:bloomberg.com",
            },
            {
                "topic": "ceo_earnings_call_statements",
                # Targets the CEO's prepared remarks specifically — the opening statement
                # is where strategic direction is declared most explicitly
                "query": f'"{name}" CEO "prepared remarks" OR "opening statement" OR "I am pleased to report" '
                f'OR "our strategy" OR "we are focused on" OR "key priorities" '
                f'OR "in the coming year" OR "we remain committed to" '
                f'"earnings" "2025" OR "2026" '
                f"site:seekingalpha.com OR site:fool.com OR site:sec.gov",
            },
            {
                "topic": "analyst_qa_from_earnings",
                # The Q&A section of earnings calls is where analysts pressure-test
                # management's claims — this surfaces risks the CEO won't volunteer
                "query": f'"{name}" "earnings call" "question and answer" OR "Q&A" OR "analyst question" '
                f'"concerns" OR "headwinds" OR "risk" OR "slowdown" OR "competition" '
                f'OR "when do you expect" OR "can you elaborate" '
                f'"2025" OR "2026" '
                f"site:seekingalpha.com OR site:fool.com",
            },
            {
                "topic": "investor_day_strategic_targets",
                # Investor days contain the longest-horizon forward statements —
                # multi-year revenue targets, product roadmaps, and workforce plans
                "query": f'"{name}" site:{clean_domain} OR "investor day" OR "analyst day" '
                f'OR "capital markets day" OR "long-term targets" OR "three year plan" '
                f'OR "five year plan" OR "strategic plan" OR "we intend to" '
                f'"2024" OR "2025" OR "2026" '
                f"site:{clean_domain} OR site:seekingalpha.com OR site:bloomberg.com",
            },
            {
                "topic": "recent_capital_investments",
                # Capital allocation signals what the company is betting on —
                # new facilities, R&D spend, and capex are leading indicators of growth areas
                "query": f'"{name}" site:{clean_domain} OR "capital investment" OR "R&D spending" '
                f'OR "new facility" OR "data center" OR "infrastructure investment" '
                f'OR "capex" OR "we are building" OR "expanding capacity" '
                f'"2024" OR "2025" OR "2026" '
                f"site:bloomberg.com OR site:wsj.com OR site:reuters.com",
            },
            {
                "topic": "hiring_signals",
                # The types of roles a company is actively hiring for reveal its
                # strategic direction more honestly than any press release
                "query": f'"{name}" site:{clean_domain} OR "we are hiring" OR "join our team" '
                f'OR "new roles" OR "open positions" OR "rapidly growing team" '
                f'OR "AI engineer" OR "data scientist" OR "product manager" '
                f'OR "expanding our" OR "building out" '
                f"site:linkedin.com OR site:builtin.com OR site:levels.fyi",
            },
            {
                "topic": "strategic_alliances_and_partnerships",
                # New partnerships signal which ecosystems and markets the company
                # is aligning with and which capabilities it is building externally
                "query": f'"{name}" site:{clean_domain} OR "strategic partnership" OR "strategic alliance" '
                f'OR "joint venture" OR "collaboration agreement" OR "signed agreement with" '
                f'OR "partnered with" OR "expanded partnership" '
                f'"2024" OR "2025" OR "2026" '
                f"site:prnewswire.com OR site:businesswire.com OR site:bloomberg.com",
            },
            {
                "topic": "mergers_and_acquisitions",
                # M&A activity reveals inorganic growth ambitions and also creates
                # integration risk for new hires joining during post-merger periods
                "query": f'"{name}" site:{clean_domain} OR "acquisition" OR "acquired" OR "merger" '
                f'OR "acquires" OR "to be acquired" OR "definitive agreement" '
                f'OR "completed acquisition" OR "purchase price" '
                f'"2024" OR "2025" OR "2026" '
                f"site:sec.gov OR site:bloomberg.com OR site:wsj.com OR site:reuters.com",
            },
            {
                "topic": "new_products_and_ventures",
                # New product launches and business line entries reveal where
                # future headcount and investment will be concentrated
                "query": f'"{name}" site:{clean_domain} OR "launched" OR "new product" OR "new service" '
                f'OR "entering the market" OR "new business unit" OR "new division" '
                f'OR "product announcement" OR "generally available" OR "beta launch" '
                f'"2024" OR "2025" OR "2026" '
                f"site:{clean_domain} OR site:techcrunch.com OR site:venturebeat.com",
            },
            {
                "topic": "market_and_geographic_expansion",
                # International expansion or new vertical entry signals where
                # the company plans to grow its workforce and customer base
                "query": f'"{name}" site:{clean_domain} OR "expansion" OR "entering" OR "new market" '
                f'OR "international growth" OR "new region" OR "opened office" '
                f'OR "APAC" OR "EMEA" OR "Latin America" OR "new vertical" '
                f'"2024" OR "2025" OR "2026" '
                f"site:{clean_domain} OR site:bloomberg.com OR site:businessinsider.com",
            },
            {
                "topic": "ai_and_technology_roadmap",
                # Technology investment direction is the clearest signal of which
                # roles will grow and which will be automated or deprioritized
                "query": f'"{name}" site:{clean_domain} OR "AI roadmap" OR "technology investment" '
                f'OR "AI strategy" OR "machine learning" OR "generative AI" OR "AI agents" '
                f'OR "platform modernization" OR "tech stack" OR "engineering investment" '
                f'"2024" OR "2025" OR "2026" '
                f"site:{clean_domain} OR site:techcrunch.com OR site:wired.com OR site:venturebeat.com",
            },
            {
                "topic": "government_and_enterprise_contracts",
                # Large contract wins are forward revenue visibility signals —
                # they drive near-term hiring and indicate where delivery headcount will grow
                "query": f'"{name}" site:{clean_domain} OR "contract win" OR "government contract" '
                f'OR "enterprise deal" OR "multi-year agreement" OR "awarded contract" '
                f'OR "selected by" OR "chosen as" OR "signed deal" '
                f'"2024" OR "2025" OR "2026" '
                f"site:{clean_domain} OR site:prnewswire.com OR site:govwin.com OR site:bloomberg.com",
            },
            {
                "topic": "divestitures_and_business_exits",
                # Selling off divisions or exiting markets is as telling as acquisitions —
                # divestitures signal where the company is de-investing and cutting headcount
                "query": f'"{name}" site:{clean_domain} OR "divested" OR "sold off" OR "exiting" '
                f'OR "discontinued" OR "wind down" OR "spinning off" OR "carve out" '
                f'OR "strategic review" OR "non-core assets" '
                f'"2024" OR "2025" OR "2026" '
                f"site:sec.gov OR site:wsj.com OR site:bloomberg.com OR site:reuters.com",
            },
        ]

    async def _run_web_research(
        self, grounding_data, web_research_tool
    ) -> Dict[str, Any]:

        # generate web search query
        working_queries = await self._generate_queries_template(
            grounding_data=grounding_data
        )

        async def process_query(item: Dict[str, Any]):
            query = item.get("query")
            # search
            web_search = await web_research_tool.search(query=query, topic="general")
            item["researched_data"] = web_search
            return item

        task = [process_query(q) for q in working_queries]
        all_processed_task = await asyncio.gather(*task, return_exceptions=True)

        researched_data_by_topic = {
            r["topic"]: r["researched_data"]
            for r in all_processed_task
            if not isinstance(r, (Exception, BaseException))
        }

        return researched_data_by_topic

    async def run_research(self, state: SubAgentState, config: RunnableConfig):

        # dispatch_job from router agent
        dispatch_job = state["job"]

        # extract grounding and job data
        job_info = dispatch_job["job_data"]
        grounding = dispatch_job["grounding_data"]

        # initiate web search tool
        web_research_tool = config.get("configurable", {}).get("web_research_tool")
        if not web_research_tool:
            raise ValueError("web search tool is not configured")

        # run web search (awaiting properly to fix earlier RuntimeWarnings)
        web_research = await self._run_web_research(
            grounding_data=grounding, web_research_tool=web_research_tool
        )

        # initiate llm analysis
        llm_analyzer_tool = config.get("configurable", {}).get("llm_summarizer")
        if not llm_analyzer_tool:
            raise ValueError("llm analyzer tool is not configured")

        # 1. Prepare Anchor Context
        direction_anchor = f"""
        TARGET COMPANY IDENTITY:
        - Legal Name: {grounding.get("company_name")}
        - Corporate Domain: {grounding.get("company_domain")}
        - LinkedIn: {grounding.get("company_linkedin_url")}
        - Industry: {grounding.get("company_industry")}
        - Official Website: {grounding.get("company_official_url")}

        JOB CONTEXT:
        - Role Being Evaluated: {job_info.get("job_title")}
        - Purpose: Assess the company's strategic direction and forward momentum to determine
            whether this is a growing, stable, or contracting employer over the next 2-3 years.
        """

        system_prompt = """
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

        user_prompt = f"""
        ### Company Grounding Context:
        {direction_anchor}

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

        llm_response = await llm_analyzer_tool.run(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            output_schema=CompanyDirectionModels,
        )

        formatted_results = {
            "job_id": job_info.get("job_id"),
            "agent_type": "company_direction",
            "data": llm_response.model_dump(),
        }

        # wrap formatted_result in list for applying reducer in agent_analysis state
        return {"agent_analysis": [formatted_results]}
