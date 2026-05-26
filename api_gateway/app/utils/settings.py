#api_gateway/app/utils/settings.py
#Используется для получения настроек из .env файла и их хранения

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """

    """

    DATABASE_URL: str = Field(..., description="DataBase URL")
    REDIS_URL: str = Field(..., description="Redis URL")

    model_config = SettingsConfigDict(
        env_file = ".env"
        ,env_file_encoding = "utf-8"
        ,case_sensitive = True
        ,extra = "allow"
        ,
    )


if __name__ == "__main__":
    settings = Settings()
    print(settings)