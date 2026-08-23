# Roadmap

## Timeline

- **Aug 26, 2026** — Idea PPT submission deadline. Deliverable:
  6-slide pitch deck (fixed SIH template, including title slide),
  exported and submitted as a PDF — no PPT/Word format accepted.
- **Sep 1, 2026** — College internal round. Deliverable: working
  prototype (V1).
- **December 2026** — SIH Grand Finale. Deliverable: full product,
  built by pulling items off the backlog below in order, as time
  allows. There is no fixed "V2" — it's whatever backlog depth we
  reach by Dec.

## V1 (build this first, nothing else)

A complete but small version of the full pipeline — every stage
genuinely works, just on limited data.

1. **Input**: plain text box only. No PDF/Excel upload yet.
2. **Retrieval**: embed input → vector search against ~50-100
   hand-curated standards → top-3 matches.
3. **Reference expansion**: flat lookup table, built by manually
   reading those 50-100 documents' reference sections once.
4. **Metadata**: two static fields per standard — `latest_version`,
   `is_mandatory_qco` — entered once, not live-checked yet.

V1 is "done" when it proves all 6 PS Expected Features exist in
miniature: semantic match, allied standards, version info,
certification flag, and natural-language text input (multilingual
comes later). Small data, but the logic is real end to end — nothing
mocked or hardcoded as a fake demo.

## Backlog (priority-ordered — pull from the top as time allows)

Each item is independently addable without touching the others (see
the file-structure-to-feature mapping in the project's structure
doc). Priority order and reasoning:

1. **Expand standards corpus (50 → 500+)** — highest priority because
   it's the highest value-per-effort item: zero new code, purely more
   data entry against the existing schema, and fully parallelizable
   across the team right now.
2. **PDF tender/spec upload (single-item)** — turns "type a
   description" into "upload a real doc," which is literally PS
   feature #1 and what judges will expect to see. Controlled scope-up
   (one product per doc).
3. **Multi-item BoQ/Excel extraction** — genuinely harder NLP
   (segmenting one doc into N separate product specs, each needing
   its own retrieval pass). Done after single-item upload works, so
   we're extending a proven path rather than building two new things
   at once.
4. **Automated version/amendment tracking** — replaces static
   hand-entered version data with a periodic re-check against BIS
   pages. Real engineering value but doesn't change what the demo
   visibly shows, so it's mid-priority (depth over flash).
5. **Multilingual input** — a translation adapter in front of the
   existing pipeline; cheap to add, but also low-risk-to-skip since
   English input already satisfies the PS's core requirement. Do it
   if time allows.
6. **Confidence/ranking explanation** ("why this standard") — surface
   the similarity score and matched terms we already compute. Builds
   judge trust cheaply, no new retrieval logic needed.
7. **Chrome extension / GeM integration** — lowest priority. The only
   item here that's pure distribution/demo polish rather than backend
   capability, and the most fragile (depends on gem.gov.in's DOM
   staying stable). Only worth it if items 1-6 are done with time to
   spare, and only if internal-round judge feedback specifically
   signals it would matter for the finale.

## Why this order

Items 1-4 all deepen backend intelligence and data — the actual
product richness goal. Items 5-6 add capability cheaply. Item 7 adds
visibility at real cost and fragility. If Dec arrives and only item 3
is reached, the product is still genuinely strong and judge-ready —
nothing on this list is required for the system to work correctly,
only for it to work more broadly.
