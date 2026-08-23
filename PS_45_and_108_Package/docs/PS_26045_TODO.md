# 🚀 IP-SAKTI Sahayak (PS 26045) - Master TODO Checklist

## 📝 CONTEXT
**Problem Statement:** IP-SAKTI Sahayak: a multilingual, RAG-based (source-cited) AI assistant for Intellectual Property and regulatory guidance in Ayurveda.
**Sponsoring Org:** Ministry of Ayush / AIIA
**Architecture:** Next.js 15 PWA → FastAPI → LangGraph Agents → Hybrid bge-m3 + BM25 + Neo4j → Bhashini Voice.

## 👥 TEAM
- **Rishii:** Frontend Lead (Next.js 15/React 19). ML Mentor only when Sahaj is stuck.
- **Sahaj:** Primary ML/RAG owner — embeddings, BM25, Neo4j, LangGraph.
- **Tanishka:** UI/UX Lead (Figma), domain research, styling.
- **Prerak:** Backend Lead (FastAPI), Docker, async pipelines.
- **Diksha:** DB & Vector Architect (PostgreSQL/Supabase, pgvector/Qdrant).
- **Member 6:** QA & Benchmarking (Ragas, ground-truth, offline demo).

---

## 🏗️ Phase 0: Pre-Development Setup

- [ ] **[P0] [Prerak] [2h]** Monorepo initialization → Deliverable: `package.json`, `pnpm-workspace.yaml`
  - Depends on: None
  - DoD: pnpm workspace configured with `frontend` and `backend` packages.
- [ ] **[P0] [Prerak] [3h]** Docker Compose base setup → Deliverable: `docker-compose.yml`, `Makefile`
  - Depends on: Monorepo init
  - DoD: Local environment running DBs (Postgres, Qdrant, Neo4j) via `make up`.
- [ ] **[P0] [Prerak] [1h]** Environment variables template → Deliverable: `.env.example`
  - Depends on: None
  - DoD: All necessary backend, frontend, and ML API keys documented.
- [ ] **[P0] [Rishii] [1h]** Git repository + branch strategy → Deliverable: `.github/PULL_REQUEST_TEMPLATE.md`
  - Depends on: None
  - DoD: Main, Dev branches protected, PR template active.
- [ ] **[P0] [Tanishka] [2h]** Figma design system setup → Deliverable: Figma project link
  - Depends on: None
  - DoD: Core brand colors, typography, and Ayush motifs defined.
- [ ] **[P0] [Rishii] [1h]** Team onboarding & tool access → Deliverable: `README.md`
  - Depends on: None
  - DoD: All members added to GitHub, Figma, and Supabase.

---

## 📚 Phase 1: Knowledge Corpus & Infrastructure (Days 1-3)

### 🎨 Rishii (Frontend)
- [ ] **[P0] [Rishii] [2h]** Next.js 15 scaffold with App Router → Deliverable: `frontend/package.json`
  - Depends on: Monorepo init
  - DoD: `pnpm create next-app` successfully run with TypeScript.
- [ ] **[P0] [Rishii] [2h]** Tailwind CSS + design tokens → Deliverable: `frontend/tailwind.config.ts`
  - Depends on: Next.js scaffold, Figma setup
  - DoD: Variables synced with Tanishka's Figma tokens.
- [ ] **[P1] [Rishii] [3h]** Layout components (3-pane workbench shell) → Deliverable: `frontend/src/app/layout.tsx`
  - Depends on: Tailwind CSS setup
  - DoD: Responsive sidebar, main chat area, and right evidence panel working.
- [ ] **[P2] [Rishii] [2h]** Auth pages (if needed) → Deliverable: `frontend/src/app/login/page.tsx`
  - Depends on: Layout components
  - DoD: Basic mockup of login and session selection.
