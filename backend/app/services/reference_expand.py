from app.db.client import supabase

def get_references(standard_id: str) -> list[dict]:
    if supabase is None:
        raise RuntimeError("Supabase client is not initialized.")
    try:
        response = supabase.table("standard_references").select(
            "referenced_id, referenced_title, relationship_type"
        ).eq("standard_id", standard_id).execute()
        return response.data
    except Exception as e:
        raise RuntimeError(f"Failed to get references for {standard_id}: {e}")
