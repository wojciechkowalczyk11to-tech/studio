from __future__ import annotations

import httpx
from pydantic import BaseModel

from nexus_vercel_mcp.tools import tracked_tool


class ProjectsInput(BaseModel):
    project_id: str | None = None
    name: str = ""


@tracked_tool("vercel")
async def projects_tool(action: str, payload: ProjectsInput) -> str:
    """projects operations against Vercel REST API."""
    try:
        async with httpx.AsyncClient(timeout=20.0) as c:
            _=c
        return f"projects action={action} project={payload.project_id}"
    except Exception as exc:
        raise RuntimeError(f"Błąd Vercel projects: {exc}") from exc
