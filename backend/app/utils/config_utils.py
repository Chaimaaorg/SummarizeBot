# -*- coding: utf-8 -*-
from loguru import logger
from pathlib import Path
from typing import Any
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import ConsoleSpanExporter
from app.config.settings import settings, yaml_configs
from app.models.agent_model import ActionPlan, ActionPlans, AgentAndToolsConfig, AgentConfig
from app.models.tool_model import PromptInput, ToolConfig, ToolsLibrary
from app.utils.config_loader import Config
from app.config.settings import settings

def get_exporter(
    exporter_name : str
) -> OTLPSpanExporter | ConsoleSpanExporter:
    
    stdout = ConsoleSpanExporter()
    if exporter_name == "dynatrace":
        
        if not settings.DT_API_URL or not settings.DT_API_TOKEN:
            logger.error("Dynatrace API URL and token are required")
            raise ValueError("Dynatrace API URL and token are required")
        
        dynatrace = OTLPSpanExporter(
                endpoint=settings.DT_API_URL + "/v2/otlp/v1/traces",
                headers={"Authorization": f"Api-Token {settings.DT_API_TOKEN}"}
            )
        return dynatrace
    else:
        return stdout 
    
def get_tool_config(
    tool_name: str,
    config_values: dict[
        str,
        Any,
    ],
) -> ToolConfig:
    """Get a tool config from a tool name and config values."""
    config_values["prompt_inputs"] = [PromptInput(**item) for item in config_values.get("prompt_inputs", [])]
    return ToolConfig(**config_values)

def load_agent_config() -> AgentConfig:
    """Get the agent config."""
    logger.info("Loading agent config from yaml file...")
    agent_config = Config(Path(settings.AGENT_CONFIG_PATH)).read()
    agent_config.action_plans = ActionPlans(
        action_plans={k: ActionPlan(**v) for k, v in agent_config.action_plans.items()}
    )
    agent_config.tools_library = ToolsLibrary(
        library={
            k: get_tool_config(
                k,
                v,
            )
            for k, v in agent_config.tools_library.library.items()
        }
    )
    agent_config.common = AgentAndToolsConfig(**agent_config.common)
    return AgentConfig(**agent_config)


def get_agent_config() -> AgentConfig:
    agent_config = yaml_configs.get("agent_config", None)
    if agent_config is None:
        agent_config = load_agent_config()
        yaml_configs["agent_config"] = agent_config
    return agent_config
