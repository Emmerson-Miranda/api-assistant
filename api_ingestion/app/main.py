# FastAPI entrypoint
from fastapi import FastAPI, HTTPException, Body
from app.models.dao import save
from app.core import config
import yaml
import json
import logging


logging.basicConfig(level=logging.INFO)

api_title = "Ingestion Service API"

app = FastAPI(title=api_title,
              description="Accepts raw OpenAPI specs (JSON/YAML), parses endpoints, and extracts semantic descriptions.", 
              version="1.0.0")


@app.on_event("startup")
async def startup_event():
    logging.info(f"Starting up the '{api_title}' ...")
    config.print_config()


@app.on_event("shutdown")
async def shutdown_event():
    logging.info(f"Shutting down the '{api_title}' ...")


@app.post("/upload")
async def upload_spec(raw_spec: str = Body(...)):
    try:
        logging.info("Processing new specification ...")  #
        try:
            spec = yaml.safe_load(raw_spec)
        except yaml.YAMLError as yerr:
            logging.error(f"YAML parsing error (trying JSON): {yerr}")
            spec = json.loads(raw_spec)

        if not isinstance(spec, dict):
            raise HTTPException(status_code=400, detail="Invalid spec format. Must be a JSON or YAML object.")

        record = save(raw_spec=raw_spec, spec=spec)
        return f"Spec processed successfully with ID: {record}"

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
