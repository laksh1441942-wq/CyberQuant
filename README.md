# AI-Powered Continuous Cyber Risk Quantification & Investment Optimization Platform

## SIH 2026 — Team Project Specification & Discussion README

> **Purpose of this document:** This README is designed for the six-member team to discuss, understand, scope, divide, and implement the SIH problem statement before starting development.
>
> **Prototype target:** A convincing, working end-to-end prototype for the internal hackathon on **2 September 2026**.
>
> **Important:** This is a prototype. We should not claim that it is production-ready, connected to real enterprise security infrastructure, or trained on confidential enterprise data unless that is actually true.

---

# 1. Problem Statement

## Title

**AI-Powered Continuous Cyber Risk Quantification and Investment Optimization Platform**

## Background

Enterprises and institutions spend heavily on cybersecurity tools, compliance programs, and risk management. However, cyber risk is still commonly communicated through qualitative categories such as:

- Low
- Medium
- High

These categories do not clearly communicate the **potential financial consequences** of cyber incidents.

This creates a gap between:

```text
Technical Cybersecurity
        ↓
Risk Management
        ↓
Business / Executive Decision-Making
```

Cyber risk is also dynamic.

New vulnerabilities appear, threat actors change tactics, business services are added or removed, and security controls improve or deteriorate.

Traditional periodic risk assessments can therefore become stale.

The proposed system should continuously analyze enterprise security and business data and answer:

> **How much cyber risk does the organization currently face, what is driving that risk, what could it cost financially, and where should the organization spend its security budget to reduce the most risk?**

---

# 2. Core Problem We Need to Solve

Our platform must bridge:

```text
TECHNICAL DATA
      ↓
CYBER RISK
      ↓
FINANCIAL EXPOSURE
      ↓
SECURITY INVESTMENT
      ↓
BUSINESS DECISION
```

Instead of telling an executive:

> "Critical vulnerability detected."

we want to tell them:

> "This vulnerability contributes approximately ₹18.5 lakh to expected annual cyber loss. Patching it for ₹1.2 lakh is estimated to reduce exposure by ₹9.7 lakh."

That is the central idea of our project.

---

# 3. Proposed Product

## Product Name

### CyberQuant

Possible tagline:

> **Turn Cyber Risk Into Business Decisions.**

Alternative:

> **Measure Risk. Predict Loss. Optimize Security Investment.**

---

# 4. What CyberQuant Should Do

CyberQuant should ingest security and business information and continuously calculate:

### 1. What assets do we have?

```text
Servers
Applications
Databases
Cloud resources
Endpoints
User accounts
Business services
```

### 2. How exposed are they?

```text
Vulnerabilities
Misconfigurations
Identity weaknesses
Endpoint alerts
Cloud risks
Threat intelligence
Security incidents
```

### 3. How important are those assets?

Example:

```text
Payroll Server       → Critical
Customer Database    → Critical
Internal Wiki        → Medium
Test Server          → Low
```

### 4. What is the probability of an incident?

Example:

```text
Probability of major incident:
18%
```

### 5. What could the incident cost?

Example:

```text
Potential financial impact:
₹1.2 Crore
```

### 6. What is the expected annual loss?

Example:

```text
Expected Annual Loss:
₹21.6 Lakh
```

### 7. What should the organization do?

Example:

```text
1. Patch internet-facing server
2. Enable MFA for privileged accounts
3. Segment critical database
4. Improve EDR coverage
```

### 8. What should management spend money on?

Example:

```text
Available Budget: ₹10 Crore

Recommended allocation:

MFA                  ₹1.2 Cr
Network Segmentation ₹3.0 Cr
EDR Expansion        ₹2.1 Cr
Critical Patching    ₹0.8 Cr
Monitoring           ₹1.4 Cr
Reserve              ₹1.5 Cr
```

The actual values in the prototype will be generated from synthetic assumptions.

---

# 5. The Main Innovation

Our strongest idea should be:

## Risk → Money → Action → Investment

Most cybersecurity dashboards stop at:

```text
Risk Score = 82
```

Our platform continues:

```text
Risk Score
    ↓
Financial Exposure
    ↓
Risk Drivers
    ↓
Possible Mitigations
    ↓
Cost of Mitigation
    ↓
Expected Risk Reduction
    ↓
ROSI
    ↓
Optimal Investment Portfolio
```

This directly addresses the business problem in the PS.

---

# 6. Core Questions Our System Should Answer

An executive should be able to ask:

### Enterprise-level

> What is our highest financial cyber risk today?

> How much cyber exposure do we currently have?

> Is our security budget adequate?

> What will happen if we reduce the security budget by 20%?

### Risk-level

> Which risks contribute most to expected annual loss?

> Which assets are responsible for most of our exposure?

> Which vulnerabilities should we fix first?

### Investment-level

> I have ₹1 crore. Where should I spend it?

> What happens if we spend ₹50 lakh on MFA?

> Which security control provides the highest risk reduction per rupee?

> What happens if we delay remediation for 30 days?

### Compliance-level

> Which NIST/CIS/ISO controls are weak?

> Which assets have missing compliance evidence?

---

# 7. Target Users

## Primary Users

### CISO

Needs:

- Enterprise cyber exposure
- Risk trends
- Investment recommendations
- Risk reduction
- ROSI

### Risk Officer

Needs:

- Quantified risk
- Risk contributors
- Business impact
- Scenario analysis
- Framework mapping

### Security Engineer / SOC Team

Needs:

- Vulnerabilities
- Assets
- Controls
- Remediation priorities
- Technical findings

### Executive / Board

Needs:

- Financial exposure
- Top risks
- Investment decisions
- Trend
- ROI

---

# 8. Prototype Persona

