import typing
from datetime import datetime
from fastapi import Request, status,HTTPException
from fastapi.responses import JSONResponse
from starlette.background import BackgroundTask
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import logging


# error reponse model
class ErrorResponse(JSONResponse):
    def __init__(
        self,
        content: typing.Any,
        status_code: int = 200,
        headers: typing.Optional[typing.Dict[str, str]] = None,
        media_type: typing.Optional[str] = None,
        background: typing.Optional[BackgroundTask] = None,
    ) -> None:
    
        super().__init__(jsonable_encoder(content), status_code, headers, media_type, background)



async def exception_middleware(request: Request,call_next):
    
    try:
       return await call_next(request)
    except HTTPException as e:
        raise e
    except IntegrityError as e:
       
        return ErrorResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        ,content={"type":type(e).__name__,"detail": e.args,"timestamp":datetime.utcnow()}
        )

    except SQLAlchemyError as e:
        return ErrorResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        ,content={"type":type(e).__name__,"detail": e.args,"timestamp":datetime.utcnow()}
        )

    except Exception as e:
        print(e)
        return ErrorResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"type":type(e).__name__,"detail": e.args,"timestamp":datetime.utcnow()},
        
        )
        
    


     
