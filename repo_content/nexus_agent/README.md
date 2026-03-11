# Nexus Agent

Centralny orkiestrator Google ADK dla projektu Nexus.

## Instalacja (Termux)
1. `pkg update && pkg upgrade`
2. `pkg install python git`
3. `python -m venv .venv && source .venv/bin/activate`
4. `pip install -r requirements.txt`

## Użycie
- `python -m nexus_agent "Przeanalizuj repozytorium"`
- `python -m nexus_agent -p "Opisz architekturę"`
- `python -m nexus_agent` (chat)
