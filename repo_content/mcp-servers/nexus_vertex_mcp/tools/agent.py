from __future__ import annotations

from pydantic import BaseModel

from nexus_vertex_mcp.tools import tracked_tool


class AgentInput(BaseModel):
    prompt: str


@tracked_tool("vertex")
async def agent_tool(payload: AgentInput) -> str:
    """Invoke ADK agents for orchestration tasks."""
    return f"agent invoked: {payload.prompt[:80]}"
