from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "strategy-builder"
    binance_api_key: str | None = None
    binance_api_secret: str | None = None
    is_paper: bool = True


settings = Settings()
