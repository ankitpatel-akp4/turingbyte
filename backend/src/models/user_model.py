from __future__ import annotations
from src.cruds.database import Base
from typing import Optional, List
from sqlalchemy import (
    Column, ForeignKey,
    String, Table, UniqueConstraint, false
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

# class UserScope(Base):
#     __tablename__="users_scopes"
#     user_id: Mapped[int] = mapped_column(ForeignKey("users.id"),primary_key=True)
#     scope_id: Mapped[int] = mapped_column(ForeignKey("scopes.id"),primary_key=True)
#     scope:Mapped["Scope"] = relationship(back_populates="scopes")
#     # UniqueConstraint('user_id', 'scope_id')

class Scope(Base):
    __tablename__="scopes"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    scope: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[Optional[str]] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str] = mapped_column()
    pic: Mapped[str] = mapped_column(nullable=False, default="default.png")
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    scopes: Mapped[List[Scope]] = relationship(
        secondary=users_scopes, lazy="raise")
    