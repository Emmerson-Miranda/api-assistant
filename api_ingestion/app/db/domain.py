# Vector storage logic (PgVector)
import json
import uuid
from sqlalchemy import Column, String, Text, ForeignKey, JSON, DateTime
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector


Base = declarative_base()


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
    part = Column(String, nullable=False)  # e.g., 'text', 'title', 'description'
    created_at = Column(DateTime, server_default=func.now())
    embedding = Column(Vector(1536), nullable=False)  # 1536 = OpenAI ada-002 output

    endpoint = relationship("APIEndpoint", back_populates="embeddings")

    def __repr__(self):
        return json.dumps({
            "id": self.id,
            "endpoint_id": self.endpoint_id,
            "model": self.model,
            "created_at": str(self.created_at)
        })
