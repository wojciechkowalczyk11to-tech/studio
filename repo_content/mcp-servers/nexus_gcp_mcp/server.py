from __future__ import annotations

import time

from mcp.server.fastmcp import FastMCP

from nexus_gcp_mcp.tools.billing import *
from nexus_gcp_mcp.tools.cloud_run import *
from nexus_gcp_mcp.tools.compute import *
from nexus_gcp_mcp.tools.iam import *
from nexus_gcp_mcp.tools.storage import *

START = time.monotonic()
mcp = FastMCP(name="nexus-gcp-mcp")
mcp.tool()( compute_tool )
mcp.tool()( cloud_run_tool )
mcp.tool()( storage_tool )
mcp.tool()( iam_tool )
mcp.tool()( billing_tool )

@mcp.tool()
async def health_check() -> str:
    """Check server health, uptime, and available tools."""
    uptime = int(time.monotonic() - START)
    return f"server=nexus-gcp-mcp;uptime={uptime};tools={len(mcp._tool_manager.list_tools())};version=0.1.0"

if __name__ == "__main__":
    mcp.run()
