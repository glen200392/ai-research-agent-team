#!/usr/bin/env bash
# ============================================================
# AI Research Agent Team — First-Time Setup Script
# Run once on a new machine: bash setup.sh
# ============================================================
set -euo pipefail

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'
info()  { echo -e "${GREEN}✓ $1${NC}"; }
warn()  { echo -e "${YELLOW}⚠ $1${NC}"; }
error() { echo -e "${RED}✗ $1${NC}"; }

echo ""
echo "======================================================"
echo "  AI Research Agent Team — Environment Setup"
echo "======================================================"
echo ""

# ── 1. Python version ─────────────────────────────────────
PYTHON=$(command -v python3 || command -v python || true)
if [ -z "$PYTHON" ]; then
    error "Python 3.10+ required. Install from https://python.org"
    exit 1
fi

PY_VERSION=$($PYTHON -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
PY_MAJOR=$($PYTHON -c "import sys; print(sys.version_info.major)")
PY_MINOR=$($PYTHON -c "import sys; print(sys.version_info.minor)")

if [ "$PY_MAJOR" -lt 3 ] || { [ "$PY_MAJOR" -eq 3 ] && [ "$PY_MINOR" -lt 10 ]; }; then
    error "Python 3.10+ required, found $PY_VERSION"
    exit 1
fi
info "Python $PY_VERSION"

# ── 2. Virtual environment ────────────────────────────────
if [ ! -d ".venv" ]; then
    warn "Creating virtual environment (.venv)..."
    $PYTHON -m venv .venv
fi
info "Virtual environment ready"

# Activate
if [ -f ".venv/bin/activate" ]; then
    # shellcheck disable=SC1091
    source .venv/bin/activate
elif [ -f ".venv/Scripts/activate" ]; then
    # Windows Git Bash
    # shellcheck disable=SC1091
    source .venv/Scripts/activate
fi

# ── 3. Install dependencies ───────────────────────────────
echo ""
echo "Installing Python dependencies..."
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt
info "Dependencies installed"

# ── 4. Environment file ───────────────────────────────────
echo ""
if [ ! -f ".env" ]; then
    if [ -f "env.example" ]; then
        cp env.example .env
        warn ".env created from env.example — please edit it with your API keys"
    else
        error "env.example not found. Cannot create .env"
        exit 1
    fi
else
    info ".env already exists"
fi

# ── 5. Provider detection ─────────────────────────────────
echo ""
echo "Detecting available providers..."
python run.py detect || true

# ── 6. Ollama auto-install prompt ─────────────────────────
if ! command -v ollama &>/dev/null; then
    echo ""
    echo "────────────────────────────────────────────────────"
    echo "  Ollama not detected (optional for local AI models)"
    echo "  Install: curl -fsSL https://ollama.ai/install.sh | sh"
    echo "  Then:    ollama pull llama3.2"
    echo "           ollama serve"
    echo "────────────────────────────────────────────────────"
fi

# ── 7. Output directories ─────────────────────────────────
mkdir -p reports tmp/pipeline pedagogy/weekly-lessons pedagogy/topic-deep-dives
info "Output directories ready"

# ── 8. Final instructions ─────────────────────────────────
echo ""
echo "======================================================"
echo "  Setup complete!"
echo ""
echo "  Next steps:"
echo "  1. Edit .env with your API keys (at minimum: one LLM key + TAVILY_API_KEY)"
echo "  2. Validate: python run.py team-a --dry-run"
echo "  3. Run:      python run.py team-a"
echo ""
echo "  For local-only (no cloud API keys):"
echo "  1. Start Ollama: ollama serve"
echo "  2. Pull a model: ollama pull llama3.2"
echo "  3. Set in .env:  DEFAULT_LLM_PROVIDER=ollama"
echo "  4. Run:          python run.py team-a"
echo ""
echo "  Full docs: see CLAUDE.md"
echo "======================================================"
