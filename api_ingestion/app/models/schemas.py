# Pydantic models
from pydantic import BaseModel
from typing import Dict, Any


class SpecIn(BaseModel):
    spec: Dict[str, Any]
