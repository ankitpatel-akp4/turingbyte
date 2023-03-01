from fastapi import Depends, HTTPException, APIRouter, status, Response
from src.services.auth_service import get_current_active_user
from src.services import scope_service
from src.schemas import user_schemas
from typing import List
import src.commons.parameters as parameters


scope_router = APIRouter(prefix="/scopes",tags=["Scope"])

   
# scope router
@scope_router.post("/",response_model=user_schemas.Scope)
async def create_scope(scope: user_schemas.ScopeCreate):
    return await scope_service.create_scope(scope)

@scope_router.put("/",response_model=user_schemas.Scope)
async def update_scope(scope: user_schemas.Scope):
    return await scope_service.update_scope(scope)

@scope_router.get("/",response_model=list[user_schemas.Scope])
async def search_scope(filter: dict = Depends(parameters.filter),page: dict = Depends(parameters.page),sort:str = parameters.sort()):
     return await scope_service.search_scope(filter=filter,sort=sort,page=page,)

@scope_router.get("/{id}",response_model=user_schemas.Scope)
async def read_scope_by_id(id:int,user = Depends(get_current_active_user)):
    scope = await scope_service.read_scope_by_id(id)
    return scope

@scope_router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_scope(id:int):
    await scope_service.delete_scope(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

