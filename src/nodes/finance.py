import asyncio
import copy
import os
import sys
from typing import Any, Dict, List

from langchain_core.runnables import RunnableConfig

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

from src.models import FinancialContextModels  # noqa: E402
from src.state import State  # noqa: E402


class FinancialData:
    def __init__(self) -> None:
        pass

    @staticmethod
    def queries_template(company_name) -> List[Dict[str, Any]]:
        return [
            {
                "topic": "revenue_growth",
                "query": f"{company_name} historical revenue growth 3-5 year CAGR analysis",
            },
            {
                "topic": "profitability",
                "query": f"{company_name} gross operating net profit margins trend analysis",
            },
            {
                "topic": "debt",
                "query": f"{company_name} debt-to-equity ratio debt-to-EBITDA leverage profile",
            },
            {
                "topic": "cash_flow",
                "query": f"{company_name} free cash flow vs operating cash flow burn rate",
            },
            {
                "topic": "revenue_concentration",
                "query": f"{company_name} revenue concentration risk 'major customers' OR 'segment diversification'",
            },
        ]

    async def run_research(self, state: State, config: RunnableConfig):
        # make new copy of queries template
        working_queries: List[Dict[str, Any]] = copy.deepcopy(
            self.queries_template(company_name=state["target_company"])
        )
        web_research_tool = config.get("configurable", {}).get("web_research_tool")
        if not web_research_tool:
            raise ValueError("web search tool is not configured")

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

        result = {"finance_research_raw": researched_data_by_topic}

        return {"raw_research": result}

    async def run_llm_analysis(self, state: State, config: RunnableConfig):

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
        Analyze the following search results for the company: {state["target_company"]}.
        Extract and synthesize information into the JSON format specified by the FinancialContextModels schema.

        ### Schema Fields to Populate:
        1. **revenue_growth**: Summarize historical revenue growth trends (3–5 year CAGR).
        2. **profitability**: Describe profit margins (gross, operating, net) and trend direction.
        3. **debt**: Assess leverage levels (debt-to-equity or debt-to-EBITDA).
        4. **cash_flow**: Describe operating and free cash flow stability/burn.
        5. **revenue_concentration**: Assess dependency on customers, products, or regions.

        ### Raw Search Results:
        {state["raw_research"].get("finance_research_raw")}

        ### Response Format:
        Return ONLY a JSON object. If information for a field is entirely missing from the text, use the default: "No data available".
        """

        llm_response = await llm_analyzer_tool.run(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            output_schema=FinancialContextModels,
        )

        return {"finance_research": llm_response}
