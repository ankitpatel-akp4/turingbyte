from sqlalchemy import desc, asc
from sqlalchemy.orm import DeclarativeBase
import asyncio

def map_attr(model:DeclarativeBase,filter:dict):
    """
        It takes an orm model and a dict of attribute value pair.
        and it returns an list of maped orm attr with their value
    """
    filters = []
    for attr,value in filter.items():
            if value is not None:
                filters.append(getattr(model,attr)==value)
    return filters
        

def map_sort(model:DeclarativeBase,sort:str):
    """
        it parses the sort statement
    """
    
    _sorts = sort.split(",")
    sorts = []
    for s in _sorts:
        if(s[0]=="-"):
            sorts.append(desc(getattr(model,s[1:])))
        else:
             sorts.append(asc(getattr(model,s[1:])))
    return sorts
    

def run_in_loop(func):
    async def wrapper(*args, **kwargs):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None,func,*args,**kwargs)
    return wrapper
         
    
