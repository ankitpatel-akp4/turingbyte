from fastapi import Depends, HTTPException, APIRouter, status,Response,UploadFile,Body
from src.services import user_service
from src.schemas import user_schemas,general_schemas
from src.commons import parameters, context



user_router = APIRouter(prefix="/users",tags=["User"])



@user_router.post("/",response_model=user_schemas.User,status_code=status.HTTP_201_CREATED)
async def create_user(user: user_schemas.UserCreate):
    return await user_service.create_user(user)

@user_router.put("/",response_model=user_schemas.User)
async def update_user(user:user_schemas.UserUpdate):

    return await user_service.update_user(user)


def filter(id: int = None, first_name: str = None, last_name: str = None,username: str = None,email: str = None,is_active: bool = None):
    return {"id": id, "first_name": first_name, "last_name": last_name, "username": username, "email": email, "is_active": first_name,"is_active":is_active}
@user_router.get("/",response_model=list[user_schemas.User])
async def search_user(filter: dict = Depends(filter),page: dict = Depends(parameters.page),sort:str = parameters.sort()):
    return await user_service.read_user(filter=filter,page=page,sort=sort)

@user_router.get("/loged-in-user",response_model=user_schemas.User)
async def read_logged_in_user():
    return context.current_context.get().user

@user_router.get("/{id}",response_model=user_schemas.User)
async def read_user_by_id(id:int):
    return await user_service.read_user_by_id(id)

@user_router.delete("/",status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id:int):
    await user_service.delete_user()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@user_router.patch("/add-pic",response_model=str)
async def add_profile_pic(data:UploadFile):
    await user_service.add_profile_pic(data)
    return "Done"

@user_router.patch("/remove-pic",response_model=str)
async def remove_profile_pic():
    await user_service.remove_profile_pic()
    return "Done"
   

@user_router.patch("/assign-scope",response_model=general_schemas.GeneralBase)
async def assign_scope(user_id:int,scope_id:int):
    await user_service.assign_scope(user_id,scope_id)
    return general_schemas.GeneralBase(message="scope has been assigned successfully")
    

@user_router.patch("/remove-scope",response_model=general_schemas.GeneralBase)
async def remove_scope(user_id:int,scope_id:int):
    await user_service.remove_scope(user_id,scope_id)
    return general_schemas.GeneralBase(message="scope has been removed successfully")
    