For the September 2 demonstration, we should simulate:

> **A medium-sized financial organization / fintech company**

Why?

Because this gives us a natural connection to:

- Financial loss
- Customer data
- Regulatory pressure
- High-value transactions
- Identity security
- RBI cybersecurity expectations

However, the architecture should remain organization-agnostic.

---

# 9. Prototype Scenario

We will create a synthetic enterprise containing:

```text
100–500 assets
20–50 business services
500–2,00,0 users
100+ vulnerabilities
10–30 security controls
Multiple threat scenarios
```

Example assets:

```text
Customer Database
Payment API
Internet Gateway
HR System
Core Banking Integration
Employee Laptops
Cloud Storage
Identity Provider
Admin Portal
Internal Application
```

Each asset will have:

```text
Asset ID
Asset Type
Business Owner
Business Criticality
Data Sensitivity
Revenue Dependency
Availability Requirement
Location
Dependencies
```

---

# 10. Security Data We Will Simulate

The real solution should be capable of ingesting data from:

- Vulnerability Management
- SIEM
- IAM
- EDR
- CSPM
- Asset Inventory
- Threat Intelligence
- Compliance systems

For the prototype, we will simulate these feeds.

Example:

```text
Vulnerability Scanner
        ↓
Vulnerability Findings

SIEM
        ↓
Security Events

IAM
        ↓
Identity / Privilege Data

EDR
        ↓
Endpoint Security Data

CSPM
        ↓
Cloud Misconfigurations

Asset Inventory
        ↓
Business Context

Threat Intelligence
        ↓
Threat Likelihood
```

---

# 11. Synthetic Data Strategy

We should NOT pretend to have real enterprise telemetry.

Instead:

> **We will generate a synthetic enterprise dataset that mimics realistic relationships between assets, vulnerabilities, controls, threats, business impact, and financial loss.**

This gives us complete control over the demo.

---

# 12. Proposed Data Model

## Asset

```text
asset_id
asset_name
asset_type
business_unit
business_criticality
data_sensitivity
revenue_dependency
availability_criticality
location
owner
```

## Vulnerability

```text
vulnerability_id
asset_id
cve_id
severity
cvss_score
exploit_available
internet_exposed
age_days
patch_available
```

## Threat

```text
threat_id
threat_type
sector
likelihood
target_asset_type
active_status
```

## Security Control

```text
control_id
control_name
control_type
implementation_status
effectiveness
cost
maintenance_cost
coverage
```

## Security Event

```text
event_id
asset_id
event_type
severity
timestamp
source
confidence
```

## Business Service

```text
service_id
service_name
owner
criticality
revenue_per_day
customers_affected
downtime_cost_per_hour
```

## Risk

```text
risk_id
asset_id
threat_id
likelihood
impact
risk_score
annualized_loss
confidence
```

## Mitigation

```text
mitigation_id
name
type
cost
implementation_time
risk_reduction
affected_assets
```

## Investment

```text
investment_id
mitigation_id
cost
expected_risk_reduction
expected_loss_reduction
rosi
```

---

# 13. Risk Quantification Engine

This is the heart of the project.

We need to convert technical findings into financial exposure.

A simplified prototype model can use:

```text
Expected Annual Loss (EAL)

= Annual Probability of Incident
  × Financial Impact of Incident
```

Example:

```text
Incident Probability = 0.20
Potential Loss        = ₹1 Crore

EAL = 0.20 × ₹1 Crore
    = ₹20 Lakh
```

This is a simplified prototype calculation, not a claim that real-world cyber risk can always be reduced to one equation.

---

# 14. Financial Impact Model

Potential loss can be composed of:

```text
Financial Impact =
    Downtime Cost
  + Data Breach Cost
  + Incident Response Cost
  + Regulatory/Compliance Cost
  + Recovery Cost
  + Customer Impact
  + Reputational Impact
```

For the prototype:

```text
Total Loss =
Downtime
+
Data
+
Recovery
+
Regulatory
+
Other Business Impact
```

We should make every assumption visible.

---

# 15. Risk Calculation Pipeline

```text
Asset
  ↓
Technical Findings
  ↓
Threat Likelihood
  ↓
Control Effectiveness
  ↓
Business Criticality
  ↓
Incident Probability
  ↓
Financial Impact
  ↓
Expected Annual Loss
```

---

# 16. Asset Criticality

Technical severity alone is not enough.

Example:

### Server A

```text
CVSS = 9.8
Business Criticality = Low
```

### Server B

```text
CVSS = 7.5
Business Criticality = Critical
```

Server B may deserve higher business priority.

Therefore our system should combine:

```text
Technical Severity
+
Business Criticality
+
Exposure
+
Threat Activity
+
Control Effectiveness
```

---

# 17. Control Effectiveness

A security control should not simply be:

```text
MFA = Enabled
```

We should model:

```text
MFA Coverage = 82%
MFA Effectiveness = 90%
Privileged Accounts Covered = 65%
Recent Incidents = 2
```

Example:

```text
Control Effectiveness = f(
    coverage,
    configuration,
    incident history,
    compliance status
)
```

This allows the platform to identify:

> "MFA exists, but only 65% of privileged accounts are protected."

---

# 18. Continuous Risk Concept

The PS emphasizes continuous risk.

We can simulate this in the prototype using changing telemetry.

Example:

### Monday

```text
Risk = ₹42 Lakh
```

### New critical vulnerability discovered

```text
Risk = ₹68 Lakh
```

### Patch deployed

```text
Risk = ₹51 Lakh
```

### MFA coverage improved

```text
Risk = ₹39 Lakh
```

The dashboard should show:

