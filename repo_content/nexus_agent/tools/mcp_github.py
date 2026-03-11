from __future__ import annotations

from typing import Any

from google.adk.tools.mcp_tool.mcp_toolset import McpToolset, StdioServerParameters


async def load_tools() -> list[Any]:
    """Load MCP tools from stdio server."""
    try:
        tools, _stack = await McpToolset.from_server(
            connection_params=StdioServerParameters(command="npx", args=["-y", "@modelcontextprotocol/server-github"])
        )
        return tools
    except Exception as exc:
        raise RuntimeError(f"Błąd połączenia MCP: {exc}") from exc
