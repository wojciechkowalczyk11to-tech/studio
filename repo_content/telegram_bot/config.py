from __future__ import annotations

import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


def _get_default_backend_url() -> str:
    if os.getenv("RUNNING_IN_DOCKER", "0") == "1":
        return "http://backend:8000"
    return "http://localhost:8000"


class BotSettings(BaseSettings):
    telegram_bot_token: str = Field(..., description="Telegram Bot Token")
    telegram_mode: str = Field("polling", description="'polling' or 'webhook'")
    webhook_url: str = Field("", description="Base URL for webhooks")
    webhook_port: int = Field(8443, description="Port for webhooks")
    webhook_path: str = Field("webhook", description="URL path for webhooks")
    webhook_secret_token: str = Field("", description="Secret token for webhook")
    backend_url: str = Field(
        default_factory=_get_default_backend_url,
        description="URL of the backend",
    )
    allowed_user_ids: list[int] = Field(default_factory=list, description="Allowed IDs")
    admin_user_ids: list[int] = Field(default_factory=list, description="Admin IDs")
    voice_enabled: bool = True
    inline_enabled: bool = True
    image_gen_enabled: bool = True
    notebook_mode_enabled: bool = True
    provider_policy_json: str = Field(
        '{"default":{"providers":{"gemini":{"enabled":true},"deepseek":{"enabled":true},"groq":{"enabled":true,"daily_usd_cap":1.0}}}}'
    )
    log_level: str = "INFO"
    log_json: bool = True
    telegram_dry_run: bool = Field(False, description="Dry run mode for CI")

    # GigaGrok specific fields
    xai_base_url: str = Field("https://api.x.ai/v1", description="xAI API Base URL")
    xai_api_key: str = Field("", description="xAI API Key")
    xai_model_reasoning: str = Field("grok-beta", description="xAI Reasoning Model")
    xai_model_fast: str = Field("grok-beta", description="xAI Fast Model")
    xai_collection_id: str = Field("", description="xAI Collection ID for RAG")
    groq_api_key: str = Field("", description="Groq API Key for STT")
    github_token: str = Field("", description="GitHub Token for workspace")
    workspace_base: str = Field("/opt/noc/workspaces", description="Workspace base path")
    max_history: int = Field(20, description="Max history messages")
    max_output_tokens: int = Field(16000, description="Max output tokens")
    default_reasoning_effort: str = Field("high", description="Reasoning effort")
    gigagrok_stage2_enabled: bool = Field(True, description="Enable stage 2 features")
    db_path: str = Field("local.db", description="Path to SQLite database")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def is_webhook_mode(self) -> bool:
        return self.telegram_mode.lower() == "webhook"

settings = BotSettings()

DEFAULT_SYSTEM_PROMPT: str = (
    "Jesteś GigaGrok — najinteligentniejszy asystent AI zasilany Grok 4.1 Fast Reasoning.\n"
    "\n"
    "Twoje cechy:\n"
    "- Myślisz głęboko przed odpowiedzią, ale pokazujesz tylko wynik i wnioski (bez ujawniania toku rozumowania).\n"
    "- Odpowiadasz konkretnie, bez zbędnego fluffu\n"
    "- Kod formatujesz w blokach z oznaczeniem języka\n"
    "- Jesteś ekspertem od programowania, analizy danych, strategii biznesowej\n"
    "- Mówisz po polsku gdy pytany po polsku, po angielsku gdy po angielsku\n"
    "- Jesteś szczery — mówisz \"nie wiem\" gdy nie wiesz\n"
    "- Przy złożonych problemach rozkładasz je na kroki\n"
    "\n"
    "Formatowanie:\n"
    "- Markdown\n"
    "- Kod w blokach ```język\n"
    "- Listy numerowane dla kroków\n"
    "- Pogrubienie dla kluczowych pojęć\n"
    "- Bądź zwięzły ale kompletny\n"
    "\n"
    "Aktualna data: {current_date}"
)

PERSONALITY_PROFILES: dict[str, str] = {
    "expert": (
        "Jesteś ekspertem technicznym. Odpowiadaj precyzyjnie, z detalami technicznymi. "
        "Używaj terminologii fachowej. Podawaj przykłady kodu gdy to stosowne."
    ),
    "simple": (
        "Odpowiadaj prosto i zrozumiale, jak dla osoby bez wiedzy technicznej. "
        "Unikaj żargonu. Używaj analogii i przykładów z życia codziennego."
    ),
    "creative": (
        "Bądź kreatywny i inspirujący. Myśl nieszablonowo. "
        "Proponuj innowacyjne rozwiązania. Używaj metafor i obrazowego języka."
    ),
    "concise": (
        "Odpowiadaj maksymalnie zwięźle. Bez wstępów, bez podsumowań. "
        "Tylko esencja odpowiedzi. Bullet pointy zamiast akapitów."
    ),
}
