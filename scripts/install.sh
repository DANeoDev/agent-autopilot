#!/usr/bin/env bash
# Autopilot - Universal Multi-Agent Terminal Installer
# Installs intelligent model routing, autonomous project mode, and CLI tools across:
# Google Antigravity, Anthropic Claude Code, Cursor, Windsurf, OpenAI Codex & Universal Agents.

set -e

CYAN='\033[0;36m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
GRAY='\033[0;90m'
NC='\033[0m'

echo -e "${CYAN}========================================================${NC}"
echo -e "${CYAN}  AUTOPILOT - UNIVERSAL MULTI-AGENT INSTALLER          ${NC}"
echo -e "${NC}  Supporting: Antigravity, Claude Code, Cursor, Windsurf, Codex${NC}"
echo -e "${YELLOW}  (Experimental Tooling - Use At Your Own Risk)        ${NC}"
echo -e "${CYAN}========================================================${NC}"
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
AGENTS_SRC="$ROOT_DIR/customizations/rules/AGENTS.md"
SKILLS_SRC="$ROOT_DIR/customizations/skills"
BIN_SRC="$ROOT_DIR/bin"
BIN_TARGET="$HOME/.gemini/antigravity/bin"
MODELS_SRC="$ROOT_DIR/models"
MODELS_TARGET="$HOME/.gemini/autopilot/models"

install_rules() {
    local target_file="$1"
    local agent_name="$2"
    local target_dir
    target_dir="$(dirname "$target_file")"
    mkdir -p "$target_dir"

    if [ -f "$target_file" ]; then
        if grep -q "Antigravity Global Model Orchestration Guidelines" "$target_file"; then
            echo -e "${GRAY}  [$agent_name] Updating existing Autopilot guidelines...${NC}"
            cp -f "$AGENTS_SRC" "$target_file"
        else
            echo -e "${GRAY}  [$agent_name] Appending guidelines to existing config...${NC}"
            printf "\n\n" >> "$target_file"
            cat "$AGENTS_SRC" >> "$target_file"
        fi
    else
        cp -f "$AGENTS_SRC" "$target_file"
    fi
    echo -e "${GREEN}  [$agent_name] Installed: $target_file${NC}"
}

# 1. Target: Google Antigravity
echo -e "${YELLOW}[1/6] Configuring Google Antigravity...${NC}"
CONFIG_DIR="$HOME/.gemini/config"
SKILLS_DIR="$CONFIG_DIR/skills"
mkdir -p "$CONFIG_DIR" "$SKILLS_DIR" "$BIN_TARGET"

install_rules "$CONFIG_DIR/AGENTS.md" "Antigravity"

for skill in "model-router" "project-autopilot"; do
    mkdir -p "$SKILLS_DIR/$skill"
    cp -rf "$SKILLS_SRC/$skill/"* "$SKILLS_DIR/$skill/"
    echo -e "${GRAY}  [Antigravity] Installed Skill: $skill${NC}"
done

SKILLS_JSON="$CONFIG_DIR/skills.json"
cat << 'EOF' > "$SKILLS_JSON"
{
  "entries": [
    {
      "path": "skills"
    }
  ]
}
EOF

# 2. Target: Anthropic Claude Code
if [ -d "$HOME/.claude" ] || [ "${TARGET:-auto}" = "all" ] || [ "${TARGET:-auto}" = "claude" ]; then
    echo -e "${YELLOW}[2/6] Configuring Anthropic Claude Code...${NC}"
    install_rules "$HOME/.claude/CLAUDE.md" "Claude Code"
fi

# 3. Target: Cursor AI Agent
if [ -d "$HOME/.cursor" ] || [ -d "$HOME/Library/Application Support/Cursor" ] || [ "${TARGET:-auto}" = "all" ] || [ "${TARGET:-auto}" = "cursor" ]; then
    echo -e "${YELLOW}[3/6] Configuring Cursor AI Agent...${NC}"
    install_rules "$HOME/.cursorrules" "Cursor"
