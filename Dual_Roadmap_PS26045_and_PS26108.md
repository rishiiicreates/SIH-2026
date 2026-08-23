# SIH 2026 — Dual-Track Execution Roadmap & Engineering Blueprint
## Final Selection: Problem Statement 26045 vs. Problem Statement 26108
**Target Problem Statements:**  
- **PS 26045:** IP-SAKTI Sahayak — Multilingual, Source-Cited AI Assistant for Ayurvedic IPR & Regulatory Guidance (*Ministry of Ayush / AIIA*)  
- **PS 26108:** AI-Powered Recommendation Engine for Identifying Applicable Indian Standards for Procurement Specifications (*Ministry of Consumer Affairs / DoCA / BIS*)  

---

## 1. Updated 6-Member Team Roles & ML Escalation Hierarchy

```
                                  ┌────────────────────────────────────────────────────────┐
                                  │               Rishii (Frontend Lead & ML Mentor)       │
                                  │  • Leads Application Frontend (Next.js 15 / React 19)  │
                                  │  • Leads Chrome Browser Extension (for GeM Portal)     │
                                  │  • On-Demand ML Escalation: Steps in when Sahaj is stuck│
                                  └─────────────┬────────────────────────────┬─────────────┘
                                                │                            │
                     ┌──────────────────────────┴──────────┐      ┌──────────┴─────────────────────────┐
                     ▼                                     ▼      ▼                                    ▼
       ┌───────────────────────────┐         ┌───────────────────────────┐         ┌───────────────────────────┐
       │     Sahaj (ML / RAG Owner)│         │     Tanishka (UI/UX)      │         │    Prerak (Backend/DevOps)│
       ├───────────────────────────┤         ├───────────────────────────┤         ├───────────────────────────┤
       │ • Owns all ML & AI models │         │ • Figma Wireframes & UX   │         │ • FastAPI Microservices   │
       │ • Hybrid Search & Reranker│         │ • Multilingual Layouts    │         │ • Docker / Kubernetes     │
       │ • Neo4j Graph RAG queries │         │ • Regulatory Domain Flows │         │ • Async Document Pipelines│
       │ • Prompt Chains & Agents  │         │ • Frontend styling co-work│         │ • Background Workers      │
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
                    │ • Vector Schema & Indexes ││ • Ground-Truth Test Cases │
                    │ • Audit & Version Tables  ││ • Multilingual Speech QA  │
                    │ • Metadata filtering rules││ • 3-Tier Zero-Risk Backup │
                    └───────────────────────────┘└───────────────────────────┘
```

### Protocol for Rishii + Sahaj ML Collaboration:
1. **Sahaj owns day-to-day ML:** Sahaj writes the Python retrieval scripts, embedding ingestion, BM25 indexing, Neo4j Cypher queries, and LangGraph agent flows.
2. **Rishii acts as ML Senior Architect & Escalation Guide:** 
   - Rishii focuses primarily on building the frontend dashboards, evidence panels, and Chrome Extension.
   - If Sahaj hits a blocker (e.g. low retrieval recall, RRF ranking anomalies, complex Neo4j Cypher traversal errors, token overflow in context windows, or slow inference latency), **Rishii steps in immediately** to debug and optimize the algorithm.

---

