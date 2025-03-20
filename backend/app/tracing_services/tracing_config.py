from opentelemetry import trace
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from app.utils.config_utils import get_exporter
from app.config.settings import settings
from loguru import logger
from app.tracing_services.tracing_context import tracing_context

def create_tracer_provider():
    provider = TracerProvider(resource=Resource.create({SERVICE_NAME: "summarizer"}))
    exporter = get_exporter(settings.EXPORTER_NAME)
    # exporter._certificate_file = False  
    batch_span_processor = BatchSpanProcessor(
        span_exporter=exporter
    )
    provider.add_span_processor(batch_span_processor)
    trace.set_tracer_provider(provider)
    return provider

def init_tracer():
    global tracer
    if 'tracer' not in globals():
        logger.warning("Initializing summarizer Tracer")
        provider = create_tracer_provider()
        tracer = trace.get_tracer("Summarizer Tracer")

        parent_span = tracer.start_span("SummarizationRoot")
        tracing_context.set_variable("parent_span_ctx", parent_span)
        logger.debug(f"Root Span Created: trace_id={parent_span.context.trace_id}, span_id={parent_span.context.span_id}")

        logger.info(f"Tracer initialized with Dynatrace exporter to {settings.DT_API_URL}")

    return tracer

def close_parent_span():
    """Ensures the parent span is ended properly."""
    parent_span = tracing_context.get_variable("parent_span_ctx")
    if parent_span is not None:
        parent_span.end()
        logger.debug(f"Parent Span Ended: trace_id={parent_span.context.trace_id}, span_id={parent_span.context.span_id}")
        tracing_context.clear_variable("parent_span_ctx")  # Clear the context
