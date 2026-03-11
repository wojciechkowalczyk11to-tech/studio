from __future__ import annotations

from pydantic import BaseModel

from nexus_vertex_mcp.tools import tracked_tool


class SearchInput(BaseModel):
    query: str


@tracked_tool("vertex")
async def search_tool(payload: SearchInput) -> str:
    """Query Vertex AI Search datastore."""
    return f"search result for: {payload.query}"
