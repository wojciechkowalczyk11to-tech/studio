# MCP Servers

Pakiet zawiera 4 serwery FastMCP: Cloudflare, GCP, Vercel, Vertex oraz hub uruchomieniowy.

## D1 DDL
```sql
CREATE TABLE IF NOT EXISTS api_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    server TEXT NOT NULL,
    tool TEXT NOT NULL,
    provider TEXT,
    model TEXT,
    input_size INTEGER,
    output_size INTEGER,
    duration_ms INTEGER,
    estimated_cost_usd REAL DEFAULT 0.0,
    success INTEGER NOT NULL,
    error_msg TEXT
);
```
