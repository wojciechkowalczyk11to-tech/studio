from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    environment: str = "development"
    cors_allowed_origins: list[str] = ["*"]
    database_url: str = "sqlite+aiosqlite:///./test.db"

settings = Settings()
