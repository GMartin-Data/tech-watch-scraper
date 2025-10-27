#!/usr/bin/env bash
set -e

# Script to run code quality checks locally
# Usage: ./scripts/lint.sh [--fix]

echo "Running Ruff linter..."

if [[ "$1" = "--fix" ]]; then
    echo "  (with auto-fix enabled)"
    uv run ruff check --fix .
else
    uv run ruff check .
fi

echo ""
echo "Running Ruff formatter..."

if [[ "$1" = "--fix" ]]; then
    echo "  (formatting files)"
    uv run ruff format .
else
    uv run ruff format --check .
fi

echo ""
echo "Code quality checks completed!"
