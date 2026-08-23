"""Supabase/Postgres connection init."""

from supabase import Client, create_client
from app.config import SUPABASE_URL, SUPABASE_KEY

_db_client: Client | None = None


def get_db() -> Client:
    """Return a singleton Supabase client instance."""
    global _db_client
    if _db_client is None:
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise ValueError(
                "SUPABASE_URL and SUPABASE_KEY environment variables must be configured."
            )
        _db_client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _db_client

