from google import genai
from google.genai.errors import APIError
from app.config import settings
from app.db.client import supabase
import math

def embed_text(text: str) -> list[float]:
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    try:
        response = client.models.embed_content(
            model=settings.EMBEDDING_MODEL,
            contents=text,
            config={"output_dimensionality": settings.EMBEDDING_DIMENSION},
        )
        return response.embeddings[0].values
    except APIError as e:
        raise RuntimeError(f"Failed to generate embedding: {e}")

def search(query: str, top_k: int = settings.TOP_K_DEFAULT) -> list[dict]:
    query_embedding = embed_text(query)

    # Try Supabase RPC first
    try:
        if supabase is None:
            raise RuntimeError("Supabase client is not initialized.")
        response = supabase.rpc("match_standards", {
            "query_embedding": query_embedding,
            "match_count": top_k
        }).execute()
        return response.data
    except Exception as e:
        # Fallback to python cosine similarity
        try:
            all_stds = supabase.table("standards").select("standard_id, title, embedding").execute()
            
            def cosine_similarity(v1, v2):
                dot_product = sum(a * b for a, b in zip(v1, v2))
                mag1 = math.sqrt(sum(a * a for a in v1))
                mag2 = math.sqrt(sum(b * b for b in v2))
                if mag1 == 0 or mag2 == 0:
                    return 0.0
                return dot_product / (mag1 * mag2)

            results = []
            for row in all_stds.data:
                if not row.get("embedding"):
                    continue
                sim = cosine_similarity(query_embedding, row["embedding"])
                results.append({
                    "standard_id": row["standard_id"],
                    "title": row["title"],
                    "similarity": sim
                })
            
            results.sort(key=lambda x: x["similarity"], reverse=True)
            return results[:top_k]

        except Exception as inner_e:
            raise RuntimeError(f"Database search failed: RPC error: {e}, Fallback error: {inner_e}")
