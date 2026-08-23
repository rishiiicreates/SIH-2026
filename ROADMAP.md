# Roadmap — PS 26108

## Timeline
- **Aug 26, 2026** — Idea PPT deadline (6-slide pitch, SIH template, PDF)
- **Sep 1, 2026** — College internal round, working V1 prototype
- **Dec 2026** — Grand Finale

## V1 Scope (Sep 1 target)
Proves all six PS Expected Features in miniature:
1. ✅ Semantic match — pgvector similarity search
2. ✅ Allied/normative standards — reference expansion via join table
3. ✅ Version info — latest revision, amendments
4. ✅ Certification flag — QCO mandatory status
5. ✅ Natural-language text input — free-text search box
6. ❌ Multilingual — deferred (backlog #5)

## V1 Definition of Done
- POST /recommend returns real results with real data
- Frontend round-trips: type description → see matching standards
- 11+ standards loaded (electrical/cable domain)
- No stubs in the request path
- No silent exception swallowing

## Backlog (priority order, pulled as time allows)
1. BM25 sparse index + RRF hybrid scoring
2. Tender document PDF/DOCX upload and parsing
3. Confidence scoring and relevance explanation
4. Tender specification clause generation (LLM-assisted)
5. Multilingual support (Bhashini integration)
6. Export to compliance matrix PDF
7. Chrome extension for GeM/CPPP portal integration
8. Voice query support (Hindi/regional)
9. Corpus expansion beyond electrical domain