```text
Risk Trend
₹68L ──╮
       │╲
₹51L   │ ╲
       │  ╲
₹39L   │   ╲
       └────────────
```

This demonstrates the "continuous" concept without needing live enterprise feeds.

---

# 19. AI/ML Layer

We should not use AI everywhere just for the sake of saying "AI-powered."

Use ML where it provides value.

## Possible ML tasks

### 1. Incident likelihood prediction

Predict probability that an asset/threat combination will lead to a security incident.

### 2. Risk trend prediction

Predict whether exposure is increasing or decreasing.

### 3. Anomaly detection

Identify unusual security telemetry.

### 4. Risk-driver ranking

Identify factors contributing most to exposure.

### 5. Mitigation impact estimation

Estimate expected reduction from a security control.

---

# 20. Initial ML Approach

Because we have approximately eight days, begin with interpretable models.

Possible models:

- Logistic Regression
- Random Forest
- Gradient Boosting
- XGBoost
- Isolation Forest for anomaly detection

Do NOT build a deep neural network unless the dataset actually justifies it.

The prototype should prioritize:

```text
Explainability
+
Reliability
+
Working Integration
```

over model complexity.

---

# 21. AI Decision Support Layer

This layer sits above the numerical risk engine.

It answers:

> What is happening?

> Why is it happening?

> What should we do?

> How much will it help?

---

# 22. LLM / Ollama Role

Ollama should act as an:

## AI Cyber Risk Analyst

The LLM receives structured system data.

Example:

```text
Enterprise EAL: ₹2.4 Cr

Top Risk:
Customer Database

Risk:
₹62 Lakh

Drivers:
- Internet exposure
- Critical vulnerability
- High data sensitivity
- Weak segmentation
- Active threat intelligence
```

Ollama generates:

> "The customer database is currently the largest contributor to expected annual cyber loss. The primary drivers are internet exposure, an exploitable vulnerability, high data sensitivity and insufficient network segmentation."

The LLM should **not invent numerical values**.

Numbers should come from the risk engine.

---

# 23. Natural Language Query Interface

The dashboard should include:

```text
Ask CyberQuant...
```

Example:

> "What is our highest financial cyber risk today?"

Response:

```text
Your highest current financial risk is the Customer
Database, contributing approximately ₹62 lakh to
Expected Annual Loss.

The top drivers are:
1. Critical vulnerability
2. Internet exposure
3. High-value customer data
4. Weak network segmentation
```

Another:

> "Which vulnerabilities contribute most to our expected losses?"

---

# 24. Scenario Simulation

This is one of the strongest demo features.

The user changes a variable.

Example:

```text
Scenario:
Enable MFA for all privileged users
```

Current:

```text
EAL = ₹2.4 Cr
```

After scenario:

```text
EAL = ₹1.9 Cr
```

Therefore:

```text
Risk Reduction = ₹50 Lakh
```

Another:

> "What happens if we delay critical patching by 30 days?"

System:

```text
Current EAL: ₹2.4 Cr
30-day delayed EAL: ₹2.8 Cr

Additional exposure:
₹40 Lakh
```

These values will be based on our prototype assumptions/model.

---

# 25. Investment Optimization

This is the feature that can make our solution stand out.

Suppose:

```text
Available Budget:
₹1 Crore
```

Possible investments:

| Control | Cost | Expected Risk Reduction |
|---|---:|---:|
| MFA | ₹20L | ₹35L |
| EDR | ₹30L | ₹42L |
| Segmentation | ₹40L | ₹60L |
| Patch Program | ₹10L | ₹25L |
| Monitoring | ₹15L | ₹18L |

The system chooses the combination that provides the maximum risk reduction within ₹1 crore.

---

# 26. Optimization Problem

Conceptually:

```text
Maximize:

Total Expected Risk Reduction

Subject to:

Total Investment Cost ≤ Budget
```

This can initially be implemented as:

- Knapsack optimization
- Integer programming
- Linear programming
- Greedy optimization baseline

We can later improve it if time permits.

---

# 27. ROSI

Return on Security Investment:

```text
ROSI ≈
(Expected Loss Reduction - Security Investment Cost)
/
Security Investment Cost
```

Example:

```text
Investment = ₹20L
Expected Loss Reduction = ₹35L

ROSI = (35 - 20) / 20
     = 75%
```

The exact formula and assumptions should be clearly documented.

---

# 28. Investment vs Risk Reduction Curve

The dashboard should show:

```text
Risk
│\
│ \
│  \
│   \____
│        \____
└────────────────
       Investment
```

This demonstrates diminishing returns.

The system can highlight:

```text
Recommended Spend Zone
```

For example:

```text
₹70L–₹90L
```

where additional spending produces meaningful risk reduction before diminishing returns become large.

---

# 29. Executive Dashboard

The first screen should immediately communicate:

```text
CYBERQUANT — EXECUTIVE RISK OVERVIEW

Enterprise Risk Score       72/100

Expected Annual Loss        ₹2.4 Cr

Current Security Budget     ₹5 Cr

Top Risk Contributor        Customer Database

Potential Risk Reduction    ₹1.1 Cr

Security Investment ROI     74%
```

Then:

```text
Risk Trend
Top Risk Contributors
Investment Opportunities
Framework Coverage
```

---

# 30. Technical Dashboard

Technical users should be able to drill down:

```text
Asset
 ↓
Vulnerability
 ↓
Threat
 ↓
Control
 ↓
Risk
 ↓
Financial Exposure
 ↓
Recommended Remediation
```

Example:

```text
Asset:
Payment API

CVSS:
9.8

Internet Exposed:
YES

Threat Activity:
HIGH

Control Effectiveness:
52%

Expected Annual Loss:
₹34L

Recommended Action:
Patch + WAF + network segmentation

Estimated Cost:
₹8L

Estimated Risk Reduction:
₹21L
```

