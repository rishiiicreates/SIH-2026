from supabase import create_client, Client
from app.config import settings

def get_supabase() -> Client:
    if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
        raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in the environment.")
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

try:
    supabase = get_supabase()
except ValueError:
    supabase = None
