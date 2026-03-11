#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

# Doctor script for Termux Gemini Agent Kit

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=== Gemini Agent Kit Doctor ==="

# 1. Environment Check
is_termux=false
if [ -n "${TERMUX_VERSION:-}" ]; then
    is_termux=true
    echo -e "${GREEN}✓ Environment: Termux detected ($TERMUX_VERSION)${NC}"
else
    echo -e "${YELLOW}! Environment: Not Termux (Linux/CI mode)${NC}"
fi

# 2. Node.js Check
if command -v node &> /dev/null; then
    NODE_VERSION=$(node -v | cut -d'v' -f2)
    NODE_MAJOR=$(echo "$NODE_VERSION" | cut -d'.' -f1)
    if [ "$NODE_MAJOR" -ge 20 ]; then
        echo -e "${GREEN}✓ Node.js: $NODE_VERSION (>=20)${NC}"
    else
        echo -e "${RED}✗ Node.js: $NODE_VERSION (Required >=20)${NC}"
        echo "  Fix: pkg install nodejs-lts (on Termux) or install Node 20+"
    fi
else
    echo -e "${RED}✗ Node.js: Not found${NC}"
    echo "  Fix: pkg install nodejs-lts"
fi

# 3. Gemini CLI Check
if command -v gemini &> /dev/null; then
    GEMINI_VERSION=$(gemini --version 2>/dev/null || echo "Unknown")
    echo -e "${GREEN}✓ Gemini CLI: Installed ($GEMINI_VERSION)${NC}"
else
    echo -e "${RED}✗ Gemini CLI: Not found${NC}"
    echo "  Fix: Run ./install.sh and answer 'Y' to npm installation prompt."
fi

# 4. Termux API Check (only on Termux)
if [ "$is_termux" = true ]; then
    if pkg list-installed 2>/dev/null | grep -q "termux-api"; then
        echo -e "${GREEN}✓ termux-api: Installed (package)${NC}"
    else
        echo -e "${RED}✗ termux-api: Package not installed${NC}"
        echo "  Fix: pkg install termux-api"
    fi

    # Check if Termux:API app is actually working (simple check)
    if command -v termux-battery-status &> /dev/null; then
         # We won't run it as it might hang if API not accessible, just check presence
         echo -e "${GREEN}✓ termux-api: Commands available${NC}"
    else
         echo -e "${YELLOW}! termux-api: Commands check skipped or missing${NC}"
    fi
    echo "  Note: Ensure 'Termux:API' app is installed from Play Store/F-Droid and permissions granted."
fi

# 5. Configuration Check
echo ""
echo "=== Configuration Check ==="
CONFIG_FILE="$HOME/.gemini/settings.json"
PYTHON_CMD=""
if command -v python3 &> /dev/null; then PYTHON_CMD="python3"; elif command -v python &> /dev/null; then PYTHON_CMD="python"; fi

if [ -f "$CONFIG_FILE" ]; then
    if [ -n "$PYTHON_CMD" ]; then
        if $PYTHON_CMD -c "import sys, json; data=json.load(open('$CONFIG_FILE')); sys.exit(0 if 'selectedAuthType' in data and 'theme' in data else 1)" 2>/dev/null; then
             echo -e "${GREEN}✓ settings.json: Valid (Auth+Theme set)${NC}"
        else
             echo -e "${RED}✗ settings.json: Missing required fields${NC}"
             echo "  Fix: Run this command to patch your config:"
             echo -e "${YELLOW}  $PYTHON_CMD -c \"import json, os; p=os.path.expanduser('~/.gemini/settings.json'); d=json.load(open(p)); d.update({'theme': 'Default', 'selectedAuthType': 'oauth-personal'}); json.dump(d, open(p,'w'), indent=2); print('Patched settings.json')\"${NC}"
        fi
    else
        echo -e "${YELLOW}! Python not found, skipping JSON validation.${NC}"
    fi
else
    echo -e "${RED}✗ settings.json: Not found at $CONFIG_FILE${NC}"
    echo "  Fix: Run ./install.sh"
fi

# 6. Current Mode & Auth
echo ""
echo "=== Authentication Mode ==="
# Using default substitution for strict mode safety
if [ "${GOOGLE_GENAI_USE_VERTEXAI:-}" == "true" ]; then
    echo -e "${YELLOW}Mode: Vertex AI${NC}"
    echo "Project ID: ${GOOGLE_CLOUD_PROJECT:-<MISSING>}"
    echo "Location:   ${GOOGLE_CLOUD_LOCATION:-<MISSING>}"

    if [ -z "${GOOGLE_CLOUD_PROJECT:-}" ]; then
        echo -e "${RED}✗ Error: GOOGLE_CLOUD_PROJECT is not set.${NC}"
        echo "  Fix: gmode vertex <PROJECT_ID> [LOCATION]"
    fi
    if [ -z "${GOOGLE_CLOUD_LOCATION:-}" ]; then
        echo -e "${RED}✗ Error: GOOGLE_CLOUD_LOCATION is not set.${NC}"
        echo "  Fix: gmode vertex <PROJECT_ID> [LOCATION] (defaults to us-central1)"
    fi
else
    echo -e "${GREEN}Mode: Google (Default)${NC}"
    echo "  - Uses default Google login."
    echo "  - To authenticate: Run 'gemini auth login'"
fi

# 7. Vertex Transition Checklist
echo ""
echo "=== How to switch to Vertex AI (Optional) ==="
echo "If you want to use Vertex AI instead of Google default auth:"
echo "1. [ ] Create a Google Cloud Project."
echo "2. [ ] Enable Vertex AI API for that project."
echo "3. [ ] Switch mode: gmode vertex <PROJECT_ID> [LOCATION]"