---

# 31. Compliance / Framework Mapping

The PS explicitly asks for mapping against:

- ISO/IEC 27001
- NIST Cybersecurity Framework
- CIS Controls
- RBI Cyber Security Framework
- SEBI Cybersecurity and Cyber Resilience Framework

We should not attempt to build every control from every framework in eight days.

Instead, build a **framework mapping engine** with a representative subset.

Example:

```text
Finding:
MFA missing for privileged users

Mapped Controls:

NIST:
Identity Management / Access Control

CIS:
Account Management / Access Control

ISO:
Access Control

RBI:
Identity and Access Management

SEBI:
Access Control / Cyber Resilience
```

For the prototype, the mapping should be based on documented reference data and clearly labeled as a prototype mapping.

---

# 32. Compliance Dashboard

Example:

```text
FRAMEWORK COVERAGE

NIST CSF          78%
ISO 27001         74%
CIS Controls      81%
RBI Framework     69%
SEBI Framework    73%
```

Clicking a framework:

```text
Control
Status
Evidence
Risk
Affected Assets
Recommended Action
```

---

# 33. Blockchain Role

Blockchain should NOT be forced into the core risk calculation.

Use it for:

## Tamper-Evident Risk & Investment Audit

When the platform produces:

```text
Risk Assessment
Investment Recommendation
Scenario Result
Compliance Report
```

we can hash the final record.

```text
Risk Report
     ↓
Canonical JSON
     ↓
SHA-256
     ↓
Sepolia
```

Store only:

```text
report_id
hash
timestamp
version
```

Do NOT put:

- Personal data
- Passwords
- Full security logs
- Sensitive vulnerabilities
- Financial account information

on a public blockchain.

---

# 34. Recommended Technology Stack

## Frontend

For the eight-day deadline:

```text
HTML
CSS
Vanilla JavaScript
Chart.js
```

Optional:

```text
Leaflet.js
```

for asset/geographic visualization.

Avoid React unless someone already knows it well.

## Backend

```text
Python
FastAPI
Pydantic
SQLAlchemy
Uvicorn
```

## Database

```text
PostgreSQL
```

## ML

```text
Python
pandas
NumPy
scikit-learn
XGBoost
```

## LLM

```text
Ollama
```

Potential fallback:

```text
Cloud LLM API
```

## Blockchain

```text
Sepolia
Solidity
Web3.py or ethers
```

---

# 35. Proposed Architecture

```text
                         EXECUTIVE / CISO
                                |
                                v
                    +-----------------------+
                    |    Web Dashboard      |
                    | Charts + Risk + Query |
                    +-----------+-----------+
                                |
                                v
                    +-----------------------+
                    |        FastAPI        |
                    |     API / Services    |
                    +-----------+-----------+
                                |
          +---------------------+----------------------+
          |                     |                      |
          v                     v                      v
 +----------------+     +---------------+     +----------------+
 |   PostgreSQL   |     | Risk Engine   |     | Compliance     |
 |                |     |               |     | Mapping        |
 | Assets         |     | Quantification|     | ISO/NIST/CIS   |
 | Vulnerabilities|     | Probability   |     | RBI/SEBI       |
 | Threats        |     | Impact        |     +----------------+
 | Controls       |     | EAL / VaR     |
 | Events         |     +-------+-------+
 +----------------+             |
                                v
                       +-------------------+
                       | AI / ML Layer     |
                       | Prediction        |
                       | Anomaly Detection |
                       | Risk Drivers      |
                       +---------+---------+
                                 |
                 +---------------+---------------+
                 |                               |
                 v                               v
        +------------------+             +-------------------+
        | Investment       |             | Ollama / LLM      |
        | Optimization     |             | AI Risk Analyst   |
        |                  |             | Explanation       |
        | Budget           |             | NL Queries        |
        | ROSI             |             | Recommendations   |
        +---------+--------+             +-------------------+
                  |
                  v
        +----------------------+
        | Scenario Simulation  |
        | What-if Analysis     |
        +----------+-----------+
                   |
                   v
        +----------------------+
        | Sepolia Audit Layer  |
        | Hash / Timestamp     |
        +----------------------+
```

---

# 36. Team Roles

There are six members.

## 1. Laksh — AI/ML + Risk Quantification + Integration

### Main responsibility

Own the mathematical/AI brain of the project.

### Tasks

- Understand cyber risk quantification
- Design risk model
- Design EAL calculation
- Feature engineering
- ML model
- Risk-driver analysis
- Scenario impact calculation
- Help integrate all components
- Understand the complete architecture

### Deliverables

```text
ml/
risk_engine/
quantification/
scenario_engine/
```

### Priority

**Highest technical priority.**

---

# 37. Saksham — Backend Engineer

### Main responsibility

FastAPI + PostgreSQL.

### Tasks

- Learn FastAPI quickly
- Database schema
- SQLAlchemy
- API endpoints
- Data ingestion APIs
- Risk APIs
- Scenario APIs
- Investment APIs
- LLM API integration
- Blockchain API integration

### Deliverables

```text
backend/
```

Main APIs:

```text
GET  /api/dashboard
GET  /api/assets
GET  /api/risks
GET  /api/vulnerabilities

POST /api/risk/calculate
POST /api/scenario
POST /api/investment/optimize

POST /api/ai/query
POST /api/audit
```

---

# 38. Shivam — Cybersecurity Architecture

### Main responsibility

Make sure the project actually makes cybersecurity sense.

### Tasks

- Vulnerability modeling
- Threat modeling
- Asset criticality
- Control effectiveness
- Attack scenarios
- Cyber-risk indicators
- Security architecture
- Threat intelligence concepts
- Privacy/security review

