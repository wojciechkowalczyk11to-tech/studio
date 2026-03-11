from __future__ import annotations

import argparse
import subprocess


def main() -> None:
    parser = argparse.ArgumentParser(description="Start selected Nexus MCP servers")
    parser.add_argument("--servers", default="cf,gcp,vercel,vertex")
    args = parser.parse_args()
    mapping = {
        "cf": "python -m nexus_cloudflare_mcp.server",
        "gcp": "python -m nexus_gcp_mcp.server",
        "vercel": "python -m nexus_vercel_mcp.server",
        "vertex": "python -m nexus_vertex_mcp.server",
    }
    processes = []
    for key in [s.strip() for s in args.servers.split(",") if s.strip()]:
        cmd = mapping.get(key)
        if cmd:
            processes.append(subprocess.Popen(cmd.split()))
    for process in processes:
        process.wait()


if __name__ == "__main__":
    main()
