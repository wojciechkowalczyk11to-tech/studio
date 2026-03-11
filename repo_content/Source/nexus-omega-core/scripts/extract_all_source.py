#!/usr/bin/env python3
"""
Extract ALL source code across all git history into a single Markdown file.

Deduplicates by blob SHA — each unique file content appears exactly once.
For blobs that map to multiple paths, all paths are listed.

Usage:
    python scripts/extract_all_source.py [--output FULL_SOURCE_CODE.md]
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

# File extensions considered "source code" (text-based, reviewable)
SOURCE_EXTENSIONS = frozenset({
    ".py", ".js", ".ts", ".tsx", ".jsx", ".html", ".css", ".scss",
    ".json", ".yaml", ".yml", ".toml", ".cfg", ".ini", ".env",
    ".sh", ".bash", ".zsh", ".fish",
    ".sql", ".graphql", ".gql",
    ".tf", ".hcl",
    ".md", ".rst", ".txt",
    ".dockerfile", ".dockerignore", ".gitignore",
    ".mako",
})

# Files without extensions that are source code
SOURCE_FILENAMES = frozenset({
    "Dockerfile", "Makefile", "Procfile", "Gemfile",
    ".dockerignore", ".gitignore", ".env.example",
    "requirements.txt", "package.json", "alembic.ini",
    "entrypoint.sh",
})

# Paths to skip entirely
SKIP_PATTERNS = frozenset({
    ".git/", "node_modules/", "__pycache__/", ".venv/",
    "dist/", "build/", ".eggs/",
})

# Binary extensions to skip
BINARY_EXTENSIONS = frozenset({
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg",
    ".woff", ".woff2", ".ttf", ".eot",
    ".zip", ".tar", ".gz", ".bz2",
    ".pyc", ".pyo", ".so", ".dylib", ".dll",
    ".db", ".sqlite", ".sqlite3",
    ".pdf", ".doc", ".docx",
})


def run_git(*args: str) -> str:
    """Run a git command and return stdout."""
    result = subprocess.run(
        ["git", *args],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def is_source_file(path: str) -> bool:
    """Determine if a path represents a source file we want to extract."""
    if any(skip in path for skip in SKIP_PATTERNS):
        return False

    p = Path(path)
    ext = p.suffix.lower()

    if ext in BINARY_EXTENSIONS:
        return False

    if p.name in SOURCE_FILENAMES:
        return True

    if ext in SOURCE_EXTENSIONS:
        return True

    # Include extensionless files in known directories
    if not ext and any(
        path.startswith(prefix) for prefix in ("scripts/", "backend/", "telegram_bot/")
    ):
        return True

    return False


def get_language_hint(path: str) -> str:
    """Return a Markdown code fence language hint for a file path."""
    ext_map = {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".tsx": "tsx",
        ".jsx": "jsx",
        ".html": "html",
        ".css": "css",
        ".scss": "scss",
        ".json": "json",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".toml": "toml",
        ".cfg": "ini",
        ".ini": "ini",
        ".sh": "bash",
        ".bash": "bash",
        ".zsh": "zsh",
        ".sql": "sql",
        ".tf": "hcl",
        ".hcl": "hcl",
        ".md": "markdown",
        ".rst": "rst",
        ".mako": "mako",
        ".dockerfile": "dockerfile",
        ".env": "bash",
        ".graphql": "graphql",
        ".gql": "graphql",
    }
    p = Path(path)
    name = p.name.lower()
    if name == "dockerfile" or name.startswith("dockerfile."):
        return "dockerfile"
    if name == "makefile":
        return "makefile"
    if name in (".gitignore", ".dockerignore"):
        return "gitignore"
    if name == "requirements.txt":
        return "text"
    if name == "package.json":
        return "json"
    if name == "alembic.ini":
        return "ini"
    if name == "entrypoint.sh":
        return "bash"
    return ext_map.get(p.suffix.lower(), "")


def collect_blobs() -> dict[str, list[str]]:
    """Collect all unique blob SHAs and their associated file paths across all commits."""
    # Get all commits across all refs
    commits = run_git("rev-list", "--all").strip().splitlines()

    # Map: blob_sha -> set of paths
    blob_paths: dict[str, set[str]] = defaultdict(set)

    for commit in commits:
        tree_output = run_git("ls-tree", "-r", commit).strip()
        if not tree_output:
            continue
        for line in tree_output.splitlines():
            # format: <mode> <type> <sha>\t<path>
            parts = line.split("\t", 1)
            if len(parts) != 2:
                continue
            meta, path = parts
            meta_parts = meta.split()
            if len(meta_parts) < 3:
                continue
            obj_type = meta_parts[1]
            blob_sha = meta_parts[2]

            if obj_type != "blob":
                continue

            if is_source_file(path):
                blob_paths[blob_sha].add(path)

    # Convert sets to sorted lists
    return {sha: sorted(paths) for sha, paths in blob_paths.items()}


def read_blob(sha: str) -> str | None:
    """Read blob content. Returns None if binary or unreadable."""
    try:
        result = subprocess.run(
            ["git", "cat-file", "-p", sha],
            capture_output=True,
            check=True,
        )
        # Try decoding as UTF-8
        return result.stdout.decode("utf-8", errors="replace")
    except (subprocess.CalledProcessError, UnicodeDecodeError):
        return None


def generate_markdown(blob_paths: dict[str, list[str]]) -> str:
    """Generate the full Markdown document."""
    # Sort blobs by their primary (first) path for deterministic ordering
    sorted_blobs = sorted(blob_paths.items(), key=lambda x: x[1][0])

    # Group by top-level directory
    groups: dict[str, list[tuple[str, list[str]]]] = defaultdict(list)
    for sha, paths in sorted_blobs:
        primary = paths[0]
        top_dir = primary.split("/")[0] if "/" in primary else "root"
        groups[top_dir].append((sha, paths))

    # Preferred group ordering
    group_order = [
        "root", ".github", "backend", "telegram_bot",
        "frontend", "mobile-app", "infra", "scripts", "docs", "tests",
    ]
    ordered_groups = []
    for g in group_order:
        if g in groups:
            ordered_groups.append((g, groups.pop(g)))
    for g in sorted(groups.keys()):
        ordered_groups.append((g, groups[g]))

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    lines: list[str] = []
    lines.append("# FULL_SOURCE_CODE.md — Complete Monolithic Source Extraction")
    lines.append("")
    lines.append("> **Repository:** `nexus-omega-core`")
    lines.append(f"> **Generated:** {now}")
    lines.append(
        "> **Method:** All unique blobs across entire git history, "
        "deduplicated by SHA."
    )
    lines.append(f"> **Total unique blobs:** {len(sorted_blobs)}")
    lines.append(
        f"> **Total unique file paths:** "
        f"{sum(len(p) for _, p in sorted_blobs)}"
    )
    lines.append("")
    lines.append("---")
    lines.append("")

    # Table of Contents
    lines.append("## Table of Contents")
    lines.append("")
    for group_name, _ in ordered_groups:
        anchor = group_name.replace(".", "").replace(" ", "-").lower()
        display = group_name if group_name != "root" else "Root Files"
        lines.append(f"- [{display}](#{anchor})")
    lines.append("")
    lines.append("---")
    lines.append("")

    blob_counter = 0
    for group_name, blobs in ordered_groups:
        display = group_name if group_name != "root" else "Root Files"
        lines.append(f"## {display}")
        lines.append("")

        for sha, paths in blobs:
            blob_counter += 1
            primary_path = paths[0]
            lang = get_language_hint(primary_path)

            # Header showing all paths this blob appears at
            if len(paths) == 1:
                lines.append(f"### `{primary_path}`")
            else:
                lines.append(f"### `{primary_path}`")
                lines.append("")
                lines.append(
                    f"*Also found at: "
                    + ", ".join(f"`{p}`" for p in paths[1:])
                    + "*"
                )

            lines.append("")
            lines.append(f"**Blob SHA:** `{sha}`")
            lines.append("")

            content = read_blob(sha)
            if content is None:
                lines.append("*Binary or unreadable content — skipped.*")
            else:
                lines.append(f"```{lang}")
                # Ensure no trailing backtick conflicts
                lines.append(content.rstrip("\n"))
                lines.append("```")

            lines.append("")
            lines.append("---")
            lines.append("")

    # Footer
    lines.append(f"*End of extraction. {blob_counter} unique blobs rendered.*")
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract all source code into a single Markdown file."
    )
    parser.add_argument(
        "--output",
        default="FULL_SOURCE_CODE.md",
        help="Output file path (default: FULL_SOURCE_CODE.md)",
    )
    args = parser.parse_args()

    print("Collecting blobs from all commits...")
    blob_paths = collect_blobs()
    print(f"Found {len(blob_paths)} unique blobs across all history.")

    print("Generating Markdown...")
    md = generate_markdown(blob_paths)

    output_path = Path(args.output)
    output_path.write_text(md, encoding="utf-8")
    print(f"Written to {output_path} ({len(md)} bytes)")


if __name__ == "__main__":
    main()
