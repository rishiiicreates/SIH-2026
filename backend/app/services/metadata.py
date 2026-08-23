"""
Stage 3: Metadata overlay.

PLAIN LOOKUP — version, amendment date, and mandatory QCO/certification
flag. Static stored fields, no reasoning involved.
"""

# from app.db.client import get_db


def get_metadata(standard_id: str) -> dict:
    """
    Return version/amendment/QCO info for `standard_id`.

    Returns a dict like:
        {
            "latest_version": "IS 694:2010",
            "amendment_date": "2018-03-01",  # or None
            "is_mandatory_qco": True,
        }

    V1: single-row lookup against the standards table (static fields
    from standards_seed.csv). Backlog item #4 (auto-tracking) later
    replaces the static fields with a periodically-refreshed source —
    this function's signature shouldn't need to change when that lands.
    """
    raise NotImplementedError
