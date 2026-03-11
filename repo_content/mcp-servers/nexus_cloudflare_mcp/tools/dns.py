from __future__ import annotations

import httpx
from pydantic import BaseModel

from nexus_cloudflare_mcp.tools import CF_API_TOKEN, tracked_tool


class DNSInput(BaseModel):
    zone_id: str
    record_id: str | None = None
    name: str = ""
    content: str = ""
    type: str = "A"


@tracked_tool("cloudflare")
async def dns_tool(action: str, payload: DNSInput) -> str:
    """List/create/update/delete Cloudflare DNS records."""
    base = f"https://api.cloudflare.com/client/v4/zones/{payload.zone_id}/dns_records"
    headers = {"Authorization": f"Bearer {CF_API_TOKEN}"} if CF_API_TOKEN else {}
    try:
        async with httpx.AsyncClient(timeout=20.0, headers=headers) as c:
            if action == "list":
                r = await c.get(base)
            elif action == "create":
                r = await c.post(base, json=payload.model_dump(exclude_none=True))
            elif action == "update" and payload.record_id:
                r = await c.put(
                    f"{base}/{payload.record_id}",
                    json=payload.model_dump(exclude_none=True),
                )
            elif action == "delete" and payload.record_id:
                r = await c.delete(f"{base}/{payload.record_id}")
            else:
                raise ValueError("Nieprawidłowa akcja DNS.")
        r.raise_for_status()
        return r.text
    except Exception as exc:
        raise RuntimeError(f"Błąd DNS Cloudflare: {exc}") from exc
