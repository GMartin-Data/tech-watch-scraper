#!/usr/bin/env bash
set -e

# Script to bump version using commitizen
# Usage: ./scripts/bump.sh [major|minor|patch]

echo "Current version: $(uv run cz version --project)"
echo ""

if [[ -z "$1" ]]; then
    echo "Bumping version automatically based on commits..."
    uv run cz bump --yes --changelog
else
    echo "Bumping $1 version..."
    uv run cz bump --increment "$1" --yes --changelog
fi

echo ""
echo "New version: $(uv run cz version --project)"
echo ""
echo "Don't forget to push your changes and tags:"
echo "  git push && git push --tags"
