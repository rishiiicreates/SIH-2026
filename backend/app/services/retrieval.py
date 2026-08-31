import json
import logging
import math
import threading
from collections import OrderedDict
from google import genai
from google.genai.errors import APIError
from postgrest.exceptions import APIError as PostgrestAPIError

from app.config import settings
from app.db.client import get_supabase

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

# Thread-safe LRU cache: same query text → same embedding vector (deterministic model)
_embedding_cache: OrderedDict[str, list[float]] = OrderedDict()
_cache_lock = threading.Lock()
MAX_CACHE_SIZE = 200

def embed_text(text: str, max_retries: int = 3) -> list[float]:
    """Embed text with Gemini, using an in-memory cache for repeated queries."""
    cache_key = text.strip().lower()
    with _cache_lock:
        if cache_key in _embedding_cache:
            _embedding_cache.move_to_end(cache_key)
            logger.debug("Embedding cache hit for: %s", text[:50])
            return _embedding_cache[cache_key]

    last_err = None
    for attempt in range(max_retries):
        try:
            client = _get_genai_client()
            model_name = settings.EMBEDDING_MODEL if settings.EMBEDDING_MODEL.startswith("models/") else f"models/{settings.EMBEDDING_MODEL}"
            response = client.models.embed_content(
                model=model_name,
                contents=text,
                config={"output_dimensionality": settings.EMBEDDING_DIMENSION},
            )
            embedding = response.embeddings[0].values

            # Store in cache (evict oldest if full)
            with _cache_lock:
                if len(_embedding_cache) >= MAX_CACHE_SIZE:
                    _embedding_cache.popitem(last=False)
                _embedding_cache[cache_key] = embedding

            return embedding
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
            "Supabase pgvector RPC 'match_standards' failed (%s). Using in-memory cosine fallback.",
            rpc_err
        )

    # Fallback path: in-memory cosine similarity
    try:
        all_stds = client.table("standards").select("standard_id, title, embedding").execute()
        results = []
        for row in all_stds.data:
            emb = row.get("embedding")
            if not emb:
                continue
            if isinstance(emb, str):
                try:
                    emb = json.loads(emb)
                except Exception:
                    continue
            sim = _cosine_similarity(query_embedding, emb)
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


def warmup():
    """Pre-warm Gemini client and Supabase connection at startup."""
    try:
        logger.info("Warming up Gemini embedding client...")
        embed_text("warmup query")
        logger.info("Warmup complete — Gemini client ready")
    except Exception as e:
        logger.warning("Gemini warmup failed (non-fatal): %s", e)

    try:
        logger.info("Warming up Supabase client connection...")
        client = get_supabase()
        if client:
            client.table("standards").select("standard_id").limit(1).execute()
            logger.info("Supabase warmup complete")
    except Exception as e:
        logger.warning("Supabase warmup failed (non-fatal): %s", e)
