from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    
    MODE: Literal["DEV", "PROD", "TEST"]

    DB_HOST: str
    DB_USER: str
    DB_PASSWORD: str
    DB_PORT: int
    DB_NAME: str

    TEST_DB_HOST: str
    TEST_DB_USER: str
    TEST_DB_PASSWORD: str
    TEST_DB_PORT: int
    TEST_DB_NAME: str

    SECRET_KEY: str

    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    model_config = SettingsConfigDict(
        env_file="../.env", env_file_encoding="utf-8"

    )
    def get_db_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


cfg = Config()
