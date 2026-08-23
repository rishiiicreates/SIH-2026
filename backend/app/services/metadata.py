from app.db.client import supabase

def get_metadata(standard_id: str) -> dict | None:
    if supabase is None:
        raise RuntimeError("Supabase client is not initialized.")
    try:
        response = supabase.table("standards").select(
            "latest_version, amendment_date, is_mandatory_qco"
        ).eq("standard_id", standard_id).execute()
        
        # If no results, return None
        if not response.data:
            return None
            
        return response.data[0]
    except Exception as e:
        raise RuntimeError(f"Failed to get metadata for {standard_id}: {e}")
