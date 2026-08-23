# File Structure — PS 26108

```
SIH-2026/
├── README.md
├── ARCHITECTURE.md
├── STACK.md
├── DATA_SOURCES.md
├── ROADMAP.md
├── SCRAPING.md
├── GEMINI.md
├── data/
│   ├── indian_standards_master_catalog.json  ← 11 verified standards (seed data)
│   ├── bis_mandatory_qco_scheme1.json       ← 752 QCO Scheme-I records
│   ├── bis_mandatory_crs_scheme2.json       ← 30 CRS Scheme-II records
│   ├── bis_normative_graph_triples.json     ← 53 reference triples
│   └── sample_procurement_tenders_eval.json ← 4 benchmark tenders
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              ← FastAPI app with CORS
│   │   ├── config.py            ← Settings (GEMINI_API_KEY, SUPABASE_URL/KEY)
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   └── recommend.py     ← POST /api/v1/recommend
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── retrieval.py     ← embed_text() + search() via pgvector
│   │   │   ├── reference_expand.py ← deterministic join query
│   │   │   └── metadata.py      ← deterministic single-row lookup
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── schemas.py       ← Pydantic request/response models
│   │   └── db/
│   │       ├── __init__.py
│   │       ├── client.py        ← Supabase client singleton
│   │       └── schema.sql       ← SQL migration (tables + RPC)
│   ├── scripts/
│   │   └── ingest_standards.py  ← Reads catalog JSON, embeds, upserts
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
└── frontend/
    ├── app/
    │   ├── page.tsx             ← Search + results (only view)
    │   ├── layout.tsx           ← Root layout
    │   └── globals.css
    ├── components/
    │   ├── SearchBar.tsx
    │   ├── ResultCard.tsx       ← IS number, title, version, QCO badge
    │   └── ReferenceList.tsx    ← Flat expandable reference list
    ├── lib/
    │   └── api.ts               ← POST /api/v1/recommend
    ├── package.json
    ├── tsconfig.json
    ├── tailwind.config.ts
    ├── next.config.ts
    └── postcss.config.mjs
```