- [ ] **[P0] [Rishii] [2h]** API client setup (fetch/axios with types) → Deliverable: `frontend/src/lib/api.ts`
  - Depends on: None
  - DoD: Typed wrapper around fetch/axios pointing to local FastAPI backend.

### 🧠 Sahaj (ML)
- [ ] **[P0] [Sahaj] [5h]** Legal document collection → Deliverable: `backend/data/raw/`
  - Depends on: None
  - DoD: Patents Act, BD Act, D&C Act, FSSAI, WIPO GRATK downloaded as PDFs.
- [ ] **[P0] [Sahaj] [4h]** Document parsing scripts → Deliverable: `backend/scripts/parse_pdfs.py`
  - Depends on: Legal doc collection
  - DoD: PDFs converted to clean text using unstructured/PyMuPDF.
- [ ] **[P0] [Sahaj] [4h]** Section-level chunking with metadata headers → Deliverable: `backend/scripts/chunker.py`
  - Depends on: Parsing scripts
  - DoD: Text split by legal sections, metadata capturing Act name and Section number.
- [ ] **[P1] [Sahaj] [2h]** Chunk quality validation → Deliverable: `backend/notebooks/chunk_review.ipynb`
  - Depends on: Chunking
  - DoD: 50 random chunks reviewed for coherency and completeness.

### ⚙️ Prerak (Backend)
- [ ] **[P0] [Prerak] [2h]** FastAPI project scaffold → Deliverable: `backend/app/main.py`
  - Depends on: Monorepo init
  - DoD: FastAPI running with Uvicorn, API router structured.
- [ ] **[P0] [Prerak] [1h]** Health check endpoint → Deliverable: `backend/app/api/v1/health.py`
  - Depends on: FastAPI scaffold
  - DoD: `/api/v1/health` returns `{"status": "ok"}`.
- [ ] **[P1] [Prerak] [3h]** Authentication middleware (JWT) → Deliverable: `backend/app/core/security.py`
  - Depends on: FastAPI scaffold
  - DoD: Endpoints protected by JWT validation.
- [ ] **[P0] [Prerak] [1h]** CORS configuration → Deliverable: `backend/app/main.py`
  - Depends on: FastAPI scaffold
  - DoD: Next.js dev server permitted in CORS origins.
- [ ] **[P1] [Prerak] [2h]** Logging & error handling setup → Deliverable: `backend/app/core/logger.py`
  - Depends on: FastAPI scaffold
  - DoD: Structured JSON logging to console/file and global exception handler.

### 🗄️ Diksha (Database)
- [ ] **[P0] [Diksha] [3h]** PostgreSQL schema design & DDL → Deliverable: `backend/db/schema.sql`
  - Depends on: None
  - DoD: Tables for users, sessions, query logs drafted.
- [ ] **[P0] [Diksha] [2h]** Supabase project setup → Deliverable: Supabase connection string
  - Depends on: Schema design
  - DoD: Cloud dev database provisioned.
- [ ] **[P0] [Diksha] [2h]** pgvector extension setup → Deliverable: `backend/db/migrations/001_pgvector.sql`
  - Depends on: Postgres running
  - DoD: `CREATE EXTENSION vector` executed.
- [ ] **[P0] [Diksha] [2h]** Qdrant collection creation → Deliverable: `backend/scripts/init_qdrant.py`
  - Depends on: Qdrant docker running
  - DoD: Collection initialized with 1024 dims (bge-m3).
- [ ] **[P1] [Diksha] [1h]** Audit log table → Deliverable: `backend/db/migrations/002_audit_log.sql`
  - Depends on: Schema design
  - DoD: Trigger or table for logging interactions.

### 🖌️ Tanishka (UX)
- [ ] **[P0] [Tanishka] [3h]** User persona research → Deliverable: `docs/personas.md`
  - Depends on: None
  - DoD: 2 personas defined (Ayurveda Doctor, Startup Founder).
- [ ] **[P0] [Tanishka] [4h]** Figma wireframes (desktop workbench) → Deliverable: Figma frames
  - Depends on: Persona research
  - DoD: 3-pane layout wireframed with citation UI.
