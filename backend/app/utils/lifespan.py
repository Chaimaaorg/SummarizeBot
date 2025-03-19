# -*- coding: utf-8 -*-
import gc
from loguru import logger
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter

from app.config.settings import settings, yaml_configs
from app.utils.config_loader import load_agent_config
from app.utils.fastapi_globals import  g

@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Start up and shutdown tasks."""
    # startup
    yaml_configs["agent_config"] = load_agent_config()
    # yaml_configs["ingestion_config"] = load_ingestion_configs()

    logger.info("Start up FastAPI [Full dev mode]")
    yield

    # shutdown
    # await FastAPICache.clear()
    await FastAPILimiter.close()
    g.cleanup()
    gc.collect()
    yaml_configs.clear()