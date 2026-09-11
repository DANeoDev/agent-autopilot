#!/usr/bin/env bash
# Antigravity Autopilot - Uninstaller for macOS & Linux

set -e

CONFIG_DIR="$HOME/.gemini/config"
SKILLS_DIR="$CONFIG_DIR/skills"
BIN_DIR="$HOME/.gemini/antigravity/bin"

echo "Uninstalling Antigravity Autopilot components..."

# Remove skills
rm -rf "$SKILLS_DIR/model-router"
rm -rf "$SKILLS_DIR/project-autopilot"
echo "  Removed custom skills."

# Remove binaries
rm -f "$BIN_DIR/agy_router.py"
rm -f "$BIN_DIR/agy_project_manager.py"
rm -f "$BIN_DIR/agy-route"
rm -f "$BIN_DIR/agy-autopilot"
rm -f "$BIN_DIR/agy-route.bat"
rm -f "$BIN_DIR/agy-autopilot.bat"
echo "  Removed CLI launchers."

echo "Autopilot components uninstalled successfully."
echo "Note: ~/.gemini/config/AGENTS.md was preserved so custom user rules are not lost."