## 2. Granular Roadmap: PS 26045 (IP-SAKTI Sahayak — Ministry of Ayush)

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                     PS 26045: IP-SAKTI Sahayak 5-Phase Implementation Plan                      │
├───────────────────┬───────────────────┬───────────────────┬───────────────────┬─────────────────┤
│ Phase 1: Corpus & │ Phase 2: Graph    │ Phase 3: Agents & │ Phase 4: Frontend │ Phase 5: QA &   │
│ Ingestion Setup   │ RAG & Embeddings  │ Wizard Logic      │ & Bhashini Voice  │ Live Jury Pitch │
├───────────────────┼───────────────────┼───────────────────┼───────────────────┼─────────────────┤
│ • Ingest Acts/Rules│ • bge-m3 dense    │ • Classification  │ • Next.js 3-pane  │ • Ragas test set│
│ • Supabase setup  │ • Neo4j Triples   │ • Dual Switch     │ • Bhashini ASR/TTS│ • Offline Docker│
│ • Metadata schema │ • Hybrid BM25     │ • ABS Form Router │ • Citation cards  │ • Pitch deck    │
└───────────────────┴───────────────────┴───────────────────┴───────────────────┴─────────────────┘
```

### Phase-by-Phase Task Breakdown for PS 26045

#### Phase 1: Knowledge Corpus & Relational Schemas (Days 1–3)
* **Sahaj (ML):** Parse full-text legal documents from India Code & e-Gazettes (*Patents Act 1970 with 2024 Rules*, *BD Act 2002 with 2023 Amendments & 2024 Rules*, *D&C Act Rule 158B*, *FSSAI Ayurveda-Aahar Regulations 2022*, *WIPO GRATK Treaty 2024*). Chunk by Section & Rule with rich metadata headers.
* **Diksha (DB):** Create Supabase / PostgreSQL tables for `statutes`, `sections`, `rules`, `forms`, `ayush_formulations`, and `audit_logs`. Configure `pgvector` or Qdrant collection with 1024-d index (`bge-m3`).
* **Prerak (Backend):** Set up FastAPI base repository with Docker Compose. Implement health check and authentication endpoints.
* **Tanishka (UX):** Research user journeys for Ayush startups vs rural *Vaidyas*. Design Figma mockups for the 3-pane research workbench and mobile voice card.
* **Rishii (Frontend):** Scaffold Next.js 15 app with Tailwind CSS, Lucide icons, and layout container components.

#### Phase 2: Hybrid Graph-RAG & Retrieval Reasoning (Days 4–6)
* **Sahaj (ML):**
  * Generate dense embeddings using `BAAI/bge-m3`.
  * Build BM25 sparse index over statutory sections.
  * Build Neo4j Knowledge Graph: nodes for `(:Act)`, `(:Section)`, `(:Rule)`, `(:Form)`, and `(:AyushCategory)` with relationships `[:CROSS_REFERENCES]`, `[:REQUIRES_FORM]`, `[:BARRED_BY_TK]`.
  * *(Escalation Trigger: If Cypher multi-hop query is slow or returning empty results, Rishii steps in to optimize the Cypher pattern and indexing).*
* **Prerak (Backend):** Build `/api/v1/search` endpoint integrating Sahaj's hybrid retriever with asynchronous streaming.
* **Member 6 (QA):** Create 25 ground-truth legal query-answer pairs covering Section 3(p) TK bar, Section 3(e) synergistic combinations, and NBA Form III approvals.

#### Phase 3: Formulation Classifier Wizard & Multi-Agent Supervisor (Days 7–9)
* **Sahaj (ML):** 
  * Implement the Formulation Classification Decision Tree in LangGraph:
    * *Check 1:* 54 First-Schedule Classical Texts $\rightarrow$ If yes, tag **Classical Medicine** (Defended by TKDL, Barred under § 3(p)).
    * *Check 2:* Standardized solvent extraction $\ge 4$ markers $\rightarrow$ Potential **Phytopharmaceutical Drug**.
    * *Check 3:* Synergistic proprietary modification $\rightarrow$ **Patent & Proprietary (P&P)**.
    * *Check 4:* Dietary wellness without disease cure claim $\rightarrow$ **FSSAI Ayurveda-Aahar**.
  * Implement the **Dual-Jurisdiction Switch Middleware**: Strict metadata scoping between `NATIONAL` (Indian Acts) and `INTERNATIONAL` (WIPO GRATK, PCT, US FDA Botanical Guidance, EU THMPD).
* **Prerak (Backend):** Implement `/api/v1/classify-formulation` and `/api/v1/abs-router` endpoints.
* **Rishii (Frontend):** Build the interactive step-by-step Formulation Wizard UI with real-time category badge updates.

#### Phase 4: Bhashini Vernacular Voice & Citation Workbench (Days 10–12)
* **Prerak & Sahaj:** Integrate Bhashini Speech-to-Text (ASR) and Text-to-Speech (TTS) APIs for Hindi, Sanskrit terms, Tamil, and Marathi.
* **Rishii (Frontend):**
  * Build the dynamic citation inspector: clicking on a citation (e.g. `[Patents Act § 3(p)]`) opens the exact gazette paragraph with highlighted text.
  * Implement Web Audio recording and playback component for mobile PWA view.
* **Tanishka (Design):** Finalize high-contrast mobile voice cards and ensure WCAG accessibility compliance.

#### Phase 5: Evaluation, Offline Dockerization & Pitch Prep (Days 13–14)
* **Member 6 & Sahaj:** Run Ragas evaluation (Context Recall $\ge 0.90$, Groundedness $\ge 0.95$).
* **Prerak & Diksha:** Lock down the 1-click offline `docker-compose.yml` image.
* **Rishii & Tanishka:** Prepare the 8-slide pitch deck and rehearse the 3-tier live demo sequence.

---

## 3. Granular Roadmap: PS 26108 (BIS Standards Engine — DoCA / BIS)

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                     PS 26108: BIS Standards Engine 5-Phase Implementation Plan                  │
├───────────────────┬───────────────────┬───────────────────┬───────────────────┬─────────────────┤
│ Phase 1: Dataset  │ Phase 2: PDF/BoQ  │ Phase 3: Hybrid   │ Phase 4: GeM Ext. │ Phase 5: Bench  │
│ Ingestion & Graph │ Extraction Engine │ RRF & QCO Checker │ & Spec Studio UI  │ & Live Pitch    │
├───────────────────┼───────────────────┼───────────────────┼───────────────────┼─────────────────┤
│ • Ingest 752 QCOs │ • Docling parser  │ • BM25 + bge-m3   │ • Chrome Ext. V3  │ • 4-Tender test │
│ • 30 CRS records  │ • BoQ Excel parser│ • Normative Graph │ • GeM autofill    │ • Docker image  │
│ • Master Catalog  │ • Technical regex │ • Version tracker │ • PDF NIT export  │ • Demo script   │
└───────────────────┴───────────────────┴───────────────────┴───────────────────┴─────────────────┘
```

