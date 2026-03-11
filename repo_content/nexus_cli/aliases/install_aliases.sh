#!/usr/bin/env bash
set -euo pipefail
TARGET="$HOME/.bashrc"
for file in nexus_aliases.sh gemini_aliases.sh; do
  echo "source $(cd "$(dirname "$0")" && pwd)/$file" >> "$TARGET"
done
echo "Aliasy zostały dodane do ~/.bashrc"
