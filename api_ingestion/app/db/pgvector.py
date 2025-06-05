# Vector storage logic (PgVector)
import json
import uuid
from sqlalchemy import create_engine, Column, String, Text, ForeignKey, JSON, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.sql import func
from sqlalchemy.exc import SQLAlchemyError
from pgvector.sqlalchemy import Vector
from app.core import config
import logging


logging.basicConfig(level=logging.INFO)

Base = declarative_base()

mock_enable = config.get_database_mock_enable()


if not mock_enable:
    engine = create_engine(config.get_database_url(), echo=True, future=True)
    SessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)


class API(Base):
    __tablename__ = "apis"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    version = Column(String, nullable=False)
    spec = Column(JSON, nullable=False)
    uploaded_at = Column(DateTime, server_default=func.now())
    endpoints = relationship("APIEndpoint", back_populates="api", cascade="all, delete-orphan")

    def __repr__(self):
        return json.dumps({
            "id": self.id,
            "title": self.title,
            "version": self.version,
            "uploaded_at": str(self.uploaded_at)
        })


class APIEndpoint(Base):
    __tablename__ = "api_endpoints"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    api_id = Column(String, ForeignKey("apis.id"), nullable=False)
    path = Column(String, nullable=False)
    method = Column(String, nullable=False)  # e.g., GET, POST
    summary = Column(Text)
    operation_id = Column(String)

    api = relationship("API", back_populates="endpoints")
    embeddings = relationship("Embedding", back_populates="endpoint", cascade="all, delete-orphan")

    def __repr__(self):
        return json.dumps({
            "id": self.id,
            "api_id": self.api_id,
            "path": self.path,
            "method": self.method,
            "summary": self.summary,
            "operation_id": self.operation_id
        })


class Embedding(Base):
    __tablename__ = "embeddings"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    endpoint_id = Column(String, ForeignKey("api_endpoints.id"), nullable=False)
    model = Column(String, nullable=False)  # e.g., text-embedding-ada-002
    created_at = Column(DateTime, server_default=func.now())
    # TODO embedding = Column(Vector(1536), nullable=False)  # 1536 = OpenAI ada-002 output

    endpoint = relationship("APIEndpoint", back_populates="embeddings")

    def __repr__(self):
        return json.dumps({
            "id": self.id,
            "endpoint_id": self.endpoint_id,
            "model": self.model,
            "created_at": str(self.created_at)
        })


def save_embedding(embedding, spec: dict) -> str:
    """Create the database tables if they do not exist."""
    logging.info(f"Database mock enable: {mock_enable}")
    new_id = str(uuid.uuid4())
    record_api = API(
        id=new_id,
        title=spec['info']['title'],
        version=spec['info']['version'],
        spec=spec
    )
    logging.info(f"Saving record: {new_id}")
    if mock_enable:
        # Mock implementation, no database interaction
        return new_id
    else:
        for path, methods in spec.get("paths", {}).items():
            for method, op in methods.items():
                summary = op.get("summary", "")
                description = op.get("description", "")
                logging.info(f"Processing endpoint: {path} {method}")
                endpoint = APIEndpoint(
                    id=str(uuid.uuid4()),
                    api_id=new_id,
                    path=path,
                    method=method.upper(),
                    summary=summary or description,
                    operation_id=op.get("operationId")
                )
                record_api.endpoints.append(endpoint)
                embedding_record = Embedding(
                    id=str(uuid.uuid4()),
                    endpoint_id=endpoint.id,
                    model=config.get_openai_model_embedding()
                )
                #endpoint.embeddings.append(embedding_record)

        session = SessionLocal()
        try:
            session.add(record_api)
            session.commit()
            logging.info(f"Saved record: {new_id}")
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Error saving API record: {e}")
            raise
        finally:
            session.close()
        return new_id


#if not mock_enable:
#    engine = create_engine(config.get_database_url(), echo=True, future=True)
#    Base.metadata.create_all(engine)
