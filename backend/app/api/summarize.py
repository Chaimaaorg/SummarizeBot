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
    """A simple route for health checks or test purposes."""
    return {"message": "FastAPI backend is running"}


@router.post("/get_summary")
async def summarize(request: SummarizeRequest) -> Any:
    """
    Endpoint pour générer un résumé.

    Parameters:
    - request: Charge utile JSON conforme au schéma SummarizeRequest.

    Returns:
    - dict: Sortie structurée contenant le résumé généré.
    """
    logger.info(f"Requête reçue: {request.dict()}") 
    chat = create_default_chat_request()
    api_key = chat.api_key or settings.OPENAI_API_KEY

    try:
        logger.info("[Étape 1] Initialisation du Meta Agent")
        print("Requête Requête reçue",request.text)
        meta_agent = agent_deps.get_meta_agent(api_key, request.text)
        logger.info("Meta Agent initialisé avec succès")
    except Exception as e:
        logger.error(f"Échec de l'initialisation du Meta Agent: {e}")
        raise HTTPException(status_code=500, detail=f"Échec de l'initialisation du Meta Agent: {str(e)}")

    try:
        logger.info("[Étape 2] Préparation de l'exécution de l'agent")
        
        if not chat or not meta_agent:
            logger.error("Données invalides pour le Meta Agent")
            raise HTTPException(status_code=400, detail="Données invalides pour le Meta Agent")
        
        chat_messages = [m.to_langchain() for m in chat.messages]
        if not chat_messages:
            raise ValueError("L'historique des messages est vide, impossible de procéder.")

        memory = get_conv_token_buffer_memory(chat_messages[:-1], api_key)
        chat_content = chat_messages[-1].content if chat_messages[-1] else ""

        logger.info("[Étape 3] Exécution du Meta Agent")

        result = await meta_agent.arun(
            input=chat_content,
            chat_history=memory.load_memory_variables({}).get("chat_history", []),
            user_settings=chat.settings,
            tags=get_meta_tags(chat),
        )

        logger.info("Exécution du Meta Agent terminée avec succès")
        return result

    except Exception as e:
        logger.error(f"Erreur lors de l'exécution du Meta Agent: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'exécution du Meta Agent: {str(e)}")

        
