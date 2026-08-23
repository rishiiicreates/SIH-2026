# GEMINI.md — Hard Rules for AI Assistants

Read these files in this order before touching code:
`PROBLEM_STATEMENT.md` → `ARCHITECTURE.md` → `STACK.md` → `DATA_SOURCES.md` → `ROADMAP.md`

## Hard Rules

### Architecture Constraints
- **No Neo4j / graph DB** — a Postgres join table (`standard_references`) handles reference lookups
- **No LangChain / LlamaIndex** — the retriever is hand-written raw Python
- **No ChromaDB / Qdrant / Milvus** — pgvector in Supabase

### Feature Boundaries
- **No Chrome extension / GeM integration** — backlog item #7, don't touch it
- **No multilingual support** — backlog item #5, deferred
- **No tender PDF upload/parsing** — backlog item #2

### Data Rules
- **No assuming a bulk BIS API/dataset exists** — it doesn't; data entry is manual
- **No fabricating IS numbers** — every `IS ####:YYYY` must be verified against bis.gov.in

### Technical Rules
- **Reference expansion and metadata are DETERMINISTIC LOOKUPS, not LLM reasoning** — 
  do not route stages 2/3 through Gemini or any model. Only stage 1 (retrieval) touches AI.
- **No silent `except Exception: pass`** — catch specific known failures, let everything else raise
- **No public/free inference API for embeddings** — Gemini API is the confirmed provider
  (`gemini-embedding-001`, `google-genai` SDK, single `GEMINI_API_KEY` env var)

### Embedding Provider
- **Confirmed:** `gemini-embedding-001` via `google-genai` SDK
- **Output dimension:** 768 (via `output_dimensionality` parameter; native is 3072)
- **Superseded:** ~~BAAI/bge-m3 via Hugging Face hosted inference~~ — do not use

### Code Quality
- Explicit error handling with specific exception types
- No unused imports or dead code
- Functions under 50 lines, files under 800 lines
- Type hints on all function signatures
