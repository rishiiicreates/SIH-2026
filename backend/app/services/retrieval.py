import logging
import math
from google import genai
from google.genai.errors import APIError
from postgrest.exceptions import APIError as PostgrestAPIError

from app.config import settings
from app.db.client import supabase, get_supabase

logger = logging.getLogger(__name__)

# Module-level singleton client for connection reuse
_genai_client = None

def _get_genai_client():
    global _genai_client
    if _genai_client is None:
        if not settings.GEMINI_API_KEY:
            raise RuntimeError("GEMINI_API_KEY is not set in environment.")
        _genai_client = genai.Client(api_key=settings.GEMINI_API_KEY)
    return _genai_client

def embed_text(text: str, max_retries: int = 3) -> list[float]:
    last_err = None
    for attempt in range(max_retries):
        try:
            client = _get_genai_client()
            response = client.models.embed_content(
                model=settings.EMBEDDING_MODEL,
                contents=text,
                config={"output_dimensionality": settings.EMBEDDING_DIMENSION},
            )
            return response.embeddings[0].values
        except Exception as e:
            last_err = e
            logger.warning("Gemini embedding attempt %d failed (%s). Retrying...", attempt + 1, e)
            global _genai_client
            _genai_client = None  # Reset client on error to reconnect
    
    logger.error("All %d Gemini embedding attempts failed: %s", max_retries, last_err)
    raise RuntimeError(f"Failed to generate embedding after {max_retries} attempts: {last_err}") from last_err



def _cosine_similarity(v1: list[float], v2: list[float]) -> float:
    dot_product = sum(a * b for a, b in zip(v1, v2))
    mag1 = math.sqrt(sum(a * a for a in v1))
    mag2 = math.sqrt(sum(b * b for b in v2))
    if mag1 == 0 or mag2 == 0:
        return 0.0
    return dot_product / (mag1 * mag2)

def search(query: str, top_k: int = settings.TOP_K_DEFAULT) -> list[dict]:
    client = get_supabase()
    if client is None:
        raise RuntimeError("Supabase client is not initialized. Check your SUPABASE_URL and SUPABASE_KEY.")

    query_embedding = embed_text(query)

    # Primary path: pgvector RPC match_standards
    try:
        response = client.rpc("match_standards", {
            "query_embedding": query_embedding,
            "match_count": top_k
        }).execute()
        if response.data and len(response.data) > 0:
            return response.data
    except Exception as rpc_err:
        logger.warning(
            "Supabase pgvector RPC 'match_standards' call failed or was unreachable (%s). Using Python in-memory cosine fallback.",
            rpc_err
        )

    # Fallback path: in-memory cosine similarity over standards table
    try:
        fresh_client = get_supabase()
        all_stds = fresh_client.table("standards").select("standard_id, title, embedding").execute()
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
        logger.error("Database search failed: %s", fallback_err)
        raise RuntimeError(f"Database search failed: {fallback_err}") from fallback_err


