from functools import wraps 
from loguru import logger
from opentelemetry import trace
from opentelemetry.trace import SpanKind
from app.utils.util_functions import calculate_price_for_tracing
from app.tracing_services.tracing_context import tracing_context
from app.utils.config_utils import get_agent_config
from app.services.helpers.llm import get_llm
import json
from typing import Any


def trace_summarization_tool(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        tracer = trace.get_tracer(__name__)
        
        parent_context = trace.set_span_in_context(tracing_context.get_variable("parent_span_ctx") or None)
        logger.debug(f"Parent Context for {self.__class__.__name__}: {parent_context}")
        with tracer.start_as_current_span(self.__class__.__name__, context=parent_context) as span:
            logger.debug(f"Span Created: {span.name}, trace_id={span.context.trace_id}, span_id={span.context.span_id}")
            try:
                # model_name = get_llm(get_agent_config().common.llm, api_key="")
                result = await func(self, *args, **kwargs)
                input_data = self.text_input
                span.set_attribute("input", input_data)
                span.set_attribute("output", result)
                # pricing = calculate_price_for_tracing(model_name, input_data, result)
                # span.set_attribute("pricing", json.dumps(pricing,ensure_ascii=False))
                return result

            except Exception as e:
                logger.error(f"Error in tracing {span.name}: {e}")
                span.record_exception(e)
                raise
    return wrapper

def trace_llm_tool_creation(func):
    """Decorator to trace the creation of LLM and tools."""
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        tracer = trace.get_tracer(__name__)
        parent_context = trace.set_span_in_context(tracing_context.get_variable("parent_span_ctx") or None)
        logger.debug(f"Parent Context for AgentFromLLMAndTools: {parent_context}")
        with tracer.start_as_current_span("AgentFromLLMAndTools", context=parent_context) as span:
            logger.debug(f"Span Created: {span.name}, trace_id={span.context.trace_id}, span_id={span.context.span_id}")
            try:
                # Capture LLM and tools details
                llm, tools = kwargs["llm"], kwargs["tools"]
                span.set_attributes({
                    "llm.class": llm.__class__.__name__,
                    "llm.name": str(llm),
                    "tools.count": len(tools),
                    "tools.names": ", ".join(type(tool).__name__ for tool in tools),
                    "prompt.message": kwargs["prompt_message"],
                    "prompt.system_context": kwargs["system_context"],
                    "action_plans.count": len(kwargs["action_plans"].action_plans),
                    "action_plans.names": ", ".join(kwargs["action_plans"].action_plans.keys()),
                })

                result = func(*args, **kwargs)

                return result

            except Exception as e:
                logger.error(f"Error in LLM tool creation span {span.name}: {e}")
                span.record_exception(e)
                span.set_attribute("error", str(e))
                raise
    return wrapper
