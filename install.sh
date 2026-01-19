#!/bin/bash
# AI Agent Config Installer
# Supports: Claude Code, OpenAI Codex

set -e

REPO="https://github.com/testkim00/ai-agent-config.git"
CONFIG_DIR="$HOME/.ai-agent-config"

echo "=== AI Agent Config Installer ==="

# Clone or update
if [ -d "$CONFIG_DIR" ]; then
    echo "Updating existing config..."
    cd "$CONFIG_DIR" && git pull
else
    echo "Cloning config repository..."
    git clone "$REPO" "$CONFIG_DIR"
fi

# Claude Code setup
if [ -d "$HOME/.claude" ]; then
    echo "Setting up Claude Code..."

    # Backup existing
    [ -d "$HOME/.claude/skills" ] && [ ! -L "$HOME/.claude/skills" ] && mv "$HOME/.claude/skills" "$HOME/.claude/skills.bak"
    [ -d "$HOME/.claude/commands" ] && [ ! -L "$HOME/.claude/commands" ] && mv "$HOME/.claude/commands" "$HOME/.claude/commands.bak"

    # Create symlinks
    ln -sf "$CONFIG_DIR/claude/skills" "$HOME/.claude/skills"
    ln -sf "$CONFIG_DIR/claude/commands" "$HOME/.claude/commands"

    echo "  ✓ Claude Code configured"
fi

# Codex setup
if [ -d "$HOME/.codex" ]; then
    echo "Setting up Codex..."

    # Backup existing
    [ -d "$HOME/.codex/skills" ] && [ ! -L "$HOME/.codex/skills" ] && mv "$HOME/.codex/skills" "$HOME/.codex/skills.bak"

    # Create symlinks
    ln -sf "$CONFIG_DIR/codex/skills" "$HOME/.codex/skills"

    echo "  ✓ Codex configured"
fi

echo ""
echo "=== Installation Complete ==="
echo "Config location: $CONFIG_DIR"
echo ""
echo "Commands:"
echo "  Sync:  $CONFIG_DIR/sync.sh"
echo "  Push:  $CONFIG_DIR/push.sh"
