import os
import sys
from datetime import datetime

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_dir)

from src.state import State  # noqa: E402


class GenerateReport:
    def __init__(self) -> None:
        pass

    def summarize(self, state: State):
        # summarize report
        summary = f"""
        # Target Company: {state["target_company"]}
        ---

        ### Leadership Research
        **CEO Tenure:**
        > {state["leadership_research"].ceo_tenure}
        **Founder Involvement**
        > {state["leadership_research"].founder_involvement}
        **Strategic Pivots:**
        > {state["leadership_research"].strategic_pivots}
        **Insider Behavior:**
        > {state["leadership_research"].insider_behavior}

        ---

        ### Industry Research
        **Cyclic or Defensive:**
        > {state["industry_research"].cyclic_or_defensive}
        **Regulatory Environment**
        > {state["industry_research"].regulatory_environment}
        **AI Distruption:**
        > {state["industry_research"].ai_distruption}
        **Competition:**
        > {state["industry_research"].competition}

        ---
        *Report generated on: {datetime.now().strftime("%Y-%m-%d")}*
        """

        return {"final_report": summary}
