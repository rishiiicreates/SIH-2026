# Tech Stack

## Backend

- **FastAPI** — API framework
- **Raw Python retriever — NO LangChain, NO LlamaIndex.**
  `services/retrieval.py` calls the embedding API directly and does
  similarity search (cosine similarity, or a pgvector query) by hand.
  This is a deliberate choice, not a temporary gap — do not suggest
  wrapping this in a framework retriever object.
- **Supabase / Postgres + pgvector** — storage for standards data,
  reference join table, and vector search
- **Orchestration**: plain sequential function calls in
  `routers/recommend.py` (`retrieval.search()` →
  `reference_expand.get()` → `metadata.get()`). No LangGraph, no
  agent framework — the pipeline is linear with no branching or
  state to manage.

### When LangGraph might become justified

Only if a future stage becomes genuinely agentic — i.e., involves
conditional branching, retries, or multi-step state (a candidate
example: multi-item BoQ segmentation that dynamically decides how
many products are in a document and loops with retry logic). Plain
linear retrieval is not that. Don't reach for orchestration tooling
until an actual branch/loop/state need appears in the code.

## Frontend

- **Next.js**
- Deployed on **Vercel**

## Deployment

- Backend + DB: **Railway** (simpler setup than Oracle Cloud's free
  tier for a hackathon timeline — Oracle requires more VM
  configuration for no added benefit at this scale)
- Frontend: **Vercel**

## Embedding model + LLM — CONFIRMED: Gemini API, FREE TIER

Both embeddings and any LLM calls (e.g. future BoQ segmentation, query
normalization) go through the **same provider** — Gemini API, via a
Google AI Studio API key on the **free tier**. No paid/billed usage.
One account, one SDK, one thing to configure.

- **Embedding model**: `gemini-embedding-001` (GA, text-only) via the
  `embed_content` endpoint. Available on the free tier with a
  generous quota (far beyond what a 100-500 row corpus + demo-time
  queries will use). This is the model `embed_text()` in
  `retrieval.py` must call — no Hugging Face, no other provider,
  no silent fallback.
- **LLM model** (if/when needed, e.g. multi-item segmentation, query
  normalization): **Gemini 2.5 Flash-Lite** or **2.0 Flash-Lite** —
  the free tier's highest-headroom text models (more RPD/TPM than
  Pro or standard Flash), and more than capable for segmentation/
  normalization tasks, which don't need heavy reasoning. Pin the
  exact stable model string when this is actually built, not
  `-latest`, so behavior doesn't shift under the team mid-project.
- **SDK**: `google-genai` Python package (`from google import genai`)
- **API key**: stored as an env var (`GEMINI_API_KEY`), loaded via
  `config.py` — same pattern as `SUPABASE_URL`/`SUPABASE_KEY`.
- **Free tier limits are per-project, not per-key** — if the team
  hits rate limits during heavy testing (e.g. everyone re-running
  ingestion at once), it's a shared quota. Stagger bulk operations
  (like re-embedding the whole corpus) rather than running them
  simultaneously across teammates.

Old guidance below (bge-m3, HF inference API, self-hosting) is
superseded — kept only as a record of what was considered and
rejected.

<details>
<summary>Superseded: earlier embedding model notes</summary>

"bge-m3 (or equivalent)" was left vague earlier, and Gemini
defaulted to Hugging Face's public inference API — which is often
rate-limited, slow, or has the model unloaded, and is not something
we want failing mid-demo. This is why the model is now locked in
explicitly above instead of left as "or equivalent."

</details>

## Error handling — general rule

Never write `except Exception: pass` (or any bare catch-and-ignore)
to "fall back" between two code paths. This hides real failures
(bad API key, network drop, malformed data) behind a fallback that
looks like it worked. Instead:
- Catch only the specific, known failure you're handling (e.g. "this
  RPC function doesn't exist yet in Supabase")
- Log or raise anything else — a loud failure during development is
  recoverable; a silent wrong answer during judging is not

## Retrieval scaling threshold

V1's fallback search path (fetch all standards, compute cosine
similarity in Python) is fine up to roughly 200-300 rows. Past that,
it becomes an unnoticed full-table-scan slowdown. Once the corpus
crosses that size (expected around backlog item #1), the Supabase
`match_standards` pgvector RPC function must actually exist and be
the primary path, not an optional one.

## Explicitly out of scope for now

- LangChain / LlamaIndex — see above
- Neo4j or any graph database — see ARCHITECTURE.md
- Any local/offline embedding infra for V1 — see ARCHITECTURE.md's
  demo resilience section
