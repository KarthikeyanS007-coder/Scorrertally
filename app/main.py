import subprocess

from fastapi import FastAPI, Depends, HTTPException, status, Request
# from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
import secrets

from sqlalchemy import text
from sqlalchemy.exc import ProgrammingError, OperationalError
from app.api.login.router import login_router
from app.config import settings
from app.exception import handle_attribute_error_handler, handle_generic_exception_handler, handle_operational_error_handler, handle_programming_error, http_exception_error_handler
from app.utlis.schema_utils import CustomResponse
from app.database.main.my_sql import _engine



app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None
)

security = HTTPBasic()

@app.get("/docs", include_in_schema=False)
def custom_swagger_ui_html(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, settings.SWAGGER_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, settings.SWAGGER_PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return get_swagger_ui_html(openapi_url="/openapi.json", title=f"{settings.PROJECT_TITLE} - Swagger UI")

@app.get("/redoc", include_in_schema=False)
def redoc_html(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, settings.SWAGGER_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, settings.SWAGGER_PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return get_redoc_html(openapi_url="/openapi.json", title=f"{settings.PROJECT_TITLE} - ReDoc")   

@app.get("/openapi.json", include_in_schema=False) 
def openapi(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, settings.SWAGGER_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, settings.SWAGGER_PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return get_openapi(title=settings.PROJECT_TITLE, version=settings.API_VERSION, description=settings.DESCRIPTION, routes=app.routes)


#HTTP Exception Handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return http_exception_error_handler(request, exc)


# MYSQL Exception Handler
@app.exception_handler(ProgrammingError)
async def programming_error_handler(request: Request, exc: ProgrammingError):
    return await handle_programming_error(request, exc)

# Operational Error Handler
@app.exception_handler(OperationalError)
async def operational_error_handler(request: Request, exc: OperationalError):
    return await handle_operational_error_handler(request, exc)

# Attribute Error Handler
@app.exception_handler(AttributeError)
async def attribute_error_handler(request: Request, exc: AttributeError):
    return await handle_attribute_error_handler(request, exc)

# Generic Exception Handler
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return await handle_generic_exception_handler(request, exc)

#Run Migration
@app.get("/run-migrations", include_in_schema=False)
async def run_migrations(credentials: HTTPBasicCredentials = Depends(security), message: str = "Auto-generated migration"):
    correct_username = secrets.compare_digest(credentials.username, settings.SWAGGER_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, settings.SWAGGER_PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    try:
        subprocess.run(['alembic', 'revision', '--autogenerate', '-m', '"{}"'.format(message)])
        subprocess.run(["alembic", "upgrade", "head"])
        return {"status": "1", "message": "Migrations run successfully", "data": None}

    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error running migrations: {str(e)}")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error running migrations: {str(e)}")

app.include_router(login_router, prefix="/FASTAPI", tags=["Login"])

@app.get("/health/db")
async def db_health():
    try:
        with _engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok", "db": "connected"}
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"DB not connected: {exc}")

