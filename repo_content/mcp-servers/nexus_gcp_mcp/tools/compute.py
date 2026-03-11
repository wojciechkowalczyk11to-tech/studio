from __future__ import annotations

from pydantic import BaseModel

from nexus_gcp_mcp.tools import tracked_tool


class ComputeInput(BaseModel):
    project_id: str
    name: str = ""


@tracked_tool("gcp")
async def compute_tool(action: str, payload: ComputeInput) -> str:
    """compute operations for GCP infrastructure."""
    try:
        return f"compute action={action} project={payload.project_id} name={payload.name}"
    except Exception as exc:
        raise RuntimeError(f"Błąd narzędzia compute: {exc}") from exc
