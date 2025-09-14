from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "strategy-builder"


settings = Settings()
