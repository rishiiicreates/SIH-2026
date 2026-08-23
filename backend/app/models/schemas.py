"""Request/response shapes for the /recommend endpoint."""

from pydantic import BaseModel


class RecommendRequest(BaseModel):
    query: str  # raw product/spec description, plain text for V1


class ReferencedStandard(BaseModel):
    standard_id: str      # e.g. "IS 694"
    title: str


class StandardMetadata(BaseModel):
    latest_version: str        # e.g. "IS 694:2010"
    amendment_date: str | None = None
    is_mandatory_qco: bool


class RecommendedStandard(BaseModel):
    standard_id: str
    title: str
    similarity_score: float           # from retrieval.py, stage 1
    references: list[ReferencedStandard]   # from reference_expand.py, stage 2
    metadata: StandardMetadata             # from metadata.py, stage 3


class RecommendResponse(BaseModel):
    query: str
    results: list[RecommendedStandard]
