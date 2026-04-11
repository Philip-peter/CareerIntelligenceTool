import asyncio
import os
import sys
from typing import Any, Dict

from langchain_core.runnables import RunnableConfig

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

from src.models import FinancialContextModels  # noqa: E402
from src.state import State  # noqa: E402


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
            # // TODO: Update pydantic model
            # {
            #     "topic": "investor_sentiment",
            #     # BONUS: Checks for official IR decks or quarterly presentations on their own domain
            #     "query": f'site:{clean_domain} "investor presentation" "quarterly results" "earnings release" 2024',
            # },
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

    async def run_research(self, inputs: Dict, state: State, config: RunnableConfig):

        # extract grounding and job data from supervisor Send payload
        # job = inputs["job_data"]
        grounding = inputs["grounding_data"]

        # initiate web search tool
        web_research_tool = config.get("configurable", {}).get("web_research_tool")
        if not web_research_tool:
            raise ValueError("web search tool is not configured")

        # run web search
        web_research = self._run_web_research(
            grounding_data=grounding, web_research_tool=web_research_tool
        )

        # initiate llm analysis
        llm_analyzer_tool = config.get("configurable", {}).get("llm_summarizer")
        if not llm_analyzer_tool:
            raise ValueError("llm analyzer tool is not configured")

        system_prompt = """
        You are a Senior Equity Research Analyst. Your task is to extract high-fidelity financial
        data from search results and map them to a specific JSON schema.

        ### Rules:
        1. **Source Grounding**: Only use the provided search results. If information is missing
           for a specific field, use the default: "No data available".
        2. **Financial Accuracy**: Interpret terms like "CAGR", "EBITDA", and "Net Margin"
           accurately. Use the historical context provided in the snippets to note trends
           (e.g., "improving", "declining", "stable").
        3. **Conciseness**: Follow the example formats provided in the field descriptions.
           Keep summaries dense and informative.
        4. **Output Format**: You must respond ONLY with a valid JSON object that matches
           the schema provided. Do not include conversational filler or markdown code blocks
           unless specifically requested.
        """

        user_prompt = f"""
        Analyze the following search results for the company: {grounding.get("company_name")}.
        Extract and synthesize information into the JSON format specified by the FinancialContextModels schema.

        ### Schema Fields to Populate:
        1. **revenue_growth**: Summarize historical revenue growth trends (3–5 year CAGR).
        2. **profitability**: Describe profit margins (gross, operating, net) and trend direction.
        3. **debt**: Assess leverage levels (debt-to-equity or debt-to-EBITDA).
        4. **cash_flow**: Describe operating and free cash flow stability/burn.
        5. **revenue_concentration**: Assess dependency on customers, products, or regions.

        ### Raw Search Results:
        {web_research}

        ### Response Format:
        Return ONLY a JSON object. If information for a field is entirely missing from the text, use the default: "No data available".
        """

        llm_response = await llm_analyzer_tool.run(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            output_schema=FinancialContextModels,
        )

        return {"finance_research": llm_response}
