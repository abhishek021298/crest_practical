import os
from pathlib import Path
from typing import List

from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    # ::::::::::::: General ::::::::::::: #
    SECRET_KEY: str
    DEBUG: bool = Field(default=False)
    APP_NAME: str = Field(default="GlovBox")

    # ::::::::::::: DB Configuration ::::::::::::: #
    SQL_ENGINE: str = Field(default="django.db.backends.postgresql")
    SQL_DATABASE: str = Field(default="postgres")
    SQL_USER: str = Field(default="postgres")
    SQL_PASSWORD: str = Field(default="postgres")
    SQL_DATABASE_HOST: str = Field(default="localhost")
    SQL_DATABASE_PORT: int = Field(default=5432)

    # ::::::::::::: CSRF and CORS ::::::::::::: #
    CSRF_TRUSTED_ORIGINS: List[str] = Field(
        default=["http://localhost:8000"]
    )
    CORS_ORIGIN_WHITELIST: List[str] = Field(
        default=["http://localhost:8000"]
    )

    # ::::::::::::: Configs ::::::::::::: #
    FRONTEND_URL: str = Field(default="http://localhost:8000")
    ADMIN_URL: str = Field(default="http://localhost:8000")
    SUPERUSER_EMAIL: str = Field(default="admin1@yopmail.com")
    PROJECT_TITLE: str
    SERVER_URL: str = Field(default="http://localhost:8000")

    # ::::::::::::: Swagger Authentication ::::::::::::: #
    SWAGGER_AUTH_USERNAME: str
    SWAGGER_AUTH_PASSWORD: str
    JWT_ALGORITHM: str = Field(default="HS256")

    # ::::::::::::: Token Expiry ::::::::::::: #
    AUTH_ACCESS_TOKEN_DAYS: int = Field(default=1)
    AUTH_REFRESH_TOKEN_DAYS: int = Field(default=30)

    class Config:
        env_file = os.path.join(BASE_DIR, ".env")
        env_file_encoding = "utf-8"


def load_settings() -> Settings:
    try:
        return Settings()
    except ValidationError as e:
        print("\n❌ Environment validation errors:")
        for error in e.errors():
            field = error["loc"][0]
            message = error["msg"]
            print(f"  - {field}: {message}")
        raise e
