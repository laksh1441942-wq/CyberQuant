# CyberQuant — AI-Powered Continuous Cyber Risk Quantification & Investment Optimization

> **Smart India Hackathon (SIH 2026)**  
> _Turn Technical Cyber Flaws into Financial Exposure and Optimal Security Investments._

---

## 📌 Project Overview

Enterprises invest heavily in cybersecurity, yet cyber risk is still predominantly communicated using qualitative ratings such as **"Low"**, **"Medium"**, or **"High"**. These labels fail to express potential financial loss, making it difficult for boards, CISOs, and executives to allocate security budgets effectively.

**CyberQuant** bridges this gap by continuously correlating technical security telemetry (vulnerabilities, misconfigurations, identity posture) with business asset criticality, computing **Expected Annual Loss (EAL)** in **Rupees (₹)**, and recommending optimal security control investments under fixed budget constraints.

---

## 🚀 Day 1 Deliverable: Synthetic Enterprise Telemetry Generator

Because real enterprise security telemetry is confidential and protected by data privacy regulations, **Day 1** delivers a realistic, correlated **Synthetic Enterprise Data Generator** (`generate_data.py`).

### Generated Datasets (`data/generated/`):

- **`assets.json`** — **150 enterprise assets** (Core Banking DB, Payment Gateway APIs, IAM servers, Cloud storage, employee laptops) with financial valuations, department owners, and downtime costs. Total valuation: **₹39.37 Crores**.
- **`vulnerabilities.json`** — **69 CVE vulnerabilities** mapped to assets with CVSS severity scores, exploit availability, and patch costs.
- **`controls.json`** — **6 enterprise security controls** (MFA, Patch Program, EDR, Network Segmentation, Cloud WAF, Backup Vault) with implementation costs, risk reduction metrics, and mapping to **RBI, NIST CSF, CIS, and ISO 27001** frameworks.
- **`threats.json`** — Active threat intelligence feeds (Ransomware, Credential Stuffing, API Abuse, Supply Chain).
- **`summary.json`** — Metadata and high-level enterprise statistics.

---

## 🛠️ Tech Stack (100% Free & Open-Source)

- **Language:** Python 3.10+
- **Backend Framework:** FastAPI + Uvicorn + Pydantic
- **Data Processing:** Pandas, NumPy
- **Optimization:** SciPy (Knapsack Algorithm)
- **Frontend:** HTML5, Modern CSS, Vanilla JS, Chart.js

---

## ⚡ Quick Start & Setup

### 1. Clone the Repository

```bash
git clone <your-github-repo-url>
cd <repo-folder>
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Data Generator

```bash
python generate_data.py
```

### Output:

```text
[DAY 1] Starting CyberQuant Synthetic Data Generator...
[OK] Generated 150 enterprise assets.
[OK] Generated 69 vulnerabilities mapped across assets.
[OK] Generated 6 security control options with framework mappings.
[SAVED] data/generated/assets.json
[SAVED] data/generated/vulnerabilities.json
[SAVED] data/generated/controls.json
[SAVED] data/generated/threats.json
[SAVED] data/generated/summary.json

======================================================================
DAY 1 TASK COMPLETE!
Total Assets Created:         150 (Valuation: INR 39.37 Crores)
Total Vulnerabilities Mapped: 69 (52 Critical)
Security Controls Defined:    6
======================================================================
```

---

## 📂 Repository Structure

```text
.
├── data/
│   └── generated/
│       ├── assets.json            # 150 enterprise computers & servers
│       ├── vulnerabilities.json   # 69 mapped CVE flaws
│       ├── controls.json          # Security controls & framework mappings
│       ├── threats.json           # Threat intelligence feeds
│       └── summary.json           # Enterprise valuation summary
├── generate_data.py               # Day 1 Synthetic Data Generator script
├── risk_engine.py                 # Day 2 FAIR Risk Quantification Engine
├── main.py                        # Day 3 FastAPI REST API Backend Server
├── requirements.txt               # Python dependencies
├── .gitignore                     # Git ignored files
└── README.md                      # Project documentation
```

---

## 🚀 Day 2 Deliverable: FAIR Risk Quantification Engine

**Day 2** delivers the mathematical risk engine (`risk_engine.py`) implementing the **FAIR (Factor Analysis of Information Risk)** standard:

* **Likelihood Calculation ($P$):** Combines CVSS vulnerability severity, internet exposure (+0.30), and active defenses (MFA -0.35, EDR -0.25).
* **Financial Impact Modeling ($I$):** Direct asset valuation + hourly downtime losses + forensic recovery costs in **Rupees (₹)**.
* **Expected Annual Loss ($\text{EAL} = P \times I$):** Computed per computer asset and aggregated across the enterprise.
* **Enterprise Risk Benchmark:**
  * **Enterprise Risk Score:** `41 / 100`
  * **Total Expected Annual Loss:** `₹12.05 Crores`
  * **Top Risk Asset:** `Identity & IAM Controller` (EAL: ₹2.74 Crores / year)
* **What-If Scenario Simulation:** Deploying Hardware Token MFA saves **₹6.74 Crores** in expected losses with **3,272% ROSI**.

Run the Risk Engine:
```bash
python risk_engine.py
```

---

## ⚡ Day 3 Deliverable: FastAPI Web Backend Server

**Day 3** delivers the high-speed REST API server (`main.py`) powered by **FastAPI** and **Uvicorn**:

* **CORS Enabled:** Seamless integration with any browser or frontend client.
* **Core API Endpoints:**
  * `GET /` — Service health check & metadata
  * `GET /api/dashboard` — Enterprise Risk Score (41/100), Total EAL (₹12.05 Cr), Potential Exposure
  * `GET /api/assets` — Evaluated inventory of all 150 assets with likelihood %, CVSS, and loss in ₹
  * `GET /api/risks/top` — Top 5 highest financial risk contributor assets
  * `POST /api/scenario` — What-If simulation engine (MFA, EDR, combined remediation)
* **Interactive Documentation:**
  * **Swagger UI:** `http://127.0.0.1:8000/docs`
  * **ReDoc:** `http://127.0.0.1:8000/redoc`

Run the Backend Server:
```bash
uvicorn main:app --reload --port 8000
```

---

## 📅 Roadmap

- [x] **Day 1:** Synthetic Enterprise Data Generator & Schema Setup
- [x] **Day 2:** FAIR Mathematical Risk Quantification Engine
- [x] **Day 3:** FastAPI REST API Backend
- [ ] **Day 4:** Knapsack Budget Optimizer & Scenario Simulator
- [ ] **Day 5:** Frontend Interactive Dashboard & Chart.js Visualizations
- [ ] **Day 6:** End-to-End Testing & Live Hackathon Demo Preparation

---

## 📜 License

MIT Open Source License.
