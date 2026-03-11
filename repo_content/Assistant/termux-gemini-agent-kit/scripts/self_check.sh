#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

# self_check.sh - Validates the repository state

echo "Running Self Check..."

# 1. Syntax Check & Strict Mode Compliance
echo "Checking shell scripts compliance (shebang & strict mode)..."
FAIL=0
while IFS= read -r -d '' script; do
    # Check shebang
    if ! grep -q "^#!/usr/bin/env bash" "$script"; then
        echo "FAILURE: $script missing portable shebang (#!/usr/bin/env bash)"
        FAIL=1
    fi
    # Check strict mode
    if ! grep -q "set -euo pipefail" "$script"; then
        echo "FAILURE: $script missing 'set -euo pipefail'"
        FAIL=1
    fi
    if ! grep -q "IFS=\$'\\\\n\\\\t'" "$script"; then
        echo "FAILURE: $script missing IFS safety"
        FAIL=1
    fi
done < <(find . -name "*.sh" -print0)

if [ "$FAIL" -eq 1 ]; then
    echo "Strict mode check failed."
    exit 1
fi

echo "Checking shell scripts syntax..."
# shellcheck disable=SC2038
find . -name "*.sh" -print0 | xargs -0 bash -n

# 2. Secret Scan (Basic)
echo "Scanning for accidental secrets..."
# Exclude .git and self_check.sh itself
if grep -rE "AIza[a-zA-Z0-9_]{35}" . --exclude-dir=.git --exclude=self_check.sh; then
    echo "FAILURE: Potential API key found."
    exit 1
fi

# 3. Config Validation
echo "Validating config JSON..."
if [ ! -f "config/gemini/settings.json" ]; then
    echo "FAILURE: config/gemini/settings.json missing."
    exit 1
fi

if command -v jq &> /dev/null; then
    jq . config/gemini/settings.json > /dev/null
    echo "JSON syntax is valid."
    if ! jq -e '.selectedAuthType and .theme' config/gemini/settings.json > /dev/null; then
         echo "FAILURE: config/gemini/settings.json missing selectedAuthType or theme."
         exit 1
    fi
elif command -v python3 &> /dev/null; then
    if ! python3 -c "import sys, json; data=json.load(open('config/gemini/settings.json')); sys.exit(0 if 'selectedAuthType' in data and 'theme' in data else 1)"; then
         echo "FAILURE: config/gemini/settings.json missing selectedAuthType or theme."
         exit 1
    fi
    echo "JSON syntax and fields valid (checked via python)."
else
    echo "jq and python3 not installed, skipping JSON validation."
fi

# 4. Command files existence & structure
echo "Checking critical files..."
if [ ! -f "config/gemini/GEMINI.md" ]; then
    echo "FAILURE: config/gemini/GEMINI.md missing."
    exit 1
fi

if command -v python3 &> /dev/null; then
    echo "Validating command TOML files..."
    python3 scripts/validate_commands.py config/gemini/commands
else
    echo "WARNING: python3 not found, skipping TOML validation."
fi

echo "Self Check Passed."