### Deliverables

```text
threat-model.md
risk-indicators.md
security-architecture.md
```

He should also challenge the ML assumptions.

---

# 39. Rajat — Cybersecurity + Data

### Main responsibility

Synthetic enterprise data + security analytics.

### Tasks

- Build synthetic dataset generator
- Asset inventory
- Vulnerability dataset
- Security event dataset
- Threat dataset
- Control dataset
- Scenario dataset
- Data validation
- ML evaluation
- Create realistic attack scenarios

### Deliverables

```text
data/
data/generator/
evaluation/
```

---

# 40. Mridul — Frontend + QA Support

Since Mridul is new, give him a manageable but meaningful role.

### Phase 1

Learn:

```text
HTML
CSS
JavaScript
Fetch API
Chart.js
```

### Phase 2

Build:

```text
Executive Dashboard
Risk Cards
Risk Charts
Investment Chart
Scenario UI
```

### Phase 3

Help with:

```text
API integration
Testing
Demo preparation
```

He should have a mentor from the team, preferably Saksham for API integration or Seema for UI/product flow.

---

# 41. Seema — Product, Presentation & QA

### Main responsibility

Own the product story and judge experience.

### Tasks

- Understand complete system
- User journey
- Executive UX
- Dashboard information hierarchy
- PPT
- Demo script
- Documentation
- Test cases
- Judge questions
- Final presentation
- Business impact explanation

She should not be isolated from technical work.

She must understand:

```text
Risk
EAL
ROSI
Investment Optimization
AI
Blockchain
Compliance
```

well enough to explain them.

---

# 42. Team Collaboration

Use GitHub.

Recommended branches:

```text
main
develop

feature/ml
feature/backend
feature/frontend
feature/cyber
feature/blockchain
feature/compliance
```

Nobody should directly experiment on `main`.

Workflow:

```text
Create branch
    ↓
Implement
    ↓
Test
    ↓
Commit
    ↓
Pull Request
    ↓
Review
    ↓
Merge
```

---

# 43. Project Folder Structure

```text
cyberquant/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   │
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── routes/
│   │   ├── services/
│   │   └── utils/
│   │
│   └── requirements.txt
│
├── ml/
│   ├── data/
│   ├── preprocessing.py
│   ├── features.py
│   ├── train.py
│   ├── predict.py
│   ├── evaluate.py
│   └── models/
│
├── risk_engine/
│   ├── likelihood.py
│   ├── impact.py
│   ├── eal.py
│   ├── var.py
│   ├── controls.py
│   └── risk_score.py
│
├── optimization/
│   ├── optimizer.py
│   ├── rosi.py
│   └── scenarios.py
│
├── compliance/
│   ├── nist.json
│   ├── iso.json
│   ├── cis.json
│   ├── rbi.json
│   └── sebi.json
│
├── blockchain/
│   ├── contracts/
│   ├── scripts/
│   └── README.md
│
├── frontend/
│   ├── index.html
│   ├── dashboard.html
│   ├── css/
│   └── js/
│
├── data/
│   ├── generate_data.py
│   └── generated/
│
├── docs/
│   ├── architecture.md
│   ├── risk-model.md
│   ├── demo.md
│   └── presentation.md
│
├── .env.example
├── .gitignore
└── README.md
```

---

# 44. API Design

## Dashboard

```http
GET /api/dashboard
```

Returns:

```json
{
  "enterprise_risk_score": 72,
  "expected_annual_loss": 24000000,
  "top_risk": "Customer Database",
  "risk_reduction_opportunity": 11000000
}
```

## Assets

```http
GET /api/assets
GET /api/assets/{id}
```

## Vulnerabilities

```http
GET /api/vulnerabilities
GET /api/vulnerabilities/{id}
```

## Risk

```http
GET /api/risks
GET /api/risks/{id}
POST /api/risk/calculate
```

## Scenario

```http
POST /api/scenario
```

Example:

```json
{
  "action": "enable_mfa",
  "coverage": 100
}
```

Response:

```json
{
  "current_eal": 24000000,
  "scenario_eal": 19000000,
  "risk_reduction": 5000000
}
```

## Investment Optimization

```http
POST /api/investment/optimize
```

Input:

```json
{
  "budget": 10000000
}
```

Output:

```json
{
  "recommended_controls": [],
  "total_cost": 9800000,
  "expected_loss_reduction": 14500000,
  "rosi": 0.48
}
```

---

# 45. Prototype Dashboard

## Executive Overview

```text
+-------------------------------------------------------+
|                  CYBERQUANT                           |
|          Enterprise Cyber Risk Overview               |
+-------------------------------------------------------+

Enterprise Risk Score           72 / 100

Expected Annual Loss            ₹2.40 Cr

Potential Maximum Loss          ₹8.60 Cr

Top Risk Contributor             Customer Database

Risk Reduction Opportunity      ₹1.10 Cr

+-------------------+-------------------+
| Risk Trend        | Risk Contributors |
|                   |                   |
|     /\            | Customer DB       |
|    /  \__         | Payment API       |
| __/                | IAM               |
+-------------------+-------------------+

Recommended Investment
[ View Optimization ]
```

---

# 46. Investment Optimization Screen

User enters:

```text
Available Security Budget:

₹1,00,00,000
```

System displays:

```text
OPTIMAL SECURITY INVESTMENT

1. Critical Patch Program
   Cost: ₹10L
   Risk Reduction: ₹25L

2. MFA Expansion
   Cost: ₹20L
   Risk Reduction: ₹35L

3. Network Segmentation
   Cost: ₹40L
   Risk Reduction: ₹60L

4. EDR Expansion
   Cost: ₹30L
   Risk Reduction: ₹42L
```

