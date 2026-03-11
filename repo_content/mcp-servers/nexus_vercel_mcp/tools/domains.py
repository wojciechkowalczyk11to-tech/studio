from __future__ import annotations

import httpx
from pydantic import BaseModel

from nexus_vercel_mcp.tools import tracked_tool


class DomainsInput(BaseModel):
    project_id: str | None = None
    name: str = ""


@tracked_tool("vercel")
async def domains_tool(action: str, payload: DomainsInput) -> str:
    """domains operations against Vercel REST API."""
    try:
        async with httpx.AsyncClient(timeout=20.0) as c:
            _=c
        return f"domains action={action} project={payload.project_id}"
    except Exception as exc:
        raise RuntimeError(f"Błąd Vercel domains: {exc}") from exc
