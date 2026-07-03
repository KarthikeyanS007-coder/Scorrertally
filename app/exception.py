import traceback

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import ProgrammingError, OperationalError

from app.log import get_logger

logger = get_logger()

class CustomHTTPException(HTTPException):
    """Custom HTTP exception class that extends FastAPI's HTTPException."""
    def __init__(self, status_code: int, detail: str, headers: dict | None = None) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        
class SessionExpiredException(CustomHTTPException):
    """Exception raised when a session has expired."""
    def __init__(self, detail: str = "Session has expired. Please log in again.", headers: dict | None = None) -> None:
        super().__init__(status_code=401, detail=detail, headers=headers)

class DatabaseException(CustomHTTPException):
    """Exception raised for database-related errors."""
    def __init__(self, detail: str = "A database error occurred.", headers: dict | None = None) -> None:
        super().__init__(status_code=500, detail=detail, headers=headers)
        
def http_exception_error_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """HTTP Exception handler to return custom messages."""
    headers = exc.headers
    return JSONResponse(status_code=exc.status_code, content={"status": "-1", "message": exc.detail}, headers=headers)

async def handle_programming_error(request: Request, exc: ProgrammingError) -> JSONResponse:
    """Handle ProgrammingError exception."""
    error_message = str(exc)
    if "Table" in error_message and "doesn't exist" in error_message:
        return JSONResponse(
            status_code=500,
            content={"status": "-1", "message": "Requested resource not found", "error": error_message},
        )
    return JSONResponse(
        status_code=500,
        content={"status": "-1", "message": "Internal server error", "error": error_message},
    )
    
async def handle_generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle generic exception."""
    traceback.print_exc() 
    return JSONResponse(
        status_code=500,
        content={"status": "-1", "message": "An error occurred", "error": str(exc)},
    )

async def handle_operational_error_handler(request: Request, exc: OperationalError) -> JSONResponse:
    """Handle OperationalError exception."""
    error_message = str(exc)
    return JSONResponse(
        status_code=500,
        content={"status": "-1", "message": "Operational error occurred", "error": error_message},
    )

async def handle_attribute_error_handler(request: Request, exc: AttributeError) -> JSONResponse:
    """Handle AttributeError exception."""
    error_message = str(exc)
    return JSONResponse(
        status_code=500,
        content={"status": "-1", "message": "Attribute error occurred", "error": error_message},
    )