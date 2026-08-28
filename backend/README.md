# ⚡ CyberQuant Backend API Service

**Engineer:** Saksham (Backend Lead)  
**Framework:** FastAPI + Uvicorn + SQLAlchemy  
**Target:** SIH 2026

---

## 📌 Overview

This directory contains the complete backend architecture for **CyberQuant**. It connects enterprise assets and vulnerabilities from the data layer, calculates financial risk (Expected Annual Loss in INR), and exposes high-performance REST API endpoints for the frontend dashboard and external integrations.

---

## 📂 Architecture Structure

```text
backend/
├── app/
│   ├── config.py              # Configuration & environment settings
│   ├── database.py            # SQLAlchemy database engine & session
│   ├── main.py                # FastAPI application entrypoint & CORS
│   │
│   ├── models/                # SQLAlchemy Database Tables
│   │   ├── asset.py           # Assets table (150 enterprise nodes)
│   │   ├── vulnerability.py   # CVE Vulnerabilities table
│   │   └── control.py         # Security Controls & Frameworks
│   │
│   ├── schemas/               # Pydantic Request/Response validation
│   │   ├── dashboard.py       # Executive overview DTOs
│   │   ├── asset.py           # Asset inventory DTOs
│   │   ├── scenario.py        # What-If simulation schemas
│   │   ├── optimize.py        # Knapsack optimizer schemas
│   │   ├── ai.py              # AI Analyst query schemas
│   │   └── compliance.py      # Framework mapping schemas
│   │
│   ├── services/              # Business Logic & Algorithms
│   │   ├── seed.py            # Auto-ingestion from data/generated/
│   │   ├── risk_service.py    # FAIR Risk Quantification & Likelihood
│   │   ├── optimizer_service.py # 0/1 Knapsack Budget Optimizer & ROSI
│   │   └── ai_service.py      # Grounded AI Analyst Response Generator
│   │
│   └── routes/                # Modular REST API Routers
│       ├── dashboard.py       # GET  /api/dashboard
│       ├── assets.py          # GET  /api/assets, GET /api/assets/{id}
│       ├── risks.py           # GET  /api/risks/top
│       ├── scenario.py        # POST /api/scenario
│       ├── optimize.py        # POST /api/investment/optimize
│       ├── ai.py              # POST /api/ai/query
│       └── compliance.py      # GET  /api/compliance
│
├── requirements.txt           # Python backend dependencies
└── README.md                  # This documentation
```

---

## 🚀 How to Run the Backend Server

1. **Install Dependencies:**
   ```bash
   pip install -r backend/requirements.txt
   ```

2. **Start the API Server:**
   ```bash
   uvicorn backend.app.main:app --reload --port 8000
   ```

3. **Interactive Documentation:**
   * **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   * **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📡 Core API Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Health check & service metadata |
| `GET` | `/api/dashboard` | Executive summary (Risk Score, EAL in ₹, Exposure) |
| `GET` | `/api/assets` | Inventory of all 150 monitored assets with EAL |
| `GET` | `/api/assets/{asset_id}` | Detailed risk profile for an individual asset |
| `GET` | `/api/risks/top` | Top N highest financial risk contributor assets |
| `POST` | `/api/scenario` | What-If simulation (e.g. `enable_mfa_all`) |
| `POST` | `/api/investment/optimize` | Knapsack budget allocation & ROSI calculation |
| `POST` | `/api/ai/query` | Natural-language query interface for AI Risk Analyst |
| `GET` | `/api/compliance` | Regulatory alignment for RBI, SEBI, NIST CSF, ISO 27001 |
