#!/usr/bin/env bash
# Antigravity Autopilot - One-Line macOS & Linux Installer
# Installs intelligent model routing, autonomous project mode, and CLI tools machine-wide.

set -e

CYAN='\033[0;36m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
GRAY='\033[0;90m'
NC='\033[0m'

echo -e "${CYAN}========================================================${NC}"
echo -e "${CYAN}  ANTIGRAVITY AUTOPILOT - MACOS & LINUX INSTALLER      ${NC}"
echo -e "${YELLOW}  (Experimental Tooling - Use At Your Own Risk)        ${NC}"
echo -e "${CYAN}========================================================${NC}"
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
CONFIG_DIR="$HOME/.gemini/config"
SKILLS_DIR="$CONFIG_DIR/skills"
BIN_TARGET="$HOME/.gemini/antigravity/bin"

# 1. Verify / Create Directories
echo -e "${YELLOW}[1/5] Checking Antigravity environment...${NC}"
mkdir -p "$CONFIG_DIR" "$SKILLS_DIR" "$BIN_TARGET"
echo -e "${GRAY}  Ensured directories: $CONFIG_DIR, $SKILLS_DIR, $BIN_TARGET${NC}"

# 2. Install Global Orchestration Rules (AGENTS.md)
echo -e "${YELLOW}[2/5] Installing Global Orchestration Guidelines...${NC}"
AGENTS_SRC="$ROOT_DIR/customizations/rules/AGENTS.md"
AGENTS_DST="$CONFIG_DIR/AGENTS.md"

if [ -f "$AGENTS_DST" ]; then
    if grep -q "Antigravity Global Model Orchestration Guidelines" "$AGENTS_DST"; then
        echo -e "${GRAY}  Updating existing Antigravity orchestration rules...${NC}"
        cp -f "$AGENTS_SRC" "$AGENTS_DST"
    else
        echo -e "${GRAY}  Existing AGENTS.md detected; merging guidelines...${NC}"
        printf "\n\n" >> "$AGENTS_DST"
        cat "$AGENTS_SRC" >> "$AGENTS_DST"
    fi
else
    cp -f "$AGENTS_SRC" "$AGENTS_DST"
fi
echo -e "${GREEN}  Installed: $AGENTS_DST${NC}"

# 3. Install Custom Skills
echo -e "${YELLOW}[3/5] Installing Global Skills (model-router, project-autopilot)...${NC}"
SKILLS_SRC="$ROOT_DIR/customizations/skills"

for skill in "model-router" "project-autopilot"; do
    mkdir -p "$SKILLS_DIR/$skill"
    cp -rf "$SKILLS_SRC/$skill/"* "$SKILLS_DIR/$skill/"
    echo -e "${GRAY}  Installed Skill: $skill -> $SKILLS_DIR/$skill${NC}"
done

# Register in skills.json
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
echo -e "${GREEN}  Configured: $SKILLS_JSON${NC}"

# 4. Install Binaries and CLI Tools
echo -e "${YELLOW}[4/5] Installing CLI Tools & Python Runners...${NC}"
cp -rf "$ROOT_DIR/bin/"* "$BIN_TARGET/"
chmod +x "$BIN_TARGET/agy-route" "$BIN_TARGET/agy-autopilot" 2>/dev/null || true

# Add to PATH in shell profile if missing
PATH_LINE="export PATH=\"\$HOME/.gemini/antigravity/bin:\$PATH\""

for rc_file in "$HOME/.zshrc" "$HOME/.bashrc" "$HOME/.profile"; do
    if [ -f "$rc_file" ]; then
        if ! grep -q ".gemini/antigravity/bin" "$rc_file"; then
            printf "\n# Antigravity Autopilot CLI\n%s\n" "$PATH_LINE" >> "$rc_file"
            echo -e "${GREEN}  Added Antigravity bin to $rc_file${NC}"
        fi
    fi
done

# 5. Verify Installation
echo -e "${YELLOW}[5/5] Running Self-Verification Test...${NC}"
python3 "$BIN_TARGET/agy_router.py" "Write unit test for user service" >/dev/null 2>&1 && {
    echo -e "${GREEN}  Verification passed!${NC}"
} || {
    echo -e "${YELLOW}  Note: Verify python3 availability if verification threw a warning.${NC}"
}

echo ""
echo -e "${CYAN}========================================================${NC}"
echo -e "${CYAN}  INSTALLATION COMPLETED SUCCESSFULLY!                 ${NC}"
echo -e "${CYAN}========================================================${NC}"
echo "Available CLI commands from your terminal (after restarting shell):"
echo "  * agy-route <prompt>      : Classify and select optimal model"
echo "  * agy-autopilot --status  : Inspect current project settings"
echo "  * agy-autopilot --enable-autopilot : Enable autonomous permissions"
echo ""
