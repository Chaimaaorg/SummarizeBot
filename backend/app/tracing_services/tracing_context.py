from contextvars import ContextVar
from dataclasses import dataclass, field

@dataclass
class TracingContext:
    parent_span_ctx: ContextVar = field(default_factory=lambda: ContextVar("SummarizationRoot", default=None))

    def set_variable(self, name: str, value):
        getattr(self, name).set(value)

    def get_variable(self, name: str):
        return getattr(self, name).get()

    def clear_variable(self, name: str):
        getattr(self, name).set([])

tracing_context = TracingContext()
