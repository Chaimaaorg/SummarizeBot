# -*- coding: utf-8 -*-
from loguru import logger
from typing import Any
from fastapi import APIRouter, HTTPException
from app.config.settings import settings
from app.deps import agent_deps
from app.services.helpers.summarize_helper import (
    create_default_chat_request,
    get_meta_tags
)
from app.services.meta_agent import get_conv_token_buffer_memory

from pydantic import BaseModel

router = APIRouter()

class SummarizeRequest(BaseModel):
    text: str

@router.get("/", operation_id="root_api_v1__get_unique")
async def root() -> Any:
    """A simple route for health checks or testing purposes."""
    return {"message": "FastAPI backend is running"}

@router.post("/get_summary")
async def summarize(request: SummarizeRequest) -> Any:
    """
    Endpoint to generate a summary.

    Parameters:
    - request: JSON payload conforming to the SummarizeRequest schema.

    Returns:
    - dict: Structured output containing the generated summary.
    """
    logger.info(f"Request received: {request.dict()}")
    chat = create_default_chat_request()
    api_key = chat.api_key or settings.OPENAI_API_KEY

    try:
        logger.info("[Step 1] Initializing the Meta Agent")
        print("Request received", request.text)
        meta_agent = agent_deps.get_meta_agent(api_key, request.text)
        logger.info("Meta Agent successfully initialized")
    except Exception as e:
        logger.error(f"Failed to initialize Meta Agent: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to initialize Meta Agent: {str(e)}")

    try:
        logger.info("[Step 2] Preparing for agent execution")
        
        if not chat or not meta_agent:
            logger.error("Invalid data for the Meta Agent")
            raise HTTPException(status_code=400, detail="Invalid data for the Meta Agent")
        
        chat_messages = [m.to_langchain() for m in chat.messages]
        if not chat_messages:
            raise ValueError("Message history is empty, unable to proceed.")

        memory = get_conv_token_buffer_memory(chat_messages[:-1], api_key)
        chat_content = chat_messages[-1].content if chat_messages[-1] else ""

        logger.info("[Step 3] Executing the Meta Agent")

        result = await meta_agent.arun(
            input=chat_content,
            chat_history=memory.load_memory_variables({}).get("chat_history", []),
            user_settings=chat.settings,
            tags=get_meta_tags(chat),
        )

        logger.info("Meta Agent execution completed successfully")
        return result

    except Exception as e:
        logger.error(f"Error during Meta Agent execution: {e}")
        raise HTTPException(status_code=500, detail=f"Error during Meta Agent execution: {str(e)}")
