from src.cruds import user_crud
from src.commons import parameters
from src.models import user_model
from src.schemas import scope_schemas
from src.cruds import user_crud
from fastapi import HTTPException


async def search_scope(filter:dict = {},sort:str = parameters.sort(), page: dict=parameters.page()):
    return await user_model.Scope.search(filter=filter,sort=sort,page=page)

async def create_scope(scope: user_model.Scope):
    scope.scope = scope.scope.strip().lower()
    new_scope = user_model.Scope(**scope.dict())
    await new_scope.save()
    return new_scope
async def update_scope(scope: scope_schemas.Scope):
    found_scope = await user_model.Scope.get(scope.id)
    found_scope.scope = scope.scope.strip().lower()
    await found_scope.update(scope.dict())
    return found_scope
    
async def read_scope_by_id(id:int):
    found_scope = await user_model.Scope.get(id)
    if not found_scope:
        raise HTTPException(status_code=400,detail=f"no record found by id: {id}")
        
    return found_scope

async def delete_scope(id:int):
    found_scope = await user_model.Scope.get(id)
    if not found_scope:
        raise HTTPException(status_code=400,detail=f"no record found by id: {id}")
    await found_scope.delete()