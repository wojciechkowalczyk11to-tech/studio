from __future__ import annotations

from pydantic import BaseModel

from nexus_cloudflare_mcp.tools import tracked_tool


class ZTInput(BaseModel):
    account_id: str
    policy_id: str | None = None


@tracked_tool("cloudflare")
async def zero_trust_tool(action: str, payload: ZTInput) -> str:
    """Manage Zero Trust policies and service tokens."""
    return f"zero-trust action={action} account={payload.account_id}"