### Phase-by-Phase Task Breakdown for PS 26108

#### Phase 1: Ingesting Pre-Compiled BIS Datasets & Graph Seeding (Days 1–3)
* **Diksha (DB):** Ingest `/Users/rishii/SIH-2026/data/` datasets:
  * `bis_mandatory_qco_scheme1.json` (752 ISI Mark QCO records).
  * `bis_mandatory_crs_scheme2.json` (30 MeitY CRS electronics records).
  * `indian_standards_master_catalog.json` (Taxonomy across 15 Division Councils).
  * `bis_normative_graph_triples.json` (Neo4j Graph Triples).
* **Sahaj (ML):** Set up dense vector embeddings on standard titles and scopes. Build an in-memory Trie index of valid IS numbers for deterministic zero-hallucination validation.
* **Prerak (Backend):** Set up FastAPI endpoints for standard lookup, QCO status query, and normative reference expansion.
* **Rishii (Frontend):** Scaffold the Desktop Procurement Workbench and initiate the Chrome Extension Manifest V3 boilerplate.
* **Tanishka (UX):** Map out the tender creation workflow on GeM (Government e-Marketplace) and design the specification generator interface.

#### Phase 2: Multi-Modal Tender Parser & Parameter Extractor (Days 4–6)
* **Sahaj (ML) & Prerak (Backend):**
  * Integrate `Docling` / `PyMuPDF` to parse multi-page tender PDFs and extract *Technical Eligibility Criteria* and *Schedule of Requirements*.
  * Implement tabular parsing for Excel BoQ sheets (`pandas` / `openpyxl`).
  * Build regex and NLP entity extractors for electrical ratings (11kV, 415V), structural grades (Fe-500D, M25), and material types (FRLSH, LTB2 Gunmetal).
  * *(Escalation Trigger: If unstructured PDF tables fail to parse cleanly, Rishii steps in to design a layout-aware bounding-box heuristic).*

#### Phase 3: Hybrid RRF Semantic Search & Normative Graph Expander (Days 7–9)
* **Sahaj (ML):**
  * Implement Reciprocal Rank Fusion (RRF) combining dense cosine similarity (`bge-m3`) and sparse BM25:
    $$\text{RRF Score}(d) = \frac{1}{60 + \text{Rank}_{\text{Dense}}(d)} + \frac{1}{60 + \text{Rank}_{\text{BM25}}(d)}$$
  * Implement the **Neo4j Normative Graph Traversal Engine**:
    $$\text{Primary Standard (IS 694)} \longrightarrow \text{Conductors (IS 8130)} \longrightarrow \text{Insulation (IS 5831)} \longrightarrow \text{Flame Test (IS 10810)}$$
  * Implement the **QCO Compliance Engine**: Checks if the product falls under mandatory ISI mark orders under Section 16 of the BIS Act 2016.
  * Implement the **Version Lifecycle Tracker**: Checks if standard is *Active*, *Superseded*, *Reaffirmed*, and attaches latest amendments (Amend. 1–3).

#### Phase 4: Chrome Browser Extension & GeM Spec Studio (Days 10–12)
* **Rishii (Frontend):**
  * Build the **Manifest V3 Chrome/Edge Browser Extension**:
    * Listens on `https://gem.gov.in/*` and `https://eprocure.gov.in/*`.
    * Floating sidebar widget that auto-detects item text entered by the procurement officer.
    * Queries the backend and displays: Recommended Standard, Mandatory QCO badge, Normative list, and a **`[+ Insert into Tender]`** button that auto-populates the GeM text area.
  * Build the **Desktop Specification Studio**: Generates formatted, copy-paste ready Technical Specification clauses and compliance tables.
