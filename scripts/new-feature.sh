#!/usr/bin/env bash
set -e

# Script to create a new feature branch
# Usage: ./scripts/new-feature.sh feature-name

if [[ -z "$1" ]]; then
    echo "Error: Feature name is required"
    echo "Usage: ./scripts/new-feature.sh feature-name"
    exit 1
fi

FEATURE_NAME="$1"
BRANCH_NAME="feature/$FEATURE_NAME"

echo "Creating new feature branch: $BRANCH_NAME"
git checkout -b "$BRANCH_NAME"

echo ""
echo "Feature branch created successfully!"
echo ""
echo "Next steps:"
echo "  1. Make your changes"
echo "  2. Run ./scripts/lint.sh to check code quality"
echo "  3. Commit with: git commit (commitizen will guide you)"
echo "  4. Push with: git push -u origin $BRANCH_NAME"
echo "  5. Create a pull request on GitHub"
