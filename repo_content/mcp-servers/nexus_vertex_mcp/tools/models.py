from __future__ import annotations

import asyncio

from google import genai
from pydantic import BaseModel

from nexus_shared.thinking import build_genai_config
from nexus_vertex_mcp.tools import tracked_tool


class ModelInput(BaseModel):
    query: str
    model: str = "gemini-3.0-flash-preview"
    api_key: str = ""


@tracked_tool("vertex")
async def models_tool(payload: ModelInput) -> str:
    """Invoke Gemini models with adaptive thinking configuration."""
    try:
        client = genai.Client(api_key=payload.api_key or None)
        cfg = build_genai_config("Vertex MCP model invocation", payload.query, command="vertex-model")
        resp = await asyncio.to_thread(
            client.models.generate_content, model=payload.model, contents=payload.query, config=cfg
        )
        return resp.text or "Brak odpowiedzi"
    except Exception as exc:
        raise RuntimeError(f"Błąd wywołania modelu Vertex: {exc}") from exc
