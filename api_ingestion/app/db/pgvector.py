# Vector storage logic (PgVector)
import uuid
from sqlalchemy import create_engine, Column, String, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, sessionmaker
from pgvector.sqlalchemy import Vector
from app.models.schemas import SpecIn
from app.core import config
import logging

logging.basicConfig(level=logging.INFO)

Base = declarative_base()

mock_enable = config.get_database_mock_enable()


if not mock_enable:
    engine = create_engine(config.get_database_url(), echo=True, future=True)
    SessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)


def get_db():
    return SessionLocal()


class SpecRecord(Base):
    __tablename__ = "openapi_specs"
    id = Column(UUID(as_uuid=False), primary_key=True)
    raw_spec = Column(JSON, nullable=False)
    embedding = Column(Vector(1536), nullable=False)  # assuming OpenAI's 1536-dimension


def save_embedding(embedding, spec: SpecIn):
    """Create the database tables if they do not exist."""
    logging.info(f"Database mock enable: {mock_enable}") 
    if mock_enable:
        # Mock implementation, no database interaction
        return SpecRecord(id=str(uuid.uuid4()), raw_spec=spec.spec, embedding=embedding)
    else:
        db = get_db()
        record = SpecRecord(id=str(uuid.uuid4()), raw_spec=spec.spec, embedding=embedding)
        db.add(record)
        db.commit()
        return record
