from pydantic_settings import BaseSettings, SettingsConfigDict
from app.log import get_logger

log = get_logger(__name__)

class Settings(BaseSettings):
    """Configuration settings for the application."""

    model_config = SettingsConfigDict(env_file="./.env", env_file_encoding="utf-8", case_sensitive=True, extra="allow")

    API_VERSION: str
    PROJECT_TITLE: str
    PROJECT_NAME: str
    DESCRIPTION: str
    
    SWAGGER_USERNAME: str
    SWAGGER_PASSWORD: str
    ACCESS_TOKEN_EXPIRATION_MINUTES: int
    
    ALGORITHM: str
    TYPE: str
    SECRET_KEY: str
    
def get_settings(env: str = "local") -> Settings:
    log.info(f"Loading settings for environment: {env}")
    return Settings.model_validate({})

settings = get_settings()

CONFIG_SETTINGS = settings
    
