# Nexus CLI

Ujednolicony interfejs CLI do pracy z modelami AI.

## Termux setup
1. `pkg update && pkg install python git`
2. `python -m venv .venv && source .venv/bin/activate`
3. `pip install -r requirements.txt`
4. `bash aliases/install_aliases.sh`

## Przykłady
- `nexus ask "co to jest MCP?"`
- `cat error.log | nexus review`
- `nexus config show`
