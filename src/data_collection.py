import copy

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
            },
            {
                "topic": "regulatory_environment",
                "query": "[Company Name] regulatory risks 10-K risk factors site:sec.gov compliance requirements government oversight industry regulation impact on revenue",
            },
            {
                "topic": "ai_distruption",
                "query": "[Company Name] AI integration strategy R&D spending AI capex competitive positioning",
            },
            {
                "topic": "competition",
                "query": "[Company Name] gross margin trend vs competitors pricing power switching costs network effects",
            },
        ]

    def run_research(self, state: State, config: RunnableConfig):
        # make new copy of queries dict
        new_queries = copy.deepcopy(self.queries)
        web_research_tool = config.get("configurable", {}).get("web_search_tool")

        # run tavily search for each query
        for i in range(len(new_queries)):
            current_query = new_queries[i].get("query")
            response = web_research_tool.search(query=current_query, topic="news")
            # add researched urls to the new_queries dict
            aggregate_discovered_urls = [r["url"] for r in response]
            new_queries[i]["relevant_urls"] = aggregate_discovered_urls  # type: ignore

        # extract relevant data


class WorkforceSignals:
    pass


class Leadership:
    pass


class RoleContext:
    pass
