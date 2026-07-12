from pydantic import BaseModel


class QueryRequest(BaseModel):
    query: str


class SummaryRequest(BaseModel):
    query: str