- [ ] **[P0] [Tanishka] [3h]** Figma wireframes (mobile voice card) → Deliverable: Figma frames
  - Depends on: Desktop wireframes
  - DoD: Mobile-first voice interaction screens designed.
- [ ] **[P1] [Tanishka] [2h]** Design tokens document → Deliverable: `docs/design_tokens.json`
  - Depends on: Wireframes
  - DoD: Handoff specs for Rishii.

### 🧪 Member 6 (QA)
- [ ] **[P0] [Member 6] [2h]** Test environment setup → Deliverable: `backend/tests/conftest.py`
  - Depends on: Backend scaffold
  - DoD: Pytest configured for FastAPI.
- [ ] **[P0] [Member 6] [3h]** Ground-truth dataset format design → Deliverable: `data/qa/format.json`
  - Depends on: None
  - DoD: JSON schema for Q&A pairs with source references.
- [ ] **[P1] [Member 6] [2h]** Initial test case skeleton (5 cases) → Deliverable: `data/qa/test_cases_v1.json`
  - Depends on: Format design
  - DoD: 5 realistic IP queries documented.

---

## 🔍 Phase 2: Hybrid Graph-RAG & Retrieval (Days 4-6)

### 🧠 Sahaj (ML)
- [ ] **[P0] [Sahaj] [4h]** bge-m3 embedding generation script → Deliverable: `backend/ml/embeddings.py`
  - Depends on: Chunking script
  - DoD: Chunks converted to 1024d vectors.
- [ ] **[P0] [Sahaj] [3h]** BM25 sparse index builder → Deliverable: `backend/ml/bm25.py`
  - Depends on: Chunking script
  - DoD: Lexical index created and stored.
- [ ] **[P0] [Sahaj] [4h]** Neo4j Knowledge Graph schema (Cypher CREATE) → Deliverable: `backend/graph/schema.cypher`
  - Depends on: None
  - DoD: Nodes for Act, Section, Concept, relationships mapped.
- [ ] **[P0] [Sahaj] [5h]** Neo4j data loader script → Deliverable: `backend/graph/loader.py`
  - Depends on: KG Schema, Parsed chunks
  - DoD: Extracted entities populated into Neo4j.
- [ ] **[P0] [Sahaj] [5h]** Hybrid search function (dense + sparse) → Deliverable: `backend/ml/retriever.py`
  - Depends on: Embeddings, BM25
  - DoD: Function returns combined results.
- [ ] **[P1] [Sahaj] [3h]** RRF score fusion implementation → Deliverable: `backend/ml/rrf.py`
  - Depends on: Hybrid search
  - DoD: Reciprocal Rank Fusion blending sparse and dense scores.
- [ ] **[P1] [Sahaj] [4h]** Cross-encoder reranker setup → Deliverable: `backend/ml/reranker.py`
  - Depends on: Hybrid search
  - DoD: BGE-Reranker re-scoring top 50 chunks to top 10.
- [ ] **[P1] [Sahaj] [2h]** Unit tests for retrieval pipeline → Deliverable: `backend/tests/test_retrieval.py`
  - Depends on: Reranker
  - DoD: Pytest passes for dummy queries.

### ⚙️ Prerak (Backend)
- [ ] **[P0] [Prerak] [4h]** `/api/v1/search` endpoint → Deliverable: `backend/app/api/v1/search.py`
  - Depends on: Hybrid search function
  - DoD: REST endpoint wrapping Sahaj's retriever.
- [ ] **[P0] [Prerak] [4h]** SSE streaming response → Deliverable: `backend/app/api/v1/chat.py`
  - Depends on: `/api/v1/search`
  - DoD: Tokens streamed to frontend via Server-Sent Events.
