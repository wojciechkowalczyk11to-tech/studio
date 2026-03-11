from __future__ import annotations

from pydantic import BaseModel

from nexus_vertex_mcp.tools import tracked_tool


class DocumentsInput(BaseModel):
    document_id: str
    content: str = ""


@tracked_tool("vertex")
async def documents_tool(action: str, payload: DocumentsInput) -> str:
    """CRUD documents in Vertex AI Search datastore."""
    return f"documents action={action} id={payload.document_id}"
