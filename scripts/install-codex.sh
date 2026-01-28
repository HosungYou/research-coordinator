#!/bin/bash
#
# Diverga Codex CLI Installer
# Installs Diverga for OpenAI Codex CLI
#
# Usage:
#   curl -sSL https://raw.githubusercontent.com/HosungYou/Diverga/main/scripts/install-codex.sh | bash
#

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

REPO_URL="https://github.com/HosungYou/Diverga.git"
DEST_DIR="$HOME/.codex/diverga"

echo -e "${CYAN}"
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║              Diverga Installer for Codex CLI                  ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Clone repository
echo -e "${BLUE}[INFO]${NC} Cloning Diverga repository..."
TMP_DIR="/tmp/diverga-codex-$$"
git clone --depth 1 "$REPO_URL" "$TMP_DIR" 2>/dev/null

# Install
echo -e "${BLUE}[INFO]${NC} Installing to $DEST_DIR..."
mkdir -p "$DEST_DIR"

cp -r "$TMP_DIR/.codex/"* "$DEST_DIR/" 2>/dev/null || true
cp "$TMP_DIR/CLAUDE.md" "$DEST_DIR/" 2>/dev/null || true
cp "$TMP_DIR/AGENTS.md" "$DEST_DIR/" 2>/dev/null || true

chmod +x "$DEST_DIR/diverga-codex.cjs" 2>/dev/null || true

# Cleanup
rm -rf "$TMP_DIR"

# Verify
echo ""
if node "$DEST_DIR/diverga-codex.cjs" help &>/dev/null; then
    echo -e "${GREEN}[✓]${NC} Installation successful!"
    echo ""
    echo "Usage:"
    echo "  node ~/.codex/diverga/diverga-codex.cjs setup"
    echo "  node ~/.codex/diverga/diverga-codex.cjs list"
    echo "  node ~/.codex/diverga/diverga-codex.cjs agent A1"
else
    echo -e "${GREEN}[✓]${NC} Files installed (run 'node ~/.codex/diverga/diverga-codex.cjs setup' to verify)"
fi

echo ""
echo "Documentation: https://github.com/HosungYou/Diverga"
