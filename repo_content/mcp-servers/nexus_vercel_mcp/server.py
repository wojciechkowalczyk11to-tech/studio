from __future__ import annotations

import time

from mcp.server.fastmcp import FastMCP

from nexus_vercel_mcp.tools.deployments import *
from nexus_vercel_mcp.tools.domains import *
from nexus_vercel_mcp.tools.env_vars import *
from nexus_vercel_mcp.tools.projects import *

START = time.monotonic()
mcp = FastMCP(name="nexus-vercel-mcp")
mcp.tool()( projects_tool )
mcp.tool()( deployments_tool )
mcp.tool()( domains_tool )
mcp.tool()( env_vars_tool )

@mcp.tool()
async def health_check() -> str:
    """Check server health, uptime, and available tools."""
    uptime = int(time.monotonic() - START)
    return f"server=nexus-vercel-mcp;uptime={uptime};tools={len(mcp._tool_manager.list_tools())};version=0.1.0"

if __name__ == "__main__":
    mcp.run()
