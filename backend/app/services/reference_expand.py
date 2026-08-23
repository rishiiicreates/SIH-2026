"""
Stage 2: Reference expansion.

PLAIN LOOKUP — not AI. Given a standard_id, fetch its normative
references from a flat join table. Do NOT let a model infer or guess
dependencies here; this is stored, structured data only.

Table shape (see DATA_SOURCES.md):
    standard_references(standard_id TEXT, referenced_id TEXT)
"""

# from app.db.client import get_db


def get_references(standard_id: str) -> list[dict]:
    """
    Return the allied/normative standards for `standard_id`.

    Returns a list of dicts like:
        {"standard_id": "IS 9283", "title": "..."}

    Implementation: a single join query against `standard_references`
    joined to the standards table for titles. Use `WITH RECURSIVE` only
    if/when a genuine multi-hop need appears — plain single-hop join
    covers V1.
    """
    raise NotImplementedError
