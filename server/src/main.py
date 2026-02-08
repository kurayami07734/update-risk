from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.routers.base import router
from src.services.cronjob import run_reddit_cronjob


@asynccontextmanager
async def lifespan(app: FastAPI):
    run_reddit_cronjob()
    yield


app = FastAPI(
    docs_url="/api/docs/swagger",
    redoc_url="/api/docs/redoc",
    lifespan=lifespan,
)


app.include_router(router)
