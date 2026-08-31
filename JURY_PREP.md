# 🛡️ MANAK (PS 26108) — Jury Defense & Technical Master Guide
> **Team:** Big Potato · **Lead:** Rishi · **Theme:** Smart Automation / Public Procurement  
> **Problem Statement ID:** PS 26108 (Ministry of Consumer Affairs, Food & Public Distribution / DoCA / BIS)  
> **Core Stack:** FastAPI + PostgreSQL (pgvector via Supabase) + Gemini API (`gemini-embedding-001`) + Next.js 14 / React

---

## 🗺️ Phase 1 — Repository Map & Architecture Trace

### 1. Repository Inventory (File-by-File Responsibility)

```
bis-standards-recommendation-engine/
├── ARCHITECTURE.md                  # Detailed technical architecture, pipeline specs, and ERD
├── DATA_SOURCES.md                  # Documentation of BIS data curation methods and seed datasets
├── GEMINI.md                        # AI assistant hard rules and architectural constraints
├── PROBLEM_STATEMENT.md             # Official SIH PS 26108 statement and scoring checklist
├── PS_26108_BIS_Standards_Procurement_Master_Blueprint.md # Extended roadmap vision and system concept
├── README.md                        # Project overview, installation instructions, and quickstart guide
├── ROADMAP.md                       # Timeline milestones (Aug 26 PPT -> Sep 1 V1 -> Dec 2026 Finale) & Backlog
├── SCRAPING.md                      # Guide and notes on BIS web portal structure and scraping strategy
├── STACK.md                         # V1 confirmed stack choices vs. explicitly rejected technologies
├── docker-compose.yml               # Multi-container orchestration (backend + frontend)
├── file_structure.md                # Quick reference map of repo directory tree
├── supabase_schema.sql              # Master PostgreSQL schema DDL (pgvector, tables, match RPC, RLS)
│
├── backend/
│   ├── Dockerfile                   # Production Python 3.11 container image definition
│   ├── README.md                    # Backend setup, virtual environment, and API documentation
│   ├── requirements.txt             # Minimal locked Python dependencies (FastAPI, uvicorn, supabase, google-genai)
│   ├── app/
│   │   ├── __init__.py              # App package marker
│   │   ├── main.py                  # FastAPI application entrypoint with lifespan warmup hook and CORS
│   │   ├── config.py                # Environment configuration loader (Settings singleton)
│   │   ├── db/
│   │   │   ├── __init__.py          # DB package marker
│   │   │   ├── client.py            # Singleton Supabase client with fail-fast credential validation
│   │   │   └── schema.sql           # Backend local copy of database DDL
│   │   ├── models/
│   │   │   ├── __init__.py          # Models package marker
│   │   │   └── schemas.py           # Pydantic v2 domain schemas (RecommendRequest, Response, Validation)
│   │   ├── routers/
│   │   │   ├── __init__.py          # Routers package marker
│   │   │   └── recommend.py         # /api/v1/recommend endpoint with concurrent ThreadPoolExecutor enrichment
│   │   └── services/
│   │       ├── __init__.py          # Services package marker
│   │       ├── retrieval.py         # Stage 1: Gemini 768-dim MRL embeddings + Supabase pgvector cosine search
│   │       ├── reference_expand.py  # Stage 2: Deterministic batch SQL join for normative & allied references
│   │       └── metadata.py          # Stage 3: Deterministic batch SQL lookup for QCO status & version info
│   └── scripts/
│       ├── ingest_standards.py      # ETL pipeline: Embeds catalog and seeds Supabase tables
│       └── evaluate_benchmarks.py   # Automated benchmark evaluation harness over 4 real-world public tenders
│
├── frontend/
│   ├── Dockerfile                   # Production Node.js 18 container image definition
│   ├── package.json                 # Frontend dependencies (Next.js 14, React 18, Tailwind, Lucide)
│   ├── tsconfig.json                # TypeScript compiler configuration
│   ├── tailwind.config.ts           # Custom Tailwind design tokens (BIS blue #0b2545, saffron #ff9933)
│   ├── next.config.mjs              # Next.js build and runtime configuration
│   ├── postcss.config.mjs           # PostCSS Tailwind preprocessing configuration
│   ├── app/
│   │   ├── layout.tsx               # Root HTML layout, font setup, and header metadata
│   │   ├── page.tsx                 # Main search dashboard with skeleton loading, errors, and empty states
│   │   └── globals.css              # Global styles and Tailwind utility classes
│   ├── components/
│   │   ├── SearchBar.tsx            # Interactive query input with 1-click sample prompt chips
│   │   ├── ResultCard.tsx           # Standard result card showing match %, QCO statutory badge, and version
│   │   └── ReferenceList.tsx        # Expandable accordion rendering categorized normative references
│   ├── lib/
│   │   └── api.ts                   # Fetch API client wrapper with 15-second AbortController timeout
│   └── types/
│       └── index.ts                 # TypeScript domain interfaces (Recommendation, Reference, Metadata)
│
└── data/
    ├── indian_standards_master_catalog.json # 11 hand-verified primary standards with references & QCO data
    ├── bis_mandatory_qco_scheme1.json       # 752 official Scheme-I (ISI Mark) mandatory QCO records
    ├── bis_mandatory_crs_scheme2.json       # 30 official Scheme-II (CRS) mandatory electronics/IT records
    ├── bis_normative_graph_triples.json     # 53 relational graph edges across standards
    └── sample_procurement_tenders_eval.json # 4 labeled real-world benchmark evaluation tenders
```

