from app.db.client import get_supabase

def get_references(standard_id: str) -> list[dict]:
    client = get_supabase()
    if client is None:
        raise RuntimeError("Supabase client is not initialized.")
    try:
        response = client.table("standard_references").select(
            "referenced_id, referenced_title, relationship_type"
        ).eq("standard_id", standard_id).execute()
        return response.data
    except Exception as e:
        raise RuntimeError(f"Failed to get references for {standard_id}: {e}")

