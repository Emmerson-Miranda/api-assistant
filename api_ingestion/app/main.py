# FastAPI entrypoint
from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel

from app.db.pgvector import get_db, save_embedding
from app.core.embeddings import generate_embedding
from app.models.schemas import SpecIn
from app.core import config
import logging


logging.basicConfig(level=logging.INFO)

app = FastAPI()

@app.post("/upload")
async def upload_spec(spec: SpecIn):
    try:
        raw_text = str(spec.spec)  # flatten the OpenAPI spec
        logging.info(f"Received spec: {raw_text[:100]}...")  # Log the first 100 characters for debugging
        embedding = generate_embedding(text=raw_text, model=config.get_openai_model_embedding())
        save_embedding(embedding=embedding, spec=spec)
        return {"message": "Uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
