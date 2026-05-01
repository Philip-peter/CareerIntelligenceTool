import asyncio
import os
import sys
from typing import Any, Dict

from langchain_core.runnables import RunnableConfig

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

from src.models import LeadershipContextModels  # noqa: E402
from src.state import SubAgentState  # noqa: E402


class Leadership:
    def _generate_queries_template(self, grounding_data):
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
                "topic": "ceo_tenure",
                "query": f'"{name}" site:{clean_domain} OR CEO tenure leadership "reorganization" OR "layoffs" OR "culture shift" '
                f'"since joining" OR "under his leadership" OR "under her leadership" employees',
            },
            {
                "topic": "founder_involvement",
                "query": f'"{name}" site:{clean_domain} OR founder "founder-led" OR "founder mode" OR "founder vision" '
                f'company culture employees "day-to-day" OR "still involved" OR "stepped back"',
            },
            {
                "topic": "strategic_pivots",
                "query": f'"{name}" site:{clean_domain} OR "strategic pivot" OR "business transformation" OR "restructuring" '
                f'employees "job cuts" OR "new direction" OR "career opportunities" OR "headcount"',
            },
            {
                "topic": "executive_reputation",
                "query": f'"{name}" site:{clean_domain} OR CEO "Glassdoor" OR "Blind" OR "employee reviews" '
                f'"approval rating" OR "leadership style" OR "management controversy" OR "executive criticism"',
            },
            {
                "topic": "leadership_stability",
                "query": f'"{name}" site:{clean_domain} OR "chief" OR "VP" OR "vice president" '
                f'"departed" OR "resigned" OR "appointed" OR "replaced" "executive turnover" OR "leadership changes" '
                f"site:businessinsider.com OR site:wsj.com OR site:bloomberg.com",
            },
            {
                "topic": "employee_treatment_during_hardship",
                "query": f'"{name}" site:{clean_domain} OR layoffs OR "workforce reduction" OR "restructuring" '
                f'"severance" OR "notice period" OR "how it was handled" OR "employees react" '
                f"site:techcrunch.com OR site:businessinsider.com OR site:glassdoor.com",
            },
            {
                "topic": "management_style_and_culture",
                "query": f'"{name}" site:{clean_domain} OR "management style" OR "work culture" OR "micromanagement" '
                f'OR "psychological safety" OR "toxic culture" OR "employee autonomy" '
                f"site:glassdoor.com OR site:teamblind.com OR site:reddit.com",
            },
            {
                "topic": "vision_and_communication_clarity",
                "query": f'"{name}" site:{clean_domain} OR CEO "all-hands" OR "town hall" OR "internal memo" OR "strategic vision" '
                f'"employees" "communication" OR "transparency" OR "roadmap" OR "blindsided"',
            },
            {
                "topic": "dei_and_values_commitment",
                "query": f'"{name}" site:{clean_domain} OR "diversity" OR "DEI" OR "inclusion" "pay equity" OR "representation" '
                f'OR "ERG" OR "diversity report" OR "DEI rollback" OR "diversity controversy" '
                f"site:{clean_domain} OR site:builtin.com",
            },
            {
                "topic": "employee_development_investment",
                "query": f'"{name}" site:{clean_domain} OR "employee development" OR "learning and development" OR "internal promotions" '
                f'OR "career growth" OR "mentorship" OR "tuition reimbursement" OR "L&D budget" '
                f"site:{clean_domain} OR site:glassdoor.com",
            },
        ]

    async def _run_web_research(
        self, grounding_data, web_research_tool
    ) -> Dict[str, Any]:

        # generate web search query
        working_queries = self._generate_queries_template(grounding_data=grounding_data)

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
        # This block forces the LLM to verify the identity of the leaders found online.
        leadership_anchor = f"""
        TARGET COMPANY IDENTITY:
        - Legal Name: {grounding.get("company_name")}
        - Corporate Domain: {grounding.get("company_domain")}
        - LinkedIn: {grounding.get("company_linkedin_url")}
        - Industry: {grounding.get("company_industry")}
        - Official Website: {grounding.get("company_official_url")}
        """

        system_prompt = """
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

        user_prompt = f"""
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

        llm_response = await llm_analyzer_tool.run(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            output_schema=LeadershipContextModels,
        )

        formatted_results = {
            "job_id": job_info.get("job_id"),
            "agent_type": "leadership",
            "data": llm_response.model_dump(),
        }

        # wrap formatted_result in list for applying reducer in agent_analysis state
        return {"agent_analysis": [formatted_results]}
