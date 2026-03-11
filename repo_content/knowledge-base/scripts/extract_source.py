#!/usr/bin/env python3
"""Extract source files from a local repository path or Git URL into Markdown documents."""

from __future__ import annotations

import argparse
import json
import mimetypes
import shutil
import subprocess
import tempfile
from collections.abc import Iterator
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

INCLUDE_EXTENSIONS: set[str] = {
    ".py",
    ".ts",
    ".js",
    ".go",
    ".rs",
    ".sh",
    ".yaml",
    ".yml",
    ".toml",
    ".json",
    ".md",
}
EXCLUDE_DIRS: set[str] = {".git", "node_modules", "__pycache__", "venv", ".venv"}
BINARY_MIME_PREFIXES: tuple[str, ...] = ("image/", "audio/", "video/", "application/zip")


@dataclass(slots=True)
class Entry:
    path: str
    source_file: str
    output_file: str
    language: str
    bytes_size: int
    extracted_at: str


def parse_size(text: str) -> int:
    units: dict[str, int] = {"kb": 1024, "mb": 1024 * 1024, "b": 1}
    normalized = text.strip().lower()
    for unit, multiplier in units.items():
        if normalized.endswith(unit):
            value = float(normalized[: -len(unit)])
            return int(value * multiplier)
    return int(normalized)


def is_git_url(repo: str) -> bool:
    return repo.startswith(("https://", "http://", "git@"))


