from cgitb import reset
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, HTTPException, Depends, status, Response
from datetime import timedelta

from src.schemas import auth_schemas, user_schemas
from src.services import auth_service, user_service
from src.commons import parameters




auth_router = APIRouter(prefix="/auths",tags=["Auth"])

ACCESS_TOKEN_EXPIRE_MINUTES = 60*24

@auth_router.post("/token", response_model=auth_schemas.Token)
async def get_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post("/signup",response_model=user_schemas.User,status_code=status.HTTP_201_CREATED)
async def signup(user: user_schemas.UserCreate):
    return await user_service.create_user(user)

# casbin policies crud
@auth_router.post("/casbin-policies",response_model=auth_schemas.CasbinPolicy,status_code=status.HTTP_201_CREATED)
async def create_casbin_policy(casbin_policy: auth_schemas.CasbinPolicyCreate):
    return await auth_service.create_casbin_policy(casbin_policy)

@auth_router.put("/casbin-policies",response_model=auth_schemas.CasbinPolicy,status_code=status.HTTP_201_CREATED)
async def update_casbin_policy(casbin_policy: auth_schemas.CasbinPolicy):
    return await auth_service.update_casbin_policy(casbin_policy)

@auth_router.delete("/casbin-policies/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_casbin_policy(id:int):
    await auth_service.delete_casbin_policy(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

def filter(id: int = None, ptype: str = None, v0:str = None, v1:str = None, v2:str = None, v3:str = None, v4:str = None, v5:str = None):
    return {"id": id, "ptype":ptype, "v0":v0, "v1":v1, "v2":v2, "v3":v3, "v4":v4, "v5":v5}
@auth_router.get("/casbin-policies",response_model=list[auth_schemas.CasbinPolicy])
async def search_casbin_policy(filter: dict = Depends(filter),page: dict = Depends(parameters.page),sort:str = parameters.sort()):
    result =  await auth_service.search_casbin_policy(filter=filter,sort=sort,page=page)
    return result

@auth_router.get("/casbin-policies/{id}",response_model=auth_schemas.CasbinPolicy)
async def read_casbin_policy_by_id(id:int):
    casbin_policy = await auth_service.read_casbin_policy_by_id(id)
    return casbin_policy

   
