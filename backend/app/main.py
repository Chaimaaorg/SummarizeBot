# -*- coding: utf-8 -*-
from loguru import logger
from typing import Dict

from fastapi import APIRouter
from fastapi_pagination import add_pagination
from app.api import summarize
from app.config.settings import settings
from app.utils.fastapi_globals import GlobalsMiddleware
from app.utils.lifespan import lifespan
from app.utils.cors import configure_cors
from fastapi import FastAPI
    
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    lifespan=lifespan,
    description = settings.PROJECT_DESCRIPTION
)


app.add_middleware(GlobalsMiddleware)

if settings.BACKEND_CORS_ORIGINS:
    configure_cors(app)

api_router = APIRouter()

@api_router.get("/")
async def root() -> Dict[str, str]:
    """An example "Hello world" FastAPI route."""
    return {"message": "FastAPI backend"}

api_router.include_router(
    summarize.router
)
app.include_router(
    api_router,
    prefix=settings.API_V1_STR,
)
add_pagination(app)






