# AGENTS.md

This file provides instructions for AI agents working on this repository.

## Core Principles

1. **Safety First**: All scripts must be fail-closed. Never expose API keys or secrets in logs.
2. **Idempotency**: All installation and update scripts must be idempotent.
3. **Termux Compatibility**: Verify all changes against Termux environment constraints (e.g., `pkg` instead of `apt`, shebangs).
4. **Localization**: Documentation for users (`README.md`) must be in Polish. Code comments and commit messages in English.

## Testing

- Run `./scripts/self_check.sh` to validate the repository state.
- Ensure `shellcheck` passes for all `.sh` files.

## Workflow

When adding new features:
1. Create a plan.
2. Implement changes.
3. Verify using `scripts/doctor.sh` and `scripts/self_check.sh`.
4. Update `config/gemini/commands` if necessary.

## Directory Structure

- `scripts/`: Management scripts (doctor, update, check).
- `termux/`: Termux-specific logic (aliases, functions).
- `config/gemini/`: Configuration files and command definitions.
