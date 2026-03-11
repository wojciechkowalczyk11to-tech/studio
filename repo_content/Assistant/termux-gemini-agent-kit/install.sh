#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

# Termux Gemini Agent Kit - Installer

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="$HOME/.gca_backups/$TIMESTAMP"
CONFIG_DIR="$HOME/.gemini"
BASHRC="$HOME/.bashrc"
# Get absolute path to repo root
REPO_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Pin specific CLI version for deterministic install
GEMINI_CLI_VERSION="${GEMINI_CLI_VERSION:-0.26.0}"

echo "=== Termux Gemini Agent Kit Installer ==="
echo "Backup Directory: $BACKUP_DIR"

# 1. Backups
mkdir -p "$BACKUP_DIR"
if [ -d "$CONFIG_DIR" ]; then
    echo "Backing up existing configuration..."
    cp -r "$CONFIG_DIR" "$BACKUP_DIR/"
fi
if [ -f "$BASHRC" ]; then
    cp "$BASHRC" "$BACKUP_DIR/bashrc.bak"
fi

# 2. Config Copy
echo "Installing configuration to $CONFIG_DIR..."
mkdir -p "$CONFIG_DIR"
cp -r "$REPO_DIR/config/gemini/"* "$CONFIG_DIR/"

# 2.1 Validate & Patch Config
echo "Validating configuration..."
PYTHON_CMD=""
if command -v python3 &> /dev/null; then PYTHON_CMD="python3"; elif command -v python &> /dev/null; then PYTHON_CMD="python"; fi

if [ -n "$PYTHON_CMD" ]; then
    SETTINGS_FILE="$CONFIG_DIR/settings.json"
    if [ -f "$SETTINGS_FILE" ]; then
         # Check if patch is needed
         if ! $PYTHON_CMD -c "import sys, json; data=json.load(open('$SETTINGS_FILE')); sys.exit(0 if 'selectedAuthType' in data and 'theme' in data else 1)" 2>/dev/null; then
             echo "Patching settings.json with defaults..."
             $PYTHON_CMD -c "import json; p='$SETTINGS_FILE'; d=json.load(open(p)); d.update({'theme': 'Default', 'selectedAuthType': 'oauth-personal'}); json.dump(d, open(p,'w'), indent=2)"
             echo "Configuration patched."
         else
             echo "Configuration is valid."
         fi
    else
         echo "Warning: settings.json not found after copy."
    fi
else
    echo "Python not found, skipping config validation."
fi

# 3. Termux Dependencies (Prompt)
# Check for Termux environment
if [ -n "${TERMUX_VERSION:-}" ]; then
    echo ""
    echo "Termux detected."
    # We use read without -r inside strict mode but 'read -r' is generally safer.
    # However, strict mode set -e might exit if read fails (EOF).
    # Since we expect user input, it's usually fine.
    # Note: echo -n is not POSIX strictly, but fine in bash.
    echo -n "Install recommended packages (nodejs-lts, git, python, termux-api)? [y/N] "
    read -r response || true
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])+$ ]]; then
        echo "Installing packages..."
        pkg install -y nodejs-lts git python termux-api
        echo "Packages installed."
    else
        echo "Skipping package installation."
    fi

    # Check for npm global install
    if command -v npm &> /dev/null; then
       echo -n "Install @google/gemini-cli@$GEMINI_CLI_VERSION via npm? [y/N] "
       read -r response_npm || true
       if [[ "$response_npm" =~ ^([yY][eE][sS]|[yY])+$ ]]; then
           echo "Installing gemini-cli..."
           npm install -g "@google/gemini-cli@$GEMINI_CLI_VERSION"
           gemini --version || true
       else
           echo "Skipping gemini-cli installation."
       fi
    else
       echo "npm not found. Skipping gemini-cli installation."
    fi
else
    echo "Not running in Termux. Skipping package installation."
fi

# 4. Bashrc Modification (Idempotent)
echo "Configuring .bashrc..."
if [ ! -f "$BASHRC" ]; then
    touch "$BASHRC"
fi

# Use a temporary file to handle sed differences and safety
TMP_BASHRC=$(mktemp)
# Trap to cleanup temp file on exit
trap 'rm -f "$TMP_BASHRC" "$TMP_BASHRC.new" 2>/dev/null || true' EXIT

cp "$BASHRC" "$TMP_BASHRC"

# Remove existing block if present
sed '/# GCA_KIT_START/,/# GCA_KIT_END/d' "$TMP_BASHRC" > "$TMP_BASHRC.new"
mv "$TMP_BASHRC.new" "$TMP_BASHRC"

# Append new block
# We ensure we have a newline before the block
if [ -s "$TMP_BASHRC" ] && [ "$(tail -c1 "$TMP_BASHRC" | wc -l)" -eq 0 ]; then
    echo "" >> "$TMP_BASHRC"
fi

cat <<EOF >> "$TMP_BASHRC"
# GCA_KIT_START
source "$REPO_DIR/termux/aliases.sh"
# GCA_KIT_END
EOF

mv "$TMP_BASHRC" "$BASHRC"

echo "Installation complete!"
echo "Please restart your shell or run: source ~/.bashrc"
echo "Run 'gmode status' to check your environment."
