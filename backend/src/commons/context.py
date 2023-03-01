from contextvars import ContextVar
current_context:ContextVar[dict] = ContextVar("current_context",default={}) 