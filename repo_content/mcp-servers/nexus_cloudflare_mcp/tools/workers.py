from __future__ import annotations

from pydantic import BaseModel

from nexus_cloudflare_mcp.tools import tracked_tool


class WorkerInput(BaseModel):
    account_id: str
    script_name: str
    content: str = ""


@tracked_tool("cloudflare")
async def workers_tool(action: str, payload: WorkerInput) -> str:
    """Deploy/update/delete workers and fetch logs."""
    return f"workers action={action} script={payload.script_name}"
