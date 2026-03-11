from __future__ import annotations

from pydantic import BaseModel

from nexus_gcp_mcp.tools import tracked_tool


class IamInput(BaseModel):
    project_id: str
    name: str = ""


@tracked_tool("gcp")
async def iam_tool(action: str, payload: IamInput) -> str:
    """iam operations for GCP infrastructure."""
    try:
        return f"iam action={action} project={payload.project_id} name={payload.name}"
    except Exception as exc:
        raise RuntimeError(f"Błąd narzędzia iam: {exc}") from exc
