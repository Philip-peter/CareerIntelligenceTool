import asyncio
import os
import sys
from typing import Any, Dict

from langchain_core.runnables import RunnableConfig

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

from src.models import IndustryContextModels  # noqa: E402
from src.state import SubAgentState  # noqa: E402


class Industry:
    async def _generate_queries_template(self, grounding_data):
        name = grounding_data["company_name"]
        domain = grounding_data["company_domain"]
        industry = grounding_data["company_industry"]

        # Clean domain (remove http/www)
        clean_domain = (
            domain.replace("https://", "").replace("http://", "").split("/")[0]
        )

        return [
            {
                "topic": "cyclic_or_defensive",
                # Reframed around workforce consequences of downturns, not stock defensiveness
                "query": f'"{name}" {industry} "economic downturn" OR "recession" OR "slowdown" '
                f'"layoffs" OR "hiring freeze" OR "budget cuts" OR "workforce impact" '
                f"site:{clean_domain} OR site:bloomberg.com OR site:wsj.com",
            },
            {
                "topic": "regulatory_environment",
                # Kept SEC grounding but added workforce and operational impact framing
                "query": f'site:sec.gov "{name}" "risk factors" "regulatory" OR "compliance" OR "government oversight" '
                f'"operations" OR "workforce" OR "business continuity" OR "license" OR "penalty"',
            },
            {
                "topic": "ai_disruption",
                # Broadened beyond company domain to capture industry-wide automation and job displacement risk
                "query": f'"{name}" {industry} "AI" OR "automation" OR "artificial intelligence" '
                f'"job displacement" OR "workforce reduction" OR "replacing roles" OR "productivity gains" '
                f'OR "AI strategy" OR "AI investment" '
                f"site:{clean_domain} OR site:techcrunch.com OR site:wired.com",
            },
            {
                "topic": "competition",
                # Reframed around competitive position as a proxy for company stability and job security
                "query": f'"{name}" {industry} competitors "market share" OR "market position" OR "competitive advantage" '
                f'"losing ground" OR "dominant player" OR "industry leader" OR "threat from" '
                f"site:{clean_domain} OR site:bloomberg.com OR site:businessinsider.com",
            },
            {
                "topic": "industry_growth_trajectory",
                # New — is the industry expanding or contracting? Directly affects hiring outlook and job security
                "query": f'{industry} "industry growth" OR "market size" OR "market forecast" OR "sector outlook" '
                f'"hiring trends" OR "talent demand" OR "expanding" OR "declining" OR "headcount growth" '
                f"site:bloomberg.com OR site:mckinsey.com OR site:forrester.com OR site:gartner.com",
            },
            {
                "topic": "consolidation_and_ma_risk",
                # New — M&A activity in the industry is a major job security risk (redundancy, culture disruption)
                "query": f'"{name}" {industry} "merger" OR "acquisition" OR "consolidation" OR "buyout" '
                f'"job cuts" OR "integration" OR "redundancies" OR "acquired by" OR "merger impact employees" '
                f"site:{clean_domain} OR site:wsj.com OR site:reuters.com OR site:bloomberg.com",
            },
            {
                "topic": "offshoring_and_automation_risk",
                # New — are roles in this industry being moved offshore or eliminated by automation?
                "query": f'"{name}" {industry} "offshoring" OR "outsourcing" OR "automation" OR "nearshoring" '
                f'"role elimination" OR "cost reduction" OR "moving jobs" OR "replacing workers" '
                f"site:{clean_domain} OR site:techcrunch.com OR site:businessinsider.com",
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
        # Dispatch job from router agent
        dispatch_job = state["job"]

        # Extract grounding and job data
        job_info = dispatch_job["job_data"]
        grounding = dispatch_job["grounding_data"]

        # Tool initialization
        web_research_tool = config.get("configurable", {}).get("web_research_tool")
        llm_analyzer_tool = config.get("configurable", {}).get("llm_summarizer")

        if not web_research_tool or not llm_analyzer_tool:
            raise ValueError("Required tools (search or llm) are not configured")

        # Run web search
        web_research = await self._run_web_research(
            grounding_data=grounding, web_research_tool=web_research_tool
        )

        # Anchor Context: Define the Company Sector and Niche
        industry_anchor = f"""
        TARGET ENTITY:
        - Company: {grounding.get("company_name")}
        - Reported Industry: {grounding.get("company_industry")}
        - Domain: {grounding.get("company_domain")}

        JOB CONTEXT:
        - Position Being Evaluated: {job_info.get("job_title")}
        - Purpose: Assess industry-level forces that affect job security, career growth,
        and employer stability for a candidate considering this role.
        """

        system_prompt = """
        ### ROLE
        You are a Senior Talent Market Intelligence Analyst specializing in industry risk assessment
        for job seekers evaluating career moves.

        ### STRATEGIC OBJECTIVE
        Synthesize raw web research and company grounding into a structured industry profile that helps
        a prospective employee understand the structural forces shaping their potential employer's sector.
        The goal is not financial analysis — it is career risk and opportunity assessment.

        ### ANALYTICAL FRAMEWORK:
        1. **Contextual Filtering**: Use the 'TARGET ENTITY' details to ensure all research findings
        are scoped to the correct industry and sector. Discard results that belong to adjacent or
        unrelated industries (e.g., distinguish 'Cloud Infrastructure' from 'Enterprise SaaS' if applicable).

        2. **Job-Applicant Lens**: Every finding should be interpreted through the question:
        "What does this mean for someone working here?" Translate industry dynamics into
        workforce implications — hiring trends, layoff risk, role stability, and career ceiling.

        3. **Role Relevance**: Where possible, relate industry forces to the specific job title provided
        in the JOB CONTEXT. A regulatory shift may affect a compliance role differently than an engineering role.

        4. **AI and Automation**: Assess whether AI represents a structural threat to roles in this
        industry or a tailwind creating new opportunities. Distinguish between AI augmenting workers
        and AI eliminating job categories outright.

        5. **Source Conflicts**: If sources disagree on market outlook or competitive position,
        default to the most recent and reputable source. Flag the disagreement in your output.

        6. **Strict JSON**: Respond ONLY with the raw JSON object. No preamble, no markdown, no explanation.
        """

        user_prompt = f"""
        ### Company & Industry Grounding:
        {industry_anchor}

        ### Web Research Results:
        {web_research}

        ### Analysis Task:
        Perform an industry analysis for {grounding.get("company_name")} in the {grounding.get("company_industry")} sector.
        Evaluate all findings through the lens of a job applicant considering a {job_info.get("job_title")} role.

        Populate ALL fields of the IndustryContextModels schema:

        1. **cyclic_or_defensive**: Is this industry cyclical or defensive? What happens to headcount
        and hiring in this sector during economic downturns? Cite historical patterns where available.

        2. **regulatory_environment**: What regulatory bodies govern this industry? How does compliance
        burden affect company operations, workforce stability, and risk of forced restructuring or shutdown?

        3. **ai_disruption**: Is AI a threat to roles in this industry or a growth driver creating new ones?
        Distinguish between automation of specific tasks vs. elimination of entire job categories.
        Relate findings to the {job_info.get("job_title")} role where possible.

        4. **competition**: How competitive is this industry and what does that mean for the company's
        stability as an employer? Does the company hold a durable market position or is it fighting
        for survival in a commoditized market?

        5. **industry_growth_trajectory**: Is the industry expanding or contracting? What does the
        talent demand outlook look like — are companies in this sector actively hiring or reducing headcount?

        6. **consolidation_and_ma_risk**: How active is M&A in this industry? Is the company a likely
        acquisition target or acquirer, and what would that mean for employees in terms of redundancies
        or culture disruption?

        7. **offshoring_and_automation_risk**: Are roles in this industry structurally at risk of being
        offshored, outsourced, or automated — independent of this company's specific performance?

        Return ONLY a JSON object. Use "No data available" for any fields where research is insufficient.
        """

        # Run llm analysis
        llm_response = await llm_analyzer_tool.run(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            output_schema=IndustryContextModels,
        )

        formatted_results = {
            "job_id": job_info.get("job_id"),
            "agent_type": "industry",
            "data": llm_response.model_dump(),
        }

        return {"agent_analysis": [formatted_results]}
