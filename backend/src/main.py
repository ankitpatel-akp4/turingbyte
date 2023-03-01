from fastapi import Depends, FastAPI,HTTPException,status,Request
from fastapi.middleware.cors import CORSMiddleware
import casbin
# # routers import
from src.routers import (
    user_router, scope_router, auth_router
    )
from src.commons.exceptions import exception_middleware
from src.cruds.database import set_db
from src.models.user_model import User
from src.services.auth_service import get_current_user_authorization
from starlette.middleware.authentication import AuthenticationMiddleware



app = FastAPI(dependencies=[Depends(set_db)
                            ,Depends(get_current_user_authorization)
                            ])


# middlewares registration
app.middleware('http')(exception_middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# routers registration
app.include_router(router=user_router.user_router)
app.include_router(router=scope_router.scope_router)
app.include_router(router=auth_router.auth_router)

@app.get("/")
async def root():
    
    return {"message": "Hello World"}

