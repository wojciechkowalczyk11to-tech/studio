from __future__ import annotations

from nexus_shared.thinking import get_thinking_level


def select_model(best: bool, local: bool, model_override: str | None) -> str:
    if model_override:
        return model_override
    if local:
        return "llama.cpp-local"
    if best:
        return "gemini-3.1-pro-preview"
    return "gemini-3.0-flash-preview"


def select_thinking(query: str, cheap: bool) -> str:
    if cheap:
        return "none"
    return get_thinking_level(query)
