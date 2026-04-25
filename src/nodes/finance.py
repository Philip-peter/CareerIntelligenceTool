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
    def _generate_queries_template(self, grounding_data):
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
                # We target the official investor relations site or SEC filings for CAGR/Revenue tables
                "query": f'site:sec.gov "{name}" "revenue growth" 3-year 5-year CAGR "historical financial results"',
            },
            {
                "topic": "profitability",
                # We look for specific margin terminology often found in tables
                "query": f'"{name}" {industry} "gross margin" "operating margin" "net profit margin" trend analysis 2023 2024',
            },
            {
                "topic": "debt",
                # Combining name with specific leverage ratios and the industry context
                "query": f'"{name}" "debt-to-equity" "debt-to-EBITDA" "total liabilities" "credit rating" leverage profile',
            },
            {
                "topic": "cash_flow",
                # Target the "Statement of Cash Flows" specifically
                "query": f'"{name}" "cash flow from operations" FCF "free cash flow" "capital expenditures" burn rate',
            },
            {
                "topic": "revenue_concentration",
                # This uses exact phrases found in the "Risk Factors" or "Notes to Financial Statements"
                "query": f'"{name}" "revenue concentration" "major customers" "percent of total revenue" "customer concentration"',
            },
            {
                "topic": "investor_sentiment",
                # BONUS: Checks for official IR decks or quarterly presentations on their own domain
                "query": f'site:{clean_domain} "investor presentation" "quarterly results" "earnings release" 2024',
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
