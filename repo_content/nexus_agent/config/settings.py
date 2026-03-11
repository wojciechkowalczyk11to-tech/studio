from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class NexusAgentSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    google_api_key: str = Field(default="")
    github_token: str = Field(default="")
    cloudflare_api_token: str = Field(default="")
    gcp_project_id: str = Field(default="")
    local_llama_url: str = Field(default="http://localhost:8080/v1/chat/completions")
