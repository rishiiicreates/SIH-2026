# SIH 2026 — 6-Member Team Role Delegation & ML Co-Leadership Matrix
**Team Structure & Workload Distribution for Top 6 Problem Statements**  
**Core Lead:** Rishii (Frontend Lead + ML Co-Lead)  
**AI Lead:** Sahaj (RAG & Graph RAG Engineer)  
**Design & Research:** Tanishka (UI/UX + Frontend + Domain Research)  
**Backend & DevOps:** Prerak (FastAPI + Docker + Kubernetes + Orchestration)  
**Database & Vector Lead:** Diksha (PostgreSQL / Supabase + Vector Schema + Metadata)  
**QA & Evaluation:** Member 6 (Corpus QA + Multilingual Testing + Benchmarking)  

---

## 1. Executive Team Dynamics & ML Co-Leadership Strategy

```
                                  ┌────────────────────────────────────────────────────────┐
                                  │                Rishii (Full-Stack & ML Lead)           │
                                  │  • Application Frontend (Next.js/React 19)             │
                                  │  • ML/RAG Architecture Co-Lead (Directing AI Workflows)│
                                  └─────────────┬────────────────────────────┬─────────────┘
                                                │                            │
                     ┌──────────────────────────┴──────────┐      ┌──────────┴─────────────────────────┐
                     ▼                                     ▼      ▼                                    ▼
       ┌───────────────────────────┐         ┌───────────────────────────┐         ┌───────────────────────────┐
       │     Sahaj (AI/RAG Lead)   │         │     Tanishka (UI/UX)      │         │    Prerak (Backend/DevOps)│
       ├───────────────────────────┤         ├───────────────────────────┤         ├───────────────────────────┤
       │ • Hybrid Search (BM25+Dense)│       │ • Figma Wireframes & UX   │         │ • FastAPI Microservices   │
       │ • Neo4j Graph RAG queries │         │ • Multilingual View/Audio │         │ • Docker / Kubernetes     │
       │ • LLM Prompt Chain & Agent│         │ • Domain Regulation Maps  │         │ • Async Job Pipelines     │
       └───────────────────────────┘         └───────────────────────────┘         └───────────────────────────┘
                     │                                                                           │
                     └──────────────────────────┬────────────────────────────────────────────────┘
                                                │
                                  ┌─────────────┴─────────────┐
                                  ▼                           ▼
                    ┌───────────────────────────┐┌───────────────────────────┐
                    │    Diksha (DB & Vectors)  ││   Member 6 (QA & Bench)   │
                    ├───────────────────────────┤├───────────────────────────┤
                    │ • PostgreSQL / Supabase   ││ • Ragas Evaluation Suite  │
                    │ • Vector Schema & Indexes ││ • Ground Truth Test Sets  │
                    │ • Version & Audit Tables  ││ • Offline Demo Fallbacks  │
                    └───────────────────────────┘└───────────────────────────┘
```

### The Rishii + Sahaj ML Workload Split
To maximize execution velocity, **Rishii** provides the high-level ML architecture, mathematical formulas (e.g. Reciprocal Rank Fusion, Triplet Graph definitions), and system integration, while assigning modular, well-scoped tasks to **Sahaj**:
* **Rishii's ML Focus:** 
  - Designing the Graph-RAG retrieval topology (Neo4j Cypher queries + vector re-ranking).
  - Designing zero-hallucination verification gates & deterministic schema constraints.
  - End-to-end integration between LLM outputs and frontend UI components (citations, graphs, audio).
* **Sahaj's ML Focus:** 
  - Implementing the chunking & embedding generation scripts (`bge-m3`, `fastembed`).
  - Setting up BM25 sparse index + vector distance retrieval scripts.
  - Prompt template assembly for classification wizards and clause generators.

---

## 2. Granular Task Delegation per Team Member

### 1. Rishii (Frontend Lead + ML Architecture Co-Lead)
* **Frontend Responsibilities:**
  * Build the primary **Next.js 15 / React 19** application with Tailwind CSS and Lucide icons.
  * Build the **Split-Pane Research Workbench** (Prompt input, dynamic streaming chat, interactive evidence panel, and bounding-box PDF inspector).
  * Build the **Manifest V3 Chrome/Edge Browser Extension** (for PS 26108 / PS 26100 GeM overlays).
* **ML / Architecture Responsibilities:**
  * Supervise and review Sahaj’s retrieval pipelines.
  * Implement the confidence scoring, safe-abstention logic, and citation verification regex.
  * Connect frontend streaming state directly to backend SSE (Server-Sent Events) endpoints.

### 2. Sahaj (AI / RAG & Graph Reasoning Engineer)
* **RAG Pipeline:**
  * Set up embedding pipelines using `BAAI/bge-m3` and dense cosine similarity in Qdrant/pgvector.
  * Implement BM25 lexical search over statutory / standards text.
  * Implement Reciprocal Rank Fusion (RRF) to merge dense and sparse candidate sets.
