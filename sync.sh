#!/bin/bash
# Sync config from remote

set -e

CONFIG_DIR="$HOME/.ai-agent-config"

if [ ! -d "$CONFIG_DIR" ]; then
    echo "Error: Config not installed. Run install.sh first."
    exit 1
fi

cd "$CONFIG_DIR"

# Check for local changes
if [ -n "$(git status --porcelain)" ]; then
    echo "Warning: Local changes detected."
    echo "  - Stash: git stash"
    echo "  - Discard: git checkout ."
    echo ""
    read -p "Discard local changes and sync? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git checkout .
    else
        echo "Sync cancelled."
        exit 1
    fi
fi

echo "Syncing from remote..."
git pull

echo "✓ Sync complete"
