# -*- coding: utf-8 -*-
# pylint: disable=cyclic-import
from typing import List,Optional,Any

from langchain.tools import BaseTool

from app.services.tools.extended_base_tool import ExtendedBaseTool
from app.services.tools.summarizer_tool import SummarizerTool
from app.utils.config_utils import get_agent_config


def get_tools(tools: List[str],text : Optional[str]) -> List[BaseTool]:
    """
    Retrieves the tools based on a list of tool names.

    This function takes a list of tool names and returns a list of BaseTool objects.
    It first gets the agent configuration and a list of all available tool classes. It then creates a list of all tools
    specified in the agent configuration. If any tool name in the input list is not in the list of all tools,
    it raises a ValueError.

    Args:
        tools (list[str]): The list of tool names.
        load_nested (bool): Whether to load nested chains too. Included to avoid circular imports

    Returns:
        list[BaseTool]: The list of BaseTool objects.

    Raises:
        ValueError: If any tool name in the input list is not in the list of all tools.
    """
    agent_config = get_agent_config()
    all_tool_classes = [
        ("summarizer_tool", SummarizerTool)
    ]
    all_tools: list[ExtendedBaseTool] = [
        c.from_config(
            config=agent_config.tools_library.library[name],
            common_config=agent_config.common,
            text_input=text if name == "summarizer_tool" else None,  
        )
        for name, c in all_tool_classes
        if name in agent_config.tools
    ]

    tools_map = {tool.name: tool for tool in all_tools}

    if any(tool_name not in tools_map for tool_name in tools):
        raise ValueError(f"Invalid tool name(s): {[tool_name for tool_name in tools if tool_name not in tools_map]}")

    return [tools_map[tool_name] for tool_name in tools]


