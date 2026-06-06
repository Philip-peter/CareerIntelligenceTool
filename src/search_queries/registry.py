from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class QueryEntry:
    id: str
    agent: str
    topic: str
    template: str
    purpose: str
    # primary_sources: list[str]
    # signal_type: str
    # job_applicant_relevance: int
    status: str = "active"
    version: int = 1
    last_reviewed: Optional[date] = None
    review_notes: Optional[str] = None


def get_queries_by_agent(agent: str, registry: list[QueryEntry]) -> list[QueryEntry]:
    return [q for q in registry if q.agent == agent and q.status == "active"]


def get_query_by_id(query_id: str, registry: list[QueryEntry]) -> Optional[QueryEntry]:
    return next((q for q in registry if q.id == query_id), None)


def render_queries(
    agent: str, grounding: dict, registry: list[QueryEntry]
) -> list[dict]:
    name = grounding.get("company_name", "")
    domain = grounding.get("company_domain", "")
    industry = grounding.get("company_industry", "")
    clean_domain = (
        domain.replace("https://", "").replace("http://", "").split("/")[0]
        if domain
        else ""
    )
    return [
        {
            "topic": entry.topic,
            "query": entry.template.format(
                name=name,
                clean_domain=clean_domain,
                industry=industry,
            ),
        }
        for entry in get_queries_by_agent(agent, registry)
    ]
