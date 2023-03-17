from fastapi import Depends, FastAPI,HTTPException,status,Request
from fastapi.middleware.cors import CORSMiddleware
# # routers import
from src.routers import (
    user_router, scope_router, auth_router, static_router, question_router
    ,submission_router
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
app.include_router(router=static_router.static_router)
app.include_router(router=question_router.question_router)
app.include_router(router=question_router.topic_router)
app.include_router(router=submission_router.submission_router)



def stream():
    with open("/home/indicate0/Desktop/turingbyte/backend/static/image/video/takeMetoYourHeart.mp4",mode='rb') as video:
        yield from video
@app.get("/")
def root():
    # return StreamingResponse(stream(),media_type="video/mp4")
    return "hello"

from fastapi.responses import StreamingResponse, FileResponse
@app.get("/a",response_class=FileResponse)
async def root1():
    
    return "/home/indicate0/Desktop/turingbyte/backend/static/image/video/takeMetoYourHeart.mp4"



