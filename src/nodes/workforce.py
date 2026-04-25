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
        industry = grounding_data["company_industry"]

        # Clean domain for site filtering
        clean_domain = (
            domain.replace("https://", "").replace("http://", "").split("/")[0]
            if domain
            else ""
        )

        return [
            {
                "topic": "layoff_history",
                # Focuses on news and layoff trackers like 'layoffs.fyi' or 'Warn Act' notices
                "query": f'"{name}" (layoff OR "headcount reduction" OR "RIF" OR "restructuring") 2024..2026',
            },
            {
                "topic": "hiring_trends",
                # site: search on their careers page and LinkedIn to gauge growth velocity
                "query": f'site:{clean_domain}/careers OR site:linkedin.com/jobs "{name}" "hiring" expansion',
            },
            {
                "topic": "executive_turnover",
                # Targeting press releases and professional news regarding C-suite exits
                "query": f'"{name}" "executive departure" OR "resignation" (CFO OR CTO OR COO OR CMO) 2025 2026',
            },
            {
                "topic": "employee_sentiments",
                # Forcing exact matches on review platforms for current sentiment
                "query": f'site:glassdoor.com OR site:indeed.com "{name}" "reviews" "CEO approval" 2025 2026',
            },
            {
                "topic": "labor_disputes",
                # Helpful for industrial/workforce grounding: unions and legal friction
                "query": f'"{name}" {industry} "union" OR "strike" OR "labor dispute" OR "unfair labor practice"',
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
        - Hiring Role: {job_info.get("job_title")}
        """

        system_prompt = """
        ### ROLE
        You are a Corporate Intelligence Analyst specializing in organizational health, workforce dynamics, and human capital risk.

        ### ANALYTICAL GUIDELINES
        1. **Identity Verification**: Use the 'TARGET ENTITY' details to filter search results. Ensure sentiments and layoff news are specific to this company and domain.
        2. **Identify Patterns**: Distinguish between isolated events (e.g., "one executive left") and systemic trends (e.g., "three CFOs in 18 months").
        3. **Categorize Signals**:
           - Stability: Consistent leadership, steady hiring.
           - Risk: High turnover, frequent layoffs, Glassdoor mentions of "low morale."
           - Growth: Surges in technical hiring, expansion into new regions.
        4. **Source Recency**: Prioritize information from the last 24 months.
        """

        user_prompt = f"""
        ### Company Grounding:
        {workforce_anchor}

        ### Web Research Results:
        {web_research}

        ### Task:
        Analyze the provided web search results to populate the WorkforceContextModels schema for {grounding.get("company_name")}.

        Extract and synthesize:
        1. **layoff_history**: Frequency and scale (e.g., 'Company conducted a 10% workforce reduction in Q3 2024').
        2. **hiring_trends**: Expansion vs. freeze signals.
        3. **executive_turnover**: Stability of the C-suite (CFO/CTO/COO).
        4. **employee_sentiments**: Public sentiment from platforms like Glassdoor or LinkedIn.

        Return ONLY a JSON object. Use "No data available" for missing fields.
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
