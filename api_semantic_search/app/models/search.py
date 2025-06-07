from pydantic import BaseModel


class SearchQuery(BaseModel):
    query: str


class SearchResult(BaseModel):
    endpoint_id: str
    path: str
    summary: str
