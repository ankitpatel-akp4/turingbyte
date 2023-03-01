from __future__ import annotations
from src.cruds.database import Base
from typing import Optional, List
from sqlalchemy import (
    Column, ForeignKey,
    String, Table, UniqueConstraint
)
from sqlalchemy.orm import (
    relationship, mapped_column, 
    Mapped
)



users_scopes = Table(
    "users_scopes",
    Base.metadata,
    Column("user_id", ForeignKey(
        "users.id", ondelete="CASCADE", onupdate="CASCADE")),
    Column("scope_id", ForeignKey("scopes.id",
           ondelete="CASCADE", onupdate="CASCADE")),
    UniqueConstraint('user_id', 'scope_id')
    
)


class Scope(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    scope: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    

class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[Optional[str]] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    scopes: Mapped[List[Scope]] = relationship(
        secondary=users_scopes, lazy="raise")
    