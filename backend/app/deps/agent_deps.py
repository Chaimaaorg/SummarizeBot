# -*- coding: utf-8 -*-
from typing import Optional,Any

from langchain.agents import AgentExecutor
from app.services.meta_agent import create_meta_agent
from app.utils.config_loader import get_agent_config
from app.utils.fastapi_globals import g


def get_meta_agent(
    api_key: Optional[str] = None,
    text : Optional[str] ={}
) -> AgentExecutor:
    agent_config = get_agent_config()
    agent_config.api_key = api_key
    return create_meta_agent(agent_config,text)
