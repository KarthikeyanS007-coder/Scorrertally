from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
import secrets
from app.api.login.router import login_router
from app.config import settings, CONFIG_SETTINGS

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

app.include_router(login_router, prefix="/api/v1", tags=["Login"])

