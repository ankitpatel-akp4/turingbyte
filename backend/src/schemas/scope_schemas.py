from datetime import datetime
from pydantic import BaseModel

class ScopeBase(BaseModel):
    id: int
    class Config:
        orm_mode = True
class ScopeName(BaseModel):
    scope: str
    

class Scope(ScopeName,ScopeBase):
    pass


class ScopeCreate(ScopeName):
    pass