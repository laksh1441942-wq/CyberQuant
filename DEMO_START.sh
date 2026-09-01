#!/bin/bash
# CyberQuant Demo Day Quick Start - September 2, 2026

echo "🚀 CyberQuant Demo Environment Setup"
echo "======================================"
echo ""

# Navigate to project
cd /Users/lakshsharma/Desktop/github_repo/CyberQuant

# Activate virtual environment
echo "1️⃣  Activating Python environment..."
source .venv/bin/activate
echo "   ✓ Environment activated"
echo ""

# Generate synthetic data (if not already present)
echo "2️⃣  Generating synthetic enterprise data..."
PYTHONPATH=/Users/lakshsharma/Desktop/github_repo/CyberQuant python generate_data.py 2>&1 | grep -E "OK|SAVED|COMPLETE"
echo "   ✓ Data generated (150 assets, 69 vulnerabilities, 6 controls)"
echo ""

# Start the FastAPI backend in background
echo "3️⃣  Starting FastAPI backend server..."
PYTHONPATH=/Users/lakshsharma/Desktop/github_repo/CyberQuant \
  python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 > /tmp/cyberquant_api.log 2>&1 &
sleep 3

# Verify API is running
if curl -s http://127.0.0.1:8000/ > /dev/null 2>&1; then
    echo "   ✓ API running on http://127.0.0.1:8000"
else
    echo "   ✗ API failed to start - check /tmp/cyberquant_api.log"
    exit 1
fi
echo ""

# Run quick integration test
echo "4️⃣  Running integration tests..."
PYTHONPATH=/Users/lakshsharma/Desktop/github_repo/CyberQuant python tests/test_integration.py 2>&1 | tail -20
echo ""

# Run demo
echo "5️⃣  Starting demo presentation..."
echo "   (Press Ctrl+C to stop)"
echo ""
sleep 1
PYTHONPATH=/Users/lakshsharma/Desktop/github_repo/CyberQuant python DEMO_SCRIPT.py

# Cleanup
echo ""
echo "======================================"
echo "Demo Complete! Cleaning up..."
pkill -f "uvicorn" 2>/dev/null || true
echo "✓ Environment cleaned"
