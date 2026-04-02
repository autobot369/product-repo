#!/usr/bin/env bash
# setup.sh — PM Workspace bootstrapper
# Usage: ./setup.sh [-- <pm_setup args>]
#
# 1. Verifies Python 3.10+
# 2. Creates .venv if missing
# 3. Creates root requirements.txt if missing (shouldn't happen in a cloned repo)
# 4. Installs all dependencies
# 5. Hands off to the Python setup CLI

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$REPO_ROOT/.venv"
REQUIREMENTS="$REPO_ROOT/requirements.txt"

# ── colours ────────────────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; BOLD='\033[1m'; RESET='\033[0m'

info()    { echo -e "${CYAN}${BOLD}[setup]${RESET} $*"; }
success() { echo -e "${GREEN}${BOLD}[setup]${RESET} $*"; }
warn()    { echo -e "${YELLOW}${BOLD}[setup]${RESET} $*"; }
error()   { echo -e "${RED}${BOLD}[setup]${RESET} $*" >&2; }

# ── 1. Python version check ────────────────────────────────────────────────────
PYTHON_BIN=""
for candidate in python3 python python3.12 python3.11 python3.10; do
    if command -v "$candidate" &>/dev/null; then
        version=$("$candidate" -c "import sys; print(sys.version_info[:2])" 2>/dev/null)
        major=$(echo "$version" | tr -d '(),' | awk '{print $1}')
        minor=$(echo "$version" | tr -d '(),' | awk '{print $2}')
        if [[ "$major" -ge 3 && "$minor" -ge 10 ]]; then
            PYTHON_BIN="$candidate"
            break
        fi
    fi
done

if [[ -z "$PYTHON_BIN" ]]; then
    error "Python 3.10 or higher is required but was not found."
    error "Install it from https://www.python.org/downloads/ then re-run this script."
    exit 1
fi

PY_VERSION=$("$PYTHON_BIN" --version 2>&1)
info "Using $PY_VERSION ($PYTHON_BIN)"

# ── 2. Virtual environment ─────────────────────────────────────────────────────
if [[ ! -d "$VENV_DIR" ]]; then
    info "Creating virtual environment at .venv ..."
    "$PYTHON_BIN" -m venv "$VENV_DIR"
    success ".venv created"
else
    info ".venv already exists — skipping creation"
fi

# Activate
if [[ -f "$VENV_DIR/bin/activate" ]]; then
    # shellcheck disable=SC1091
    source "$VENV_DIR/bin/activate"
elif [[ -f "$VENV_DIR/Scripts/activate" ]]; then
    # Windows / Git Bash
    # shellcheck disable=SC1091
    source "$VENV_DIR/Scripts/activate"
else
    error "Could not find venv activation script. Delete .venv and retry."
    exit 1
fi

# ── 3. requirements.txt guard ──────────────────────────────────────────────────
if [[ ! -f "$REQUIREMENTS" ]]; then
    warn "requirements.txt not found at repo root — generating from tool requirements ..."
    python "$REPO_ROOT/tools/setup/bootstrap_requirements.py"
    success "requirements.txt created"
fi

# ── 4. Install dependencies ────────────────────────────────────────────────────
info "Installing dependencies from requirements.txt ..."
pip install --quiet --upgrade pip
pip install --quiet -r "$REQUIREMENTS"
success "Dependencies installed"

echo ""
echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo -e "${BOLD}  PM Workspace Setup${RESET}"
echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo ""

# ── 5. Hand off to Python CLI ─────────────────────────────────────────────────
exec python -m tools.setup "$@"
