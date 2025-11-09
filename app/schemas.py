from pydantic import BaseModel, Field
from typing import List

class RecommendRequest(BaseModel):
    query: str = Field(..., description="Natural language query or JD text. If URL, prefix with http(s)://")
    k: int = Field(10, ge=1, le=10)

class Recommendation(BaseModel):
    name: str
    url: str
    test_type: str
    score: float

class RecommendResponse(BaseModel):
    recommendations: List[Recommendation]