* **Prerak & Diksha:** Build background PDF export service generating downloadable Notice Inviting Tender (NIT) documents.

#### Phase 5: Benchmark Evaluation, Offline Docker & Finale Pitch (Days 13–14)
* **Member 6 (QA):** Run the 4 benchmark evaluation tenders from [`sample_procurement_tenders_eval.json`](file:///Users/rishii/SIH-2026/data/sample_procurement_tenders_eval.json) to measure standard recommendation accuracy.
* **Prerak & Diksha:** Package the entire system into an air-gapped Docker Compose image with zero external API dependencies.
* **Rishii & Tanishka:** Prepare the 8-slide finale deck and record the 60fps backup demo video showing live GeM portal autofill.

---

## 4. 36-Hour Hackathon Grand Finale Hour-by-Hour Playbook

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                       36-Hour SIH Grand Finale Execution Timeline                           │
├───────────────────────┬───────────────────────┬─────────────────────┬───────────────────────┤
│ Hours 00 – 08         │ Hours 08 – 18         │ Hours 18 – 28       │ Hours 28 – 36         │
├───────────────────────┼───────────────────────┼─────────────────────┼───────────────────────┤
│ • Local Docker up     │ • Core Pipelines live │ • Mentoring Round 2 │ • UI Polish & Freeze  │
│ • Database seeding    │ • Mentoring Round 1   │ • Edge-case fix     │ • 3-Tier Demo Setup   │
│ • UI scaffolding      │ • Pivot on feedback   │ • Ragas evaluation  │ • Final Jury Pitch    │
└───────────────────────┴───────────────────────┴─────────────────────┴───────────────────────┘
```

| Hour Interval | Sahaj (ML & Models) | Rishii (Frontend & Extension) | Prerak & Diksha (Backend & DB) | Tanishka & Member 6 (UX & QA) |
| :--- | :--- | :--- | :--- | :--- |
| **H 00 – 04** | Verify embeddings & test hybrid RRF script locally. | Verify Next.js container & UI design tokens. | `docker-compose up`, verify Neo4j & Supabase seeding. | Review presentation slides & organize test dataset. |
| **H 04 – 10** | Wire RAG retrieval pipeline & Cypher queries to API. | Build dynamic streaming chat & evidence cards. | Test API latency; enable CORS & WebSocket / SSE stream. | Conduct manual testing on sample documents. |
| **H 10 – 14** | **MENTOR ROUND 1:** Showcase live RAG & graph traversal. | **MENTOR ROUND 1:** Demonstrate UI & live search. | Monitor backend logs during mentor interaction. | Capture all mentor feedback & requested tweaks. |
| **H 14 – 22** | **PIVOT SPRINT:** Tune prompts / add requested domain rules. | **PIVOT SPRINT:** Integrate Chrome Extension / Voice. | Add PDF export endpoint & optimize DB cache. | Update test cases based on mentor queries. |
| **H 22 – 28** | **MENTOR ROUND 2:** Showcase mentor feedback implementation. | **MENTOR ROUND 2:** Demonstrate GeM Extension / Voice. | Verify data consistency & container stability. | Run Ragas benchmarks & prepare evaluation charts. |
| **H 28 – 32** | Model freeze. Test zero-hallucination validation gate. | Code freeze. Polish UI micro-interactions & animations. | Test offline local Docker mode (disable WiFi to verify). | Verify all citations point to legitimate clauses. |
| **H 32 – 36** | Rehearse technical architecture explanation. | Lead live software demonstration during Jury Pitch. | Stand by server logs and container health monitor. | Manage slide transitions and timekeeping. |

---

## 5. Live Demonstration Protocol (3-Tier Zero-Risk Strategy)

To ensure the team never fails due to venue Wi-Fi drops or cloud API timeouts:
1. **Tier 1 (Primary — Live Cloud):** Hosted on Vercel (Frontend) + Render / AWS (FastAPI Backend + Managed Neo4j / Supabase).
2. **Tier 2 (Secondary — Local Air-Gapped Docker):** Entire stack running on Rishii’s or Prerak’s laptop via `docker-compose.yml` with local Ollama / vLLM model fallback and pre-seeded SQLite/Chroma/Neo4j.
3. **Tier 3 (Zero-Risk Fallback — 60fps Video Walkthrough):** Pre-recorded high-resolution walkthrough covering every user flow (Formulation Wizard, GeM Extension autofill, Normative Graph, Bhashini Voice).
