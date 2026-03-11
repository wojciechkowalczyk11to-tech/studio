from __future__ import annotations

import asyncio
from collections.abc import Sequence

ALLOWED_COMMANDS = {"ls", "pwd", "cat", "echo", "git", "python", "python3", "pytest"}


async def safe_exec(command: Sequence[str]) -> str:
    """Execute whitelisted shell command with timeout."""
    if not command or command[0] not in ALLOWED_COMMANDS:
        raise ValueError("Niedozwolone polecenie.")
    try:
        proc = await asyncio.create_subprocess_exec(*command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=30)
        if proc.returncode != 0:
            raise RuntimeError(f"Polecenie zakończone błędem: {stderr.decode().strip()}")
        return stdout.decode().strip()
    except TimeoutError as exc:
        raise RuntimeError("Przekroczono limit czasu polecenia (30s).") from exc
    except Exception as exc:
        raise RuntimeError(f"Błąd wykonania polecenia: {exc}") from exc