Then:

```text
Total Investment: ₹1 Cr

Expected Risk Reduction:
₹1.20 Cr

ROSI:
20%
```

The actual numbers should come from our model/data, not hardcoded claims in the final presentation.

---

# 47. Scenario Simulator

UI:

```text
WHAT-IF SIMULATOR

Current EAL:
₹2.40 Cr

Scenario:
[ Enable MFA for privileged accounts ]

Coverage:
[ 100% ]

Implementation Cost:
₹20L

Predicted New EAL:
₹1.90 Cr

Risk Reduction:
₹50L

ROSI:
150%
```

Other scenarios:

```text
[ Patch critical vulnerabilities ]

[ Increase EDR coverage ]

[ Deploy network segmentation ]

[ Improve backup resilience ]

[ Delay remediation by 30 days ]

[ Reduce security budget by 20% ]
```

---

# 48. Natural Language Interface

Example UI:

```text
Ask CyberQuant

"What is our highest financial cyber risk today?"
```

The system should:

```text
User Question
     ↓
Intent Detection
     ↓
Fetch structured data
     ↓
Risk Engine / Database
     ↓
Ollama
     ↓
Natural-language answer
```

Do not let the LLM directly calculate important financial values if those values can be obtained from the deterministic risk engine.

---

# 49. Risk Driver Visualization

Example:

```text
WHY IS CUSTOMER DATABASE HIGH RISK?

Internet Exposure       ██████████
Critical Vulnerability  █████████
Data Sensitivity        █████████
Threat Activity         ███████
Weak Segmentation       ██████
Control Effectiveness   █████
```

This improves explainability.

---

# 50. Framework Mapping

Create a mapping table:

```text
Finding
   ↓
Security Control
   ↓
Framework References
```

Example:

```text
Finding:
Privileged accounts without MFA

Mapped Frameworks:

NIST CSF:
Identity / Access Control

CIS Controls:
Account Management

ISO/IEC 27001:
Access Control

RBI:
Identity & Access Management

SEBI:
Cybersecurity / Access Control
```

The exact mapping must be validated against the actual framework/control wording before claiming regulatory compliance.

---

# 51. Continuous Risk Simulation

Since real live telemetry may not be available during the demo, create a simulation.

Button:

```text
SIMULATE NEW TELEMETRY
```

Events:

```text
New Critical CVE
New SIEM Alert
MFA Coverage Decreases
Threat Actor Activity Increases
Patch Deployed
```

Dashboard updates:

```text
Before:
EAL = ₹2.4 Cr

After New Vulnerability:
EAL = ₹2.9 Cr

After Patch:
EAL = ₹2.1 Cr
```

This visually demonstrates continuous risk.

---

# 52. 8-Day Development Plan

## August 25 — Understand + Design

### Everyone

- Read PS
- Agree on interpretation
- Choose product name
- Choose demo organization
- Freeze architecture
- Create GitHub repository

### Laksh

Risk model design.

### Saksham

FastAPI/PostgreSQL architecture.

### Shivam

Threat/control model.

### Rajat

Data schema.

### Mridul

Dashboard wireframe.

### Seema

User journey + presentation outline.

### End-of-day requirement

Everyone should be able to explain the product in 60 seconds.

---

# 53. August 26 — Data + Backend

### Laksh

Implement:

```text
risk_score
likelihood
impact
EAL
```

### Saksham

Implement:

```text
FastAPI
PostgreSQL
SQLAlchemy
Models
```

### Shivam

Define:

```text
threats
controls
risk factors
```

### Rajat

Build:

```text
synthetic data generator
```

### Mridul

Build:

```text
dashboard HTML/CSS
```

### Seema

Build:

```text
PPT structure
demo story
```

---

# 54. August 27 — Risk Engine

Working pipeline:

```text
Asset
 ↓
Vulnerability
 ↓
Threat
 ↓
Control
 ↓
Likelihood
 ↓
Impact
 ↓
EAL
```

This is the first major milestone.

---

# 55. August 28 — AI + API Integration

Connect:

```text
ML
 ↓
Risk Engine
 ↓
FastAPI
 ↓
PostgreSQL
 ↓
Frontend
```

At the end of the day:

> Dashboard should display actual calculated risk from the backend.

---

# 56. August 29 — Investment Optimization

Implement:

```text
Budget
 ↓
Possible Controls
 ↓
Optimization
 ↓
Recommended Portfolio
 ↓
Risk Reduction
 ↓
ROSI
```

This should become the core interactive demo.

---

# 57. August 30 — Ollama + Scenario Simulation

Implement:

```text
Natural language query
Scenario simulator
AI explanations
```

Example:

> "What happens if we enable MFA?"

---

# 58. August 31 — Compliance + Blockchain + Integration

Only after the core system works.

Implement:

```text
Framework mapping
Sepolia audit hash
```

Then freeze features.

---

# 59. September 1 — Testing + Presentation

No major new features.

Test:

```text
Dashboard
Risk calculation
Scenario
Optimization
LLM
Blockchain
Framework mapping
```

Prepare:

- PPT
- Demo
- Backup screenshots
- Backup video
- Offline fallback
- Judge Q&A

---

# 60. September 2 — Demo

## Recommended 6–8 Minute Demo

### 0:00–0:45

Problem.

> "Organizations know their vulnerabilities, but executives often cannot answer the financial question: how much could these risks cost us, and where should we spend the next rupee?"

### 0:45–1:30

Introduce CyberQuant.

```text
Technical telemetry
       ↓
AI Risk Quantification
       ↓
Financial Exposure
       ↓
Investment Optimization
```

### 1:30–2:30

Dashboard.

