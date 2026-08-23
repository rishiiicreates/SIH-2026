# BIS Standards Recommendation Engine Backend

This is the FastAPI backend for the SIH-2026 BIS Standards Recommendation Engine.

## Setup

1. Create a virtual environment: `python -m venv venv`
2. Activate it: `source venv/bin/activate`
3. Install requirements: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and fill in your keys.
5. Run the server: `uvicorn app.main:app --reload`

## Ingesting Data
Run the ingest script to populate the Supabase DB:
`python scripts/ingest_standards.py`
