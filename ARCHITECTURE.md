# Architecture — PS 26108 BIS Standards Recommendation Engine

## 3-Stage Linear Pipeline

```
User Query (plain text) 
    → Stage 1: Retrieval (AI — semantic search)
    → Stage 2: Reference Expansion (deterministic — DB join)
    → Stage 3: Metadata Enrichment (deterministic — DB lookup)
    → Response
```

### Stage 1: Retrieval (AI)
- Embed the user's query via `gemini-embedding-001` (768-dim, MRL truncated)
- Search `standards` table via pgvector `match_standards()` RPC
- Fallback: Python cosine-similarity if RPC unavailable
- Returns top-K standards ranked by semantic similarity

### Stage 2: Reference Expansion (Deterministic)
- For each matched standard, query `standard_references` join table
- Returns normative references, test methods, allied standards, installation codes
- **No LLM involvement** — pure SQL join

### Stage 3: Metadata Enrichment (Deterministic)
- Single-row lookup against `standards` for each match
- Returns: latest version, amendment info, QCO mandatory status
- **No LLM involvement** — pure SQL lookup

## Database Schema

### `standards` table
| Column | Type | Description |
|--------|------|-------------|
| standard_id | text PK | e.g. "IS 694:2010" |
| title | text | Full standard title |
| scope | text | Keywords + description for embedding context |
| embedding | vector(768) | gemini-embedding-001 output |
| latest_version | text | Revision + reaffirmation info |
| amendment_date | text | Latest amendment reference |
| is_mandatory_qco | boolean | Whether QCO compliance is mandatory |

### `standard_references` join table
| Column | Type | Description |
|--------|------|-------------|
| standard_id | text FK | Parent standard |
| referenced_id | text | Referenced standard ID |
| referenced_title | text | Title of referenced standard |
| relationship_type | text | RAW_MATERIAL, TEST_METHOD, etc. |

### `match_standards()` RPC
pgvector similarity search function — takes a query embedding and match count,
returns standard_id, title, and cosine similarity score.

## What This Architecture Does NOT Include
- No Neo4j or graph database — Postgres join tables handle references
- No LangChain/LlamaIndex — raw Python + google-genai SDK
- No LLM reasoning for stages 2/3 — deterministic lookups only
- No Chrome extension / GeM integration (backlog item #7)
- No bulk BIS API (doesn't exist) — data is manually curated
