from fastapi import APIRouter, HTTPException
from app.models.schemas import RecommendRequest, RecommendResponse, StandardRecommendation, ReferenceItem, MetadataInfo
from app.services.retrieval import search
from app.services.reference_expand import get_references
from app.services.metadata import get_metadata

router = APIRouter()

@router.post("/recommend", response_model=RecommendResponse)
def recommend_standards(request: RecommendRequest):
    try:
        search_results = search(request.query, request.top_k)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    recommendations = []
    for res in search_results:
        standard_id = res["standard_id"]
        title = res["title"]
        similarity = res.get("similarity", 0.0)
        
        try:
            refs = get_references(standard_id)
            reference_items = [
                ReferenceItem(
                    referenced_id=r["referenced_id"],
                    title=r.get("referenced_title"),
                    relationship_type=r.get("relationship_type")
                ) for r in refs
            ]
        except RuntimeError as e:
            print(f"Warning: {e}")
            reference_items = []

        try:
            meta = get_metadata(standard_id)
            if meta:
                metadata_info = MetadataInfo(
                    latest_version=meta.get("latest_version"),
                    amendment_date=meta.get("amendment_date"),
                    is_mandatory_qco=meta.get("is_mandatory_qco", False)
                )
            else:
                metadata_info = None
        except RuntimeError as e:
            print(f"Warning: {e}")
            metadata_info = None
            
        recommendations.append(
            StandardRecommendation(
                standard_id=standard_id,
                title=title,
                similarity=similarity,
                references=reference_items,
                metadata=metadata_info
            )
        )
        
    return RecommendResponse(
        query=request.query,
        recommendations=recommendations,
        total_results=len(recommendations)
    )
