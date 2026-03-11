"""Minimal smoke tests to verify project structure."""

from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_pyproject_exists() -> None:
    assert (ROOT / "pyproject.toml").is_file()


def test_readme_exists() -> None:
    assert (ROOT / "README.md").is_file()


def test_knowledge_base_scripts_importable() -> None:
    """Verify knowledge-base scripts are valid Python."""
    scripts_dir = ROOT / "knowledge-base" / "scripts"
    for py_file in scripts_dir.glob("*.py"):
        source = py_file.read_text(encoding="utf-8")
        ast.parse(source, filename=str(py_file))
