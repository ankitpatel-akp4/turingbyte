from fastapi import HTTPException, Request
from typing import Optional, Dict
import asyncio
import casbin
from fastapi.security import OAuth2PasswordBearer
from httpcore import request
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext

from src.services import user_service
from src.models.user_model import User
from src.models import auth_model
from src.schemas.auth_schemas import TokenData
from src.commons import config, context, util, parameters
from src.cruds.database import LocalSession
from .auth import casbin_adapter

# password hashing and varification
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def authenticate_user(username: str, password: str):
    try:
        user = await user_service.read_user_by_username(username)
    except HTTPException as e:
        return False
    if not _verify_password(password, user.password):
        return False
    return user


# jwt token
class OAuth2PasswordBearerOverride(OAuth2PasswordBearer):
   
    async def __call__(self, request: Request) -> Optional[str]:
        authorization = request.headers.get("Authorization")
        if authorization in ["Basic Og==", None]:
            return "guest"
        else:
            return await super().__call__(request)


oauth2_scheme = OAuth2PasswordBearerOverride(tokenUrl="auths/token")

SECRET_KEY = config.settings.secret_key
ALGORITHM = config.settings.algorithm


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        if token == 'guest':
            return await user_service.read_user_by_username(username=token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await user_service.read_user_by_username(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# authorization
# casbin config
adapter = casbin_adapter.Adapter(
    sessionmaker=LocalSession, db_class=auth_model.CasbinPolicy)
e = casbin.Enforcer("model.conf", adapter=adapter)
e.add_named_matching_func("g", casbin.util.regex_match)


# @util.run_in_loop
# def refresh_casbin_policies():
#     global e
#     e.clear_policy()
#     e = casbin.Enforcer("model.conf", adapter=adapter)


@util.run_in_loop
def run_get_current_user_authorization(req: Request, curr_user: User):
    obj = req.url.path
    act = req.method
    sub = " ".join(e.scope for e in curr_user.scopes)
    print(sub,obj,act)
    if not (e.enforce(sub, obj, act)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="access denied"
        )


async def get_current_user_authorization(req: Request, curr_user: User = Depends(get_current_active_user)):
    # loop = asyncio.get_running_loop()
    # await loop.run_in_executor(None,run_get_current_user_authorization,req, curr_user)

    await run_get_current_user_authorization(req,curr_user)
    context.current_context.get().user = curr_user



# casbin policy crud
async def search_casbin_policy(filter: dict = {}, sort: str = parameters.sort(), page: dict = parameters.page()):
    return await auth_model.CasbinPolicy.search(filter=filter, sort=sort, page=page)


def convert_policy_in_list(policy)->list[str]:
    list1 = []
    for x in ["v0","v1","v2","v3","v4","v5"]:
        if hasattr(policy,x) and getattr(policy,x) is not None:
            list1.append(getattr(policy,x))
    return list1


async def create_casbin_policy(casbin_policy: auth_model.CasbinPolicy):
    # new_casbin_policy = auth_model.CasbinPolicy(**casbin_policy.dict())
    # await new_casbin_policy.save()
    # await refresh_casbin_policies()
    if casbin_policy.ptype == "p":
        res = await asyncio.get_running_loop().run_in_executor(None,e.add_policy,*convert_policy_in_list(casbin_policy))
    
    if casbin_policy.ptype == "g":
        res = await asyncio.get_running_loop().run_in_executor(None,e.add_grouping_policy,*convert_policy_in_list(casbin_policy))
    if not res:
        raise HTTPException(status_code=400,detail="operation unsuccessful")
    
    new_casbin_policy = (await auth_model.CasbinPolicy.search(filter=casbin_policy.dict()))
    if len(new_casbin_policy)<=0:
        raise HTTPException(status_code=400,detail=f"could not find the record for {casbin_policy.dict()}")
    return new_casbin_policy[0]





    


async def update_casbin_policy(casbin_policy: auth_model.CasbinPolicy):
    found_casbin_policy = await read_casbin_policy_by_id(casbin_policy.id)
    # await found_casbin_policy.update(casbin_policy.dict())
    # await refresh_casbin_policies()
    if casbin_policy.ptype == "p":
        result = await asyncio.get_running_loop().run_in_executor(None,e.update_policy,convert_policy_in_list(found_casbin_policy),convert_policy_in_list(casbin_policy))
    
    if casbin_policy.ptype == "p":
        result = await found_casbin_policy.update(casbin_policy.dict())
    

    if not result:
        raise HTTPException(status_code=400,detail="could not update the policy")
    return casbin_policy


async def read_casbin_policy_by_id(id: int):
    found_casbin_policy = await auth_model.CasbinPolicy.get(id)
    if not found_casbin_policy:
        raise HTTPException(
            status_code=400, detail=f"no record found by id: {id}")
    return found_casbin_policy


async def delete_casbin_policy(id: int):
    found_casbin_policy = await auth_model.CasbinPolicy.get(id)
    if not found_casbin_policy:
        raise HTTPException(
            status_code=400, detail=f"no record found by id: {id}")
    if found_casbin_policy.ptype == "p":
        await asyncio.get_running_loop().run_in_executor(None,e.remove_policy,*convert_policy_in_list(found_casbin_policy))
    
    if found_casbin_policy.ptype == "g":
        await asyncio.get_running_loop().run_in_executor(None,e.remove_grouping_policies,*convert_policy_in_list(found_casbin_policy))

    
