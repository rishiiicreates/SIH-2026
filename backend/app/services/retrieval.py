import logging
import math
from google import genai
from google.genai.errors import APIError
from postgrest.exceptions import APIError as PostgrestAPIError

from app.config import settings
from app.db.client import supabase

logger = logging.getLogger(__name__)

def embed_text(text: str) -> list[float]:
    if not settings.GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is not set in environment.")
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    try:
        response = client.models.embed_content(
            model=settings.EMBEDDING_MODEL,
            contents=text,
            config={"output_dimensionality": settings.EMBEDDING_DIMENSION},
        )
        return response.embeddings[0].values
    except APIError as e:
        logger.error("Gemini embedding API call failed: %s", e)
        raise RuntimeError(f"Failed to generate embedding: {e}") from e

def _cosine_similarity(v1: list[float], v2: list[float]) -> float:
    dot_product = sum(a * b for a, b in zip(v1, v2))
    mag1 = math.sqrt(sum(a * a for a in v1))
    mag2 = math.sqrt(sum(b * b for b in v2))
    if mag1 == 0 or mag2 == 0:
        return 0.0
    return dot_product / (mag1 * mag2)

def search(query: str, top_k: int = settings.TOP_K_DEFAULT) -> list[dict]:
    if supabase is None:
        raise RuntimeError("Supabase client is not initialized. Check your SUPABASE_URL and SUPABASE_KEY.")

    query_embedding = embed_text(query)

    # Primary path: pgvector RPC match_standards
    try:
        response = supabase.rpc("match_standards", {
            "query_embedding": query_embedding,
            "match_count": top_k
        }).execute()
        return response.data
    except PostgrestAPIError as rpc_err:
        logger.warning(
            "Supabase pgvector RPC 'match_standards' failed (%s). Falling back to Python in-memory cosine similarity.",
            rpc_err
        )
    except Exception as unexpected_err:
        logger.error("Unexpected error executing RPC match_standards: %s", unexpected_err)
        raise RuntimeError(f"Database vector RPC execution failed: {unexpected_err}") from unexpected_err

    # Fallback path: in-memory cosine similarity over standards table
    try:
        all_stds = supabase.table("standards").select("standard_id, title, embedding").execute()
        results = []
        for row in all_stds.data:
            if not row.get("embedding"):
                continue
            sim = _cosine_similarity(query_embedding, row["embedding"])
            results.append({
                "standard_id": row["standard_id"],
                "title": row["title"],
                "similarity": sim
            })
        
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]
    except Exception as fallback_err:
        logger.error("Python cosine similarity fallback also failed: %s", fallback_err)
        raise RuntimeError(f"Database fallback search failed: {fallback_err}") from fallback_err

