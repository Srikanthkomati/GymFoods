from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):

    # -----------------------------
    # Application Info
    # -----------------------------
    APP_NAME: str = "Fitness Assistant API"
    VERSION: str = "1.0.0"


    # -----------------------------
    # Database
    # -----------------------------
    DATABASE_URL: str


    # -----------------------------
    # Security
    # -----------------------------
    SECRET_KEY: str
    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7


    # -----------------------------
    # Environment
    # -----------------------------
    ENVIRONMENT: str = "development"


    class Config:
        env_file = ".env"
        case_sensitive = True


# -----------------------------
# Singleton Settings Object
# -----------------------------
@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()