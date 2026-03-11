from __future__ import annotations

from pydantic import BaseModel

from nexus_gcp_mcp.tools import tracked_tool


class StorageInput(BaseModel):
    project_id: str
    name: str = ""


@tracked_tool("gcp")
async def storage_tool(action: str, payload: StorageInput) -> str:
    """storage operations for GCP infrastructure."""
    try:
        return f"storage action={action} project={payload.project_id} name={payload.name}"
    except Exception as exc:
        raise RuntimeError(f"Błąd narzędzia storage: {exc}") from exc
