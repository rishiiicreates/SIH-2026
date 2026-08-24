from pydantic import BaseModel, Field, field_validator

class RecommendRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000, description="Product description or procurement spec")
    top_k: int = Field(default=5, ge=1, le=20)

    @field_validator('query')
    @classmethod
    def validate_query(cls, v: str) -> str:
        trimmed = v.strip()
        if not trimmed:
            raise ValueError("Query string cannot be empty or whitespace.")
        return trimmed

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
