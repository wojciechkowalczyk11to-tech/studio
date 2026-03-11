from __future__ import annotations

from pathlib import Path


def read_file(path: str) -> str:
    """Read text file from workspace."""
    try:
        return Path(path).read_text(encoding="utf-8")
    except Exception as exc:
        raise RuntimeError(f"Nie udało się odczytać pliku: {exc}") from exc


def write_file(path: str, content: str) -> None:
    """Write text file to workspace."""
    try:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    except Exception as exc:
        raise RuntimeError(f"Nie udało się zapisać pliku: {exc}") from exc


def search_files(root: str, pattern: str) -> list[str]:
    """Search files recursively for glob pattern."""
    try:
        return [str(p) for p in Path(root).rglob(pattern)]
    except Exception as exc:
        raise RuntimeError(f"Nie udało się wyszukać plików: {exc}") from exc
