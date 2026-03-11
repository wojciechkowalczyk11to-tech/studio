#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

# Termux Gemini Agent Kit - Aliases & Setup

# Get the directory of this script to source functions reliably
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ -f "$SCRIPT_DIR/functions.sh" ]; then
    # shellcheck disable=SC1091
    source "$SCRIPT_DIR/functions.sh"
fi

# Aliases
alias gstat='gmode status'
