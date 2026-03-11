from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel

CONFIG_PATH = Path.home() / ".nexus" / "config.json"

class RuntimeConfig(BaseModel):
    default_model: str = "gemini-3.0-flash-preview"
    default_thinking: str = "medium"
    cost_alert_daily: float = 5.0
    language: str = "pl"

def load_config() -> RuntimeConfig:
    try:
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        if not CONFIG_PATH.exists():
            cfg = RuntimeConfig()
            CONFIG_PATH.write_text(cfg.model_dump_json(indent=2), encoding="utf-8")
            return cfg
        return RuntimeConfig(**json.loads(CONFIG_PATH.read_text(encoding="utf-8")))
    except Exception as exc:
        raise RuntimeError(f"Nie udało się wczytać konfiguracji: {exc}") from exc

def save_config(cfg: RuntimeConfig) -> None:
    try:
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        CONFIG_PATH.write_text(cfg.model_dump_json(indent=2), encoding="utf-8")
    except Exception as exc:
        raise RuntimeError(f"Nie udało się zapisać konfiguracji: {exc}") from exc
