# -*- coding: utf-8 -*-
import json
import re
from loguru import logger
from datetime import datetime
from typing import List
from app.models.message_model import IChatQuery, IChatMessage

def get_meta_tags(chat: IChatQuery) -> List[str]:
    """
    Generate meta tags for tracking purposes in chat sessions.
    Args:
        chat (IChatQuery): The chat object containing metadata.
    Returns:
        List[str]: List of meta tags generated from the chat data.
    """
    if not chat:
        logger.warning("Chat data is empty or None while generating meta tags.")
        return []
    try:
        return [
            "agent_chat",
            f"user_email={chat.user_email}",
            f"conversation_id={chat.conversation_id}",
            f"message_id={chat.new_message_id}",
            f"timestamp={datetime.now()}",
            f"version={chat.settings.version if chat.settings else 'N/A'}",
        ]
    except AttributeError as error:
        logger.error(f"Error generating meta tags: {error}")
        return []


def create_default_chat_request() -> IChatQuery:
    """
    Create a default chat request template for quick testing or usage.
    Returns:
        IChatQuery: Predefined chat request object with default values.
    """
    try:
        return IChatQuery(
            messages=[
                IChatMessage(role="user", content="launch actif data extraction tool")
            ],
            api_key="",
            conversation_id="d1128740-93ed-4740-a78e-aa8540bc5089",
            new_message_id="deca7c25-077d-4e6f-85a1-186582d20843",
            user_email="no-auth",
            settings={"data": {}, "version": 1},
        )
    except Exception as e:
        logger.error(f"Error creating default Meta Agent request: {e}")
        raise
