# Data Sources

## The core constraint

**There is no public bulk API or downloadable dataset for Indian
Standards.** This was directly checked (web search, Aug 2026) — BIS
does not offer a bulk export. Data acquisition is manual/scraped
work, not a solved problem. Any suggestion that assumes an API exists
should be treated as wrong until proven otherwise.

## Standards corpus (title, scope, references, version, QCO status)

- **bis.gov.in "Know Your Standard"** — free, searchable by IS number
  or keyword. Gives title, status, amendments, related docs. Browsable
  only, not bulk-exportable — must be looked up standard-by-standard.
- **manakonline.in** — BIS's newer standardization portal, catalogue
  listing. Same constraint: browsable, not bulk-downloadable.
- **Individual IS PDF front matter** — every standard document lists
  its own "Normative References" section. This is the actual source
  of truth for the reference graph (stage 3 of the pipeline) — not a
  database anywhere, the documents themselves. Some are available
  free via BIS's "download indigenous standards free of cost" page;
  others are behind BIS's paid distributor (BSB Edge).
- **QCO (Quality Control Order) list** — BIS publishes which product
  categories fall under mandatory certification (Section 16 of the
  BIS Act). This needs to be captured as a lookup table, not inferred.

## Test/input data (sample tenders, BoQs)

- **GeM portal (gem.gov.in)** — publishes past tenders/NIT documents
  publicly. Scrape a sample set as realistic test input for the
  PDF/BoQ upload feature (backlog item #2/#3). This is separate from
  the standards corpus — it's what we feed the system to test it, not
  what we retrieve from.

## Practical acquisition strategy by phase

- **V1**: hand-curate ~50-100 standards in one domain (e.g.,
  electrical/cable, matching the PS's own examples) by manually
  reading their BIS pages and PDF front matter once. Small but
  complete — every field genuinely filled in, not mocked.
- **Backlog item #1 (corpus expansion)**: same method, scaled and
  parallelized across the team — this is the highest value-per-effort
  backlog item precisely because it needs no new code, only more data
  entry against the same schema.
- **Backlog item #4 (version/amendment auto-tracking)**: once the
  static approach is proven, a scheduled scraper can re-check BIS
  pages periodically instead of manual re-entry.

## Seed file schema (`backend/data/standards_seed.csv`)

Columns: `standard_id, title, scope, latest_version, amendment_date,
is_mandatory_qco, referenced_standard_ids`

`referenced_standard_ids` gets normalized into the join table
(`standard_id → referenced_id`) by `ingest_standards.py` — don't
store it as a single denormalized field in the live DB.
