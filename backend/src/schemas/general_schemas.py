from datetime import datetime
from pydantic import BaseModel



class GeneralBase(BaseModel):
    message:str
