from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class _Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=".env",
        env_file_encoding="utf-8",
        secrets_dir="secrets",
        extra="ignore",
    )

    RENDER_DOCKER_BASE_URL: str = Field(default="")
    VERCEL_BASE_URL: str = Field(default="")
    LOCAL_BASE_URL: str = Field(default="")

    USERNAME_API: str = Field(default="")


Settings = _Settings()
