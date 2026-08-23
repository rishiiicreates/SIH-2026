# Architecture

## The core insight

This problem is three small, distinct problems, not one big AI system:

1. **Semantic retrieval** — text query → correct IS number(s). This is
   the only part that genuinely needs AI/embeddings.
2. **Dependency resolution** — "this standard requires these other
   standards too." This is a **structured lookup problem**, because
   every IS document lists its normative references explicitly in its
   front matter. It is NOT something an LLM should infer or reason
   about — that risks confidently wrong answers in a compliance
   domain where wrong answers matter more than in a chatbot.
3. **Metadata overlay** — version, amendment status, mandatory
   certification (QCO/CRS/Hallmarking). Also structured data, not AI.

**Design rule: keep AI scoped to stage 1 only.** Everything else is
deterministic lookup. This is the single most important architectural
decision in this project — do not let it drift.

## Pipeline (4 stages)

```
Input → Retrieval (AI) → Reference Expansion (lookup) → Metadata (lookup) → Output
```

1. **Input normalization** — whatever comes in (raw text, PDF, BoQ
   Excel row) gets reduced to clean text describing a product/spec.
   Extraction only, no intelligence needed here.
2. **Semantic retrieval** — embed the clean text, vector-search
   against the standards corpus (title + scope embedded), return
   top-k candidates. This is where "semantic not keyword" (PS feature
   #2) actually happens.
3. **Reference expansion** — take the top match's IS number, look up
   its stored reference list in a flat join table
   (`standard_id → referenced_standard_id`). Satisfies PS feature #3.
4. **Metadata overlay** — attach latest version/amendment (PS feature
   #4) and QCO/mandatory-certification flag (PS feature #5) from
   stored fields.

Orchestration across these stages is plain sequential Python function
calls in `routers/recommend.py` — no agent framework, because the
flow is linear with no branching or state. See STACK.md for when that
might change.

## Why NOT a graph database (Neo4j)

This gets suggested often because "standards reference other
standards" sounds like a graph problem. It technically is a graph,
but the graph's *shape* doesn't need graph-database machinery:

- Low node count (hundreds to low-thousands of standards)
- Low edge count (a handful of references per standard)
- Low query depth (1-3 hop lookups: "what does X reference" / "what
  references X")
- Low write frequency (updates on amendment, roughly yearly)

Postgres handles this natively with a join table and, if needed,
`WITH RECURSIVE` for multi-hop traversal. Adding Neo4j would mean: a
second database to keep in sync, a second query language (Cypher) for
the team to learn, and a second deployment target — all for zero
functional gain at this scale. Graph databases earn their place at
millions of nodes or genuine multi-hop pathfinding/graph-algorithm
needs. We have neither.

**Revisit only if:** by the December finale, we hit an actual query
pattern Postgres can't express well. Stay open, don't be dogmatic —
but the default is no.

## Why NOT a Chrome extension / GeM integration (for now)

A browser extension changes *where* the UI renders (inside
gem.gov.in's DOM) — it doesn't add any new intelligence or capability
over our own web UI. It's a distribution feature, not a
problem-solving feature, and it's fragile because we don't control
that DOM (a GeM site update can break it anytime).

This is backlog item #7 (lowest priority) — only worth doing once
core backend richness (items 1-6) is done, and only if judges at the
internal round specifically signal that live-portal integration
matters for the finale.

## Definition of "over-engineered" for this project

Not "harder than the team can currently do" — the team can learn
anything given enough time. Over-engineered means: **solving a
problem the current tool already solves, with a new tool, for no
capability gain** — or building infrastructure ahead of proven data
and logic. The biggest real risk isn't Neo4j specifically, it's
building any impressive-looking shell (extension, graph DB,
multi-agent orchestration) before the core loop — real data in, real
recommendation out — is proven end to end.

## Demo resilience (not the same as "offline mode")

The stack (FastAPI + Supabase + Vercel) is fully internet-dependent
by design — that's correct and doesn't need to change. Wifi risk
during judging is solved with a fallback, not offline architecture:

- A recorded video/GIF walkthrough of the working prototype as backup
- Optionally, a tiny local demo mode with 5-10 hardcoded results
  runnable via `localhost`, no live DB call needed

Building true offline capability (bundled vector DB, local embedding
model) is real effort for a risk a recorded backup already solves.
Skip it for V1; only revisit if the Dec "offline Docker image"
backlog item becomes relevant.
