from fastapi import APIRouter
from fastapi.responses import FileResponse

static_router = APIRouter(prefix="/static")
@static_router.get("/images/{file_name}",response_class=FileResponse)
async def image(file_name:str):
    return f"/home/indicate0/Pictures/images/{file_name}"
