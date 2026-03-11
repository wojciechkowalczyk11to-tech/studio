#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

# update.sh - Updates CLI and refreshes config

# Pin specific CLI version for deterministic install
GEMINI_CLI_VERSION="${GEMINI_CLI_VERSION:-0.26.0}"

echo "=== Gemini Agent Kit Updater ==="

# 1. Update CLI
if command -v npm &> /dev/null; then
    echo "Updating global gemini-cli to version $GEMINI_CLI_VERSION..."
    npm install -g "@google/gemini-cli@$GEMINI_CLI_VERSION"
    gemini --version || true
else
    echo "npm not found. Skipping CLI update."
fi

# 2. Update Repo
if [ -d ".git" ]; then
    echo "Pulling latest changes..."
    git pull
else
    echo "WARNING: .git directory not found (likely installed via ZIP)."
    echo "Skipping git pull. To update the repo scripts/config:"
    echo "  1. Download the latest ZIP."
    echo "  2. Extract and overwrite files."
    echo "  Or switch to git: git clone ... && ./install.sh"
fi

# 3. Refresh Config
echo "Refreshing configuration..."
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="$HOME/.gca_backups/update_$TIMESTAMP"
CONFIG_DIR="$HOME/.gemini"

if [ -d "$CONFIG_DIR" ]; then
    echo "Backing up existing config to $BACKUP_DIR..."
    mkdir -p "$BACKUP_DIR"
    cp -r "$CONFIG_DIR" "$BACKUP_DIR/"
fi

echo "Applying new configuration..."
mkdir -p "$CONFIG_DIR"
cp -r config/gemini/* "$CONFIG_DIR/"

echo "Update complete. Backup stored in $BACKUP_DIR"
