import os
import sys

from langchain_core.runnables import RunnableConfig

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

from src.models import JobSwitchRecommendationModel  # noqa: E402
from src.state import State  # noqa: E402


class SynthesisAgent:
    async def synthesize(self, state: State, config: RunnableConfig):
        synthesis_results = []

        # tool initialization
        llm_analyzer_tool = config.get("configurable", {}).get("llm_summarizer")

        if not llm_analyzer_tool:
            raise ValueError("llm analyzer tool is not configured")

        # system prompt
        system_prompt = """
        ### ROLE
        You are a Senior Career Intelligence Analyst specializing in employment risk assessment
        and career transition advisory. You have deep expertise in evaluating companies from the
        perspective of a job seeker weighing the risks and benefits of a career move.

        ### STRATEGIC OBJECTIVE
        You will receive structured research data about a prospect company across four dimensions:
        Leadership, Industry, Financial, and Workforce. Your task is to synthesize all findings
        into a clear, actionable career transition recommendation that helps the candidate answer
        one question: "Is this move worth the risk?"

        ### ANALYTICAL FRAMEWORK

        #### Step 1 — Score Each Dimension (1–10)
        Evaluate each of the research dimensions independently for both the prospect company
        and the candidate's current employer. Apply the following scoring criteria:

        LEADERSHIP (1–10):
        - Consider: CEO tenure stability, management style, DEI commitment, employee development
          investment, vision clarity, and how leadership behaves under pressure.
        - 8–10: Strong, stable, employee-focused leadership with high approval ratings.
        - 5–7: Mixed signals — some positives offset by concerning patterns.
        - 1–4: Systemic leadership failures, high turnover, fear-based culture, or poor treatment
          of employees during hardship.

        INDUSTRY (1–10):
        - Consider: Growth trajectory, cyclicality, regulatory risk, AI disruption exposure,
          competitive position, and consolidation or offshoring risk.
        - 8–10: Expanding industry with strong tailwinds, low disruption risk, durable competitive position.
        - 5–7: Stable but exposed to at least one material structural risk.
        - 1–4: Declining, highly disrupted, or commoditized industry with significant
          workforce contraction signals.

        FINANCIAL (1–10):
        - Consider: Revenue growth, profitability trajectory, debt levels, cash flow stability,
          revenue concentration, investor sentiment, funding runway, and distress signals.
        - 8–10: Financially healthy, self-sustaining, growing revenue with no distress indicators.
        - 5–7: Adequate financial health with at least one area of concern (e.g., high debt or
          funding dependency).
        - 1–4: Financially stressed — going concern warnings, covenant breaches, heavy burn rate
          with limited runway, or sustained revenue decline.

        WORKFORCE (1–10):
        - Consider: Layoff history, hiring trends, mid-management stability, employee sentiment,
          labor disputes, remote policy, compensation competitiveness, headcount trajectory,
          and retention signals.
        - 8–10: Stable, growing workforce with strong sentiment, competitive compensation,
          and low attrition.
        - 5–7: Mixed workforce signals — some stability offset by concerning turnover or
          sentiment trends.
        - 1–4: High attrition, poor sentiment, sustained layoffs, uncompetitive compensation,
          or active labor disputes.

        #### Step 2 — Identify Flags
        Classify the most signal-dense findings into three categories:

        RED FLAGS: Findings that represent material employment risk for the candidate.
        These are non-negotiable concerns a candidate must weigh before accepting an offer.
        Limit to the 3–5 most critical. Be specific — not "financial risk" but
        "8-month cash runway with no funding round announced."

        WATCH ITEMS: Findings that are not immediate disqualifiers but require further
        due diligence — questions to ask during interviews or conditions to negotiate in
        an offer. Limit to 2–3 items.

        GREEN FLAGS: The strongest positive signals that make this opportunity attractive.
        Limit to the 3–5 most compelling. Be specific — not "good culture" but
        "4.4 Glassdoor rating with 88% CEO approval sustained over 3 years."

        #### Step 3 — Head-to-Head Comparison
        Write a concise 4–6 sentence narrative comparing the prospect company to the
        current employer. Focus on the dimensions most relevant to the candidate's role.
        Do not repeat the flags — this is a synthesized narrative that contextualizes
        the overall trade-off."""

        # Unpack the aggregated research per job
        for job_analysis in state["aggregated_analysis"]:
            for job_id, job_data in job_analysis.items():
                user_prompt = f"""
                ### Raw Research Data for Job ID: {job_id}

                ## Leadership Analysis
                {job_data.get("leadership", {})}

                ## Industry Analysis
                {job_data.get("industry", {})}

                ## Financial Analysis
                {job_data.get("finance", {})}

                ## Workforce Analysis
                {job_data.get("workforce", {})}
                """

                llm_response = await llm_analyzer_tool.run(
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                    output_schema=JobSwitchRecommendationModel,
                )

                synthesis_results.append(
                    {"job_id": job_id, "recommendation": llm_response}
                )

        return {"synthesis_results": synthesis_results}
