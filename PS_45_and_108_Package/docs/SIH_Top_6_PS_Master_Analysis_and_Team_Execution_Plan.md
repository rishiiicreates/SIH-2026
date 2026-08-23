# SIH 2026 — Top 6 Problem Statements Master Analysis & Execution Plan
**Comprehensive Technical, Architectural, and Team-Fit Report**  
**Problem Statements Covered:** `PS 26045` • `PS 26107` • `PS 26108` • `PS 26130` • `PS 26100` • `PS 26101`  

---

## 1. Executive Comparison & Ranking Matrix

| Rank | Problem Statement ID | Core System & Theme | Primary RAG / AI Architecture | Team Fit | Primary Risk Factor | Recommended Decision |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | **PS 26045** | **IP-SAKTI Sahayak**<br>*(Ayurveda IPR & Regulatory Assistant)* | Core RAG + Neo4j Graph + Multi-Agent Orchestration + Bhashini Voice | **10/10** | Sourcing verified gazettes and statutory copyright. | **Best Overall Fit:** Maximum AI differentiation, high national impact (Ayush heritage). |
| **2** | **PS 26107** | **BIS Intelligent Assistant**<br>*(Standards & BIS Services for MSMEs)* | Full RAG over BIS documents + Certification Router | **9.5/10** | Incomplete public standard text datasets. | **Safest Pure-RAG:** Easiest to demo, high public utility. |
| **3** | **PS 26108** | **Indian Standards Recommendation**<br>*(Procurement Specs on GeM/CPPP)* | Semantic RAG + Normative Graph + QCO Compliance Engine | **10/10** | Version/revision accuracy on obscure standards. | **Best Graph-RAG:** Highly technical, live Chrome Extension on GeM creates massive jury impact. |
| **4** | **PS 26130** | **Industrial Approvals Platform**<br>*(Govt of Maharashtra Single Window)* | RAG over State Policies + Workflow State Machine + Timeline Automation | **10/10** | State-level regulatory scope explosion. | **Best Workflow Automation:** Differentiator is the deterministic approval engine. |
| **5** | **PS 26100** | **Integrated Bid Compliance**<br>*(MoPNG / GeM Tender Verification)* | Document AI (OCR) + RAG over GCC/GeM Rules + Deterministic Checks | **9/10** | Simulating government verification APIs (GST/PAN). | **Best Enterprise Product:** High business value for public procurement officers. |
| **6** | **PS 26101** | **AI Learning & Competency Platform**<br>*(MoSPI / iGOT Karmayogi)* | RAG over Statistical Courseware + Adaptive MCQs + Competency Graph | **9/10** | Modeling complex civil-service competency taxonomies. | **Best EdTech Product:** High data accessibility, great visual assessment flow. |

---

## 2. Deep Dive Analysis Across All 6 Problem Statements

---

### 1. PS 26045: IP-SAKTI Sahayak (Ministry of Ayush)
* **Goal:** A multilingual, source-grounded AI assistant navigating Ayurvedic IPR (Patents, TM, GI, Plant Varieties), Access & Benefit Sharing (Biological Diversity Act 2023), and drug/food licensing (D&C Rule 158B, FSSAI Ayurveda-Aahar).
* **System Breakdown:**
  1. *Formulation Classification Wizard:* Interactive dialogue determining Classical vs P&P vs New Drug vs Phytopharmaceutical vs Ayurveda-Aahar vs Cosmetic.
  2. *Dual-Jurisdiction Switch:* Domestic Indian Laws vs International Treaties (WIPO GRATK 2024, PCT, Nagoya, US FDA, EU THMPD).
  3. *ABS Compliance Helper:* Routes Indian/Foreign entities to NBA Forms I, II, III, IV.
  4. *Vernacular Voice:* Speech-to-speech interaction via Bhashini ASR/TTS.
* **Team Ownership:**
  - *Rishii (Frontend & ML Co-Lead):* Research workbench UI, formulation wizard, confidence scoring & citation verification regex.
  - *Sahaj (AI Lead):* Multi-agent supervisor, hybrid BM25 + dense search, Neo4j statutory graph.
  - *Tanishka (Design & Research):* Legal UX, formulation question flows, design tokens.
  - *Prerak (Backend):* FastAPI microservices, Bhashini API integration, Docker deployment.
  - *Diksha (Database):* Supabase schemas, vector store, audit trail tables.
  - *Member 6 (QA):* Ayush case-law test cases, citation accuracy benchmarks.

---

### 2. PS 26107: Intelligent Assistant for Indian Standards & BIS Services (DoCA)
* **Goal:** AI assistant helping industries, consumers, and labs understand Indian Standards, ISI mark licensing, Compulsory Registration Scheme (CRS), hallmarking, and lab test facilities.
* **System Breakdown:**
  1. *Product-to-Standard Mapper:* Maps colloquial consumer product queries to exact IS numbers.
  2. *Certification & Licensing Guide:* Explains step-by-step procedures for obtaining Scheme-I (ISI Mark) and Scheme-II (CRS) licenses.
  3. *Hallmarking & Lab Locator:* Interactive map and search tool for BIS-recognized testing laboratories.
* **Team Ownership:**
  - *Rishii & Tanishka:* Clean consumer/MSME chatbot UI, lab map locator, standards cards.
  - *Sahaj & Rishii:* Semantic retrieval over BIS catalogs, prompt engineering for certification procedures.
  - *Prerak & Diksha:* BIS data ingestion, vector indexing, caching layer for fast search.
  - *Member 6:* User query test bank (consumer complaints, MSME licensing questions).

