from __future__ import annotations

import time

from mcp.server.fastmcp import FastMCP

from nexus_vertex_mcp.tools.agent import *
from nexus_vertex_mcp.tools.documents import *
from nexus_vertex_mcp.tools.models import *
from nexus_vertex_mcp.tools.search import *

START = time.monotonic()
mcp = FastMCP(name="nexus-vertex-mcp")
mcp.tool()( search_tool )
mcp.tool()( documents_tool )
mcp.tool()( agent_tool )
mcp.tool()( models_tool )

@mcp.tool()
async def health_check() -> str:
    """Check server health, uptime, and available tools."""
    uptime = int(time.monotonic() - START)
    return f"server=nexus-vertex-mcp;uptime={uptime};tools={len(mcp._tool_manager.list_tools())};version=0.1.0"

if __name__ == "__main__":
    mcp.run()
