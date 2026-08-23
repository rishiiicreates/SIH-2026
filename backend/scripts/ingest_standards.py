"""
One-time / periodic script: reads standards_seed.csv, generates
embeddings, writes standards + references into the DB.

Not part of the live app — run manually (or on a schedule later,
for backlog item #4).

CSV schema (see DATA_SOURCES.md):
    standard_id, title, scope, latest_version, amendment_date,
    is_mandatory_qco, referenced_standard_ids

`referenced_standard_ids` (a delimited string in the CSV) gets
normalized into the `standard_references` join table here — don't
store it as a single field in the live standards table.
"""

import csv

# from app.services.retrieval import embed_text
# from app.db.client import get_db

SEED_PATH = "backend/data/standards_seed.csv"


def load_seed_rows(path: str = SEED_PATH) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def ingest():
    rows = load_seed_rows()
    for row in rows:
        # 1. embed_text(row["title"] + " " + row["scope"])
        # 2. upsert into `standards` table (id, title, scope, embedding,
        #    latest_version, amendment_date, is_mandatory_qco)
        # 3. split row["referenced_standard_ids"], insert one row per
        #    reference into `standard_references`
        raise NotImplementedError


if __name__ == "__main__":
    ingest()
