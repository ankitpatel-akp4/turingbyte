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


class CasbinPolicy(Base):
    __tablename__ = "casbin_policies"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    ptype: Mapped[str] = mapped_column(nullable=True)
    v0: Mapped[str] = mapped_column(nullable=True)
    v1: Mapped[str] = mapped_column(nullable=True)
    v2: Mapped[str] = mapped_column(nullable=True)
    v3: Mapped[str] = mapped_column(nullable=True)
    v4: Mapped[str] = mapped_column(nullable=True)
    v5: Mapped[str] = mapped_column(nullable=True)
    def __str__(self):
        arr = [self.ptype]
        for v in (self.v0, self.v1, self.v2, self.v3, self.v4, self.v5):
            if v is None:
                break
            arr.append(v)
        return ", ".join(arr)

    def __repr__(self):
        return '<CasbinRule {}: "{}">'.format(self.id, str(self))