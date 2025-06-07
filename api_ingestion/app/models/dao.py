# Vector storage logic (PgVector)
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from app.core import config
from app.db.domain_simplified import API
from app.services.embeddings import generate_embedding
import logging


logging.basicConfig(level=logging.INFO)

Base = declarative_base()

mock_enable = config.get_database_mock_enable()


if not mock_enable:
    engine = create_engine(config.get_database_url(), echo=True, future=True)
    SessionLocal = sessionmaker(bind=engine)


def save(raw_spec: str, spec: dict) -> str:
    logging.info(f"Database mock enable: {mock_enable}")
    new_id = str(uuid.uuid4())
    mdl = config.get_openai_model_embedding()
    embedding = generate_embedding(text=raw_spec, model=mdl)
    record_api = API(
        id=new_id,
        title=spec['info']['title'],
        version=spec['info']['version'],
        embedding=embedding,
        model=mdl,
        spec=spec
    )
    logging.info(f"Saving record: {new_id}")

    if mock_enable:
        # Mock implementation, no database interaction
        return new_id
    else:
        _save(record_api)
        return new_id


def _save(db_record):
    session = SessionLocal()
    new_id = db_record.id
    try:
        session.add(db_record)
        session.commit()
        logging.info(f"Record saved: {new_id}")
    except SQLAlchemyError as e:
        session.rollback()
        logging.error(f"Error saving record: {new_id}")
        raise e
    finally:
        session.close()

# if not mock_enable:
#    engine = create_engine(config.get_database_url(), echo=True, future=True)
#    Base.metadata.create_all(engine)
