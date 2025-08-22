#!/bin/bash

# Claude Code Multi-Agent System Uninstaller
# This script removes the agent system from Claude Code

echo "🤖 Claude Code Multi-Agent System Uninstaller"
echo "============================================"
echo ""
echo "⚠️  WARNING: This will remove all agents and their data!"
echo ""
read -p "Are you sure you want to uninstall? (y/N): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Uninstall cancelled."
    exit 0
fi

echo ""
echo "🔄 Uninstalling..."

# Remove agents
if [ -d "$HOME/.claude/agents" ]; then
    echo "  - Removing agents..."
    rm -rf "$HOME/.claude/agents"
fi

# Optionally remove observation data
echo ""
read -p "Remove observation data and history? (y/N): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [ -d "$HOME/.claude/observation" ]; then
        echo "  - Removing observation infrastructure..."
        rm -rf "$HOME/.claude/observation"
    fi
    if [ -d "$HOME/.claude/global-observation" ]; then
        echo "  - Removing global observation data..."
        rm -rf "$HOME/.claude/global-observation"
    fi
fi

# Remove other components
if [ -d "$HOME/.claude/ledgers" ]; then
    echo "  - Removing ledgers..."
    rm -rf "$HOME/.claude/ledgers"
fi

if [ -f "$HOME/.claude/task-registry.json" ]; then
    echo "  - Removing task registry..."
    rm -f "$HOME/.claude/task-registry.json"
fi

if [ -f "$HOME/.claude/agent-protocols.md" ]; then
    echo "  - Removing agent protocols..."
    rm -f "$HOME/.claude/agent-protocols.md"
fi

echo ""
echo "✅ Uninstall complete!"
echo ""
echo "Note: The ~/.claude directory was preserved for other Claude Code data."
echo "      You can manually remove it if no longer needed."
echo ""