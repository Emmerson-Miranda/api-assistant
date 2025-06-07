# Vector storage logic (PgVector)
import json
import uuid
from sqlalchemy import Column, String, JSON, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector


Base = declarative_base()


class API(Base):
    __tablename__ = "apis"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    version = Column(String, nullable=False)
    spec = Column(JSON, nullable=False)
    embedding = Column(Vector(1536), nullable=False)  # 1536 = OpenAI ada-002 output
    model = Column(String, nullable=False)  # e.g., text-embedding-ada-002
    uploaded_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return json.dumps({
            "id": self.id,
            "title": self.title,
            "version": self.version,
            "model": self.model,
            "uploaded_at": str(self.uploaded_at)
        })
