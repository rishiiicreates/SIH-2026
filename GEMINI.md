# Project Context — Read This First

This is an SIH 2026 hackathon project (PS 26108). Before suggesting any
architecture, feature, or code, read these files in the project root:

1. `PROBLEM_STATEMENT.md` — what we are actually being judged on
2. `ARCHITECTURE.md` — the pipeline design and why it's scoped this way
3. `STACK.md` — exact tech choices, including what NOT to suggest
4. `DATA_SOURCES.md` — where data comes from and its real constraints
5. `ROADMAP.md` — current build phase and the ordered backlog
6. `SCRAPING.md` — how BIS standards data and GeM tender samples are
   acquired, and the rules for both scrapers

## Hard rules for suggestions

- Do NOT suggest Neo4j, graph databases, or any new database engine.
  Reference lookups are solved with a join table in the existing
  Postgres/Supabase instance. This has already been evaluated and
  rejected — see ARCHITECTURE.md for the reasoning.
- Do NOT suggest LangChain, LlamaIndex, or any RAG framework for the
  retriever. The retriever is hand-written raw Python. See STACK.md.
- Do NOT suggest a Chrome extension, GeM portal integration, or any
  new frontend surface unless explicitly asked. These are backlog
  item #7 (lowest priority) — see ROADMAP.md.
- Do NOT assume a bulk BIS standards API or dataset exists. It does
  not. See DATA_SOURCES.md before suggesting any data-fetching code.
- Match whichever phase (V1 or a specific backlog item) is currently
  being worked on — check ROADMAP.md before proposing scope.
- Never silently catch-and-ignore an exception to "fall back" between
  two code paths (e.g. `except Exception: pass`). Catch only the
  specific known failure being handled; let anything else raise or
  log loudly. A silent wrong answer during judging is worse than a
  visible crash during development. See STACK.md.
- Do NOT default to a public/free inference API (e.g. Hugging Face's
  hosted inference endpoint) for embeddings without it being
  explicitly confirmed first — see STACK.md's embedding model section.
- Do NOT build one generic scraper for both BIS standards and GeM
  tenders — they're different targets with different shapes and
  purposes. See SCRAPING.md.

The team is 6 people, all working from this same context. Consistency
across suggestions matters more than any single clever idea.