- [ ] **[P0] [Prerak] [2h]** Request validation (Pydantic) → Deliverable: `backend/app/schemas/chat.py`
  - Depends on: FastAPI setup
  - DoD: Strict validation on incoming query payloads.
- [ ] **[P1] [Prerak] [2h]** Rate limiting middleware → Deliverable: `backend/app/core/rate_limit.py`
  - Depends on: None
  - DoD: Maximum 20 requests per minute per IP.

### 🗄️ Diksha (Database)
- [ ] **[P1] [Diksha] [3h]** Vector index optimization (HNSW tuning) → Deliverable: `backend/db/migrations/003_hnsw.sql`
  - Depends on: Qdrant/pgvector populated
  - DoD: Query latency under 50ms for dense search.
- [ ] **[P1] [Diksha] [2h]** Metadata filtering queries → Deliverable: `backend/db/queries/filter.sql`
  - Depends on: Postgres schema
  - DoD: Fast filtering by Act or Year.
- [ ] **[P1] [Diksha] [3h]** Query performance benchmarks → Deliverable: `docs/benchmarks_db.md`
  - Depends on: HNSW tuning
  - DoD: Latency numbers recorded.

### 🧪 Member 6 (QA)
- [ ] **[P0] [Member 6] [4h]** 25 ground-truth legal Q&A pairs → Deliverable: `data/qa/ground_truth.json`
  - Depends on: Initial 5 cases
  - DoD: Diverse coverage of BD Act, D&C Act, etc.
- [ ] **[P0] [Member 6] [3h]** Ragas evaluation script skeleton → Deliverable: `backend/scripts/evaluate_rag.py`
  - Depends on: Ragas library installed
  - DoD: Script can read JSON and evaluate a dummy response.
- [ ] **[P1] [Member 6] [3h]** Retrieval accuracy baseline measurement → Deliverable: `docs/baseline_metrics.md`
  - Depends on: Hybrid search, Ground-truth
  - DoD: Hit Rate and MRR computed for base retriever.

---

## 🤖 Phase 3: Multi-Agent System & Classification (Days 7-9)

### 🧠 Sahaj (ML)
- [ ] **[P0] [Sahaj] [4h]** LangGraph supervisor agent → Deliverable: `backend/agents/supervisor.py`
  - Depends on: None
  - DoD: Graph setup to route queries to specialized agents.
- [ ] **[P0] [Sahaj] [3h]** Formulation Classification Agent → Deliverable: `backend/agents/classifier.py`
  - Depends on: Supervisor
  - DoD: Classifies query into ASU drugs, food supplements, or cosmetics.
- [ ] **[P0] [Sahaj] [3h]** National IP & Regulatory Agent → Deliverable: `backend/agents/national.py`
  - Depends on: Supervisor
  - DoD: Handles D&C Act and Patent Act (India) queries.
- [ ] **[P0] [Sahaj] [3h]** International & Export Agent → Deliverable: `backend/agents/international.py`
  - Depends on: Supervisor
  - DoD: Handles FDA, EMA, WHO guidelines.
- [ ] **[P0] [Sahaj] [3h]** ABS & Biodiversity Agent → Deliverable: `backend/agents/biodiversity.py`
  - Depends on: Supervisor
  - DoD: Specializes in NBA approvals and Form I/II/III.
- [ ] **[P1] [Sahaj] [2h]** TKDL Prior-Art Search Agent → Deliverable: `backend/agents/tkdl.py`
  - Depends on: Supervisor
  - DoD: Mocks or interfaces with TKDL data structures.
- [ ] **[P0] [Sahaj] [3h]** Dual-Jurisdiction Switch middleware → Deliverable: `backend/agents/middleware/jurisdiction.py`
  - Depends on: National/International agents
  - DoD: Can contextualize answers based on India vs US toggle.
- [ ] **[P0] [Sahaj] [2h]** Agent unit tests → Deliverable: `backend/tests/test_agents.py`
  - Depends on: All agents
  - DoD: Router correctly directs 10 diverse test queries.

