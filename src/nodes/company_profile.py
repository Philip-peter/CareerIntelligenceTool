import os
import sys

from langchain_core.runnables import RunnableConfig

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

from src.models import CompanyProfileModel  # noqa: E402
from src.state import State  # noqa: E402


class CompanyProfile:
    def __init__(self) -> None:
        pass

    @staticmethod
    def queries_template(target_company: str) -> str:
        return f"'{target_company}' (site:linkedin.com/company OR site:crunchbase.com) 'about' 'industry' 'headquarters'"

    async def run_research(self, state: State, config: RunnableConfig):
        working_query = self.queries_template(target_company=state["target_company"])

        web_research_tool = config.get("configurable", {}).get("web_research_tool")
        if not web_research_tool:
            raise ValueError("web search tool is not configured")

        research = await web_research_tool.search(query=working_query)
        result = {"target_company_research_raw": research}

        return {"raw_research": result}

    async def run_llm_analysis(self, state: State, config: RunnableConfig):

        llm_analyzer_tool = config.get("configurable", {}).get("llm_summarizer")
        if not llm_analyzer_tool:
            raise ValueError("llm analyzer tool is not configured")

        system_prompt = """
        You are an expert Business Intelligence Analyst specializing in corporate taxonomy.
        Your task is to analyze raw search results and provide a high-fidelity classification
        following these exact string conventions:

        ### Classification Rules:

        1. **Industry**: Use specific professional categories (e.g., "Fintech," "SaaS," "Biotechnology").
        2. **Core Product/Service**: Identify the primary offering (e.g., "AI-driven fraud detection platform").
        3. **Company Type**: You must choose exactly one of these strings:
            - "Public" (if a stock ticker exists)
            - "Private" (if privately held)
            - "Unknown" (if no ownership data is found)
        4. **Company Maturity**: You must choose exactly one of these strings:
            - "Startup" (mentions of venture capital, Series A-E, or 'early-stage')
            - "Established" (operating 10+ years, stable non-venture firm, or mature public entity)
        5. **Primary Revenue Driver**: Identify the specific product line, business unit, or service category that contributes
        the majority of the firm's operating income or represents its core growth engine (e.g., "Public Cloud Infrastructure (AWS),"
        "Membership Ecosystem (Prime)," or "Digital Advertising Services").

        ### Operational Constraints:
        - **Evidence-Based**: Only use provided text. Do not hallucinate.
        - **Strict Formatting**: Ensure the values for 'Company Type' and 'Company Maturity' match the options provided above exactly.
        """

        user_prompt = f"""
        Analyze the following extracted data to build a concise profile for {state["target_company"]}.

        Data Sources:
        - Web Search Results: {state["raw_research"].get("target_company_research_raw")}

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
            output_schema=CompanyProfileModel,
        )

        return {"target_company_profile": llm_response}
