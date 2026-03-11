#!/usr/bin/env python3
"""Upload markdown documents to Vertex AI Search datastore."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

import requests  # type: ignore[import-untyped]


def load_index(index_path: Path) -> list[dict[str, Any]]:
    try:
        data = json.loads(index_path.read_text(encoding="utf-8"))
    except OSError as error:
        raise RuntimeError(f"Nie udało się otworzyć index.json: {error}") from error
    except json.JSONDecodeError as error:
        raise RuntimeError(f"Nieprawidłowy format index.json: {error}") from error
    documents: list[dict[str, Any]] = data.get("documents", [])
    return documents


def load_access_token() -> str:
    token = os.environ.get("GCP_ACCESS_TOKEN", "").strip()
    if not token:
        raise RuntimeError("Brak tokenu GCP_ACCESS_TOKEN. Ustaw zmienną środowiskową.")
    return token


def upload_document(
    project_id: str, location: str, datastore_id: str, document_id: str, content: str, token: str
) -> None:
    url = (
        "https://discoveryengine.googleapis.com/v1/projects/"
        f"{project_id}/locations/{location}/collections/default_collection/"
        f"dataStores/{datastore_id}/branches/default_branch/documents?documentId={document_id}"
    )
    payload = {
        "structData": {"source": "nexus-kb", "document_id": document_id},
        "content": {
            "mimeType": "text/markdown",
            "rawBytes": content.encode("utf-8").decode("latin1"),
        },
    }
    try:
        response = requests.post(
            url,
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json=payload,
            timeout=30,
        )
    except requests.RequestException as error:
        raise RuntimeError(f"Błąd połączenia z Vertex AI Search: {error}") from error

    if response.status_code not in {200, 201}:
        raise RuntimeError(
            f"Vertex AI Search zwrócił błąd {response.status_code}: {response.text[:500]}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Uploader dokumentów KB do Vertex AI Search.")
    parser.add_argument(
        "--index", default="knowledge-base/index.json", help="Ścieżka do index.json"
    )
    parser.add_argument("--base-dir", default=".", help="Katalog bazowy dla plików z index.json")
    parser.add_argument("--project-id", default=os.getenv("GCP_PROJECT_ID", ""))
    parser.add_argument("--location", default=os.getenv("VERTEX_LOCATION", "global"))
    parser.add_argument("--datastore-id", default=os.getenv("VERTEX_DATASTORE_ID", ""))
    args = parser.parse_args()

    if not args.project_id or not args.datastore_id:
        raise RuntimeError("Brak GCP_PROJECT_ID lub VERTEX_DATASTORE_ID.")

    token = load_access_token()
    entries = load_index(Path(args.index))
    base_dir = Path(args.base_dir)

    uploaded = 0
    for entry in entries:
        output_file = entry.get("output_file", "")
        path = (base_dir / output_file).resolve()
        if not path.exists():
            continue
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
            document_id = entry.get("path", output_file).replace("/", "__")[:120]
            upload_document(
                args.project_id, args.location, args.datastore_id, document_id, content, token
            )
            uploaded += 1
        except OSError as error:
            raise RuntimeError(f"Nie udało się odczytać pliku {path}: {error}") from error

    print(f"Wysłano dokumentów: {uploaded}")


if __name__ == "__main__":
    main()
