from datetime import datetime
from pydantic import BaseModel
from .scope_schemas import *



class UserBase(BaseModel):
    id:int
    class Config:
        orm_mode = True
class UserProfile(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    class Config:
        orm_mode = True


class UserCreate(UserProfile):
    password: str
    
class UserUpdate(UserBase):
    id:int
    

class User(UserProfile,UserBase):
    is_active: bool
    created_at: datetime
    scopes: list[Scope]
    

   
