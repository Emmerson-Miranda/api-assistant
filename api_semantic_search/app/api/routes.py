# API routes
from fastapi import FastAPI, HTTPException
from app.core import config
from app.models.search import SearchQuery, SearchResult
from app.models.dao import semantic_search
from typing import List
import logging


class SemanticSearchAPI:

    def __init__(self):
        self.title = "Semantic Search API"
        self.app = FastAPI(title=self.title)

        @self.app.on_event("startup")
        async def startup_event():
            logging.info(f"Starting up the '{self.title}' ...")
            config.print_config()

        @self.app.on_event("shutdown")
        async def shutdown_event():
            logging.info(f"Shutting down the '{self.title}' ...")
            config.print_config()

        @self.app.post("/search", response_model=List[SearchResult])
        async def search(query: SearchQuery):
            try:
                return semantic_search(query)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
