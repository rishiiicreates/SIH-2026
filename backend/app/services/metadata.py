import logging
from app.db.client import get_supabase

logger = logging.getLogger(__name__)

def get_metadata(standard_id: str) -> dict | None:
    """Get metadata for a single standard."""
    try:
        client = get_supabase()
        if client is None:
            return None
        response = client.table("standards").select(
            "standard_id, latest_version, amendment_date, is_mandatory_qco"
        ).eq("standard_id", standard_id).execute()

        if not response.data:
            return None
        return response.data[0]
    except Exception as e:
        logger.warning("Failed to get metadata for %s: %s", standard_id, e)
        return None

def get_metadata_batch(standard_ids: list[str]) -> dict[str, dict | None]:
    """Get metadata for multiple standards in a single DB query."""
    if not standard_ids:
        return {}

    try:
        client = get_supabase()
        if client is None:
            return {sid: None for sid in standard_ids}
        response = client.table("standards").select(
            "standard_id, latest_version, amendment_date, is_mandatory_qco"
        ).in_("standard_id", standard_ids).execute()

        # Index by standard_id
        result: dict[str, dict | None] = {sid: None for sid in standard_ids}
        for row in (response.data or []):
            result[row["standard_id"]] = {
                "latest_version": row.get("latest_version"),
                "amendment_date": row.get("amendment_date"),
                "is_mandatory_qco": row.get("is_mandatory_qco", False),
            }
        return result
    except Exception as e:
        logger.warning("Batch metadata lookup failed: %s. Returning empty.", e)
        return {sid: None for sid in standard_ids}
