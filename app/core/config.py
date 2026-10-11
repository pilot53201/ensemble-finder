from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class MatchWeights(BaseModel):
    """Relative weights for the matching formula. Auto-normalized at runtime"""

    repertoire: float = Field(default=0.5, ge=0.0)
    level: float = Field(default=0.3, ge=0.0)
    city: float = Field(default=0.2, ge=0.0)
    instruments: float = Field(default=0.1, ge=0.0)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_nested_delimiter="__",
    )

    database_url: str = "postgresql+asyncpg://ensemble:ensemble@db:5432/ensemble"
    redis_url: str = "redis://redis:6379"
    debug: bool = False

    match_weights: MatchWeights = MatchWeights()


settings = Settings()
