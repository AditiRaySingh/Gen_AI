from pydantic import BaseModel
from typing import Any


class QueryResponse(BaseModel):
    query: str
    generated_logic: dict
    result: Any
    confidence_score: float
    explanation: str