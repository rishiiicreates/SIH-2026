# V1 File Structure — Raw Python (No LangChain/Framework)

```
sih-standards-engine/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   # FastAPI entrypoint — just starts the app, includes routers
│   │
│   │   ├── config.py
│   │   # env vars, embedding model name, DB connection string
│   │
│   │   ├── routers/
│   │   │   └── recommend.py
│   │   │   # POST /recommend — raw Python orchestration: calls retrieval → reference_expand → metadata in sequence, no LangGraph/agent needed since flow is linear
│   │
│   │   ├── services/
│   │   │   ├── retrieval.py
│   │   │   # CUSTOM RETRIEVER — calls embedding API directly, does cosine similarity / pgvector query yourself, no LangChain retriever object
│   │   │
│   │   │   ├── reference_expand.py
│   │   │   # plain SQL lookup: given a standard_id, fetch its normative references — not AI, just a join query
│   │   │
│   │   │   └── metadata.py
│   │   │   # plain lookup: version, amendment, QCO/certification flag — static fields, no reasoning
│   │
│   │   ├── models/
│   │   │   └── schemas.py
│   │   # Pydantic request/response shapes — kept even without a framework, since FastAPI needs these regardless
│   │
│   │   └── db/
│   │       └── client.py
│   │       # DB connection init (Supabase client or raw psycopg2 — your choice, doesn't affect structure)
│   │
│   ├── scripts/
│   │   └── ingest_standards.py
│   │   # one-time script: reads standards_seed.csv, generates embeddings yourself, writes to DB — run manually, not part of live app
│   │
│   ├── data/
│   │   └── standards_seed.csv
│   │   # your ~50-100 hand-curated standards: title, scope, references, version, QCO flag
│   │
│   ├── requirements.txt
│   │   # minimal: fastapi, uvicorn, psycopg2 or supabase-py, an embeddings SDK (e.g. openai) — no langchain
│   │
│   └── .env.example
│
├── frontend/
│   ├── app/
│   │   ├── page.tsx
│   │   # search box + results — single view, no nav for V1
│   │
│   │   └── layout.tsx
│   │
│   ├── components/
│   │   ├── SearchBar.tsx
│   │   ├── ResultCard.tsx
│   │   │   # IS number, title, version badge, QCO badge
│   │   └── ReferenceList.tsx
│   │       # flat expandable list of allied standards, not a graph viz
│   │
│   ├── lib/
│   │   └── api.ts
│   │   # calls your FastAPI /recommend endpoint
│   │
│   └── package.json
│
└── README.md
```

**Where this differs from a framework-based setup:** only `services/retrieval.py` and `scripts/ingest_standards.py` change internally — you write the embedding calls, similarity search, and any orchestration loops yourself instead of instantiating LangChain objects. Every other file's job stays identical. `routers/recommend.py` is plain sequential function calls (`result = retrieval.search(query)` → `refs = reference_expand.get(result.id)` → `meta = metadata.get(result.id)`) — no orchestration framework needed since there's no branching or state to manage yet.
