#!/bin/bash
# Push local config changes to remote

set -e

CONFIG_DIR="$HOME/.ai-agent-config"

if [ ! -d "$CONFIG_DIR" ]; then
    echo "Error: Config not installed. Run install.sh first."
    exit 1
fi

cd "$CONFIG_DIR"

# Check for changes
if [ -z "$(git status --porcelain)" ]; then
    echo "No changes to push."
    exit 0
fi

echo "Changes:"
git status --short
echo ""

read -p "Commit message: " msg

if [ -z "$msg" ]; then
    msg="config: update"
fi

git add -A
git commit -m "$msg"
git push

echo "✓ Push complete"
