from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = "postgresql+asyncpg://ensemble:ensemble@db:5432/ensemble"
    redis_url: str = "redis://redis:6379"
    debug: bool = False


settings = Settings()