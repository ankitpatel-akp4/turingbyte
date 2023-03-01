from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, HTTPException, Depends, status
from datetime import timedelta

from src.schemas import auth_schemas, user_schemas
from src.services import auth_service, user_service





auth_router = APIRouter(prefix="/auths",tags=["Auth"])

ACCESS_TOKEN_EXPIRE_MINUTES = 30

@auth_router.post("/token", response_model=auth_schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    print(form_data.password,form_data.username)
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


@auth_router.post("/signpu",response_model=user_schemas.User,status_code=status.HTTP_201_CREATED)
async def signup(user: user_schemas.UserCreate):
    return await user_service.create_user(user)