* **Graph & Agent Reasoning:**
  * Write Cypher graph queries in Neo4j to expand normative trees and statutory cross-references.
  * Assemble LangGraph multi-agent supervisors (Classifier Agent, National Agent, International Agent).

### 3. Tanishka (UI/UX Lead, Frontend Collaborator & Domain Researcher)
* **Design & User Experience:**
  * Design comprehensive Figma prototypes for both desktop research mode and mobile/PWA layouts.
  * Create custom design tokens, dark/light mode palettes, and responsive layouts tailored to Indian government DPI standards.
* **Domain Research & Presentation:**
  * Map out the step-by-step user onboarding flows (e.g., Ayush formulation wizard, business industrial checklists).
  * Design visual regulatory cards and intuitive compliance status indicators (Green = Compliant, Yellow = Missing Reference, Red = QCO Violation).

### 4. Prerak (Backend API, Orchestration & DevOps Lead)
* **FastAPI Backend Services:**
  * Build modular, asynchronous FastAPI microservices (`/api/v1/classify`, `/api/v1/search`, `/api/v1/generate-clause`, `/api/v1/audit`).
  * Implement JWT authentication, rate limiting, and session state management.
  * Build background ingestion pipelines using Celery / Redis or FastAPI BackgroundTasks for parsing multi-page tender PDFs.
* **DevOps & Infrastructure:**
  * Author the unified, one-click `docker-compose.yml` orchestrating FastAPI, Next.js, Neo4j, and Supabase/PostgreSQL.
  * Set up cloud deployments on Render / AWS / Vercel + local air-gapped fallback environment.

### 5. Diksha (Database Architect, Supabase & Vector Storage Lead)
* **Database & Relational Modeling:**
  * Design normalized PostgreSQL / Supabase schemas for users, formulation scenarios, tender documents, audit logs, and version metadata.
  * Implement row-level security (RLS) and encrypted session storage for DPDP Act 2023 compliance.
* **Vector & Metadata Indexes:**
  * Set up `pgvector` / Qdrant collections with HNSW indexing and metadata filtering (e.g. `jurisdiction == 'NATIONAL'`, `is_active == true`, `division_council == 'ETD'`).
  * Maintain audit trail tables logging every user query, retrieved passage ID, confidence score, and timestamp.

### 6. Member 6 (Corpus QA, Benchmarking & Evaluation Lead)
* **Evaluation & Testing (Ragas Suite):**
  * Build golden evaluation datasets containing 25+ real-world ground-truth test cases per problem statement.
  * Measure and log RAG Triad scores: **Context Relevance**, **Groundedness / Faithfulness**, and **Answer Relevance**.
* **Multilingual QA & Demo Fallback:**
  * Test Bhashini speech-to-text accuracy across Hindi, Tamil, Marathi, and Hinglish.
  * Prepare high-resolution 60fps screen recordings of the complete live demo as a zero-risk backup during SIH jury evaluations.

---

## 3. Hour-by-Hour 36-Hour Hackathon Team Sync Protocol

| Time Window | Rishii & Sahaj (Frontend & AI) | Prerak & Diksha (Backend & DB) | Tanishka & Member 6 (Design & QA) |
| :--- | :--- | :--- | :--- |
| **Hours 00 – 04** | Scaffold Next.js UI & implement hybrid RRF logic. | Launch Docker Compose, seed Neo4j & Supabase tables. | Finalize Figma UI tokens; build 25-case ground truth test set. |
| **Hours 04 – 12** | Wire streaming chat UI with RAG engine & graph explorer. | Build FastAPI endpoints; connect vector search & Celery parser. | Build demo data cards; test PDF parsing on edge-case tenders. |
| **Hours 12 – 16** | **MENTOR ROUND 1:** Live prototype demo; capture judge suggestions. | **MENTOR ROUND 1:** Document technical questions from jury. | **MENTOR ROUND 1:** Note UX & domain feedback from mentors. |
| **Hours 16 – 24** | **THE PIVOT SPRINT:** Implement mentor feedback & Chrome Extension. | Optimize query latency; add PDF export background service. | Refine presentation slides; run Ragas faithfulness benchmarks. |
| **Hours 24 – 30** | **MENTOR ROUND 2:** Showcase extension & Bhashini voice features. | Verify database durability; lock down air-gapped local build. | Conduct end-to-end rehearsal; verify all source citations. |
| **Hours 30 – 36** | **CODE FREEZE:** Polish UI, test responsive layouts, prep demo script. | Test 3-Tier Demo Strategy (Cloud + Localhost Docker + Video). | Polish final pitch deck; run live demo dry runs with jury timer. |
