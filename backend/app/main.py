"""FastAPI entrypoint — starts the app, includes routers."""

from fastapi import FastAPI

from app.routers import recommend

app = FastAPI(title="IS Standards Recommendation Engine")

app.include_router(recommend.router)