---

### 2. Request-Flow Architecture Narrative

Here is the exact step-by-step path of a user request from browser keystroke to rendered response:

```
[User Browser]
      │ 1. User enters spec (or clicks chip) -> "5 HP submersible agricultural pump"
      ▼
[frontend/app/page.tsx: handleSearch()]
      │ 2. Sets isLoading=true, calls fetchRecommendations()
      ▼
[frontend/lib/api.ts: fetchRecommendations()]
      │ 3. Instantiates AbortController (15s timeout), sends POST to http://localhost:8000/api/v1/recommend
      ▼
[backend/app/main.py: CORS Middleware]
      │ 4. Verifies CORS headers (allow_origins=["*"], credentials=False)
      ▼
[backend/app/routers/recommend.py: recommend_standards()]
      │ 5. Pydantic validator (RecommendRequest) trims whitespace and enforces 1 <= len <= 2000
      ▼
[backend/app/services/retrieval.py: search()]
      │ 6. Checks in-memory LRU embedding cache (_embedding_cache, cap 200)
      │    • Cache Hit -> immediate 768-dim vector
      │    • Cache Miss -> calls Google Gemini API (gemini-embedding-001 with output_dimensionality=768)
      │ 7. Calls Supabase RPC `match_standards(query_embedding, top_k)`
      │    • Primary: Executes cosine distance `1 - (embedding <=> query_embedding)` in PostgreSQL via pgvector
      │    • Fallback (if RPC unreachable): In-memory cosine similarity computation over fetched standard vectors
      │ 8. Returns Top-K primary standard candidates: [standard_id, title, similarity]
      ▼
[backend/app/routers/recommend.py: ThreadPoolExecutor(max_workers=2)]
      │ 9. Extracts candidate IDs (e.g., ['IS 14220:2018', 'IS 778:1984'])
      │ 10. Concurrently executes 2 batch SQL queries (eliminating N+1 overhead):
      │     ├── Task A [reference_expand.py]: SELECT FROM standard_references WHERE standard_id IN (...)
      │     └── Task B [metadata.py]: SELECT FROM standards WHERE standard_id IN (...)
      │ 11. Assembles Pydantic RecommendResponse with populated references and QCO/version metadata
      ▼
[frontend/app/page.tsx]
      │ 12. Receives JSON payload -> sets data state, isLoading=false
      ▼
[frontend/components/ResultCard.tsx & ReferenceList.tsx]
      │ 13. Renders:
      │     • Match Percentage Chip (e.g. "86% Match")
      │     • QCO Statutory Compliance Badge ("QCO Mandatory" vs "No QCO")
      │     • Latest Published Version & Reaffirmation Year
      │     • Interactive Accordion with Color-Coded Normative Reference Badges (RAW_MATERIAL, TEST_METHOD, etc.)
```

---

### 3. Load-Bearing Logic vs. Scaffolding & Boilerplate

