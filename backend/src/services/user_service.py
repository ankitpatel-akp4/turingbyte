from fastapi import Depends, HTTPException, UploadFile, status
from src.cruds.database import get_db
from src.commons import parameters, context
from src.schemas import user_schemas
from src.models import user_model
from src.services import auth_service
import aiofiles
import os

async def read_user(filter: dict = {}, sort: str = parameters.sort(), page: dict = parameters.page()):
    users = await user_model.User.search(page=page, sort=sort, filter=filter, eager_load=["scopes"])
    return users


async def read_user_by_id(id: int):
    found_user = await user_model.User.get(id, ["scopes"])
    if not found_user:
        raise HTTPException(
            status_code=400, detail=f"no record found by id: {id}")
    return found_user

async def read_logged_in_user():
    user =  context.current_context.get().user
    return user


async def read_user_by_username(username: str) -> user_model.User:
    found_user = await user_model.User.get_by_attr(attr="username", value=username, eager_load=["scopes"])
    if len(found_user) < 1:
        raise HTTPException(
            status_code=400, detail=f"no record found by id: {id}")
    return found_user[0]


async def create_user(user: user_schemas.UserCreate):
    user.password = auth_service.get_password_hash(user.password)
    new_user = user_model.User(**user.dict())
    default_scope = await user_model.Scope.get(id=1)
    new_user.scopes.append(default_scope)
    await new_user.save()
    new_user = await user_model.User.get(new_user.id, ["scopes"])
    return new_user


async def update_user(user: user_schemas.UserUpdate):
    found_user:user_model.User = context.current_context.get().user
    if not found_user:
        raise HTTPException(
            status_code=400, detail=f"no record found by id: {user.id}")
    await found_user.update(user.dict())
    return found_user


async def delete_user():
    user:user_model.User = context.current_context.get().user

    if not user:
        raise HTTPException(
            status_code=400, detail=f"no record found by id: {id}")
    await user.delete()


async def assign_scope(user_id, scope_id):
    user: user_model.User = await user_model.User.get(id=user_id, eager_load=["scopes"])
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user not foud by id: {user_id}")

    scope: user_model.Scope = await user_model.Scope.get(scope_id)
    if not scope:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"scope not foud by id: {scope_id}")

    if scope in user.scopes:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail=f"user {user_id} already has the scope {scope.id}")

    user.scopes.append(scope)
    user.update()


async def remove_scope(user_id, scope_id):
    user: user_model.User = await user_model.User.get(id=user_id, eager_load=["scopes"])
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user not foud by id: {user_id}")

    scope: user_model.Scope = await user_model.Scope.get(scope_id)
    if not scope:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"scope not foud by id: {scope_id}")

    if scope in user.scopes:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail=f"user {user_id} already has the scope {scope.id}")

    user.scopes.remove(scope)

async def add_profile_pic(data:UploadFile):
    user:user_model.User = context.current_context.get().user
    user.pic = user.username+data.filename
    async with aiofiles.open(f"/home/indicate0/Pictures/images/{user.pic}","wb") as file:
        await file.write(await data.read())
    await user.update()
    
async def remove_profile_pic():
    user:user_model.User = context.current_context.get().user
    if user.pic != "default.png":
        
        path = f"/home/indicate0/Pictures/images/{user.pic}"
        user.pic = "default.png"
        await user.update()
        if os.path.exists(path):
            os.remove(path)
        else:
            print(f"path: {path}")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="you dont have a profile pic yet")    
    

    

# [{'first_name': 'string', 'last_name': 'string', 'username': 'string', 'email': 'string', 'password': 'stringdkf', 'scopes': [{'id': 1, 'scope': 'ROLE_USER'}]}]


