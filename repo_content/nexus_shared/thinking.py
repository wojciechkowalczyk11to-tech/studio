"""Shared adaptive reasoning helper used across Nexus components."""

from __future__ import annotations

from typing import Literal

ThinkingLevel = Literal["none", "low", "medium", "high"]


def get_thinking_level(query: str, command: str = "") -> ThinkingLevel:
    """Determine Gemini reasoning depth based on query complexity."""
    greetings = [
        "cześć", "hej", "siema", "jak się masz", "co u ciebie", "hi", "hello", "hey", "what's up", "yo",
    ]
    query_lower = query.lower().strip()

    if any(g in query_lower for g in greetings) and len(query_lower) < 50:
        return "none"

    if len(query) < 30 and "?" not in query:
        return "low"

    if len(query) > 500 or any(
        kw in query_lower
        for kw in [
            "architektur", "zaprojektuj", "przeanalizuj", "zaudytuj", "architect", "design", "analyze", "audit", "debug",
            "security", "bezpieczeń", "optymali", "refactor",
        ]
    ):
        return "high"

    return "medium"


def get_budget(query: str, command: str = "") -> int:
    """Return numerical thinking budget for the provided query."""
    budgets = {"none": 0, "low": 1024, "medium": 8192, "high": 32768}
    return budgets[get_thinking_level(query, command)]


def build_genai_config(
    system_prompt: str,
    query: str,
    command: str = "",
    temperature: float = 0.7,
    max_tokens: int = 8192,
):
    """Build complete GenerateContentConfig with adaptive thinking budget."""
    from google import genai

    level = get_thinking_level(query, command)
    budget = get_budget(query, command)

    augmented_prompt = system_prompt
    if level in ("medium", "high"):
        augmented_prompt += (
            f"\n\n[REASONING MODE: {level.upper()}] "
            "Decompose the query into sub-problems. "
            "Analyze each component. "
            "Verify your answer before responding."
        )

    thinking = genai.types.ThinkingConfig(thinking_budget=budget) if level != "none" else None

    return genai.types.GenerateContentConfig(
        system_instruction=augmented_prompt,
        temperature=temperature,
        max_output_tokens=max_tokens,
        thinking_config=thinking,
    )
