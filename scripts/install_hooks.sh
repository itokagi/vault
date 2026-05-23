#!/usr/bin/env bash
# Install git hooks for the LLM Wiki vault.
set -e
REPO_ROOT="$(git rev-parse --show-toplevel)"
git config core.hooksPath .githooks
chmod +x "$REPO_ROOT/.githooks/pre-commit"
echo "Hooks installed. git will run .githooks/pre-commit before each commit."
