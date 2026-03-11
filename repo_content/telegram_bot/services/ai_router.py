"""Route AI requests to appropriate provider based on mode/config."""

from __future__ import annotations

import httpx
from typing import AsyncGenerator

from config import settings
from services.grok_client import GrokClient

class AIRouter:
    def __init__(self, grok_client: GrokClient | None = None):
        self.grok_client = grok_client or GrokClient(
            api_key=settings.xai_api_key,
            base_url=settings.xai_base_url
        )

    async def route_stream(
        self,
        query: str,
        mode: str,
        provider_override: str | None = None,
        token: str | None = None,
        history: list[dict[str, str]] | None = None,
        system_prompt: str | None = None,
    ) -> AsyncGenerator[dict, None]:
        """
        Route the request and yield chunks.
        Yields dicts with keys: 'type' (content, status, metadata, error), 'chunk' (str), 'message' (str), 'footer' (str)
        """
        if provider_override == "grok" or mode == "deep":
            # Use Grok Client directly
            if not history:
                history = []
            
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.extend(history)
            messages.append({"role": "user", "content": query})

            model = settings.xai_model_reasoning if mode == "deep" else settings.xai_model_fast

            try:
                async for chunk in self.grok_client.chat_stream(
                    messages=messages,
                    model=model,
                    temperature=0.6,
                ):
                    if chunk.get("type") == "reasoning":
                        yield {"type": "status", "message": "Myślę..."}
                    elif chunk.get("type") == "content":
                        yield {"type": "content", "chunk": chunk["content"]}
                    elif chunk.get("type") == "error":
                        yield {"type": "error", "message": chunk["error"]}
                
                # We could yield metadata here if we calculate cost
                yield {"type": "metadata", "footer": f"Model: {model}"}

            except Exception as e:
                yield {"type": "error", "message": str(e)}

        else:
            # Use Backend API
            async with httpx.AsyncClient(timeout=120.0) as client:
                try:
                    async with client.stream(
                        "POST",
                        f"{settings.backend_url}/api/v1/chat/stream",
                        headers={"Authorization": f"Bearer {token}"} if token else {},
                        json={
                            "query": query,
                            "mode": mode,
                            "provider": provider_override,
                        },
                    ) as response:
                        response.raise_for_status()
                        async for line in response.aiter_lines():
                            if not line or not line.startswith("data: "):
                                continue
                            data_str = line[6:]
                            if data_str == "[DONE]":
                                break
                            import json
                            try:
                                data = json.loads(data_str)
                                yield data
                            except json.JSONDecodeError:
                                continue
                except Exception as e:
                    yield {"type": "error", "message": str(e)}