### 🎨 Rishii (Frontend)
- [ ] **[P0] [Rishii] [4h]** Formulation Wizard UI (step-by-step) → Deliverable: `frontend/src/components/Wizard.tsx`
  - Depends on: Layout components
  - DoD: Multi-step form for defining ingredients and intended use.
- [ ] **[P1] [Rishii] [2h]** Category badge components → Deliverable: `frontend/src/components/Badges.tsx`
  - Depends on: Tailwind config
  - DoD: UI markers for "ASU Drug", "Nutraceutical", etc.
- [ ] **[P0] [Rishii] [3h]** Real-time classification updates → Deliverable: `frontend/src/hooks/useAgentState.ts`
  - Depends on: SSE endpoint
  - DoD: UI updates agent thinking steps live.
- [ ] **[P0] [Rishii] [2h]** Jurisdiction toggle component → Deliverable: `frontend/src/components/JurisdictionToggle.tsx`
  - Depends on: None
  - DoD: Switch between "Domestic (India)" and "Export".

### ⚙️ Prerak (Backend)
- [ ] **[P0] [Prerak] [2h]** `/api/v1/classify-formulation` endpoint → Deliverable: `backend/app/api/v1/agents.py`
  - Depends on: Classification Agent
  - DoD: REST wrapper for the classifier agent.
- [ ] **[P0] [Prerak] [2h]** `/api/v1/abs-router` endpoint → Deliverable: `backend/app/api/v1/agents.py`
  - Depends on: ABS Agent
  - DoD: REST wrapper for ABS agent.
- [ ] **[P0] [Prerak] [2h]** `/api/v1/jurisdiction-switch` endpoint → Deliverable: `backend/app/api/v1/agents.py`
  - Depends on: Jurisdiction middleware
  - DoD: Endpoint accepts jurisdiction flags.
- [ ] **[P1] [Prerak] [4h]** WebSocket for real-time agent status → Deliverable: `backend/app/api/v1/ws.py`
  - Depends on: LangGraph agents
  - DoD: WebSocket emits "Thinking...", "Searching DB...", etc.

---

## 🎙️ Phase 4: Voice, Citations & Frontend Polish (Days 10-12)

### 🧠⚙️ Sahaj + Prerak (Integration)
- [ ] **[P0] [Sahaj, Prerak] [5h]** Bhashini ASR API integration → Deliverable: `backend/app/services/bhashini.py`
  - Depends on: Bhashini API keys
  - DoD: Audio bytes to Hindi/English text.
- [ ] **[P0] [Sahaj, Prerak] [3h]** Bhashini NMT integration → Deliverable: `backend/app/services/nmt.py`
  - Depends on: Bhashini API keys
  - DoD: Query translation (Hindi -> English) and Response (English -> Hindi).
- [ ] **[P0] [Sahaj, Prerak] [4h]** Bhashini TTS integration → Deliverable: `backend/app/services/tts.py`
  - Depends on: Bhashini API keys
  - DoD: Final text to playable Audio URL/bytes.
- [ ] **[P1] [Sahaj] [3h]** Ayurvedic Concept Normalizer (term mapping) → Deliverable: `backend/ml/normalizer.py`
  - Depends on: None
  - DoD: Maps colloquial Hindi terms to exact botanical/Sanskrit names before DB search.

### 🎨 Rishii (Frontend)
- [ ] **[P0] [Rishii] [4h]** Citation inspector component → Deliverable: `frontend/src/components/Citation.tsx`
  - Depends on: RAG results format
  - DoD: Clicking `[1]` opens popup with exact PDF snippet.
- [ ] **[P1] [Rishii] [3h]** Gazette paragraph highlighting → Deliverable: `frontend/src/components/Highlighter.tsx`
  - Depends on: Citation inspector
  - DoD: Highlights the exact sentence in the source card.