def resolve_repo(repo: str) -> tuple[Path, Path | None]:
    path = Path(repo)
    if path.exists():
        return path.resolve(), None

    if not is_git_url(repo):
        raise ValueError(f"Nieprawidłowa ścieżka repozytorium: {repo}")

    temp_dir = Path(tempfile.mkdtemp(prefix="nexus-extract-"))
    try:
        subprocess.run(
            ["git", "clone", "--depth", "1", repo, str(temp_dir)],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as error:
        raise RuntimeError(
            f"Nie udało się sklonować repozytorium: {error.stderr.strip()}"
        ) from error
    return temp_dir, temp_dir


def detect_language(path: Path) -> str:
    mapping: dict[str, str] = {
        ".py": "python",
        ".ts": "typescript",
        ".js": "javascript",
        ".go": "go",
        ".rs": "rust",
        ".sh": "bash",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".toml": "toml",
        ".json": "json",
        ".md": "markdown",
    }
    return mapping.get(path.suffix.lower(), "text")


def should_skip_path(path: Path) -> bool:
    if any(part in EXCLUDE_DIRS for part in path.parts):
        return True
    if path.suffix.lower() not in INCLUDE_EXTENSIONS:
        return True
    mime, _ = mimetypes.guess_type(str(path))
    if mime and any(mime.startswith(prefix) for prefix in BINARY_MIME_PREFIXES):
        return True
    return False


def iter_files(repo_root: Path) -> Iterator[Path]:
    for path in repo_root.rglob("*"):
        if path.is_file() and not should_skip_path(path):
            yield path


def load_index(index_path: Path) -> dict[str, Any]:
    if not index_path.exists():
        return {"version": "1.0", "generated_at": "", "documents": []}
    try:
        result: dict[str, Any] = json.loads(index_path.read_text(encoding="utf-8"))
        return result
    except (OSError, json.JSONDecodeError):
        return {"version": "1.0", "generated_at": "", "documents": []}


def write_chunked_markdown(
    source: Path, output_base: Path, rel_path: str, max_size: int
) -> list[Path]:
    chunks: list[Path] = []
    output_base.parent.mkdir(parents=True, exist_ok=True)
    header = f"# Source: {rel_path}\n\n```{detect_language(source)}\n"
    footer = "\n```\n"

    part = 1
    current = output_base
    bytes_written = 0
    handle = current.open("w", encoding="utf-8")
    handle.write(header)
    bytes_written = len(header.encode("utf-8"))

    try:
        with source.open("r", encoding="utf-8", errors="ignore") as src:
            for line in src:
                encoded = line.encode("utf-8")
                projected = bytes_written + len(encoded) + len(footer.encode("utf-8"))
                if projected > max_size:
                    handle.write(footer)
                    handle.close()
                    chunks.append(current)
                    part += 1
                    current = output_base.with_name(
                        f"{output_base.stem}.part{part}{output_base.suffix}"
                    )
                    handle = current.open("w", encoding="utf-8")
                    handle.write(header)
                    bytes_written = len(header.encode("utf-8"))
                handle.write(line)
                bytes_written += len(encoded)
    finally:
        handle.write(footer)
        handle.close()
        chunks.append(current)

    return chunks


def slugify(rel_path: str) -> str:
    return rel_path.replace("/", "__").replace("\\", "__")


def existing_large_enough(path: Path, new_files: list[Path]) -> bool:
    if not path.exists():
        return False
    existing_size = path.stat().st_size
    new_size = sum(file.stat().st_size for file in new_files if file.exists())
    return existing_size >= new_size


def extract_repo(repo_root: Path, output: Path, max_size: int, skip_existing: bool) -> None:
    is_single_file_output = output.suffix.lower() == ".md"
    index_path = output.parent / "index.json" if is_single_file_output else output / "index.json"
    index = load_index(index_path)
    known_paths = {entry.get("path", "") for entry in index.get("documents", [])}
    documents: list[dict] = []

    if is_single_file_output:
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("w", encoding="utf-8") as handle:
            for source in iter_files(repo_root):
                rel_path = str(source.relative_to(repo_root))
                if skip_existing and rel_path in known_paths:
                    continue
                language = detect_language(source)
                handle.write(f"# Source: {rel_path}\n\n```{language}\n")
                try:
                    with source.open("r", encoding="utf-8", errors="ignore") as src:
                        for line in src:
                            handle.write(line)
                except OSError as error:
                    raise RuntimeError(
                        f"Nie udało się odczytać pliku {rel_path}: {error}"
                    ) from error
                handle.write("\n```\n\n")
                documents.append(
                    Entry(
                        path=rel_path,
                        source_file=rel_path,
                        output_file=str(output),
                        language=language,
                        bytes_size=source.stat().st_size,
                        extracted_at=datetime.now(timezone.utc).isoformat(),
                    ).__dict__
                )
    else:
        output.mkdir(parents=True, exist_ok=True)
        for source in iter_files(repo_root):
            rel_path = str(source.relative_to(repo_root))
            if skip_existing and rel_path in known_paths:
                continue
            stem = slugify(rel_path)
            target = output / f"{stem}.md"
            chunks = write_chunked_markdown(source, target, rel_path, max_size)
            if existing_large_enough(target, chunks):
                for chunk in chunks:
                    if chunk.exists() and chunk != target:
                        chunk.unlink(missing_ok=True)
                continue
            for chunk in chunks:
                documents.append(
                    Entry(
                        path=rel_path,
                        source_file=rel_path,
                        output_file=str(chunk.relative_to(output.parent)),
                        language=detect_language(source),
                        bytes_size=chunk.stat().st_size,
                        extracted_at=datetime.now(timezone.utc).isoformat(),
                    ).__dict__
                )

    index["generated_at"] = datetime.now(timezone.utc).isoformat()
    combined = [*index.get("documents", []), *documents]
    unique: dict[tuple[str, str], dict] = {}
    for item in combined:
        key = (item.get("path", ""), item.get("output_file", ""))
        unique[key] = item
    index["documents"] = list(unique.values())
    index_path.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Ekstraktor kodu źródłowego do bazy wiedzy.")
    parser.add_argument("--repo", required=True, help="Ścieżka lokalna lub URL repozytorium Git")
    parser.add_argument("--output", required=True, help="Plik .md lub katalog docelowy")
    parser.add_argument(
        "--max-file-size", default="500KB", help="Maksymalny rozmiar pliku wyjściowego"
    )
    parser.add_argument(
        "--skip-existing", action="store_true", help="Pomiń pliki już obecne w index.json"
    )
    args = parser.parse_args()

    temp_path: Path | None = None
    try:
        repo_root, temp_path = resolve_repo(args.repo)
        max_size = parse_size(args.max_file_size)
        extract_repo(repo_root, Path(args.output), max_size, args.skip_existing)
    finally:
        if temp_path and temp_path.exists():
            shutil.rmtree(temp_path, ignore_errors=True)


if __name__ == "__main__":
    main()
