import logging
from supabase import create_client, Client
from app.config import settings

logger = logging.getLogger(__name__)

_supabase_client: Client | None = None

def get_supabase() -> Client:
    """Return the singleton Supabase client, creating it once on first call."""
    global _supabase_client
    if _supabase_client is not None:
        return _supabase_client

    if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
        raise RuntimeError(
            "SUPABASE_URL and SUPABASE_KEY must be configured in environment (.env). "
            "Please configure your Supabase project credentials."
        )
    _supabase_client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    logger.info("Supabase client initialized (singleton)")
    return _supabase_client

# Eagerly initialize at import — fail fast on bad config
try:
    supabase = get_supabase()
except RuntimeError as e:
    logger.error("Supabase client initialization failed: %s", e)
    supabase = None
