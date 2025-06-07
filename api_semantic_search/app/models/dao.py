# Vector storage logic (PgVector)
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core import config
from app.models.search import SearchQuery, SearchResult
from typing import List
import logging


logging.basicConfig(level=logging.INFO)

Base = declarative_base()

mock_enable = config.get_database_mock_enable()


if not mock_enable:
    engine = create_engine(config.get_database_url(), echo=True, future=True)
    SessionLocal = sessionmaker(bind=engine)


def semantic_search(query: SearchQuery) -> List[SearchResult]:
    dummy = [
        SearchResult(
            endpoint_id="12345",
            path="/api/v1/resource",
            summary="Retrieve resource"
        )
    ]
    return dummy
