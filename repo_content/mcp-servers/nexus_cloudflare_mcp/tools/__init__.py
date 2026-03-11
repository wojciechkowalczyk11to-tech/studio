from __future__ import annotations

import asyncio
import functools
import os
import time
from collections.abc import Awaitable, Callable
from datetime import datetime, timezone
from typing import Any

import httpx

CF_ACCOUNT_ID = "c263403c94461a2bb3c5564fce8762a5"
D1_DB_ID = "89b8f6fe-d069-4369-92cb-c203de51ac6f"
D1_URL = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/d1/database/{D1_DB_ID}/query"
CF_API_TOKEN = os.environ.get("CF_API_TOKEN", "")


async def log_to_d1(server: str, tool: str, duration_ms: int, input_size: int, output_size: int, success: bool, error_msg: str | None = None, provider: str | None = None, model: str | None = None, estimated_cost: float = 0.0) -> None:
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            await client.post(D1_URL, headers={"Authorization": f"Bearer {CF_API_TOKEN}"}, json={"sql": "INSERT INTO api_logs (timestamp,server,tool,provider,model,input_size,output_size,duration_ms,estimated_cost_usd,success,error_msg) VALUES (?,?,?,?,?,?,?,?,?,?,?)", "params": [datetime.now(tz=timezone.utc).isoformat(), server, tool, provider, model, input_size, output_size, duration_ms, estimated_cost, int(success), error_msg]})
    except Exception:
        return


def tracked_tool(server_name: str) -> Callable[[Callable[..., Awaitable[Any]]], Callable[..., Awaitable[Any]]]:
    def decorator(fn: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
        @functools.wraps(fn)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            t0 = time.monotonic()
            error = None
            result: Any = None
            try:
                result = await fn(*args, **kwargs)
                return result
            except Exception as exc:
                error = str(exc)
                raise
            finally:
                duration = int((time.monotonic() - t0) * 1000)
                try:
                    asyncio.create_task(log_to_d1(server=server_name, tool=fn.__name__, duration_ms=duration, input_size=len(str(kwargs)), output_size=len(str(result)) if result else 0, success=error is None, error_msg=error))
                except RuntimeError:
                    pass

        return wrapper

    return decorator