---

### 3. PS 26108: Standards Recommendation Engine for Procurement (DoCA / BIS)
* **Goal:** Ingest tender descriptions and BoQ tables, recommend primary and normative Indian Standards, and enforce mandatory Quality Control Orders (QCOs).
* **System Breakdown:**
  1. *Tender Document Parser:* Layout-aware PDF/Excel parser extracting technical specifications.
  2. *Normative Graph Expansion:* Neo4j graph linking Primary Standards $\rightarrow$ Raw Materials $\rightarrow$ Test Methods $\rightarrow$ Installation Safety Codes.
  3. *QCO Legal Safeguard:* Validates whether products are mandated for ISI marking under Central Government orders.
  4. *GeM Chrome Extension:* Injects live recommendations directly into active GeM tender creation screens.
* **Team Ownership:**
  - *Rishii (Frontend & Extension):* Manifest V3 Chrome Extension, Tender Clause Studio, RRF algorithm design.
  - *Sahaj (AI/RAG):* Hybrid search pipeline, Neo4j Cypher normative expander.
  - *Tanishka (UX & Research):* GeM workflow analysis, clause comparison view design.
  - *Prerak (Backend):* PDF parsing microservice (Docling), background processing.
  - *Diksha (Database):* BIS catalog storage, QCO gazette database, vector embeddings.
  - *Member 6 (QA):* Real-world tender evaluation benchmark test suite.

---

### 4. PS 26130: Streamlining Industrial Approvals (Govt of Maharashtra)
* **Goal:** A workflow automation and regulatory intelligence platform that generates customized industrial clearance checklists, tracks document lifecycles, and manages parallel approval workflows under the Maharashtra Single Window Act.
* **System Breakdown:**
  1. *Business Profile Classifier:* Evaluates sector, land zone, investment bracket, and power/water requirements.
  2. *Approval Dependency Engine:* Builds directed acyclic graphs (DAG) of serial vs parallel clearance paths (MIDC, MPCB Consent to Establish, Fire NOC, DISH).
  3. *Document Validator & Expiry Tracker:* Tracks pre-conditions, renewals, and statutory compliance timelines.
* **Team Ownership:**
  - *Rishii & Tanishka:* Business onboarding wizard, interactive approval timeline Gantt/DAG view.
  - *Sahaj & Rishii:* Policy RAG over Maharashtra Industrial Policy and NOC checklists.
  - *Prerak & Diksha:* Finite state machine (FSM) backend, notification workers, document storage.
  - *Member 6 (QA):* Multi-sector industrial scenario testing (chemical, textile, IT).

---

### 5. PS 26100: AI Integrated Bid Compliance Platform for GeM (MoPNG)
* **Goal:** Automatically evaluates vendor bids against tender technical criteria, General Conditions of Contract (GCC), and GeM procurement rules using document AI and deterministic rule engines.
* **System Breakdown:**
  1. *Bid Document OCR & Entity Extractor:* Extracts data from balance sheets, ISO certificates, Make-in-India declarations, and OEM authorization letters.
  2. *Deterministic Verification Layer:* Programmatically checks PAN, GST format, turnover thresholds, and blacklisting registries.
  3. *RAG Compliance Reasoner:* Interprets qualitative technical eligibility clauses and highlights discrepancies.
* **Team Ownership:**
  - *Rishii & Tanishka:* Enterprise compliance officer dashboard, side-by-side bid verification matrix.
  - *Sahaj & Rishii:* Clause interpretation RAG, discrepancy detection algorithms.
  - *Prerak & Diksha:* High-throughput OCR pipeline, document storage, audit log schema.
  - *Member 6 (QA):* Synthetic bidder dataset generation with intentional compliance flaws for testing.

---

### 6. PS 26101: AI Learning & Assessment Platform for iGOT (MoSPI)
* **Goal:** Identifies statistical and domain competency gaps among government officials, recommends customized training paths, and automatically generates verifiable MCQs and case quizzes from courseware.
* **System Breakdown:**
  1. *Competency Ontology Graph:* Maps statistical concepts (sampling, econometric modeling, data visualization) to job roles.
  2. *Adaptive Quiz Generator:* Generates distractors, answer keys, and source-cited explanations from uploaded PDFs.
  3. *Personalized Learning Path:* Updates competency mastery states based on quiz performance.
* **Team Ownership:**
  - *Rishii & Tanishka:* Interactive quiz interface, radar-chart competency mastery dashboard.
  - *Sahaj & Rishii:* RAG over statistical textbooks, MCQ generation & hallucination validation prompts.
  - *Prerak & Diksha:* Learner progress API, quiz state management, courseware vector index.
  - *Member 6 (QA):* Statistical curriculum QA, MCQ validation test set.

---

## 3. Shared Reusable Engineering Foundation

All six problem statements share a unified architectural backbone, ensuring zero wasted effort during early prototyping:
* **Frontend:** Next.js 15 / React 19 + Tailwind CSS + Lucide Icons + Web Audio API.
* **Backend:** FastAPI (Python 3.11) with async endpoints and Server-Sent Events (SSE).
* **Database:** PostgreSQL / Supabase with `pgvector` extension for metadata & vectors.
* **Graph DB:** Neo4j Community Edition (Dockerized) for relational ontologies.
* **Evaluation:** Ragas Framework (Context Precision, Faithfulness, Answer Relevance).
