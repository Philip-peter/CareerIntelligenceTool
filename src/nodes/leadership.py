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
        linkedin_url = grounding_data.get("company_linkedin_url", "")

        # Clean domain for site filtering
        clean_domain = (
            domain.replace("https://", "").replace("http://", "").split("/")[0]
            if domain
            else ""
        )

        return [
            {
                "topic": "ceo_tenure",
                # Focuses on the "Management" section of official filings and earnings sentiment
                "query": f'site:sec.gov "{name}" CEO tenure "biography" "previous experience" earnings call sentiment',
            },
            {
                "topic": "founder_involvement",
                # Targeting Proxy Statements (DEF 14A) which detail voting power and ownership
                "query": f'site:sec.gov "{name}" "founder" "beneficial ownership" "voting power" "dual-class" "board of directors"',
            },
            {
                "topic": "strategic_pivots",
                # Looking for letters to shareholders or official restructuring announcements on their domain
                "query": f'site:{clean_domain} "letter to shareholders" "restructuring" "strategic shift" "business transformation"',
            },
            {
                "topic": "insider_behavior",
                # Form 4 is the specific legal requirement for insider trades
                "query": f'site:sec.gov "{name}" "Form 4" "insider trading" "executive compensation" "shares held" buying selling',
            },
            {
                "topic": "executive_reputation",
                # Leveraging the LinkedIn grounding data to find news about the executive team's reputation
                "query": f'site:{linkedin_url} "{name}" executive leadership team "Glassdoor" ratings "Glassdoor" CEO approval "departure" "turnover"',
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

        # distpatch_job from router agent
        dispatch_job = state["job"]

        # extract grounding and job data from supervisor Send payload
        job = dispatch_job["job_data"]
        grounding = dispatch_job["grounding_data"]

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
        ### ROLE
        You are a Senior Equity Research Analyst specializing in corporate governance and leadership transitions. Your task is to extract structured leadership insights from provided web search results.

        ### OBJECTIVE
        Analyze the provided text to populate a specific JSON schema. You must maintain high analytical standards, distinguishing between factual data (e.g., tenure years) and market signals (e.g., performance trends).

        ### EXTRACTION RULES
        1.  **Strict Schema Adherence:** Your output must be a single JSON object matching the requested schema exactly.
        2.  **No Data Handling:** If search results do not contain information for a specific field, use the default value: "No data available".
        3.  **Synthesize, Don't Just Copy:** Combine information from multiple search snippets to provide a comprehensive summary for each field.
        4.  **Tone:** Professional, objective, and data-driven.

        ### OUTPUT FORMAT
        Provide only the raw JSON. Do not include conversational filler, markdown code blocks (unless specified), or explanations outside of the JSON structure.
        """

        user_prompt = f"""
        ### Task
        Analyze the following search results for the company: {grounding.get("company_name")}
        Extract leadership context for the company into the JSON format specified by the LeadershipContextModels schema.

        ### Schema Fields to Populate:
        1. **ceo_tenure**: State tenure length and performance impact (improvement/decline).
        2. **founder_involvement**: Describe current roles (leadership/board) and ownership stake.
        3. **strategic_pivots**: Identify major business model shifts and their outcomes.
        4. **insider_behavior**: Analyze recent stock buying/selling trends and executive ownership.

        ### Raw Search Results:
        {web_research}
        """

        llm_response = await llm_analyzer_tool.run(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            output_schema=LeadershipContextModels,
        )

        formatted_results = {
            "job_id": job.get("job_id"),
            "agent_type": "leadership",
            "data": llm_response.model_dump(),
        }

        # wrap formatted_result in list for applying reducer in agent_analysis state
        return {"agent_analysis": [formatted_results]}
