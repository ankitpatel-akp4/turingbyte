from __future__ import annotations
from typing import TYPE_CHECKING
from contextvars import ContextVar
from pydantic import BaseModel

if TYPE_CHECKING:
    from src.models import user_model
    from sqlalchemy.ext.asyncio import AsyncSession 
class CurrentContext(BaseModel):
    user:user_model.User=None
    db_session:AsyncSession=None

current_context:ContextVar[CurrentContext] = ContextVar("current_context",default=CurrentContext())
