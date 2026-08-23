from pydantic import BaseModel, Field

class RecommendRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Product description or procurement spec")
    top_k: int = Field(default=5, ge=1, le=20)

class ReferenceItem(BaseModel):
    referenced_id: str
    title: str | None = None
    relationship_type: str | None = None

class MetadataInfo(BaseModel):
    latest_version: str | None = None
    amendment_date: str | None = None
    is_mandatory_qco: bool = False

class StandardRecommendation(BaseModel):
    standard_id: str
    title: str
    similarity: float
    references: list[ReferenceItem] = []
    metadata: MetadataInfo | None = None

class RecommendResponse(BaseModel):
    query: str
    recommendations: list[StandardRecommendation]
    total_results: int
