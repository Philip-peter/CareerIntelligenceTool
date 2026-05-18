import asyncio
import os
import sys
from typing import Any, Dict

from langchain_core.runnables import RunnableConfig

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

from src.models import WorkforceContextModels  # noqa: E402
from src.state import SubAgentState  # noqa: E402


class Workforce:
    def _generate_queries_template(self, grounding_data):
        name = grounding_data["company_name"]
        domain = grounding_data["company_domain"]
        # industry = grounding_data["company_industry"]

        # Clean domain for site filtering
        clean_domain = (
            domain.replace("https://", "").replace("http://", "").split("/")[0]
            if domain
            else ""
        )

        return [
            {
                "topic": "layoff_history",
                # Added layoff tracker sites and WARN Act as primary sources; fixed date range syntax
                "query": f'"{name}" site:{clean_domain} OR "layoff" OR "headcount reduction" OR "RIF" OR "restructuring" '
                f'"2024" OR "2025" OR "2026" '
                f"site:layoffs.fyi OR site:techcrunch.com OR site:businessinsider.com OR site:warn-tracker.com",
            },
            {
                "topic": "hiring_trends",
                # Replaced unreliable path/LinkedIn site: filtering with hiring signal keywords from news sources
                "query": f'"{name}" site:{clean_domain} OR "hiring" OR "open roles" OR "headcount growth" OR "expansion" '
                f'"actively recruiting" OR "talent acquisition" OR "hiring freeze" OR "paused hiring" '
                f"site:builtin.com OR site:techcrunch.com OR site:businessinsider.com",
            },
            {
                "topic": "mid_management_turnover",
                # Differentiated from leadership agent's executive_turnover — focuses on director/VP layer churn
                "query": f'"{name}" site:{clean_domain} OR "director" OR "VP" OR "vice president" OR "senior manager" '
                f'"left" OR "departed" OR "resigned" OR "laid off" '
                f"site:linkedin.com OR site:glassdoor.com OR site:teamblind.com",
            },
            {
                "topic": "employee_sentiments",
                # Restructured into clean syntax; added Blind and Fishbowl alongside Glassdoor and Indeed
                "query": f'"{name}" site:{clean_domain} OR "employee reviews" OR "work culture" OR "CEO approval" '
                f'"pros and cons" OR "recommend to a friend" OR "employee experience" '
                f"site:glassdoor.com OR site:teamblind.com OR site:fishbowlapp.com OR site:indeed.com",
            },
            {
                "topic": "labor_disputes",
                # Expanded to include NLRB filings and wrongful termination which are more discoverable than active strikes
                "query": f'"{name}" site:{clean_domain} OR "union" OR "strike" OR "labor dispute" '
                f'OR "unfair labor practice" OR "NLRB" OR "wrongful termination" OR "class action employees" '
                f"site:nlrb.gov OR site:reuters.com OR site:bloomberg.com",
            },
            {
                "topic": "remote_and_flexibility_policy",
                # New — RTO mandates correlate with voluntary attrition spikes; critical decision factor for candidates
                "query": f'"{name}" site:{clean_domain} OR "remote work" OR "hybrid policy" OR "return to office" '
                f'OR "RTO mandate" OR "work from home" OR "flexible work" OR "in-office requirement" '
                f"site:glassdoor.com OR site:techcrunch.com OR site:businessinsider.com",
            },
            {
                "topic": "compensation_and_benefits",
                # New — salary competitiveness and benefits quality directly affect switching risk assessment
                "query": f'"{name}" site:{clean_domain} OR "salary" OR "compensation" OR "total compensation" '
                f'OR "benefits" OR "equity" OR "RSU" OR "401k" OR "health insurance" OR "pay transparency" '
                f"site:glassdoor.com OR site:levels.fyi OR site:teamblind.com OR site:reddit.com",
            },
            {
                "topic": "headcount_trajectory",
                # New — overall workforce growth/contraction trend distinct from specific layoff events
                "query": f'"{name}" site:{clean_domain} OR "headcount" OR "total employees" OR "workforce size" '
                f'OR "growing team" OR "shrinking" OR "hiring slowdown" OR "attrition" '
                f"site:macrotrends.net OR site:businessinsider.com OR site:bloomberg.com",
            },
            {
                "topic": "employee_tenure_and_retention",
                # New — high turnover is one of the strongest red flags regardless of cause
                "query": f'"{name}" site:{clean_domain} OR "employee tenure" OR "average tenure" OR "retention rate" '
                f'OR "high turnover" OR "employees leave" OR "attrition rate" OR "revolving door" '
                f"site:glassdoor.com OR site:linkedin.com OR site:teamblind.com",
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

        # run web search (awaiting to fix the RuntimeWarning)
        web_research = await self._run_web_research(
            grounding_data=grounding, web_research_tool=web_research_tool
        )

        # initiate llm analysis
        llm_analyzer_tool = config.get("configurable", {}).get("llm_summarizer")
        if not llm_analyzer_tool:
            raise ValueError("llm analyzer tool is not configured")

        # 1. Anchor Context: Ground the workforce analysis
        workforce_anchor = f"""
        TARGET ENTITY FOR ANALYSIS:
        - Company: {grounding.get("company_name")}
        - Domain: {grounding.get("company_domain")}
        - Industry: {grounding.get("company_industry")}
        - LinkedIn: {grounding.get("company_linkedin_url")}

        JOB CONTEXT:
        - Role Being Evaluated: {job_info.get("job_title")}
        - Purpose: Assess workforce health and employment risk for a candidate considering this role.
        """

        system_prompt = """
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

        user_prompt = f"""
        ### Company Grounding:
        {workforce_anchor}

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

        llm_response = await llm_analyzer_tool.run(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            output_schema=WorkforceContextModels,
        )

        formatted_results = {
            "job_id": job_info.get("job_id"),
            "agent_type": "workforce",
            "data": llm_response.model_dump(),
        }

        # wrap formatted_result in list for applying reducer in agent_analysis state
        return {"agent_analysis": [formatted_results]}
