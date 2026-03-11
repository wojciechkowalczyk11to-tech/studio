# Fusion – Selective Import from nexus-omega-core

This directory contains **selectively imported production-quality files** from
[nexus-omega-core](https://github.com/wojciechkowalczyk11to-tech/nexus-omega-core)
(default branch, commit `1cccd05`).

Import strategy: **default-branch code is the source of truth**, with selective
imports of DevOps/infra + DB/RAG/payments files that prove operational maturity.

## What's Inside

### CI/CD Workflows (`.github/workflows/`)
| File | Purpose |
|------|---------|
| `ci.yml` | Continuous integration pipeline |
| `docker-smoke.yml` | Docker smoke test workflow |

### Scripts (`scripts/`)
| File | Purpose |
|------|---------|
| `backup_db.sh` | PostgreSQL database backup script |

### Infrastructure (`infra/gcp/`)
| File | Purpose |
|------|---------|
| `terraform/main.tf` | Terraform: Google Cloud Run + Cloud SQL + pgvector |
| `cloud-run-backend.yaml` | Cloud Run backend service definition |
| `cloud-run-bot.yaml` | Cloud Run bot service definition |
| `cloudbuild.yaml` | Google Cloud Build pipeline |

### Database Models (`app/db/models/`)
Typed SQLAlchemy 2.0 models with vector/RAG cosine search support:

| File | Purpose |
|------|---------|
| `payment.py` | **Telegram Stars payments** – payment model |
| `rag_chunk.py` | **RAG** – vector chunks with pgvector embeddings |
| `rag_item.py` | **RAG** – source items for retrieval |
| `user.py` | User model with subscription tiers |
| `session.py` | Chat session model |
| `message.py` | Message model |
| `ledger.py` | Credit ledger for token accounting |
| `agent_trace.py` | Agent execution traces |
| `audit_log.py` | Audit log entries |
| `invite_code.py` | Invite code system |
| `tool_counter.py` | Tool usage counters |
| `user_memory.py` | User memory storage |
| `base.py` | SQLAlchemy base + mixins |
| `session.py` (db/) | Database session factory |

### Telegram Bot Handlers (`telegram_bot/handlers/`)
| File | Purpose |
|------|---------|
| `subscribe_handler.py` | **Payments** – Telegram Stars subscription flow |
| `unlock_handler.py` | **Payments** – Feature unlock via Stars |
| `chat_handler.py` | Chat message handling |
| `chat_handler_streaming.py` | Streaming chat responses |
| `document_handler.py` | Document upload/processing |
| `help_handler.py` | Help command |
| `mode_handler.py` | Mode switching (GPT/Gemini/etc.) |
| `provider_handler.py` | AI provider selection |
| `start_handler.py` | Bot start/onboarding |

## Two Databases: RAG & Payments

1. **RAG Database** – pgvector-powered cosine similarity search
   - Models: `rag_chunk.py`, `rag_item.py`
   - Operator: `<=>` (cosine distance)

2. **Payments Database** – Telegram Stars integration
   - Models: `payment.py`, `ledger.py`
   - Handlers: `subscribe_handler.py`, `unlock_handler.py`