- [ ] **[P0] [Rishii] [4h]** Web Audio recording component → Deliverable: `frontend/src/components/VoiceRecorder.tsx`
  - Depends on: None
  - DoD: Press-and-hold to record audio, returns Blob.
- [ ] **[P0] [Rishii] [3h]** Mobile PWA voice card → Deliverable: `frontend/src/app/mobile/page.tsx`
  - Depends on: VoiceRecorder
  - DoD: Mobile-optimized full-screen voice UI.
- [ ] **[P0] [Rishii] [4h]** Streaming chat interface → Deliverable: `frontend/src/components/Chat.tsx`
  - Depends on: SSE endpoint
  - DoD: Markdown renders incrementally, auto-scrolls.
- [ ] **[P0] [Rishii] [3h]** Evidence panel with source cards → Deliverable: `frontend/src/components/EvidencePanel.tsx`
  - Depends on: None
  - DoD: Right sidebar shows PDF thumbnails and Act summaries.
- [ ] **[P2] [Rishii] [2h]** Dark/light mode toggle → Deliverable: `frontend/tailwind.config.ts` + Component
  - Depends on: Tailwind
  - DoD: Standard theme switching using `next-themes`.
- [ ] **[P1] [Rishii] [2h]** Loading states & skeletons → Deliverable: `frontend/src/components/Skeletons.tsx`
  - Depends on: None
  - DoD: Pulse animations while waiting for ML endpoints.
- [ ] **[P1] [Rishii] [1h]** Error boundaries → Deliverable: `frontend/src/components/ErrorBoundary.tsx`
  - Depends on: None
  - DoD: React tree doesn't crash on bad API data.
- [ ] **[P2] [Rishii] [1h]** 404/error pages → Deliverable: `frontend/src/app/not-found.tsx`
  - Depends on: None
  - DoD: Custom branded 404 page.

### 🖌️ Tanishka (Design)
- [ ] **[P0] [Tanishka] [3h]** High-contrast mobile voice cards → Deliverable: Figma screens
  - Depends on: None
  - DoD: Readability checked for outdoor mobile use.
- [ ] **[P1] [Tanishka] [2h]** WCAG accessibility audit → Deliverable: `docs/a11y_report.md`
  - Depends on: Frontend implemented
  - DoD: Verify contrast ratios and ARIA labels.
- [ ] **[P0] [Tanishka] [3h]** Final UI polish pass → Deliverable: GitHub Issues for Rishii
  - Depends on: Frontend deployed
  - DoD: Alignment and spacing verified against Figma.
- [ ] **[P2] [Tanishka] [2h]** Animation/transition review → Deliverable: Figma prototypes
  - Depends on: None
  - DoD: Micro-interactions defined for voice listening state.

---

## ✅ Phase 5: Evaluation, Docker & Demo (Days 13-14)

### 🧪 QA & ML (Member 6, Sahaj)
- [ ] **[P0] [Member 6, Sahaj] [4h]** Run full Ragas evaluation → Deliverable: `docs/ragas_results.csv`
  - Depends on: Ragas script, Phase 3 agents
  - DoD: Evaluation over all 25 ground-truth queries.
- [ ] **[P0] [Member 6] [2h]** Context Recall >= 0.90 verification → Deliverable: `docs/metrics.md`
  - Depends on: Full Ragas run
  - DoD: Verify metric is met, else flag Sahaj for reranker tweak.
- [ ] **[P0] [Member 6] [2h]** Groundedness >= 0.95 verification → Deliverable: `docs/metrics.md`
  - Depends on: Full Ragas run
  - DoD: Verify no hallucinations.
- [ ] **[P1] [Member 6] [3h]** Edge case testing → Deliverable: `docs/edge_cases.md`
  - Depends on: Phase 4
  - DoD: Test queries in mixed Hindi-English, typos, out-of-domain.
