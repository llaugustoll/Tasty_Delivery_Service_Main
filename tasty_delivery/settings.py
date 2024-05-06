from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings

import os


class Settings(BaseSettings):
    VERSION: str = Field("")

    # POSTGRES

    DB_USERNAME: str = Field(os.environ['DB_USERNAME'])
    DB_PASSWORD: str = Field(os.environ["DB_PASSWORD"])
    DB_HOST: str = Field(os.environ["DB_HOST"])
    DB_DATABASE: str = Field(os.environ["DB_DATABASE"])

    # TOKEN
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(1440)
    SECRET_KEY: str = Field('')
    ALGORITHM: str = Field('HS256')


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