| Component / File | Classification | Exact Role & Logic Weight |
|---|---|---|
| `backend/app/services/retrieval.py` | **Load-Bearing** | Stage 1 Core: Gemini API integration, MRL 768-dim vector extraction, LRU vector cache, Supabase pgvector RPC, and in-memory cosine fallback. |
| `backend/app/services/reference_expand.py` | **Load-Bearing** | Stage 2 Core: Batch relational expansion of normative references, test methods, and allied codes via single SQL `IN` query. |
| `backend/app/services/metadata.py` | **Load-Bearing** | Stage 3 Core: Batch statutory metadata retrieval (QCO flag, latest revision, amendment dates) via single SQL `IN` query. |
| `backend/app/routers/recommend.py` | **Load-Bearing** | Pipeline Orchestration: ThreadPoolExecutor concurrent dispatch of Stage 2 & Stage 3, combining results into validated schema. |
| `backend/scripts/evaluate_benchmarks.py` | **Load-Bearing** | Benchmark Test Harness: Automated evaluation against 4 real public tenders (calculating Top-1, Top-3 Recall, MRR, QCO accuracy). |
| `backend/scripts/ingest_standards.py` | **Load-Bearing** | Data Ingestion Pipeline: Parses catalog JSON, embeds title+scope via Gemini, and upserts standards & references tables. |
| `supabase_schema.sql` | **Load-Bearing** | Database Definition: pgvector extension, table schemas, `match_standards` cosine distance RPC, and RLS policies. |
| `frontend/components/ResultCard.tsx` | **Load-Bearing** | UI Representation: Displays similarity %, statutory QCO compliance indicators, and version tracking. |
| `frontend/components/ReferenceList.tsx` | **Load-Bearing** | UI Representation: Color-coded taxonomy renderer for normative links (RAW_MATERIAL, TEST_METHOD, COMPONENT, SAFETY_CODE). |
| `frontend/lib/api.ts` | **Load-Bearing** | Network Resilience: 15-second AbortController timeout, standardized error serialization. |
| `backend/app/config.py` | **Scaffolding / Config** | Environment variable reading (`.env`) with default fallbacks. |
| `backend/app/db/client.py` | **Scaffolding / Infra** | Supabase client singleton setup and fail-fast validation. |
| `backend/app/models/schemas.py` | **Scaffolding / Contracts**| Pydantic v2 data transfer objects and string trimming validators. |
| `backend/app/main.py` | **Scaffolding / Glue** | FastAPI instantiation, CORS setup, router mounting, and lifespan warmup. |
| `docker-compose.yml`, `Dockerfile` | **Scaffolding / Infra** | Container packaging for local and cloud deployment. |

---

### 4. 🚨 Reality Check: Live V1 Implementation vs. Roadmap Vision

When defending before the SIH jury, **never claim features that exist only in blueprint markdown**. Here is the explicit status:

| Feature | Code Status in Repo | Truthful Jury Answer |
|---|---|---|
| **Semantic AI Retrieval** | ✅ **Implemented & Live** | 768-dim Gemini embeddings + pgvector cosine similarity RPC. |
| **Normative Reference Graph** | ✅ **Implemented & Live** | Deterministic relational join table `standard_references` in PostgreSQL. |
| **QCO Verification** | ✅ **Implemented & Live** | Deterministic lookup on `is_mandatory_qco` based on official DPIIT / MeitY gazettes. |
| **Version & Amendment Tracking**| ✅ **Implemented & Live** | Parsed and surfaced from BIS master catalog schema. |
| **Sparse BM25 + Dense RRF Hybrid**| ⏳ **Backlog / Spec** | V1 uses dense embedding retrieval. Hybrid BM25+RRF is architected in Roadmap item #1. |
| **Tender PDF/DOCX Parsing** | ⏳ **Backlog / Spec** | V1 accepts raw text/spec inputs. PDF table/BoQ extraction is Roadmap item #2. |
| **LLM Clause Generator** | ⏳ **Backlog / Spec** | V1 outputs structured compliance metadata. Generative NIT drafting is Roadmap item #4. |
| **Bhashini Multilingual ASR** | ⏳ **Backlog / Spec** | Roadmap item #5 for regional language voice/text input. |
| **Browser Extension for GeM** | ⏳ **Backlog / Spec** | Roadmap item #7 for direct portal overlay. |
