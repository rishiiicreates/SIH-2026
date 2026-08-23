# SIH-2026 — AI-Powered Recommendation Engine for Indian Standards

**Problem Statement:** PS 26108  
**Ministry:** Consumer Affairs, Food & Public Distribution (DoCA) / Bureau of Indian Standards (BIS)  
**Category:** Software · **Theme:** Smart Automation  

> Given a plain-text product description (e.g., *"5 HP submersible agricultural pump"*), recommend
> the applicable Indian Standards (IS), their normative references, version info, and QCO
> mandatory status.

---

## Quick Start

### Backend
```bash
cd backend
cp .env.example .env   # Fill in your Supabase + Gemini API keys
pip install -r requirements.txt

# Run the SQL in app/db/schema.sql in your Supabase SQL editor first

# Ingest seed data
python scripts/ingest_standards.py

# Start the server
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000 and try: *"PVC insulated copper cable for building wiring"*

---

## Architecture

3-stage linear pipeline:
1. **Retrieval** (AI) — embed query via `gemini-embedding-001`, pgvector similarity search
2. **Reference Expansion** (deterministic) — join query against `standard_references` table
3. **Metadata** (deterministic) — single-row lookup for version, amendments, QCO status

See [ARCHITECTURE.md](ARCHITECTURE.md) for full details.

## Stack
- **Backend:** Python / FastAPI / Supabase (pgvector)
- **Embeddings:** Gemini API (`gemini-embedding-001`, 768-dim)
- **Frontend:** Next.js / TypeScript / Tailwind CSS
- **Deploy:** Vercel (frontend) + Supabase (backend)

See [STACK.md](STACK.md) for decisions and rationale.

## Documentation
Read in this order:
1. [ARCHITECTURE.md](ARCHITECTURE.md) — system design
2. [STACK.md](STACK.md) — technology choices
3. [DATA_SOURCES.md](DATA_SOURCES.md) — where data comes from
4. [ROADMAP.md](ROADMAP.md) — timeline and scope
5. [SCRAPING.md](SCRAPING.md) — data collection guide
6. [GEMINI.md](GEMINI.md) — hard rules for AI assistants

## Data
- 11 verified Indian Standards in `data/indian_standards_master_catalog.json`
- 752 QCO Scheme-I records in `data/bis_mandatory_qco_scheme1.json`
- 30 CRS Scheme-II records in `data/bis_mandatory_crs_scheme2.json`
- 53 normative reference triples in `data/bis_normative_graph_triples.json`

## Team
Built for the **Smart India Hackathon 2026** internal round (Sep 1, 2026).