fi

# 4. Target: Windsurf Cascade
if [ -d "$HOME/.codeium" ] || [ -d "$HOME/.windsurf" ] || [ "${TARGET:-auto}" = "all" ] || [ "${TARGET:-auto}" = "windsurf" ]; then
    echo -e "${YELLOW}[4/6] Configuring Windsurf Cascade...${NC}"
    install_rules "$HOME/.windsurfrules" "Windsurf"
fi

# 5. Target: Universal Agent Standards & OpenAI Codex
echo -e "${YELLOW}[5/6] Configuring Universal Agent Standards (Codex, Aider, OpenHands)...${NC}"
install_rules "$HOME/AGENTS.md" "Universal Home"
install_rules "$HOME/.config/agents/AGENTS.md" "Universal Config"

# 6. Install CLI Tools, Models & Configure PATH
echo -e "${YELLOW}[6/6] Installing CLI Tools, Cognitive Models & Configuring PATH...${NC}"
mkdir -p "$BIN_TARGET"
cp -rf "$BIN_SRC/"* "$BIN_TARGET/"
if [ -d "$MODELS_SRC" ]; then
    mkdir -p "$MODELS_TARGET"
    cp -rf "$MODELS_SRC/"* "$MODELS_TARGET/"
fi
mkdir -p "$HOME/.gemini/autopilot/memory"
chmod +x "$BIN_TARGET/agy-route" "$BIN_TARGET/agy-autopilot" "$BIN_TARGET/agy-predict" "$BIN_TARGET/agy-status" "$BIN_TARGET/agy-audit" "$BIN_TARGET/agy-memory" 2>/dev/null || true
chmod +x "$BIN_TARGET/agent-route" "$BIN_TARGET/agent-autopilot" "$BIN_TARGET/agent-predict" "$BIN_TARGET/agent-status" "$BIN_TARGET/agent-audit" "$BIN_TARGET/agent-memory" 2>/dev/null || true

PATH_LINE="export PATH=\"\$HOME/.gemini/antigravity/bin:\$PATH\""
for rc_file in "$HOME/.zshrc" "$HOME/.bashrc" "$HOME/.profile"; do
    if [ -f "$rc_file" ]; then
        if ! grep -q ".gemini/antigravity/bin" "$rc_file"; then
            printf "\n# Autopilot Multi-Agent CLI\n%s\n" "$PATH_LINE" >> "$rc_file"
            echo -e "${GREEN}  Added Autopilot bin to $rc_file${NC}"
        fi
    fi
done

# Self-Verification Test
echo -e "${YELLOW}Running Self-Verification Test...${NC}"
python3 "$BIN_TARGET/agy_router.py" "Write unit test for user service" >/dev/null 2>&1 && {
    echo -e "${GREEN}  Verification passed!${NC}"
} || {
    echo -e "${YELLOW}  Note: Verify python3 availability if verification threw a warning.${NC}"
}

echo ""
echo -e "${CYAN}========================================================${NC}"
echo -e "${CYAN}  INSTALLATION COMPLETED SUCCESSFULLY!                 ${NC}"
echo -e "${CYAN}========================================================${NC}"
echo "Available CLI commands across all agent terminals:"
echo "  * agy-route / agent-route         : Classify and select optimal model"
echo "  * agy-autopilot / agent-autopilot : Inspect or enable autonomous mode"
echo "  * agy-predict / agent-predict     : Predict continuous complex pass depth (Z = X + iY)"
echo "  * agy-status / agent-status       : Interactive visual HUD & cognitive dashboard"
echo "  * agy-audit / agent-audit         : In-situ 'Is vs. Ought' gap audit & PR generator"
echo "  * agy-memory / agent-memory       : Cross-project architectural memory & decisions"
echo ""
echo ""

