import asyncio
import copy
import os
import sys
from typing import Any, Dict, List

from langchain_core.runnables import RunnableConfig

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

from src.state import State  # noqa: E402


class CompanyProfile:
    def __init__(self) -> None:
        pass

    @staticmethod
    def queries_template(target_company: str) -> str:
        return f"'{target_company}' (site:linkedin.com/company OR site:crunchbase.com) 'about' 'industry' 'headquarters'"

    async def run_research(self, state: State, config: RunnableConfig):
        working_query = copy.deepcopy(
            self.queries_template(target_company=state["target_company"])
        )
        web_research_tool = config.get("configurable", {}).get("web_research_tool")
        if not web_research_tool:
            return ValueError("web search tool is not configured")

        response = await web_research_tool.search(query=working_query)
        print(response)
        return {"target_company_research_raw": response}

    async def run_llm_analysis(self, state: State, config: RunnableConfig):

        llm_analyzer_tool = config.get("configurable", {}).get("llm_summarizer")
        if not llm_analyzer_tool:
            raise ValueError("llm analyzer tool is not configured")

        system_prompt = """
        You are an expert Business Intelligence Analyst specializing in corporate taxonomy. Your task is to analyze raw search results to provide a high-fidelity classification of a company.

        Rules:
        1. Industry: Use standard professional categories (e.g., "Fintech," "SaaS," "Biotechnology," "Renewable Energy"). Avoid generic terms like "Business" or "Tech."
        2. Core Product/Service: Identify the primary revenue generator. What do they actually sell? (e.g., "AI-driven fraud detection platform" vs. just "Software").
        3. Company Type:
            - Identify as 'Public' if a stock ticker (e.g., NASDAQ: AMZN) exists.
            - Identify as 'Startup/In-Funding' if Series A-E or Venture Capital is mentioned.
            - Identify as 'Private/Established' if it is a mature firm without a ticker or recent venture funding.
        4. Evidence-Based: Only use the provided text. If the industry is ambiguous.
        """

        user_prompt = f"""
        Analyze the following extracted data to build a concise profile for {state["target_company"]}.

        Data Sources:
        - Web Search Results: {state["target_company_research_raw"]}

        Please extract and map the following:
        1. Industry: (The specific market sector)
        2. Core Product/Service: (The main offering)
        3. Company Type: (Public, Startup/In-Funding, or Private/Established)
        4. Primary Revenue Model: (e.g., B2B SaaS, E-commerce, Professional Services)

        Return the data in a clean, structured format matching the requested schema.
        """

        llm_response = await llm_analyzer_tool.run(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            output_schema=None,
        )
        return {"target_company_profile": llm_response}
