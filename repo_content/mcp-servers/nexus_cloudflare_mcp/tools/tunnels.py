from __future__ import annotations

from pydantic import BaseModel

from nexus_cloudflare_mcp.tools import tracked_tool


class TunnelInput(BaseModel):
    account_id: str
    tunnel_id: str | None = None
    name: str = ""


@tracked_tool("cloudflare")
async def tunnels_tool(action: str, payload: TunnelInput) -> str:
    """List/create/delete Cloudflare tunnels."""
    return f"tunnels action={action} account={payload.account_id}"
