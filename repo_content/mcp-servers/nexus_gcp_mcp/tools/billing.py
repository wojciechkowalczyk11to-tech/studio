from __future__ import annotations

from pydantic import BaseModel

from nexus_gcp_mcp.tools import tracked_tool


class BillingInput(BaseModel):
    project_id: str
    name: str = ""


@tracked_tool("gcp")
async def billing_tool(action: str, payload: BillingInput) -> str:
    """billing operations for GCP infrastructure."""
    try:
        return f"billing action={action} project={payload.project_id} name={payload.name}"
    except Exception as exc:
        raise RuntimeError(f"Błąd narzędzia billing: {exc}") from exc
