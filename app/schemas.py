from pydantic import BaseModel
from typing import List

class QueryRequest(BaseModel):
    question: str
    top_k: int = 4

class SourceChunk(BaseModel):
    source: str
    page: int
    content: str

class QueryResponse(BaseModel):
    answer: str
    faithfulness_score: float
    is_grounded: bool
    sources: List[SourceChunk]
