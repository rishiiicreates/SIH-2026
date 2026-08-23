from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import recommend

app = FastAPI(title="BIS Standards Recommendation Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(recommend.router, prefix="/api/v1")

@app.get("/")
def health_check():
    return {"status": "ok", "message": "BIS Standards Recommendation Engine Backend is running"}
