"""
POST /recommend

Plain sequential orchestration — no LangGraph/agent framework. The
pipeline is linear (no branching, no state), so plain function calls
are correct here. See ARCHITECTURE.md + STACK.md for when that
might change (e.g. multi-item BoQ segmentation, backlog item #3).
"""

from fastapi import APIRouter

from app.models.schemas import RecommendRequest, RecommendResponse
from app.services import retrieval, reference_expand, metadata

router = APIRouter()


@router.post("/recommend", response_model=RecommendResponse)
def recommend(request: RecommendRequest) -> RecommendResponse:
    # Stage 1: semantic retrieval (AI)
    matches = retrieval.search(request.query, top_k=3)

    results = []
    for match in matches:
        standard_id = match["standard_id"]

        # Stage 2: reference expansion (lookup, not AI)
        references = reference_expand.get_references(standard_id)

        # Stage 3: metadata overlay (lookup, not AI)
        meta = metadata.get_metadata(standard_id)

        results.append({
            "standard_id": standard_id,
            "title": match["title"],
            "similarity_score": match["similarity_score"],
            "references": references,
            "metadata": meta,
        })

    return RecommendResponse(query=request.query, results=results)
