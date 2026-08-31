import logging
from app.db.client import get_supabase

logger = logging.getLogger(__name__)

def get_references(standard_id: str) -> list[dict]:
    """Get normative references for a single standard."""
    try:
        client = get_supabase()
        if client is None:
            return []
        response = client.table("standard_references").select(
            "referenced_id, referenced_title, relationship_type"
        ).eq("standard_id", standard_id).execute()
        return response.data or []
    except Exception as e:
        logger.warning("Failed to get references for %s: %s", standard_id, e)
        return []

def get_references_batch(standard_ids: list[str]) -> dict[str, list[dict]]:
    """Get normative references for multiple standards in a single DB query."""
    if not standard_ids:
        return {}

    try:
        client = get_supabase()
        if client is None:
            return {sid: [] for sid in standard_ids}
        response = client.table("standard_references").select(
            "standard_id, referenced_id, referenced_title, relationship_type"
        ).in_("standard_id", standard_ids).execute()

        # Group by standard_id
        grouped: dict[str, list[dict]] = {sid: [] for sid in standard_ids}
        for row in (response.data or []):
            sid = row["standard_id"]
            if sid in grouped:
                grouped[sid].append({
                    "referenced_id": row["referenced_id"],
                    "referenced_title": row.get("referenced_title"),
                    "relationship_type": row.get("relationship_type"),
                })
        return grouped
    except Exception as e:
        logger.warning("Batch reference lookup failed: %s. Returning empty.", e)
        return {sid: [] for sid in standard_ids}
