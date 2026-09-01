#!/usr/bin/env bash
# ==============================================================================
# CyberQuant Backend Launcher (macOS & Linux)
# ==============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Detect python3 vs python
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python"
fi

echo "=================================================================="
echo "🚀 Starting CyberQuant Backend (macOS / Linux)"
echo "API Docs: http://127.0.0.1:8000/docs"
echo "=================================================================="

$PYTHON_CMD -m uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
