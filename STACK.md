# Technology Stack — PS 26108

## Confirmed Stack (V1)

| Layer | Technology | Status |
|-------|-----------|--------|
| **Backend** | Python 3.11+ / FastAPI | Confirmed |
| **Database** | Supabase (PostgreSQL + pgvector) | Confirmed |
| **Embeddings** | Gemini API — `gemini-embedding-001` (768-dim via MRL) | Confirmed |
| **Frontend** | Next.js (App Router) + TypeScript + Tailwind CSS | Confirmed |
| **Deploy (Frontend)** | Vercel | Confirmed |
| **Deploy (Backend)** | TBD (Railway / Render / Supabase Edge) | V1: localhost |

## Embedding Provider Decision

**Confirmed:** Gemini API (`gemini-embedding-001`)
- Free tier via `google-genai` SDK
- Single `GEMINI_API_KEY` env var
- 768-dimensional output (truncated via `output_dimensionality` parameter)
- Same API key serves future LLM calls if needed

**Superseded:** ~~BAAI/bge-m3 via Hugging Face hosted inference API~~
- Removed: `EMBEDDING_API_URL`, `EMBEDDING_API_KEY` env vars
- Removed: raw urllib calls to HF endpoint

## What We Do NOT Use
- ~~Neo4j~~ — Postgres join table for references
- ~~LangChain / LlamaIndex~~ — raw Python
- ~~ChromaDB / Qdrant / Milvus~~ — pgvector in Supabase
- ~~BM25 / Reciprocal Rank Fusion~~ — deferred to backlog
- ~~Hugging Face inference API~~ — superseded by Gemini

## Python Dependencies
```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.0
supabase>=2.0.0
google-genai>=1.0.0
python-dotenv>=1.0.0
```
