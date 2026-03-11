#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

echo "=== Termux Gemini Agent Kit Uninstaller ==="
BASHRC="$HOME/.bashrc"

# 1. Remove bashrc block
if [ -f "$BASHRC" ]; then
    echo "Removing configuration from .bashrc..."
    TMP_BASHRC=$(mktemp)
    trap 'rm -f "$TMP_BASHRC"' EXIT

    sed '/# GCA_KIT_START/,/# GCA_KIT_END/d' "$BASHRC" > "$TMP_BASHRC"
    mv "$TMP_BASHRC" "$BASHRC"
    echo "Removed."
fi

# 2. Config removal (Optional)
echo -n "Do you want to remove the configuration directory (~/.gemini)? [y/N] "
read -r response_rm || true
if [[ "$response_rm" =~ ^([yY][eE][sS]|[yY])+$ ]]; then
    rm -rf "$HOME/.gemini"
    echo "Configuration removed."
else
    echo "Configuration preserved."
fi

# 3. Restore Backup (Optional)
BACKUP_ROOT="$HOME/.gca_backups"
if [ -d "$BACKUP_ROOT" ]; then
    echo ""
    echo "Found backups in $BACKUP_ROOT."
    echo -n "Do you want to restore a backup? [y/N] "
    read -r response_restore || true
    if [[ "$response_restore" =~ ^([yY][eE][sS]|[yY])+$ ]]; then
        echo "Available backups:"
        ls -1 "$BACKUP_ROOT"
        echo ""
        echo -n "Enter backup timestamp to restore (or empty to cancel): "
        read -r backup_ts || true
        if [ -n "$backup_ts" ]; then
             BACKUP_PATH="$BACKUP_ROOT/$backup_ts"
             if [ -d "$BACKUP_PATH" ]; then
                 if [ -f "$BACKUP_PATH/bashrc.bak" ]; then
                     cp "$BACKUP_PATH/bashrc.bak" "$BASHRC"
                     echo "Restored .bashrc."
                 fi
                 # Check if .gemini backup exists
                 if [ -d "$BACKUP_PATH/.gemini" ]; then
                    rm -rf "$HOME/.gemini"
                    cp -r "$BACKUP_PATH/.gemini" "$HOME/"
                    echo "Restored ~/.gemini."
                 fi
                 echo "Restore complete."
             else
                 echo "Backup not found."
             fi
        fi
    fi
fi

echo "Uninstallation complete."
