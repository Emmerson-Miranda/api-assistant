# FastAPI entrypoint
from app.api.routes import SemanticSearchAPI
import logging


logging.basicConfig(level=logging.INFO)

semantic_api = SemanticSearchAPI()
app = semantic_api.app
