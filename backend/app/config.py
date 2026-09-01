import os
from pathlib import Path

# Cross-platform path resolution (works identically on Windows, macOS, and Linux)
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BASE_DIR.parent

# Primary Database: PostgreSQL (as specified by team architecture)
DEFAULT_PG_URL = "postgresql://postgres:postgres@localhost:5432/cyberquant"
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_PG_URL)

# Fallback path only if local developer PostgreSQL service is temporarily unstarted
SQLITE_FALLBACK_URL = f"sqlite:///{(BASE_DIR / 'cyberquant.db').as_posix()}"
MOCK_MODE = os.getenv("MOCK_MODE", "false").lower() == "true"

# Target Enterprise Profile (Calibrated for Section 8 & 9 of SIH 2026 Specification)
COMPANY_NAME = "Fintech Enterprise (Medium-Sized Bank & Financial Services)"
COMPANY_SECTOR = "Banking & Financial Services (RBI / SEBI Regulated)"
APP_NAME = "CyberQuant Risk Engine API"
VERSION = "1.0.0"
DESCRIPTION = f"{COMPANY_NAME} — Continuous Cyber Risk Quantification & Investment Optimization"
