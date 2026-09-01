@echo off
:: ==============================================================================
:: CyberQuant Backend Launcher (Windows)
:: ==============================================================================
echo ==================================================================
echo Starting CyberQuant Backend (Windows)
echo API Docs: http://127.0.0.1:8000/docs
echo ==================================================================

python -m uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
