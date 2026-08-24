# 🇮🇳 AI-Powered Recommendation Engine for Indian Standards (BIS)

> **Smart India Hackathon (SIH 2026)** · **Problem Statement ID:** 26108  
> **Ministry:** Ministry of Consumer Affairs, Food & Public Distribution — Department of Consumer Affairs (DoCA) / Bureau of Indian Standards (BIS)  
> **Theme:** Smart Automation / Public Procurement  
> **Repository:** `github.com/rishiiicreates/SIH-2026`

---

## 📑 Table of Contents
1. [Overview & Problem Context](#-overview--problem-context)
2. [Key Features](#-key-features)
3. [System Architecture](#-system-architecture)
4. [Prerequisites](#-prerequisites)
5. [Step-by-Step Installation & Setup](#-step-by-step-installation--setup)
   - [Step 1: Clone the Repository](#step-1-clone-the-repository)
   - [Step 2: Supabase Database Setup](#step-2-supabase-database-setup)
   - [Step 3: Backend Configuration (.env)](#step-3-backend-configuration-env)
   - [Step 4: Python Virtual Environment & Dependencies](#step-4-python-virtual-environment--dependencies)
   - [Step 5: Ingest Standards Data into Database](#step-5-ingest-standards-data-into-database)
   - [Step 6: Run Automated Benchmark Evaluation](#step-6-run-automated-benchmark-evaluation)
   - [Step 7: Start the FastAPI Backend Server](#step-7-start-the-fastapi-backend-server)
   - [Step 8: Start the Next.js Frontend App](#step-8-start-the-nextjs-frontend-app)
6. [Interactive Web UI & Sample Queries](#-interactive-web-ui--sample-queries)
7. [API Documentation & Swagger UI](#-api-documentation--swagger-ui)
8. [Troubleshooting & Common Errors](#-troubleshooting--common-errors)
9. [Project Directory Layout](#-project-directory-layout)
10. [Documentation Index](#-documentation-index)

---

## 🎯 Overview & Problem Context

In India's public procurement ecosystem (>₹4 Lakh Crore annually across GeM, CPPP, Indian Railways IREPS, Defence, and State Portals), procurement officials routinely author technical specifications without standardization expertise.

With over **22,000+ Indian Standards (IS)** published by BIS:
1. **Vocabulary Mismatch:** Commercial trade descriptions (*"5 HP submersible agricultural pump"*) fail basic keyword searches for formal BIS titles (*"Submersible Pumpsets — Specification (IS 14220)"*).
2. **Outdated Standards:** Tenders cite withdrawn or superseded revisions (e.g. citing *IS 456:1978* instead of *IS 456:2000 Reaffirmed 2021*).
3. **Missing Normative References:** Tenders specify a primary product standard without citing mandatory testing standards (e.g., specifying a cable without *IS 10810* flame retardant test or *IS 8130* conductor purity).
4. **Omission of Mandatory QCOs:** Quality Control Orders (QCOs) issued under Section 16 of the BIS Act 2016 make standard compliance legally binding; omitting them causes legal disputes and substandard goods supply.

**Our Solution:** An automated, 3-stage recommendation engine that analyzes natural-language technical descriptions and delivers primary applicable standards, full normative testing trees, current lifecycle revisions, and mandatory QCO certification badges in under 2 seconds.

---

## ✨ Key Features

* **🧠 Semantic Vector Retrieval:** Powered by Google's `gemini-embedding-001` (768-dimensional dense vectors via Matryoshka Representation Learning) and Supabase `pgvector` cosine similarity search.
* **🛡️ Deterministic Reference Expansion:** Zero LLM hallucination risk. Relational join lookups instantly resolve normative raw material standards, test methods, component specifications, and installation codes.
* **📜 Regulatory & QCO Enforcement:** Automatically tags Central Ministry Quality Control Orders (DPIIT, Ministry of Steel, MeitY CRS, Ministry of Textiles) requiring mandatory ISI Mark (Scheme-I) or Compulsory Registration (Scheme-II).
* **🔄 Active Lifecycle & Amendment Guard:** Verifies current revision status, reaffirmation years, and latest active amendments.
* **🎨 Modern Web UI:** Clean, responsive Next.js 14 + Tailwind CSS dashboard with expandable reference accordions and color-coded tags.
* **📊 Automated Benchmark Test Harness:** Integrated evaluation suite verifying accuracy against real-world GeM, CPWD, WRD, and IREPS tenders.

---

## 🏗️ System Architecture

The engine follows a **3-stage linear pipeline** that strictly isolates probabilistic AI retrieval from deterministic regulatory logic:

```
┌─────────────────────────────────────────────────────────────┐
│  User Procurement Description (e.g. "5 HP submersible pump")│
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
 ┌───────────────────────────────────────────────────────────┐
 │ STAGE 1: AI Semantic Vector Retrieval                     │
 │ • Model: gemini-embedding-001 (768-dim via MRL)           │
 │ • DB: Supabase pgvector cosine similarity (<=>)           │
 │ • Output: Top-K Ranked Candidate Standards                │
 └─────────────────────────────┬─────────────────────────────┘
                               │
                               ▼
 ┌───────────────────────────────────────────────────────────┐
 │ STAGE 2: Deterministic Reference Expansion (Zero LLM)     │
 │ • SQL Join: standard_references table                     │
 │ • Output: Normative testing methods, raw materials, codes │
 └─────────────────────────────┬─────────────────────────────┘
                               │
                               ▼
 ┌───────────────────────────────────────────────────────────┐
 │ STAGE 3: Deterministic Regulatory & Metadata Enrichment   │
 │ • SQL Lookup: standards metadata columns                  │
 │ • Output: Latest revision, reaffirmation, QCO status      │
 └─────────────────────────────┬─────────────────────────────┘
                               │
                               ▼
 ┌───────────────────────────────────────────────────────────┐
 │ Output: Pydantic RecommendResponse / Next.js Result Cards │
 └───────────────────────────────────────────────────────────┘
```

---

## 💻 Prerequisites

Ensure you have the following installed on your machine:
* **Python:** `3.10`, `3.11`, or `3.12` ([Download Python](https://www.python.org/downloads/))
* **Node.js:** `18.x` or `20.x` LTS + `npm` ([Download Node.js](https://nodejs.org/))
* **Git:** Version control ([Download Git](https://git-scm.com/))
* **Gemini API Key:** Free tier from [Google AI Studio](https://aistudio.google.com/apikey)
* **Supabase Account & Project:** Free PostgreSQL database from [Supabase](https://supabase.com)

---

## 🚀 Step-by-Step Installation & Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/rishiiicreates/SIH-2026.git bis-standards-engine
cd bis-standards-engine
```

---

### Step 2: Supabase Database Setup

1. Log in to [Supabase](https://supabase.com/dashboard) and select (or create) your project.
2. In the left navigation sidebar, click on **SQL Editor** (icon with `>_`).
3. Click **New query**, open the [`supabase_schema.sql`](supabase_schema.sql) file from this repository, copy all contents, paste them into the SQL Editor, and click **Run**.

```sql
-- 1. Enable pgvector extension
create extension if not exists vector;

-- 2. Create standards table with 768-dim vector embedding
create table if not exists standards (
  standard_id text primary key,
  title text not null,
  scope text,
  embedding vector(768),
  latest_version text,
  amendment_date text,
  is_mandatory_qco boolean default false
);

-- 3. Create standard_references join table
create table if not exists standard_references (
  standard_id text references standards(standard_id),
  referenced_id text,
  referenced_title text,
  relationship_type text,
  primary key (standard_id, referenced_id)
);

-- 4. Create the match_standards vector search function
create or replace function match_standards(query_embedding vector(768), match_count int)
returns table (standard_id text, title text, similarity float)
language sql stable
as $$
  select standard_id, title, 1 - (embedding <=> query_embedding) as similarity
  from standards
  order by embedding <=> query_embedding
  limit match_count;
$$;

-- 5. Enable Row Level Security (RLS) policies for read & write
alter table standards enable row level security;
alter table standard_references enable row level security;

create policy "Allow public read access to standards" on standards for select using (true);
create policy "Allow public insert/update to standards" on standards for all using (true) with check (true);

create policy "Allow public read access to standard_references" on standard_references for select using (true);
create policy "Allow public insert/update to standard_references" on standard_references for all using (true) with check (true);
```
👉 *You will see: `Success. No rows returned`.*

---

### Step 3: Backend Configuration (`.env`)

1. Copy the example environment file inside `backend/`:
   ```bash
   cp backend/.env.example backend/.env
   ```
2. Open `backend/.env` in your code editor and populate your keys:
   ```env
   # Supabase Project URL & Anon/Service Key (from Project Settings -> API)
   SUPABASE_URL=https://your-project-ref.supabase.co
   SUPABASE_KEY=your-supabase-anon-or-service-role-key

   # Gemini API Key (from https://aistudio.google.com/apikey)
   GEMINI_API_KEY=your-gemini-api-key
   ```

---

### Step 4: Python Virtual Environment & Dependencies

Navigate to the `backend/` directory, create a virtual environment, and install required packages:

#### On macOS / Linux:
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

#### On Windows (PowerShell / Command Prompt):
```powershell
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

---

### Step 5: Ingest Standards Data into Database

With your virtual environment activated, run the ingestion script to embed and populate the verified Indian Standards catalog into Supabase:

```bash
python scripts/ingest_standards.py
```

**Expected Terminal Output:**
```text
Processing IS 694:2010...
Processing IS 7098 (Part 1):1988...
Processing IS 1180 (Part 1):2014...
Processing IS 456:2000...
Processing IS 1786:2008...
Processing IS 1489 (Part 1):2015...
Processing IS 14220:2018...
Processing IS 778:1984...
Processing IS 13252 (Part 1):2010...
Processing IS 10322 (Part 5/Sec 1):2012...
Processing IS 16391:2015...
Ingestion completed successfully.
```

---

### Step 6: Run Automated Benchmark Evaluation

To verify that vector retrieval, reference expansion, and QCO classification are functioning with high accuracy across real public procurement tenders:

```bash
python scripts/evaluate_benchmarks.py
```

**Benchmark Results:**
```text
===========================================================================
📊 BIS STANDARDS RECOMMENDATION ENGINE — BENCHMARK EVALUATION HARNESS
===========================================================================
• Total Tenders Evaluated:     4 (GeM, CPWD, WRD, IREPS)
• Top-1 Accuracy:              100.0% (4/4)
• Top-3 Recall (Ground Truth): 100.0% (8/8 ground truth standards captured)
• MRR (Mean Reciprocal Rank):  1.000
• QCO Mandatory Accuracy:      100.0%
• Avg Retrieval Latency:       1414.5 ms
===========================================================================
```

---

### Step 7: Start the FastAPI Backend Server

```bash
uvicorn app.main:app --port 8000 --reload
```

* **API Health Check:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* **Interactive Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

### Step 8: Start the Next.js Frontend App

Open a **new terminal window**, navigate to `frontend/`, and run:

```bash
cd frontend
npm install
npm run dev
```

Open your browser at: 🌐 **[http://localhost:3000](http://localhost:3000)** *(or port `3001` if `3000` is in use)*.

---

## 🔍 Interactive Web UI & Sample Queries

Try pasting any of these real-world procurement queries into the search bar:

### 1. Electrical Cables & Wiring
* **Input Query:** `"PVC insulated copper cable for electrical wiring in residential buildings"`
* **Recommended Standard:** `IS 694:2010` *(PVC Insulated Cables up to 1100V)*
* **Compliance Badge:** `✓ QCO Mandatory` *(DPIIT Wires and Cables Order)*
* **Normative References:**
  * `[RAW_MATERIAL]` `IS 8130:2013` (Conductors for electric cables)
  * `[RAW_MATERIAL]` `IS 5831:1984` (PVC insulation and sheath compounds)
  * `[TEST_METHOD]` `IS 10810 (Part 41, 61, 62)` (Oxygen index, flame retardance, fire resistance)
  * `[INSTALLATION_CODE]` `IS 732:2019` (Code of practice for electrical wiring installations)

### 2. Agricultural & Irrigation Pumps
* **Input Query:** `"5 HP Three-Phase submersible agricultural borewell pump"`
* **Recommended Standard:** `IS 14220:2018` *(Submersible Pumpsets)*
* **Compliance Badge:** `✓ QCO Mandatory` *(DPIIT / Heavy Industries Order)*
* **Normative References:**
  * `[COMPONENT]` `IS 9283:2013` (Motors for submersible pumpsets)
  * `[TEST_METHOD]` `IS 11346:2002` (Acceptance tests for pumps)
  * `[SAFETY_CODE]` `IS 3043:2018` (Code of practice for earthing)

### 3. Civil & Structural Steel
* **Input Query:** `"Fe 500D TMT reinforcement steel bars for foundation RCC columns"`
* **Recommended Standard:** `IS 1786:2008` *(High Strength Deformed Steel Bars for Concrete Reinforcement)*
* **Compliance Badge:** `✓ QCO Mandatory` *(Ministry of Steel Order)*
* **Normative References:**
  * `[TEST_METHOD]` `IS 1608 (Part 1):2018` (Metallic tensile test)
  * `[TEST_METHOD]` `IS 1599:2019` (Bend test)
  * `[INSTALLATION_CODE]` `IS 2502:1963` (Bending and fixing of reinforcement bars)

---

## 📡 API Documentation & Swagger UI

### `POST /api/v1/recommend`

#### Request Body
```json
{
  "query": "5 HP submersible agricultural pump",
  "top_k": 5
}
```

#### Response (200 OK)
```json
{
  "query": "5 HP submersible agricultural pump",
  "recommendations": [
    {
      "standard_id": "IS 14220:2018",
      "title": "Submersible Pumpsets - Specification",
      "similarity": 0.7495,
      "references": [
        {
          "referenced_id": "IS 9283:2013",
          "title": "Motors for submersible pumpsets - Specification",
          "relationship_type": "COMPONENT"
        },
        {
          "referenced_id": "IS 11346:2002",
          "title": "Code for acceptance tests for agricultural and water supply pumps",
          "relationship_type": "TEST_METHOD"
        }
      ],
      "metadata": {
        "latest_version": "First Revision, Reaffirmed 2023 - Amendment No. 1 (2020), Amendment No. 2 (2022)",
        "amendment_date": "2022",
        "is_mandatory_qco": true
      }
    }
  ],
  "total_results": 1
}
```

---

## 🛠️ Troubleshooting & Common Errors

| Issue / Error | Cause | Fix |
|---|---|---|
| `function match_standards does not exist` | Supabase SQL schema was not executed | Run [`supabase_schema.sql`](supabase_schema.sql) in your Supabase SQL Editor. |
| `RuntimeError: SUPABASE_URL and SUPABASE_KEY must be configured` | Missing `backend/.env` file | Create `backend/.env` and paste your Supabase URL & Key. |
| `RuntimeError: GEMINI_API_KEY is not set in environment` | Missing Gemini key in `backend/.env` | Add `GEMINI_API_KEY=` in `backend/.env`. |
| `Failed to fetch recommendations` in UI | Backend server is not running | Ensure `uvicorn app.main:app --port 8000` is active. |
| `EADDRINUSE: address already in use :::3000` | Port 3000 is occupied by another app | Run Next.js on port 3001: `npm run dev -- -p 3001`. |
| Windows PowerShell: `running scripts is disabled on this system` | Execution policy restricted | Run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` before activating `.venv`. |

---

## 📁 Project Directory Layout

```
bis-standards-recommendation-engine/
├── supabase_schema.sql            # Complete Supabase PostgreSQL + pgvector + RLS setup
├── backend/
│   ├── app/
│   │   ├── db/
│   │   │   ├── client.py          # Fail-fast Supabase client singleton
│   │   │   └── schema.sql         # Backend copy of DB schema
│   │   ├── models/
│   │   │   └── schemas.py         # Pydantic request/response schemas
│   │   ├── routers/
│   │   │   └── recommend.py       # POST /recommend 3-stage endpoint
│   │   ├── services/
│   │   │   ├── retrieval.py       # Gemini 768-dim embedding + pgvector search
│   │   │   ├── reference_expand.py# Deterministic normative references join
│   │   │   └── metadata.py        # Deterministic QCO & version lookup
│   │   ├── config.py              # Environment configuration
│   │   └── main.py                # FastAPI app initialization + CORS
│   ├── scripts/
│   │   ├── ingest_standards.py    # Embeds & populates catalog into Supabase
│   │   └── evaluate_benchmarks.py # Benchmark test harness (4 real tenders)
│   ├── requirements.txt           # Python dependencies
│   ├── .env.example               # Environment template
│   └── README.md
├── frontend/                      # Next.js 14 App Router
│   ├── app/
│   │   ├── page.tsx               # Main single-view search dashboard
│   │   ├── layout.tsx             # Root layout & meta tags
│   │   └── globals.css            # Tailwind & global styles
│   ├── components/
│   │   ├── SearchBar.tsx          # Large search input with loading state
│   │   ├── ResultCard.tsx         # Standard card with similarity %, QCO badge
│   │   └── ReferenceList.tsx      # Expandable normative references list
│   ├── lib/
│   │   └── api.ts                 # Backend API client
│   ├── types/
│   │   └── index.ts               # Shared TypeScript domain interfaces
│   ├── package.json
│   ├── tailwind.config.ts
│   └── next.config.mjs
├── data/                          # The 8 official BIS datasets
│   ├── indian_standards_master_catalog.json (11 verified primary standards)
│   ├── bis_mandatory_qco_scheme1.json (752 ISI Mark QCO records)
│   ├── bis_mandatory_crs_scheme2.json (30 CRS Scheme-II records)
│   ├── bis_normative_graph_triples.json (53 normative triples)
│   └── sample_procurement_tenders_eval.json (4 benchmark tenders)
├── ARCHITECTURE.md                # 3-stage pipeline architecture design
├── STACK.md                       # Confirmed stack documentation
├── DATA_SOURCES.md                # Data collection standards & manual curation
├── ROADMAP.md                     # V1 scope & milestone timeline
├── SCRAPING.md                    # Data entry guide for team members
├── GEMINI.md                      # AI developer rules & constraints
├── PROBLEM_STATEMENT.md           # Verbatim PS 26108 problem statement
├── PS_26108_BIS_Standards_Procurement_Master_Blueprint.md
└── README.md
```

---

## 📚 Documentation Index

To explore specific architectural decisions and guides, read the documentation in this order:
1. [`PROBLEM_STATEMENT.md`](PROBLEM_STATEMENT.md) — Official SIH 2026 PS 26108 definition.
2. [`ARCHITECTURE.md`](ARCHITECTURE.md) — Detailed 3-stage retrieval, expansion, and metadata design.
3. [`STACK.md`](STACK.md) — Confirmed technology choices and superseded alternatives.
4. [`DATA_SOURCES.md`](DATA_SOURCES.md) — Manual curation methodology and BIS catalog sources.
5. [`ROADMAP.md`](ROADMAP.md) — Sprint timeline and V1 feature guarantees.
6. [`SCRAPING.md`](SCRAPING.md) — Step-by-step data entry guide for expanding the standard corpus.
7. [`GEMINI.md`](GEMINI.md) — Strict rules and constraints for AI agents.

---

## 👥 Team
Built with ❤️ for **Smart India Hackathon 2026** by Team **PS 26108**.
