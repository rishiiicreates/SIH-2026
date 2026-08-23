"""
Stage 1: Semantic retrieval.

CUSTOM RETRIEVER — no LangChain/LlamaIndex. Calls the embedding API
directly and does similarity search by hand (cosine similarity, or a
pgvector query against Supabase).

This is the ONLY stage that should involve AI/model reasoning. See
ARCHITECTURE.md for why stages 2 and 3 are plain lookups instead.
"""

import json
import math
import urllib.error
import urllib.request

from app.config import EMBEDDING_API_KEY, EMBEDDING_API_URL, EMBEDDING_MODEL
from app.db.client import get_db


def cosine_similarity(v1: list[float], v2: list[float]) -> float:
    """Calculate cosine similarity between two vectors in pure Python."""
    if not v1 or not v2 or len(v1) != len(v2):
        return 0.0
    dot_product = sum(a * b for a, b in zip(v1, v2))
    norm_v1 = math.sqrt(sum(a * a for a in v1))
    norm_v2 = math.sqrt(sum(b * b for b in v2))
    if norm_v1 == 0.0 or norm_v2 == 0.0:
        return 0.0
    return dot_product / (norm_v1 * norm_v2)


def embed_text(text: str) -> list[float]:
    """
    Call the embedding API (e.g. BAAI/bge-m3 or OpenAI-compatible endpoint) directly
    and return the embedding vector.
    
    No framework wrapper (no LangChain/LlamaIndex) — uses standard HTTP request.
    """
    if not text.strip():
        raise ValueError("Cannot embed empty text.")

    # Determine endpoint: use custom URL or default Hugging Face Inference API
    if EMBEDDING_API_URL:
        endpoint = EMBEDDING_API_URL
    else:
        model_name = EMBEDDING_MODEL or "BAAI/bge-m3"
        endpoint = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_name}"

    headers = {
        "Content-Type": "application/json",
    }
    if EMBEDDING_API_KEY:
        headers["Authorization"] = f"Bearer {EMBEDDING_API_KEY}"

    payload = json.dumps({"inputs": text, "options": {"wait_for_model": True}}).encode("utf-8")
    req = urllib.request.Request(endpoint, data=payload, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
            
            # Handle HF feature-extraction output: either list[float] or list[list[float]]
            if isinstance(result, list):
                if result and isinstance(result[0], list):
                    return result[0]
                return result
            # Handle OpenAI-compatible response format: {"data": [{"embedding": [...]}]}
            elif isinstance(result, dict) and "data" in result and len(result["data"]) > 0:
                return result["data"][0]["embedding"]
            else:
                raise ValueError(f"Unexpected embedding response format: {result}")
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Embedding API HTTP error {e.code}: {error_body}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Failed to connect to embedding API: {e.reason}") from e


def search(query: str, top_k: int = 3) -> list[dict]:
    """
    Embed `query`, then vector-search against the standards table.

    Returns a list of dicts:
        [
            {"standard_id": "IS 694", "title": "...", "similarity_score": 0.87},
            ...
        ]

    Retrieval strategy:
      1. Generates embedding vector for query via embed_text().
      2. Attempts pgvector RPC `match_standards` via Supabase client.
      3. Fallback: fetches standards with embeddings and computes cosine similarity
         in pure Python if RPC is not configured.
    """
    query_vector = embed_text(query)
    supabase = get_db()

    # 1. Attempt Supabase pgvector RPC
    try:
        rpc_response = supabase.rpc(
            "match_standards",
            {
                "query_embedding": query_vector,
                "match_count": top_k,
            },
        ).execute()

        if rpc_response.data and len(rpc_response.data) > 0:
            return [
                {
                    "standard_id": item["standard_id"],
                    "title": item["title"],
                    "similarity_score": round(float(item.get("similarity", 0.0)), 4),
                }
                for item in rpc_response.data
            ]
    except Exception:
        # Fallback to direct table query if RPC is not present in Supabase
        pass

    # 2. Fallback: manual cosine similarity search over stored standards
    response = supabase.table("standards").select("standard_id, title, embedding").execute()
    records = response.data or []

    scored_records = []
    for record in records:
        emb = record.get("embedding")
        if not emb:
            continue
        # Handle stringified embeddings or list of floats
        if isinstance(emb, str):
            try:
                emb = json.loads(emb)
            except Exception:
                continue
        score = cosine_similarity(query_vector, emb)
        scored_records.append({
            "standard_id": record["standard_id"],
            "title": record.get("title", ""),
            "similarity_score": round(score, 4),
        })

    # Sort descending by similarity score and take top_k
    scored_records.sort(key=lambda x: x["similarity_score"], reverse=True)
    return scored_records[:top_k]

