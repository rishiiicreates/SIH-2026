# Web Scraping — BIS Standards & GeM Tenders

Two separate scraping targets with different shapes, different
scales, and different timelines. Do not build one generic scraper for
both — they need different logic.

## Target 1: BIS standards data (needed now, ~100-150 records)

**Source**: bis.gov.in "Know Your Standard" and/or manakonline.in.
Both are browsable, not bulk-exportable — see DATA_SOURCES.md.

**What to extract per standard**: standard_id, title, scope, latest
version, amendment date, normative references (from the PDF's own
front matter — this may need PDF text extraction, not just HTML
scraping), mandatory QCO status.

**Scale**: 100-150 standards is small enough that semi-manual
scraping (a script that fetches each known standard's page + a human
spot-checking output) is more reliable than a fully autonomous
crawler right now. Don't over-invest in crawler robustness for a
one-time 150-row pull — that effort is better spent later, at
backlog item #1 (scaling to 500+), where volume actually justifies
it.

**Stack**: `requests` + `BeautifulSoup4` for static HTML pages.
If any pages are JS-rendered, use `Playwright` instead (see existing
project notes — both are already known/used tools, no new library
needed).

**Output**: write directly into `backend/data/standards_seed.csv`
(matches the schema in DATA_SOURCES.md), so it feeds straight into
`ingest_standards.py` without a translation step.

## Target 2: GeM tender/BoQ documents (needed later, for backlog item #2/#3 testing — scaling comes after)

**Source**: gem.gov.in public tender listings.

**Purpose**: these are test *input* documents (to validate the
PDF/BoQ upload feature), not data that gets embedded into the
standards corpus. Keep this scraper and its output completely
separate from Target 1 — different purpose, different pipeline.

**What to extract**: raw tender/NIT PDF files, or BoQ Excel sheets,
as-is. No parsing needed at scrape time — parsing happens later in
`services/pdf_extract.py` (backlog item #2), not in the scraper.

**Scale note**: "just a handful now, more later" — start with maybe
10-20 sample tenders to build/test the upload feature, revisit volume
when backlog item #3 (multi-item BoQ extraction) is actually being
built.

**Stack**: same as Target 1 — `requests`/`BeautifulSoup4`, or
`Playwright` if the listing page is JS-rendered or requires
interaction (pagination, filters) to reach individual tender PDFs.

## Rules for both scrapers

- **Check `robots.txt` first** (`bis.gov.in/robots.txt`,
  `gem.gov.in/robots.txt`) before writing the scraper, and don't
  crawl disallowed paths. Not legally binding by itself, but ignoring
  it is the fastest way to get blocked mid-project — a real risk with
  a Sep 1 / Dec deadline.
- **Rate limit deliberately** — add a delay between requests (e.g.
  1-2 seconds), don't hammer either site. These are government
  portals; getting IP-blocked would stall the whole data pipeline.
- **Cache raw fetched pages/PDFs locally** before parsing, so a
  parsing bug doesn't mean re-scraping from scratch.
- **No login-walled or personal data** — everything scraped here is
  public tender/standard listing data, not user accounts or private
  submissions. Stay within that boundary.
- **This is public-interest, non-commercial student data
  acquisition** — still worth checking each site's terms of service
  once before scaling up scraping volume, particularly before backlog
  item #1's larger pull.

## Where new files go (matches existing file structure)

```
backend/
├── scripts/
│   ├── ingest_standards.py        # existing — loads seed CSV into DB
│   ├── scrape_bis_standards.py    # NEW — Target 1, writes standards_seed.csv
│   └── scrape_gem_tenders.py      # NEW — Target 2, writes to data/sample_tenders/
├── data/
│   ├── standards_seed.csv         # existing
│   └── sample_tenders/            # NEW — raw PDFs/Excels for testing upload feature
```
