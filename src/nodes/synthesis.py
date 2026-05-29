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

        # simulated current employer
        simulated_current_employer = {
            "job_id": "current_employer",
            "current_company_profile": {
                "Current Job Title": "Principal Security Analyst",
                "Current Company": "Dayforce",
                "Current Company Industry": "Human Capital Management (HCM) / HR Technology",
                "Current Company Official Website": "https://www.dayforce.com/",
                "Prospect Company Official Linkedin": "https://www.linkedin.com/company/dayforce/",
            },
            "data": {
                "leadership": {
                    "ceo_tenure": (
                        "David Ossip has served as CEO since 2013 — over 12 years — making him one of "
                        "the longest-tenured CEOs in the HCM software sector. He is the original founder "
                        "of Dayforce (acquired by Ceridian in 2012) and led the company's full transformation "
                        "from a legacy payroll provider to a cloud HCM platform and a $2B+ revenue business. "
                        "His tenure has included a major brand pivot in February 2024 from Ceridian to Dayforce "
                        "and a 5% global workforce reduction in Q1 2025 framed as a strategic realignment. "
                        "Ossip has been recognized as Canada's Most Admired CEO for Transformational Leadership "
                        "and previously named one of Glassdoor's Highest Rated CEOs."
                    ),
                    "founder_involvement": (
                        "David Ossip is both the founder and active CEO, serving as Executive Chair and CEO "
                        "simultaneously. His involvement is deep and day-to-day — he is credited with the "
                        "strategic vision behind the Dayforce platform and the company's $5B revenue target. "
                        "Founder presence provides strong mission alignment and product conviction but also "
                        "concentrates decision-making. Some Glassdoor reviews note the broader C-suite has "
                        "become more financially driven under new executives hired alongside Ossip, creating "
                        "a tension between founder culture and institutional growth pressures."
                    ),
                    "strategic_pivots": (
                        "Dayforce executed two major pivots in recent years: (1) a full cloud transformation "
                        "from legacy Ceridian infrastructure completed over 2018-2022, and (2) a legal name "
                        "and brand change from Ceridian to Dayforce in February 2024, unifying the company "
                        "around its flagship product. A third pivot is underway — aggressive international "
                        "expansion and Global Payroll buildout targeting multinational enterprises. The 2025 "
                        "5% workforce reduction was framed as a realignment to support this expansion, "
                        "eliminating roles in areas of lower strategic priority. Some US technology positions "
                        "have been outsourced or moved offshore as part of cost restructuring."
                    ),
                    "executive_reputation": (
                        "David Ossip holds strong personal approval ratings — historically recognized on "
                        "Glassdoor's Highest Rated CEOs list and awarded transformational leadership recognition. "
                        "However, recent Glassdoor reviews note a bifurcation: the CEO is widely respected, "
                        "but newer C-suite hires — particularly the CRO — have received significant criticism "
                        "for fear-based management, poor sales leadership, and cultural deterioration in the "
                        "sales organization. Overall Glassdoor rating sits in the 3.5-3.8 range with mixed "
                        "recent sentiment, a meaningful decline from prior years when the company was "
                        "consistently rated a best place to work."
                    ),
                    "leadership_stability": (
                        "C-suite stability is a material concern. Glassdoor reviews consistently cite 'huge "
                        "turnover at the most senior C-level positions with excellent leaders leaving.' "
                        "New C-suite hires post-rebrand have been described as financially focused and "
                        "stock-price driven rather than culture-driven. Jeremy Johnson joined as CFO in 2024. "
                        "The CRO role has been a source of significant employee criticism. Director and VP "
                        "level stability is mixed — the 2025 layoffs and team realignments have disrupted "
                        "mid-management continuity in several business units."
                    ),
                    "employee_treatment_during_hardship": (
                        "The February 2025 5% global workforce reduction (~800-1,000 employees) was announced "
                        "via an internal letter from the CEO and disclosed via SEC 8-K filing. The company "
                        "allocated $18-21M for severance payments and employee benefits, suggesting meaningful "
                        "severance packages. The restructuring was framed around strategic focus rather than "
                        "financial distress. However, Glassdoor reviews note mass layoffs have occurred even "
                        "after profitable quarters, which has eroded trust. The communication was relatively "
                        "transparent by industry standards but the pattern of recurring reductions has created "
                        "a low job security perception among employees."
                    ),
                    "management_style_and_culture": (
                        "Culture is described as bifurcated in recent reviews. Product and engineering teams "
                        "report a collaborative, innovation-focused environment consistent with Ossip's "
                        "founder-led vision. The sales organization is described very differently — fear-based "
                        "management under the current CRO, with micromanagement and high attrition. "
                        "The company has been named a Top 100 Most Loved Workplace by Newsweek for two "
                        "consecutive years and made Computerworld's Best Places to Work in IT list, "
                        "suggesting the positive culture signals are genuine in some parts of the organization "
                        "but inconsistent across functions."
                    ),
                    "vision_and_communication_clarity": (
                        "Strategic vision is clearly articulated: $5B revenue and $1B+ free cash flow as "
                        "long-term targets, with AI-powered HCM and Global Payroll as the primary growth vectors. "
                        "David Ossip communicates regularly through earnings calls, investor presentations, "
                        "and internal all-hands. The February 2025 layoff communication was delivered via "
                        "a personal letter before the SEC filing, suggesting reasonable internal transparency. "
                        "However, some employees report being surprised by the scale of team changes, "
                        "indicating communication may not fully cascade below senior levels."
                    ),
                    "dei_and_values_commitment": (
                        "Dayforce publishes an annual ESG report (most recent: 'Impact through Innovation 2024') "
                        "covering five pillars including 'Our People.' The company has received a Seramount "
                        "Global Inclusion Index recognition and a Silver Medal EcoVadis sustainability rating. "
                        "Named one of America's Most Responsible Companies by Newsweek. No major public DEI "
                        "controversies or rollbacks identified. However, the outsourcing of US technology "
                        "positions overseas raises questions about equitable workforce practices domestically."
                    ),
                    "employee_development_investment": (
                        "Dayforce acquired eloomi A/S (a learning experience platform) in Q1 2024, "
                        "signaling investment in learning and development both as a product capability "
                        "and an internal practice. The company offers unlimited vacation (manager-approved) "
                        "and is recognized on Computerworld's Best Places to Work in IT list. "
                        "Internal mobility and career pathing signals are mixed — some reviews praise "
                        "growth opportunities while others cite the 2025 restructuring as having eliminated "
                        "clear career paths in affected teams."
                    ),
                },
                "industry": {
                    "cyclic_or_defensive": (
                        "HCM software is largely defensive — HR, payroll, and workforce management are "
                        "mission-critical functions that organizations maintain even during downturns. "
                        "SaaS subscription models create revenue stability through multi-year contracts. "
                        "However, Dayforce's exposure to SMB and mid-market customers introduces some "
                        "cyclicality — smaller customers churn at higher rates during recessions. "
                        "The 2025 5% headcount reduction despite continued revenue growth suggests "
                        "the company itself is not immune to cost discipline pressures even in a "
                        "relatively stable sector."
                    ),
                    "regulatory_environment": (
                        "HCM and payroll software operates under substantial regulatory oversight — "
                        "employment law, payroll tax compliance, GDPR, CCPA, and jurisdiction-specific "
                        "labor regulations across 160+ countries where Dayforce operates. Compliance is "
                        "actually a core competitive advantage and revenue driver for Dayforce (230+ "
                        "compliance updates delivered in 2025 alone). Regulatory complexity creates "
                        "high switching costs for customers, which supports revenue stability. "
                        "No material regulatory risk to Dayforce's operations has been flagged in "
                        "recent SEC filings."
                    ),
                    "ai_disruption": (
                        "AI is a tailwind for Dayforce as a product category — the company is actively "
                        "investing in Dayforce Co-Pilot (GenAI assistant), AI Agents for workflow automation, "
                        "and AI-enhanced Demand Forecasting. These capabilities were made generally available "
                        "in Q4 2024. As an HCM platform, Dayforce benefits from AI adoption rather than "
                        "being threatened by it. Internally, AI and automation may reduce headcount needs "
                        "in implementation services and support roles over time, which partially explains "
                        "the 2025 restructuring narrative around 'investing in innovation.'"
                    ),
                    "competition": (
                        "The HCM market is intensely competitive. Workday leads the enterprise segment with "
                        "~9.8% market share and $7.5B+ in HCM revenue. Dayforce holds approximately 3.84% "
                        "market share, ranked 9th globally. Primary competitors include Workday, Oracle HCM, "
                        "SAP SuccessFactors, UKG, ADP, and Microsoft Dynamics. Dayforce differentiates on "
                        "native payroll and time on a unified codebase — a genuine technical advantage "
                        "in frontline and hourly-workforce industries. Some Glassdoor reviews cite "
                        "Workday, UKG, and Oracle pulling ahead on full ERP integration, which represents "
                        "a credible competitive risk in the upper-enterprise segment."
                    ),
                    "industry_growth_trajectory": (
                        "The global HCM market was valued at $58.7B in 2024, growing 11.7% YoY, and is "
                        "forecast to reach $81.1B by 2029 at a 6.7% CAGR. Strong structural tailwinds "
                        "from workforce complexity, global payroll demand, compliance requirements, and "
                        "AI integration are driving sustained investment across all HCM vendors. "
                        "Talent demand in HCM software — engineering, product, implementations, and "
                        "customer success — remains healthy industry-wide despite Dayforce's own 2025 "
                        "headcount reduction."
                    ),
                    "consolidation_and_ma_risk": (
                        "The HCM sector has seen moderate M&A activity — Dayforce itself acquired eloomi "
                        "in Q1 2024. Larger consolidation risk exists from Oracle, SAP, or private equity "
                        "interest in mid-tier HCM players. Dayforce's market cap and public listing "
                        "(NYSE/TSX: DAY) make it a viable acquisition target, though its founder-CEO "
                        "control and strategic trajectory make a near-term acquisition unlikely. "
                        "A change of control event would represent a material culture and job security "
                        "risk for employees."
                    ),
                    "offshoring_and_automation_risk": (
                        "Dayforce has been outsourcing US technology and support positions overseas as "
                        "part of its cost reduction strategy — confirmed in Glassdoor reviews and "
                        "consistent with the 2025 restructuring's cost savings narrative ($80M annualized). "
                        "Roles most at risk are US-based implementation consultants, technical support, "
                        "and QA engineering. Product management, senior engineering, and sales roles "
                        "appear less exposed. AI automation of routine implementation and support tasks "
                        "is an additional medium-term risk for services-facing roles."
                    ),
                },
                "finance": {
                    "revenue_growth": (
                        "Dayforce has delivered consistent double-digit revenue growth. Q3 2024 total revenue "
                        "was $440M, up 17% YoY. Q1 2025 total revenue was $481.8M, up 11.7% YoY (13.6% on "
                        "constant currency). Dayforce recurring revenue — the highest-quality revenue stream "
                        "— grew 19% YoY in Q3 2024. Revenue growth is moderating from peak levels but "
                        "remains healthy. The company is targeting $5B in long-term revenue, implying "
                        "significant continued growth from the current ~$1.9B annualized run rate. "
                        "Growth trajectory is positive for employer stability."
                    ),
                    "profitability": (
                        "Dayforce is generating operating profits and improving margins. Operating cash flow "
                        "year-to-date through Q3 2024 was $200.1M, up 54% YoY. The 2025 restructuring "
                        "is expected to generate $65M in pre-tax cost savings in FY2025 and $80M annualized. "
                        "Q1 2025 operating margins remain below the software sector average per analyst "
                        "commentary, indicating room for improvement. The shift in CEO compensation toward "
                        "FCF metrics in 2025 signals management is prioritizing profitability alongside growth — "
                        "a positive signal for financial sustainability."
                    ),
                    "debt": (
                        "Dayforce is a publicly traded company (NYSE/TSX: DAY) with a $500M share buyback "
                        "program underway — $66M+ returned to shareholders as of Q1 2025. The company's "
                        "debt profile is not flagged as a concern in recent SEC filings. Investment grade "
                        "positioning is supported by improving cash flows. Capital allocation toward buybacks "
                        "alongside growth investment suggests management confidence in balance sheet strength. "
                        "No covenant breaches or credit rating concerns identified."
                    ),
                    "cash_flow": (
                        "Cash flow is a standout positive. Operating cash flow grew 54% YTD through Q3 2024 "
                        "to $200.1M. Q1 2025 operating cash was ~$50M, sufficient to fund $30M in share "
                        "repurchases. The $1B+ FCF target is the long-term anchor of management's financial "
                        "strategy. Free cash flow trajectory is positive and self-sustaining — Dayforce does "
                        "not rely on external capital to fund operations, a strong employer stability signal."
                    ),
                    "revenue_concentration": (
                        "Dayforce serves thousands of enterprise customers across diverse industries including "
                        "healthcare, retail, manufacturing, government, and financial services. Customer "
                        "examples from recent earnings include organizations ranging from 1,400 to 100,000 "
                        "employees across 28+ countries. No single customer concentration risk has been "
                        "disclosed in recent SEC filings. The Government of Canada is a high-profile customer "
                        "but represents a contract win rather than a concentration risk. Revenue diversification "
                        "is a positive signal for employer stability."
                    ),
                    "investor_sentiment": (
                        "Analyst and investor sentiment is cautiously positive. Management raised profitability "
                        "guidance following the 2025 restructuring. Q1 2025 earnings reinforced momentum with "
                        "strong sales growth. However, Dayforce's TSR of 107 in 2024 versus 206 for the "
                        "S&P 1500 Application Software peer index shows meaningful relative underperformance, "
                        "suggesting investors are cautious about the pace of margin expansion and competitive "
                        "positioning versus Workday and Oracle. Say-on-Pay received 91.4% approval at the "
                        "2024 AGM, reflecting shareholder alignment with executive direction."
                    ),
                    "funding_and_runway": (
                        "Not applicable — Dayforce is a publicly traded company (NYSE: DAY, TSX: DAY) with "
                        "self-sustaining operations funded by recurring SaaS revenue and strong operating "
                        "cash flow. No external funding dependency. The $500M share repurchase program "
                        "signals balance sheet confidence. Financial runway is not a concern for this employer."
                    ),
                    "financial_distress_signals": (
                        "No financial distress signals identified. No going concern warnings, covenant breaches, "
                        "credit downgrades, or missed payments in any reviewed SEC filings or news sources. "
                        "The 2025 restructuring was proactive cost optimization, not a distress response — "
                        "supported by simultaneous buyback activity and raised profitability guidance. "
                        "Dayforce's financial health as an employer is stable."
                    ),
                },
                "workforce": {
                    "layoff_history": (
                        "Dayforce conducted a 5% global workforce reduction in February 2025, affecting "
                        "approximately 800-1,000 employees. The company allocated $18-21M for severance "
                        "and benefits. This follows a pattern flagged in Glassdoor reviews of 'mass layoffs "
                        "being common' even after profitable quarters — suggesting recurring restructuring "
                        "is embedded in the company's operating model rather than being a one-off event. "
                        "No WARN Act violations or wrongful termination class actions identified in public records."
                    ),
                    "hiring_trends": (
                        "Dayforce continues to hire selectively post-restructuring, particularly in product, "
                        "AI/engineering, and international expansion roles. The Q1 2025 restructuring was "
                        "explicitly framed as a reallocation of investment rather than a net headcount reduction "
                        "— cost savings are being reinvested into strategic growth initiatives. "
                        "However, overall hiring velocity has slowed compared to 2022-2023 levels. "
                        "International roles and AI-adjacent functions are growing while US-based services "
                        "and support roles are contracting."
                    ),
                    "mid_management_turnover": (
                        "Mid-management stability is a meaningful concern based on Glassdoor and Blind signals. "
                        "The 2025 restructuring involved team realignments that disrupted director and VP-level "
                        "continuity in several business units. The sales organization has seen significant "
                        "director-level churn under the current CRO's leadership — repeatedly cited in reviews "
                        "as a cultural deterioration driver. Engineering and product management mid-levels "
                        "appear more stable."
                    ),
                    "employee_sentiments": (
                        "Glassdoor sentiment is mixed and trending negative versus historical highs. "
                        "Recurring positive themes: CEO David Ossip is genuinely respected, strong product, "
                        "good benefits, unlimited PTO, and a collaborative engineering culture. "
                        "Recurring negative themes: C-suite instability, fear-based sales culture under the "
                        "CRO, job insecurity from recurring layoffs, and US positions being moved offshore. "
                        "The company has been named a Most Loved Workplace for two consecutive years by "
                        "Newsweek, suggesting an institutional culture foundation that is being tested by "
                        "recent leadership and structural changes."
                    ),
                    "labor_disputes": (
                        "No active union organizing, strikes, or NLRB unfair labor practice filings identified. "
                        "No employee class action lawsuits or significant wrongful termination cases found "
                        "in public records. Labor relations appear stable from a legal and regulatory "
                        "standpoint despite the 2025 layoffs."
                    ),
                    "remote_and_flexibility_policy": (
                        "Dayforce operates with a hybrid work model. The company has offices in Minneapolis "
                        "and Toronto as primary HQs with a distributed global workforce. Unlimited PTO "
                        "is a stated benefit (manager-approved). No blanket return-to-office mandate has "
                        "been publicly announced. Remote and hybrid arrangements appear to vary by role "
                        "and team — implementation and customer-facing roles have more in-office or "
                        "travel requirements than product and engineering. Work-life balance is frequently "
                        "cited positively in Glassdoor reviews."
                    ),
                    "compensation_and_benefits": (
                        "Compensation is described as competitive within the HCM software sector. "
                        "Benefits include unlimited PTO, strong health coverage, and equity-based compensation. "
                        "CEO compensation is 90% equity-based with performance RSUs tied to FCF and revenue "
                        "targets — equity alignment extends through the organization. Some reviews note "
                        "below-market base salaries offset by equity, which creates retention risk if "
                        "the stock underperforms. Dayforce's 2024 TSR underperformed its software peer "
                        "index, which may have impacted equity compensation value for employees."
                    ),
                    "headcount_trajectory": (
                        "Dayforce headcount has been effectively flat to slightly declining since 2023 "
                        "following rapid growth in 2021-2022. The February 2025 5% reduction represents "
                        "the most significant single event. The company frames future headcount growth "
                        "as targeted and strategic — AI and international expansion roles growing while "
                        "US-based services roles shrink. Net workforce size is expected to grow modestly "
                        "as the company scales toward $5B revenue, but the pace of hiring is unlikely "
                        "to return to 2021-2022 levels."
                    ),
                    "employee_tenure_and_retention": (
                        "Average employee tenure signals are mixed. Long-tenured employees exist in product "
                        "and engineering functions where culture is described positively. Attrition is "
                        "notably higher in the sales organization following leadership changes under the "
                        "current CRO — a recurring theme across multiple Glassdoor reviews spanning 2024-2025. "
                        "The recurring restructuring cycle and offshore outsourcing of US roles has increased "
                        "voluntary attrition among high performers who cite job insecurity as a primary "
                        "motivator for leaving. Retention risk is elevated relative to 2020-2022 levels."
                    ),
                },
            },
        }

        # system prompt
        system_prompt = """
        ### ROLE
        You are a Senior Career Intelligence Analyst specializing in employment risk assessment
        and career transition advisory. You have deep expertise in evaluating companies from the
        perspective of a job seeker weighing the risks and benefits of a career move.

        ### STRATEGIC OBJECTIVE
        You will receive structured research data about a prospect company across various dimensions:
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
                # extract prospect company profile
                prospect_company_profile = {
                    "job_title": job_data.get("job", {}).get(
                        "job_title", "Not Available"
                    ),
                    "job_posting_link": job_data.get("job", {}).get(
                        "job_posting_link", "Not Available"
                    ),
                    "job_description": job_data.get("job", {}).get(
                        "job_description", "Not Available"
                    ),
                    "job_salary": job_data.get("job", {}).get(
                        "job_salary", "Not Available"
                    ),
                    "job_hiring_team": job_data.get("job", {}).get(
                        "job_hiring_team", "Not Available"
                    ),
                    "company_name": job_data.get("company", {}).get(
                        "company_name", "Not Available"
                    ),
                    "company_industry": job_data.get("company", {}).get(
                        "company_industry", "Not Available"
                    ),
                    "company_official_url": job_data.get("company", {}).get(
                        "company_official_url", "Not Available"
                    ),
                    "company_linkedin_url": job_data.get("company", {}).get(
                        "company_linkedin_url", "Not Available"
                    ),
                }

                # user prompt
                user_prompt = f"""

                ### CURRENT EMPLOYER DATA:
                {simulated_current_employer["data"]}

                ### Raw Research Data for Prospective Employer

                ## Job ID: {job_id}

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
                    {
                        "job_id": job_id,
                        "current_company_profile": prospect_company_profile,
                        "prospect_company_profile": prospect_company_profile,
                        "recommendation": llm_response.model_dump(),
                    }
                )

        return {"synthesis_results": synthesis_results}