- [ ] **[P0] [Member 6] [3h]** Multilingual voice testing → Deliverable: `docs/voice_tests.md`
  - Depends on: Bhashini integration
  - DoD: Test 10 queries spoken in Hindi, Marathi, etc.

### ⚙️🗄️ Backend & DB (Prerak, Diksha)
- [ ] **[P0] [Prerak, Diksha] [4h]** Docker Compose finalization → Deliverable: `docker-compose.prod.yml`
  - Depends on: All code complete
  - DoD: Entire stack starts with `docker-compose up --build`.
- [ ] **[P0] [Prerak] [2h]** Air-gapped mode testing (disable WiFi) → Deliverable: Video proof
  - Depends on: Docker prod
  - DoD: Everything except Bhashini works offline.
- [ ] **[P1] [Diksha] [2h]** Database backup/restore scripts → Deliverable: `backend/scripts/pg_dump.sh`
  - Depends on: Docker prod
  - DoD: Easy export of vectors for the judging panel.
- [ ] **[P0] [Prerak] [2h]** Environment variable documentation → Deliverable: `README.md`
  - Depends on: All integrations
  - DoD: Step-by-step setup guide for the jury.

### 🎨 Team Wide (Rishii, Tanishka, All)
- [ ] **[P0] [Tanishka] [4h]** 8-slide pitch deck → Deliverable: PDF presentation
  - Depends on: Metrics
  - DoD: Problem, Solution, Architecture, Novelty, Metrics, Roadmap.
- [ ] **[P0] [Rishii] [2h]** Live demo script → Deliverable: `docs/demo_script.md`
  - Depends on: Phase 4
  - DoD: Step-by-step click path mapped out for 3-minute presentation.
- [ ] **[P0] [All] [2h]** 3-tier demo setup verification → Deliverable: Hardware check
  - Depends on: None
  - DoD: Laptops configured, phones connected to local network.
- [ ] **[P0] [Rishii] [2h]** 60fps backup video recording → Deliverable: `demo.mp4`
  - Depends on: Full system
  - DoD: Screen recording of a flawless run just in case.
- [ ] **[P0] [All] [3h]** Rehearsal (3 dry runs minimum) → Deliverable: Peer feedback
  - Depends on: Demo script
  - DoD: Pitch fits exactly within time limits.

---

## 🚀 Stretch Goals (P3 — Only if time permits)
- [ ] **[P3] [Prerak] [4h]** Multi-user session management
- [ ] **[P3] [Rishii] [3h]** Export as PDF report
- [ ] **[P3] [Tanishka] [3h]** Analytics dashboard UI
- [ ] **[P3] [Sahaj] [5h]** Automated gazette update checker
- [ ] **[P3] [Prerak] [6h]** Integration with IP India portal APIs (if available)

---

## 🔒 Security Checklist
- [ ] No hardcoded secrets in source control (git history clean).
- [ ] Input validation on all FastAPI endpoints via Pydantic.
- [ ] SQL injection prevention (parameterized queries via asyncpg/SQLAlchemy).
- [ ] DPDP Act compliance (PII redaction from user query logs).
- [ ] Rate limiting on public-facing FastAPI endpoints.
- [ ] CORS properly configured, not using `*` in production.

---

## 📊 Evaluation Metrics Targets

| Metric | Target | Current Status | Owner |
|--------|--------|----------------|-------|
| Retrieval Hit Rate | ≥ 0.90 | Pending | Sahaj / Member 6 |
| MRR@5 | ≥ 0.85 | Pending | Sahaj / Member 6 |
| Answer Groundedness (Ragas) | ≥ 0.95 | Pending | Member 6 |
| Context Recall (Ragas) | ≥ 0.90 | Pending | Member 6 |
| Avg Search Latency | ≤ 500ms | Pending | Diksha / Prerak |
| Voice ASR WER (Word Error Rate) | ≤ 10% | Pending | Sahaj |
| UI Lighthouse Score (Perf/A11y) | ≥ 95 | Pending | Rishii / Tanishka |
