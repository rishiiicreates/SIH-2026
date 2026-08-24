import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import recommend

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Warm up Gemini + Supabase connections at startup."""
    from app.services.retrieval import warmup
    warmup()
    yield

app = FastAPI(title="BIS Standards Recommendation Engine", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(recommend.router, prefix="/api/v1")

@app.get("/")
def health_check():
    return {"status": "ok", "message": "BIS Standards Recommendation Engine Backend is running"}
