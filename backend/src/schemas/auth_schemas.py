from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class CasbinPolicyBase(BaseModel):
    id: int

    class Config:
        orm_mode = True



class CasbinPolicyCreate(BaseModel):
    ptype: str
    v0: str
    v1: str
    v2: Optional[str] 
    v3: Optional[str] 
    v4: Optional[str] 
    v5: Optional[str] 
    class Config:
        orm_mode = True


class CasbinPolicy(CasbinPolicyCreate, CasbinPolicyBase):
    created_at: Optional[datetime]


