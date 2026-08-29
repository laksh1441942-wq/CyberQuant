import os
from pathlib import Path

# Cross-platform path resolution (works identically on Windows, macOS, and Linux)
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BASE_DIR.parent

DEFAULT_SQLITE_PATH = (BASE_DIR / "cyberquant.db").as_posix()
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DEFAULT_SQLITE_PATH}")
MOCK_MODE = os.getenv("MOCK_MODE", "false").lower() == "true"

APP_NAME = "CyberQuant Risk Engine API"
VERSION = "1.0.0"
DESCRIPTION = "AI-Powered Continuous Cyber Risk Quantification & Investment Optimization Platform (SIH 2026)"
