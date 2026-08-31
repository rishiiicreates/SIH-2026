import logging
from concurrent.futures import ThreadPoolExecutor
from fastapi import APIRouter, HTTPException
from app.models.schemas import RecommendRequest, RecommendResponse, StandardRecommendation, ReferenceItem, MetadataInfo
from app.services.retrieval import search
from app.services.reference_expand import get_references_batch
from app.services.metadata import get_metadata_batch

logger = logging.getLogger(__name__)
router = APIRouter()

# Reusable thread pool for parallel batch DB queries
_batch_executor = ThreadPoolExecutor(max_workers=8, thread_name_prefix="rec_batch")

@router.post("/recommend", response_model=RecommendResponse)
def recommend_standards(request: RecommendRequest):
    try:
        search_results = search(request.query, request.top_k)
    except RuntimeError as e:
        logger.error("Search failure for query '%s': %s", request.query, e)
        raise HTTPException(status_code=500, detail=str(e))

    if not search_results:
        return RecommendResponse(
            query=request.query,
            recommendations=[],
            total_results=0
        )

    # Collect all standard IDs from search results
    standard_ids = [res["standard_id"] for res in search_results]

    # Batch fetch concurrently using shared executor
    refs_future = _batch_executor.submit(get_references_batch, standard_ids)
    meta_future = _batch_executor.submit(get_metadata_batch, standard_ids)
    all_refs = refs_future.result()
    all_meta = meta_future.result()

    # Assemble response using pre-fetched data
    recommendations = []
    for res in search_results:
        standard_id = res["standard_id"]
        title = res["title"]
        similarity = res.get("similarity", 0.0)

        # References from batch result
        refs = all_refs.get(standard_id, [])
        reference_items = [
            ReferenceItem(
                referenced_id=r["referenced_id"],
                title=r.get("referenced_title"),
                relationship_type=r.get("relationship_type")
            ) for r in refs
        ]

        # Metadata from batch result
        meta = all_meta.get(standard_id)
        metadata_info = None
        if meta:
            metadata_info = MetadataInfo(
                latest_version=meta.get("latest_version"),
                amendment_date=meta.get("amendment_date"),
                is_mandatory_qco=meta.get("is_mandatory_qco", False)
            )

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
