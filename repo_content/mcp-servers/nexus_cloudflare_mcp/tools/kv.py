from __future__ import annotations

from pydantic import BaseModel

from nexus_cloudflare_mcp.tools import tracked_tool


class KVInput(BaseModel):
    account_id: str
    namespace_id: str | None = None
    key: str | None = None
    value: str | None = None


@tracked_tool("cloudflare")
async def kv_tool(action: str, payload: KVInput) -> str:
    """Manage KV namespaces and key-value pairs."""
    return f"kv action={action} namespace={payload.namespace_id}"
