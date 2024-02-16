from fastapi import Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

class DMException(Exception):
    def __init__(self, err: Exception):
        self.err = err

async def DM_exception_handler(request: Request, exc: DMException):
    if type(exc.err) == IntegrityError:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "There is a duplicate key value that violates the unique constraint",
                "detail": str(exc.err.__dict__['orig'])
            }
        )
    
    return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

class StatusException(Exception):
    def __init__(self):
        pass

async def Status_exception_handler(request: Request, exc: StatusException):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "message": f"Cannot creat new session because the driver is working or the vehicle is active"
        }
    )

class Request_validation_exception(Exception):
    def __init__(self, field:str, detail:str):
        self.field = field
        self.detail = detail

async def Request_validation_exception_handler(request: Request, exc: Request_validation_exception):
    return JSONResponse(
        status_code=452,
        content={
            "field": exc.field,
            "detail": exc.detail
        }
    )

class Valid_time_period_exception(Exception):
    def __init__(self):
        pass

async def Valid_time_period_exception_handler(request: Request, exc: Valid_time_period_exception):
    return JSONResponse(
        status_code=453,
        content={
            "detail": "the end_time must be set after the start_time."
        }
    )