from __future__ import annotations

import time

from mcp.server.fastmcp import FastMCP

from nexus_cloudflare_mcp.tools.dns import *
from nexus_cloudflare_mcp.tools.kv import *
from nexus_cloudflare_mcp.tools.tunnels import *
from nexus_cloudflare_mcp.tools.workers import *
from nexus_cloudflare_mcp.tools.zero_trust import *

START = time.monotonic()
mcp = FastMCP(name="nexus-cloudflare-mcp")
mcp.tool()( dns_tool )
mcp.tool()( tunnels_tool )
mcp.tool()( workers_tool )
mcp.tool()( kv_tool )
mcp.tool()( zero_trust_tool )

@mcp.tool()
async def health_check() -> str:
    """Check server health, uptime, and available tools."""
    uptime = int(time.monotonic() - START)
    return f"server=nexus-cloudflare-mcp;uptime={uptime};tools={len(mcp._tool_manager.list_tools())};version=0.1.0"

if __name__ == "__main__":
    mcp.run()
