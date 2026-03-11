from __future__ import annotations

from pydantic import BaseModel

from nexus_gcp_mcp.tools import tracked_tool


class CloudRunInput(BaseModel):
    project_id: str
    name: str = ""


@tracked_tool("gcp")
async def cloud_run_tool(action: str, payload: CloudRunInput) -> str:
    """cloud_run operations for GCP infrastructure."""
    try:
        return f"cloud_run action={action} project={payload.project_id} name={payload.name}"
    except Exception as exc:
        raise RuntimeError(f"Błąd narzędzia cloud_run: {exc}") from exc
