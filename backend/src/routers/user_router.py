from fastapi import Depends, HTTPException, APIRouter, status,Response
from src.services import user_service
from src.schemas import user_schemas,general_schemas
from src.commons import parameters



user_router = APIRouter(prefix="/users",tags=["User"])



@user_router.post("/",response_model=user_schemas.User,status_code=status.HTTP_201_CREATED)
async def create_user(user: user_schemas.UserCreate):
    return await user_service.create_user(user)

@user_router.put("/",response_model=user_schemas.User)
async def update_user(user:user_schemas.UserUpdate):
    return await user_service.update_user(user)

@user_router.get("/",response_model=list[user_schemas.User])
async def search_user(filter: dict = Depends(parameters.filter),page: dict = Depends(parameters.page),sort:str = parameters.sort()):
    return await user_service.read_user(filter=filter,page=page,sort=sort)

@user_router.get("/{id}",response_model=user_schemas.User)
async def read_user_by_id(id:int):
    return await user_service.read_user_by_id(id)

@user_router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id:int):
    await user_service.delete_user(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@user_router.patch("/assign-scope",response_model=general_schemas.GeneralBase)
async def assign_scope(user_id:int,scope_id:int):
    await user_service.assign_scope(user_id,scope_id)
    return general_schemas.GeneralBase(message="scope has been assigned successfully")
    

@user_router.patch("/remove-scope",response_model=general_schemas.GeneralBase)
async def remove_scope(user_id:int,scope_id:int):
    await user_service.remove_scope(user_id,scope_id)
    return general_schemas.GeneralBase(message="scope has been removed successfully")
    

