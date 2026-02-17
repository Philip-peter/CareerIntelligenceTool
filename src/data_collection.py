from langchain_core.runnables import RunnableConfig

from state import State


class FinancialData:
    def __init__(self) -> None:
        pass

    def run_research(self, state, config):
        return """"""


class IndustryContext:
    def __init__(self) -> None:
        self.queries = [
            {
                "topic": "cyclic_or_defensive",
                "query": "[Company Name] is it cyclical or defensive analyst commentary recession sensitivity operating margin volatility",
                "relevant_url": [],
            },
            {
                "topic": "regulatory_environment",
                "query": "[Company Name] regulatory risks 10-K risk factors site:sec.gov compliance requirements government oversight industry regulation impact on revenue",
                "relevant_url": [],
            },
            {
                "topic": "ai_distruption",
                "query": "[Company Name] AI integration strategy R&D spending AI capex competitive positioning",
                "relevant_url": [],
            },
            {
                "topic": "competition",
                "query": "[Company Name] gross margin trend vs competitors pricing power switching costs network effects",
                "relevant_url": [],
            },
        ]

    def run_research(self, state: State, config: RunnableConfig):
        web_research_tool = config.get("configurable", {}).get("web_search_tool")
        # search relevant urls
        for research in self.queries:
            response = web_research_tool.search(query=research["query"], topic="news")
            research["relevant_url"] = [response["url"]]

        # extract relevant data


class WorkforceSignals:
    pass


class Leadership:
    pass


class RoleContext:
    pass
