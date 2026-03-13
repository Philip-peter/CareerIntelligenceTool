import asyncio
import copy
import os
import sys
from typing import Any, Dict, List

from langchain_core.runnables import RunnableConfig

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

from src.models import IndustryContextModels  # noqa: E402
from src.state import State  # noqa: E402


class Industry:
    def __init__(self) -> None:
        pass

    @staticmethod
    def queries_template(company_name):
        return [
            {
                "topic": "cyclic_or_defensive",
                "query": f"[{company_name}] is it cyclical or defensive analyst commentary recession sensitivity operating margin volatility",
            },
            {
                "topic": "regulatory_environment",
                "query": f"[{company_name}] regulatory risks 10-K risk factors site:sec.gov compliance requirements government oversight industry regulation impact on revenue",
            },
            {
                "topic": "ai_distruption",
                "query": f"[{company_name}] AI integration strategy R&D spending AI capex competitive positioning",
            },
            {
                "topic": "competition",
                "query": f"[{company_name}] gross margin trend vs competitors pricing power switching costs network effects",
            },
        ]

    async def run_research(
        self, state: State, config: RunnableConfig
    ) -> Dict[str, Any]:
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

        result = {"industry_research_raw": researched_data_by_topic}

        return {"raw_research": result}

    async def run_llm_analysis(self, state: State, config: RunnableConfig):

        llm_analyzer_tool = config.get("configurable", {}).get("llm_summarizer")
        if not llm_analyzer_tool:
            raise ValueError("llm analyzer tool is not configured")

        system_prompt = """
        You are a Senior Equity Research Analyst specializing in industrial organization and strategic moat analysis. Your task is to synthesize raw web search data into a structured industry profile.

        ### Guidelines:
        - **Evidence-Based:** Base every claim on the provided search results. If the data is conflicting, highlight the consensus.
        - **Specifics Over Generalities:** Use concrete examples (e.g., mention specific regulators like the FDA or specific competitors like ASML).
        - **Nuance:** Distinguish between "cyclical" and "defensive" by referencing historical performance during downturns if available.
        - **Strict Output:** You must output valid JSON that conforms to the provided schema. Do not include introductory text or conversational filler.
        """

        user_prompt = f"""
        ### Task
        Analyze the following search results for the company: [INSERT COMPANY NAME].
        Extract and synthesize information into the JSON format specified by the IndustryContextModels schema.

        ### Schema Fields to Populate:
        1. **cyclic_or_defensive**: Classify the industry type and cite recession performance.
        2. **regulatory_environment**: Detail oversight levels, compliance costs, and specific agencies.
        3. **ai_distruption**: Evaluate AI as a threat (headwind) or opportunity (tailwind).
        4. **competition**: Map the landscape, including market share, moats, and key rivals.

        ### Raw Search Results:
        {state["raw_research"].get("industry_research_raw")}

        ### Response Format:
        Return ONLY a JSON object. If information for a field is entirely missing from the text, use the default: "No data available".
        """

        llm_response = await llm_analyzer_tool.run(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            output_schema=IndustryContextModels,
        )

        return {"industry_research": llm_response}
