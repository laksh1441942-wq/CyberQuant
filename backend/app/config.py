import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'cyberquant.db')}")
MOCK_MODE = os.getenv("MOCK_MODE", "false").lower() == "true"

APP_NAME = "CyberQuant Risk Engine API"
VERSION = "1.0.0"
DESCRIPTION = "AI-Powered Continuous Cyber Risk Quantification & Investment Optimization Platform (SIH 2026)"
