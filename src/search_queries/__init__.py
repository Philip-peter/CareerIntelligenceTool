from . import (
    finance_queries,
    industry_queries,
    leadership_queries,
    strategic_direction_queries,
    workforce_queries,
)

QUERY_REGISTRY = (
    leadership_queries.LEADERSHIP_QUERIES
    + industry_queries.INDUSTRY_QUERIES
    + workforce_queries.WORKFORCE_QUERIES
    + finance_queries.FINANCE_QUERIES
    + strategic_direction_queries.STRATEGIC_DIRECTION_QUERIES
)
