# N.O.C — Nexus Omega Core Monorepo

N.O.C is a public monorepo that consolidates multiple projects from the Nexus ecosystem:
- FastAPI backend
- Telegram-first bot
- ADK orchestrator agent
- MCP admin servers
- Unified CLI and operational scripts

This repository is designed for local development (Docker Compose), CI/CD (GitHub Actions), and cloud deployment (Cloud Run + GHCR).

## Architecture

```text
                                +-------------------------+
                                |      Telegram Users     |
                                +------------+------------+
                                             |
                                             v
+----------------------+        +------------+------------+        +---------------------+
|   Nexus CLI/Termux   +------->+   FastAPI Backend       +------->+ PostgreSQL + Redis  |
|  (nexus ask/chat)    |        |  /api/v1 + auth + RBAC  |        | state + cache        |
+-----------+----------+        +------------+------------+        +----------+----------+
            |                                |
            |                                v
            |                    +-----------+-------------+
            |                    | Telegram Bot (aiogram)  |
            |                    +-----------+-------------+
            |                                |
            v                                v
+-----------+--------------+      +----------+------------+
|  Nexus ADK Agent         |<---->| MCP Hub (Cloudflare,  |
|  gemini-3.0-flash-preview|      | GCP, Vercel, Vertex)  |
+--------------------------+      +-----------------------+
```

## Repository Layout

- `.github/workflows/` — CI/CD pipelines
- `Source/nexus-omega-core/` — imported backend/bot core source
- `scripts/` — deployment and workstation bootstrap scripts
- `knowledge-base/` — KB integration scripts and schemas
- `docker-compose.yml` — local full stack
- `docker-compose.prod.yml` — production overrides

## Quick Start

### 1. Clone and configure

```bash
git clone https://github.com/wojciechkowalczyk11to-tech/N.0.C.git
cd N.O.C
cp .env.example .env
```

### 2. Start local stack

```bash
make dev
make logs
```

### 3. Useful commands

```bash
make test
make lint
make format
make db-migrate
```

## CI/CD

### CI (`.github/workflows/ci.yml`)
- Runs on `push` to `main` and PRs to `main`
- Matrix: Python 3.11 and 3.12
- Jobs:
  - Ruff lint
  - mypy type-check
  - pytest
  - Bandit security scan
  - TruffleHog secret scan (fails build on verified findings)
- After successful push to `main`, generates `FULL_SOURCE_CODE.md` artifact via KB extractor

### CD (`.github/workflows/deploy.yml`)
- Trigger: Git tag matching `v*`
- Builds and pushes images to GHCR:
  - backend
  - telegram-bot
  - nexus-agent
  - mcp-servers
- Deploys backend image to Cloud Run
- Creates GitHub Release with generated changelog

## Termux Setup (Android)

```bash
bash scripts/setup-termux.sh
```

The script installs required packages, Python environment, aliases, cloud tools, and performs interactive `.env` setup.

## Debian Setup (ThinkPad / VM)

```bash
sudo bash scripts/setup-debian.sh
```

The script provisions Docker, cloudflared, code-server, Node.js 20, UFW, and SSH hardening.

## Security Policy

- Never commit real secrets.
- Use `.env.example` placeholders only.
- Use GitHub Actions secret storage for CI/CD credentials.
- Secret scanning is mandatory in CI.

## Knowledge Base Integration

KB is integrated in a non-destructive way:
- `knowledge-base/scripts/extract_source.py` can generate source dumps
- `knowledge-base/scripts/upload_to_vertex.py` can upload generated docs to Vertex AI Search
- Existing content is preserved via skip/size guards

## License

This repository is public and intended for collaborative open-source development.
