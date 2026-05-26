import asyncio
import os
import sys
from typing import Any, Dict

from langchain_core.runnables import RunnableConfig

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

from src.models import FinancialContextModels  # noqa: E402
from src.state import SubAgentState  # noqa: E402


class FinancialData:
    async def _generate_queries_template(self, grounding_data):
        name = grounding_data["company_name"]
        domain = grounding_data["company_domain"]
        industry = grounding_data["company_industry"]

        # Clean the domain to use as a site filter
        clean_domain = (
            domain.replace("https://", "").replace("http://", "").split("/")[0]
            if domain
            else ""
        )

        return [
            {
                "topic": "revenue_growth",
                # Added IR domain alongside SEC; added recent years and reframed around growth trajectory
                "query": f'"{name}" site:{clean_domain} OR site:sec.gov '
                f'"revenue growth" OR "annual revenue" OR "revenue trend" '
                f'"2023" OR "2024" OR "2025" "year over year" OR "YoY" OR "CAGR" '
                f'"growing" OR "declining" OR "flat revenue"',
            },
            {
                "topic": "profitability",
                # Added domain grounding, updated date range, reframed around financial sustainability
                "query": f'"{name}" site:{clean_domain} OR site:sec.gov {industry} '
                f'"gross margin" OR "operating margin" OR "net margin" OR "EBITDA" '
                f'"2024" OR "2025" "profitable" OR "profitability" OR "operating loss" OR "path to profitability"',
            },
            {
                "topic": "debt",
                # Added SEC and credit agency sources; debt is most reliably found in filings and ratings reports
                "query": f'"{name}" site:{clean_domain} OR site:sec.gov '
                f'"debt-to-equity" OR "debt-to-EBITDA" OR "total liabilities" OR "long-term debt" '
                f'"credit rating" OR "leverage" OR "covenant" OR "refinancing" '
                f"site:moodys.com OR site:spglobal.com OR site:fitchratings.com",
            },
            {
                "topic": "cash_flow",
                # Added domain grounding; burn rate and runway are the most job-applicant-relevant signals
                "query": f'"{name}" site:{clean_domain} OR site:sec.gov '
                f'"cash flow from operations" OR "free cash flow" OR "FCF" '
                f'"capital expenditures" OR "burn rate" OR "cash runway" OR "cash position" '
                f'"2024" OR "2025"',
            },
            {
                "topic": "revenue_concentration",
                # Strengthened with explicit SEC grounding — this language appears verbatim in 10-K Risk Factors
                "query": f'"{name}" site:{clean_domain} OR site:sec.gov '
                f'"revenue concentration" OR "customer concentration" OR "major customers" '
                f'"percent of total revenue" OR "accounts for" OR "single customer" OR "top 10 customers"',
            },
            {
                "topic": "investor_sentiment",
                # Added analyst sources alongside IR; counterbalances optimistic official IR content
                "query": f'"{name}" site:{clean_domain} OR "investor presentation" OR "earnings release" '
                f'OR "analyst rating" OR "price target" OR "outlook" OR "guidance" '
                f'"2024" OR "2025" OR "2026" '
                f"site:seekingalpha.com OR site:bloomberg.com OR site:wsj.com",
            },
            {
                "topic": "funding_and_runway",
                # New — critical for private/startup employers; strong role at underfunded company is high risk
                "query": f'"{name}" site:{clean_domain} '
                f'"funding round" OR "Series A" OR "Series B" OR "venture capital" OR "raised" '
                f'OR "runway" OR "cash reserves" OR "burn rate" OR "IPO" OR "pre-IPO" '
                f"site:crunchbase.com OR site:techcrunch.com OR site:bloomberg.com",
            },
            {
                "topic": "financial_distress_signals",
                # New — earliest warning indicators that won't appear in standard revenue/margin queries
                "query": f'"{name}" site:{clean_domain} OR site:sec.gov '
                f'"going concern" OR "covenant breach" OR "credit downgrade" OR "missed payment" '
                f'OR "debt restructuring" OR "bankruptcy" OR "financial difficulty" OR "liquidity risk" '
                f"site:bloomberg.com OR site:wsj.com OR site:reuters.com",
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

        # distpatch job data from router agent
        dispatch_job = state["job"]
        job_info = dispatch_job["job_data"]
        grounding = dispatch_job["grounding_data"]

        # tool initialization
        web_research_tool = config.get("configurable", {}).get("web_research_tool")
        llm_analyzer_tool = config.get("configurable", {}).get("llm_summarizer")

        # run web search
        if not web_research_tool:
            raise ValueError("web search tool is not configured")

        web_research = await self._run_web_research(
            grounding_data=grounding, web_research_tool=web_research_tool
        )

        # run llm analysis
        if not llm_analyzer_tool:
            raise ValueError("llm analyzer tool is not configured")

        # Anchor Context
        company_anchor = f"""
        COMPANY IDENTITY:
        - Name: {grounding.get("company_name")}
        - Industry: {grounding.get("company_industry")}
        - Primary Domain: {grounding.get("company_domain")}
        - Official URL: {grounding.get("company_official_url")}
        - LinkedIn: {grounding.get("company_linkedin_url")}

        JOB CONTEXT:
        - Target Role: {job_info.get("job_title")}
        - Role Description: {job_info.get("job_description")[:500]}...
        """

        system_prompt = """
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

        user_prompt = f"""
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

        llm_response = await llm_analyzer_tool.run(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            output_schema=FinancialContextModels,
        )

        formatted_results = {
            "job_id": job_info.get("job_id"),
            "agent_type": "finance",
            "data": llm_response.model_dump(),
        }

        # wrap formatted_result in list for applying reducer in agent_analysis state
        return {"agent_analysis": [formatted_results]}