Show:

```text
Enterprise Risk
EAL
Top Risk
Risk Trend
```

### 2:30–3:30

Click the highest-risk asset.

Show:

```text
Technical findings
Business criticality
Control effectiveness
Financial impact
EAL
```

### 3:30–4:30

Scenario:

> "What happens if we enable MFA?"

Show:

```text
Before EAL
After EAL
Risk reduction
Cost
ROSI
```

### 4:30–5:30

Investment optimization.

Input:

```text
Budget = ₹1 Crore
```

Show:

```text
Recommended controls
Investment
Risk reduction
ROSI
```

### 5:30–6:15

Ask AI:

> "What is our highest financial cyber risk today?"

Show explanation.

### 6:15–6:45

Show:

```text
Framework mapping
```

### 6:45–7:15

Show:

```text
Blockchain audit
```

### 7:15–8:00

Close:

> "CyberQuant does not replace security teams. It translates technical exposure into financial intelligence and helps leadership decide where cybersecurity investment produces the greatest measurable reduction in risk."

---

# 61. What We Must NOT Build

With only about eight days, do not attempt:

- Full enterprise SIEM
- Full vulnerability scanner
- Full EDR
- Real bank integrations
- Real cloud security integrations
- Full compliance implementation
- Production-grade IAM
- Complex microservices
- Autonomous security agent
- Fully automated incident response
- Huge deep-learning model
- Mobile application
- Complex blockchain architecture
- Hundreds of compliance controls

We are building a **working decision-support prototype**, not replacing an enterprise GRC platform.

---

# 62. MVP Priority

## Tier 1 — Absolutely Required

```text
[ ] Asset inventory
[ ] Vulnerability data
[ ] Threat/control data
[ ] Risk quantification
[ ] Financial exposure
[ ] EAL
[ ] Executive dashboard
[ ] Risk drivers
[ ] Investment optimization
[ ] Scenario simulation
[ ] FastAPI
[ ] PostgreSQL
```

## Tier 2 — Strong Differentiators

```text
[ ] AI analyst
[ ] Natural-language queries
[ ] ROSI
[ ] Continuous risk simulation
[ ] Framework mapping
[ ] Risk reduction curve
```

## Tier 3 — Extra

```text
[ ] Sepolia audit
[ ] VaR
[ ] Advanced anomaly detection
[ ] Advanced attack graph
[ ] More frameworks
[ ] More sophisticated optimization
```

If Tier 1 is unstable, do not work on Tier 3.

---

# 63. Security and Privacy Principles

The system itself handles potentially sensitive security information.

Therefore:

- Minimize sensitive data.
- Use synthetic data for the demo.
- Do not expose credentials.
- Store API keys in `.env`.
- Never commit `.env`.
- Do not place sensitive telemetry on public blockchain.
- Use masked identifiers.
- Validate all API inputs.
- Apply authentication if time permits.
- Keep audit records immutable where appropriate.

---

# 64. Model Explainability

Every important number should have a traceable explanation.

For example:

```text
EAL = ₹62L

Why?

Probability = 0.20
Impact = ₹3.1 Cr

0.20 × ₹3.1 Cr
≈ ₹62L
```

Then:

```text
Probability increased because:
- Internet exposed
- Critical CVE
- Active threat
- Weak controls
```

This makes the model easier to defend to judges.

---

# 65. Important Assumptions

We must clearly separate:

### Observed data

What the system receives.

### Model estimate

What the ML/risk engine calculates.

### Business assumption

For example:

```text
Downtime cost/hour = ₹5L
```

### Scenario estimate

What happens under a hypothetical change.

Never present assumptions as real-world facts.

---

# 66. Metrics We Should Show

For ML:

- Precision
- Recall
- F1
- ROC-AUC where appropriate
- Calibration if feasible

For risk:

- Risk before/after remediation
- EAL before/after
- Risk reduction
- Prediction confidence

For investment:

- Cost
- Expected loss reduction
- ROSI
- Risk reduction per ₹ spent

For product:

```text
Top 10 risks identified
Top financial contributors
Potential risk reduction
Recommended investment
```

---

# 67. Judge Questions

## Q1. Why monetary risk?

Because "High Risk" does not tell management whether the issue represents ₹1 lakh or ₹10 crore of potential exposure.

---

## Q2. How do you calculate financial impact?

We combine business impact assumptions such as downtime, data-breach impact, recovery cost, regulatory exposure and other modeled costs.

---

## Q3. Where did your data come from?

For the prototype, we use synthetic enterprise telemetry because real enterprise security telemetry is confidential and not publicly available to the team.

---

## Q4. Is this actually continuous?

The architecture supports telemetry ingestion and recalculation. For the prototype, we simulate incoming telemetry to demonstrate how risk changes when new events occur.

---

## Q5. Why AI?

AI/ML helps estimate incident likelihood, detect patterns, predict risk trends and prioritize risk drivers. Deterministic calculations remain responsible for critical financial calculations where appropriate.

---

## Q6. Why LLM?

The LLM provides natural-language explanations and allows non-technical stakeholders to query structured risk information.

---

## Q7. Can the LLM manipulate the financial values?

The design should prevent this. Numerical values come from the risk engine/database, while the LLM receives structured data and explains it.

---

## Q8. Why blockchain?

Blockchain is used for tamper-evident auditing of risk assessments, recommendations and reports—not as the primary risk engine.

---

## Q9. Why optimize investments?

Security budgets are finite. The problem is not simply identifying risk; it is deciding which security investments produce the greatest risk reduction within the available budget.

---

## Q10. How does this help a CISO?

It provides:

```text
Risk
+
Financial Exposure
+
Top Drivers
+
Recommended Actions
+
Investment ROI
```

