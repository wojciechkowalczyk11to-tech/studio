from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    api_token: str = Field(default="")

    gcp_project_id: str = Field(default="")
    vertex_datastore_id: str = Field(default="")
    region: str = Field(default="europe-central2")
