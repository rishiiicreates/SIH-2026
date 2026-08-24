import logging
from supabase import create_client, Client
from app.config import settings

logger = logging.getLogger(__name__)

def get_supabase() -> Client:
    if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
        raise RuntimeError(
            "SUPABASE_URL and SUPABASE_KEY must be configured in environment (.env). "
            "Please configure your Supabase project credentials."
        )
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

# Singleton client instance — fail fast on invalid configuration
try:
    supabase = get_supabase()
except RuntimeError as e:
    logger.error("Supabase client initialization failed: %s", e)
    supabase = None