in one decision-support platform.

---

## Q11. Can it replace a CISO?

No.

It is decision support, not autonomous governance.

---

## Q12. Can it replace a SIEM/EDR/vulnerability scanner?

No.

It consumes their outputs and correlates them with business context.

---

# 68. Strong One-Line Pitch

> **CyberQuant continuously transforms technical cybersecurity telemetry into monetary risk and tells organizations exactly where to invest their security budget for maximum measurable risk reduction.**

---

# 69. Stronger 30-Second Pitch

> "Today, organizations know their vulnerabilities, alerts and compliance gaps, but executives still struggle to answer one question: how much financial cyber risk are we carrying, and where should we spend our next security rupee? CyberQuant continuously correlates technical security telemetry with asset criticality and control effectiveness, estimates financial exposure such as Expected Annual Loss, explains the major risk drivers, simulates remediation scenarios, and optimizes security investments under a fixed budget. This converts cybersecurity from a technical checklist into a measurable business investment decision."

---

# 70. Final Product Flow

```text
               ENTERPRISE
                   |
                   v
        +---------------------+
        | Security Telemetry  |
        +----------+----------+
                   |
                   v
        +---------------------+
        | Data Normalization  |
        +----------+----------+
                   |
                   v
        +---------------------+
        | Asset + Business    |
        | Context             |
        +----------+----------+
                   |
                   v
        +---------------------+
        | Risk Quantification |
        +----------+----------+
                   |
          +--------+--------+
          |                 |
          v                 v
      Probability        Impact
          |                 |
          +--------+--------+
                   |
                   v
             Financial Risk
                   |
                   v
                EAL / VaR
                   |
          +--------+--------+
          |                 |
          v                 v
    Risk Drivers       AI Analyst
          |                 |
          +--------+--------+
                   |
                   v
            Recommendations
                   |
                   v
          Scenario Simulation
                   |
                   v
          Investment Optimizer
                   |
                   v
             ROSI / ROI
                   |
                   v
          Executive Decision
                   |
                   v
            Audit / Governance
```

---

# 71. Team Discussion Checklist

Before coding, the six members must agree on:

- [ ] Exact interpretation of the PS
- [ ] Product name
- [ ] Demo organization
- [ ] Target users
- [ ] Assets we will simulate
- [ ] Security telemetry we will simulate
- [ ] Risk calculation formula
- [ ] Financial impact assumptions
- [ ] EAL calculation
- [ ] ML model
- [ ] Control effectiveness model
- [ ] Investment optimization algorithm
- [ ] ROSI formula
- [ ] Scenario engine
- [ ] LLM role
- [ ] Framework mapping scope
- [ ] Blockchain role
- [ ] Database schema
- [ ] API schema
- [ ] Dashboard design
- [ ] Team ownership
- [ ] GitHub workflow
- [ ] August 27 milestone
- [ ] August 29 milestone
- [ ] August 31 feature freeze
- [ ] September 2 demo

---

# 72. Questions the Team Should Debate

These are intentionally open questions. Do not blindly accept the proposed design.

## Risk

1. What exactly should our Enterprise Risk Score represent?
2. Should it be 0–100, monetary-only, or both?
3. How should likelihood be calculated?
4. How should control effectiveness affect likelihood?
5. How should asset criticality affect impact?

## Financial

6. What costs should be included in financial impact?
7. How will we justify our assumptions?
8. Should we show EAL only or also VaR?
9. How should we model uncertainty?

## AI

10. Which part actually requires ML?
11. Which part should remain deterministic?
12. How do we prevent hallucinated recommendations?
13. How do we explain model outputs?

## Investment

14. What controls will we allow the optimizer to choose?
15. What is our budget?
16. How do we model cost?
17. How do we model risk reduction?
18. How do we handle dependencies between controls?

## Continuous Monitoring

19. What changes when new telemetry arrives?
20. How quickly should risk be recalculated?
21. How will we simulate this on one laptop?

## Compliance

22. How many controls from each framework will we demonstrate?
23. How will we validate our mappings?

## Blockchain

24. What exactly should be hashed?
25. What business problem does blockchain solve?
26. What must never go on-chain?

## Demo

27. What is the one feature judges must remember?
28. What happens if Ollama fails?
29. What happens if Sepolia is unavailable?
30. What happens if the ML model produces an unexpected result?

---

# 73. Definition of Done — September 2

The project is ready when the following works on a single laptop:

```text
START APPLICATION
        |
        v
EXECUTIVE DASHBOARD
        |
        v
CURRENT ENTERPRISE RISK
        |
        v
TOP FINANCIAL RISK
        |
        v
DRILL DOWN INTO ASSET
        |
        v
SEE TECHNICAL + BUSINESS DRIVERS
        |
        v
SEE EXPECTED ANNUAL LOSS
        |
        v
RUN WHAT-IF SCENARIO
        |
        v
SEE RISK REDUCTION
        |
        v
ENTER SECURITY BUDGET
        |
        v
OPTIMIZE INVESTMENT
        |
        v
SEE ROSI
        |
        v
ASK AI ANALYST
        |
        v
SHOW FRAMEWORK MAPPING
        |
        v
OPTIONALLY RECORD AUDIT ON SEPOLIA
```

If this flow is stable, the prototype is ready.

---

# 74. Most Important Rule for the Team

## Do not build a cybersecurity dashboard.

Build a:

# **Cyber Risk Decision Engine**

The dashboard is only the interface.

The real product is:

```text
Technical Data
      ↓
Quantified Financial Risk
      ↓
Risk Drivers
      ↓
What-If Scenarios
      ↓
Investment Optimization
      ↓
Business Decision
```

That is the story we should take to the judges.
