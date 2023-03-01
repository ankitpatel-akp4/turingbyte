from fastapi import HTTPException, Request
import asyncio
import casbin
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext

from src.services import user_service
from src.models.user_model import User
from src.schemas.auth_schemas import TokenData
from src.commons import config, context





# password hashing and varification
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

async def authenticate_user(username: str, password: str):
    try:
        user = await user_service.read_user_by_username(username)
    except HTTPException as e:
        return False
    if not verify_password(password, user.password):
        return False
    return user


# jwt token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auths/token")
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

async def get_current_active_user(current_user:User =Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# authorization
# 
e = casbin.Enforcer("model.conf", "policy.csv")
e.add_named_matching_func("g",casbin.util.regex_match)

def run_get_current_user_authorization(req: Request,curr_user:User):
    # e = casbin.Enforcer("model.conf", "policy.csv")
    # e.add_named_matching_func("g",casbin.util.regex_match)
    obj = req.url.path
    act = req.method
    sub = " ".join(e.scope for e in curr_user.scopes)
    if not(e.enforce(sub, obj, act)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Method not authorized for this user")
    
     
async def get_current_user_authorization(req: Request,curr_user:User =Depends(get_current_active_user)):
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None,run_get_current_user_authorization,req, curr_user)
    context.current_context.get()["current_user"] = curr_user
        
         