# queries/__init__.py

from search_queries.finance_queries import FINANCE_QUERIES
from search_queries.industry_queries import INDUSTRY_QUERIES
from search_queries.leadership_queries import LEADERSHIP_QUERIES
from search_queries.strategic_direction_queries import STRATEGIC_DIRECTION_QUERIES
from search_queries.workforce_queries import WORKFORCE_QUERIES

# Query registry for future development for an agent that improves the queries
QUERY_REGISTRY = (
    LEADERSHIP_QUERIES
    + INDUSTRY_QUERIES
    + WORKFORCE_QUERIES
    + FINANCE_QUERIES
    + STRATEGIC_DIRECTION_QUERIES
)
