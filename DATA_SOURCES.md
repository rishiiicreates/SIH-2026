# Data Sources — PS 26108

## Primary Data Source
**Manual curation** from [bis.gov.in](https://www.bis.gov.in) "Know Your Standard" pages
and each standard's own PDF front matter for normative reference lists.

There is **no bulk BIS API or downloadable dataset**. Every standard entry is hand-verified.

## Current Seed Data (in `/data/`)

| File | Records | Description |
|------|---------|-------------|
| `indian_standards_master_catalog.json` | 11 standards | Primary standards with full normative refs, QCO details, allied standards, keywords |
| `bis_mandatory_qco_scheme1.json` | 752 records | Official Scheme-I (ISI Mark) mandatory products |
| `bis_mandatory_crs_scheme2.json` | 30 records | Official Scheme-II (CRS) mandatory electronics/IT |
| `bis_normative_graph_triples.json` | 53 triples | Reference relationships between standards |
| `sample_procurement_tenders_eval.json` | 4 tenders | Real-world benchmark evaluation tenders |

## V1 Target
50–100 standards in the electrical/cable domain. The current 11 entries prove the pipeline
end-to-end. The remaining 40–90 are parallelizable data-entry work for the team.

## Data Entry Process
1. Search bis.gov.in for the standard number
2. Record: IS number, year, revision, title, reaffirmed year, status
3. Extract normative references from the standard's clause 2 / front matter
4. Check QCO status against DPIIT gazette notifications
5. Add to `indian_standards_master_catalog.json`
6. Run `ingest_standards.py` to embed and load into Supabase
