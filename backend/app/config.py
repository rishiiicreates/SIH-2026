"""Env vars, model names, DB connection settings."""

import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL", "BAAI/bge-m3")
EMBEDDING_API_KEY = os.environ.get("EMBEDDING_API_KEY")
EMBEDDING_API_URL = os.environ.get("EMBEDDING_API_URL")

