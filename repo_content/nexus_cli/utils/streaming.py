from __future__ import annotations

import sys


def stream_text(text: str) -> None:
    """Termux-safe output without cursor escapes."""
    sys.stdout.write(text + "\n")
    sys.stdout.flush()
