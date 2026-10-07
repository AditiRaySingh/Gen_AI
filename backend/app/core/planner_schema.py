from pydantic import BaseModel, Field
from typing import Optional, List


class QueryPlan(BaseModel):
    metric: str
    dimensions: List[str] = Field(default_factory=list)
    filters: List[dict] = Field(default_factory=list)
    operation: str
    limit: Optional[int] = None
    comparison: Optional[str] = None