"""
================================================================================
CYBERQUANT — DAY 1 TASK: SYNTHETIC ENTERPRISE DATA GENERATOR
================================================================================
Author: Backend Team
Purpose: Generates a realistic synthetic enterprise dataset for a medium-sized
         Fintech / Banking organization with 150 assets, vulnerabilities,
         security controls, and threat scenarios.

Outputs (saved in data/generated/):
  1. assets.json          - 150 servers, databases, cloud APIs, laptops
  2. vulnerabilities.json - 120+ CVE vulnerabilities mapped to assets
  3. controls.json        - 8 enterprise security controls with costs & efficacy
  4. threats.json         - Active threat intelligence feeds
  5. summary.json         - High-level overview of the generated company
================================================================================
"""

import os
import sys
import json
import random
from datetime import datetime

# Configure UTF-8 stdout if supported
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Set random seed so numbers are consistent
random.seed(42)

# Determine workspace directory
WORKSPACE_DIR = r"c:\Users\win 10\OneDrive\Desktop\SIH PROJECT"
OUTPUT_DIR = os.path.join(WORKSPACE_DIR, "data", "generated")
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("[DAY 1] Starting CyberQuant Synthetic Data Generator...")

# ==============================================================================
# 1. GENERATE ASSETS (150 Servers, Databases, APIs, Endpoints)
# ==============================================================================

ASSET_TEMPLATES = [
    # Critical Tier (High Financial Value)
    {"name": "Core Banking Database", "type": "Database", "dept": "Core Banking", "crit": "Critical", "val_range": (40000000, 60000000), "downtime_hr": 800000, "internet": False},
    {"name": "Customer KYC & PII Store", "type": "Database", "dept": "Compliance", "crit": "Critical", "val_range": (35000000, 50000000), "downtime_hr": 500000, "internet": False},
    {"name": "Payment Gateway API", "type": "API Server", "dept": "Payments", "crit": "Critical", "val_range": (25000000, 40000000), "downtime_hr": 600000, "internet": True},
    {"name": "Identity & IAM Controller", "type": "IAM Server", "dept": "IT Security", "crit": "Critical", "val_range": (20000000, 35000000), "downtime_hr": 450000, "internet": True},
    {"name": "SWIFT / UPI Settlement Node", "type": "Financial Node", "dept": "Treasury", "crit": "Critical", "val_range": (30000000, 45000000), "downtime_hr": 750000, "internet": False},
    
    # High Tier
    {"name": "Mobile Banking Backend", "type": "Application", "dept": "Digital Banking", "crit": "High", "val_range": (15000000, 25000000), "downtime_hr": 300000, "internet": True},
    {"name": "Admin Management Portal", "type": "Web Portal", "dept": "Operations", "crit": "High", "val_range": (10000000, 18000000), "downtime_hr": 200000, "internet": True},
    {"name": "Trading & Investment Engine", "type": "Trading Engine", "dept": "Wealth", "crit": "High", "val_range": (18000000, 28000000), "downtime_hr": 400000, "internet": False},
    {"name": "Credit Scoring Microservice", "type": "Microservice", "dept": "Lending", "crit": "High", "val_range": (8000000, 15000000), "downtime_hr": 150000, "internet": False},
    {"name": "Cloud Storage Bucket (Statements)", "type": "Cloud Storage", "dept": "Customer Ops", "crit": "High", "val_range": (10000000, 20000000), "downtime_hr": 100000, "internet": True},
    
    # Medium Tier
    {"name": "Internal HR & Payroll System", "type": "Web Portal", "dept": "Human Resources", "crit": "Medium", "val_range": (3000000, 6000000), "downtime_hr": 50000, "internet": False},
    {"name": "Customer Support Ticketing", "type": "SaaS / App", "dept": "Support", "crit": "Medium", "val_range": (2000000, 4500000), "downtime_hr": 40000, "internet": True},
    {"name": "Internal Analytics Warehouse", "type": "Data Warehouse", "dept": "BI & Analytics", "crit": "Medium", "val_range": (4000000, 8000000), "downtime_hr": 60000, "internet": False},
    {"name": "Marketing Automation Engine", "type": "Web App", "dept": "Marketing", "crit": "Medium", "val_range": (1500000, 3500000), "downtime_hr": 30000, "internet": True},
    {"name": "Corporate Email Server (Exchange)", "type": "Email Server", "dept": "IT Operations", "crit": "Medium", "val_range": (5000000, 9000000), "downtime_hr": 80000, "internet": True},
]

assets = []
asset_id_counter = 101

# 1. Create named anchor assets
for tmpl in ASSET_TEMPLATES:
    val = round(random.randint(tmpl["val_range"][0], tmpl["val_range"][1]), -4)
    assets.append({
        "asset_id": f"AST-{asset_id_counter}",
        "asset_name": tmpl["name"],
        "asset_type": tmpl["type"],
        "department": tmpl["dept"],
        "business_criticality": tmpl["crit"],
        "asset_value_inr": val,
        "downtime_cost_per_hour_inr": tmpl["downtime_hr"],
        "is_internet_exposed": tmpl["internet"],
        "mfa_enabled": random.choice([True, False]) if tmpl["crit"] != "Critical" else random.choice([True, True, False]),
        "edr_installed": random.choice([True, True, False]),
        "owner": f"Lead_{tmpl['dept'].replace(' ', '_')}"
    })
    asset_id_counter += 1

# 2. Fill remaining up to 150 assets (Employee Laptops, Branch Routers, Testing Servers)
for i in range(len(assets), 150):
    tier = random.choices(["Medium", "Low"], weights=[0.25, 0.75])[0]
    if tier == "Medium":
        name = f"Branch Office Gateway #{i-15}"
        a_type = "Network Router"
        dept = "Branch Ops"
        val = random.randint(1000000, 3000000)
        downtime = 25000
        exposed = True
    else:
        name = f"Developer / Staff Workstation #{i-30}"
        a_type = "Endpoint Workstation"
        dept = random.choice(["Engineering", "Finance", "Legal", "Sales"])
        val = random.randint(150000, 450000)
        downtime = 5000
        exposed = False

    assets.append({
        "asset_id": f"AST-{asset_id_counter}",
        "asset_name": name,
        "asset_type": a_type,
        "department": dept,
        "business_criticality": tier,
        "asset_value_inr": round(val, -3),
        "downtime_cost_per_hour_inr": downtime,
        "is_internet_exposed": exposed,
        "mfa_enabled": random.choice([True, False, False]),
        "edr_installed": random.choice([True, False]),
        "owner": f"User_{dept.lower()}_{i}"
    })
    asset_id_counter += 1

print(f"[OK] Generated {len(assets)} enterprise assets.")

# ==============================================================================
# 2. GENERATE VULNERABILITIES (CVEs)
# ==============================================================================

CVE_SAMPLES = [
    {"cve": "CVE-2024-3094", "name": "XZ Utils Backdoor RCE", "cvss": 10.0, "severity": "Critical", "patch_cost": 80000},
    {"cve": "CVE-2024-21413", "name": "Microsoft Outlook RCE MonikerLink", "cvss": 9.8, "severity": "Critical", "patch_cost": 50000},
    {"cve": "CVE-2023-44487", "name": "HTTP/2 Rapid Reset DDoS", "cvss": 7.5, "severity": "High", "patch_cost": 40000},
    {"cve": "CVE-2023-38606", "name": "Kernel Memory Corruption Flaw", "cvss": 8.8, "severity": "High", "patch_cost": 65000},
    {"cve": "CVE-2024-21762", "name": "FortiOS SSL-VPN Out-of-Bounds Write", "cvss": 9.6, "severity": "Critical", "patch_cost": 90000},
    {"cve": "CVE-2023-22515", "name": "Confluence Broken Access Control", "cvss": 9.8, "severity": "Critical", "patch_cost": 45000},
    {"cve": "CVE-2024-3400", "name": "PAN-OS Command Injection", "cvss": 10.0, "severity": "Critical", "patch_cost": 100000},
    {"cve": "CVE-2023-48795", "name": "SSH Terrapin Prefix Truncation", "cvss": 5.9, "severity": "Medium", "patch_cost": 25000},
    {"cve": "CVE-2024-23897", "name": "Jenkins CLI Arbitrary File Read", "cvss": 9.8, "severity": "Critical", "patch_cost": 35000},
    {"cve": "CVE-2023-46604", "name": "Apache ActiveMQ RCE", "cvss": 9.8, "severity": "Critical", "patch_cost": 60000},
    {"cve": "CVE-2024-0012", "name": "PAN-OS Management Interface Auth Bypass", "cvss": 9.3, "severity": "Critical", "patch_cost": 75000},
    {"cve": "CVE-2023-34362", "name": "MOVEit Transfer SQL Injection", "cvss": 9.8, "severity": "Critical", "patch_cost": 85000},
]

vulnerabilities = []
vuln_id = 1001

for asset in assets:
    if asset["business_criticality"] in ["Critical", "High"]:
        num_vulns = random.randint(1, 3)
    else:
        num_vulns = random.choices([0, 1], weights=[0.6, 0.4])[0]
        
    for _ in range(num_vulns):
        sample = random.choice(CVE_SAMPLES)
        cvss = min(10.0, max(4.0, round(sample["cvss"] + random.uniform(-0.4, 0.2), 1)))
        
        vulnerabilities.append({
            "vuln_id": f"VUL-{vuln_id}",
            "asset_id": asset["asset_id"],
            "asset_name": asset["asset_name"],
            "cve_id": sample["cve"],
            "vulnerability_name": sample["name"],
            "cvss_score": cvss,
            "severity": "Critical" if cvss >= 9.0 else ("High" if cvss >= 7.0 else "Medium"),
            "is_exploit_public": random.choice([True, True, False]),
            "patch_available": True,
            "patch_cost_inr": sample["patch_cost"],
            "days_unpatched": random.randint(5, 120),
            "status": "OPEN"
        })
        vuln_id += 1

print(f"[OK] Generated {len(vulnerabilities)} vulnerabilities mapped across assets.")

# ==============================================================================
# 3. GENERATE SECURITY CONTROLS
# ==============================================================================

controls = [
    {
        "control_id": "CTRL-01",
        "name": "Critical Patch Program",
        "category": "Vulnerability Management",
        "description": "Rapid automated patch deployment for all CVSS >= 8.5 vulnerabilities within 48 hours.",
        "cost_inr": 1000000,          # ₹10 Lakhs
        "expected_risk_reduction_inr": 2500000, # ₹25 Lakhs saved
        "annual_maintenance_inr": 200000,
        "implementation_days": 14,
        "framework_mapping": ["NIST CSF: PR.IP-12", "CIS Control 7", "RBI Sec 4.2", "ISO 27001 A.12.6.1"]
    },
    {
        "control_id": "CTRL-02",
        "name": "Hardware Token MFA Expansion",
        "category": "Identity & Access Management",
        "description": "Mandatory FIDO2 hardware security keys for 100% of privileged and admin accounts.",
        "cost_inr": 2000000,          # ₹20 Lakhs
        "expected_risk_reduction_inr": 3500000, # ₹35 Lakhs saved
        "annual_maintenance_inr": 300000,
        "implementation_days": 21,
        "framework_mapping": ["NIST CSF: PR.AC-7", "CIS Control 6", "RBI Sec 3.1", "SEBI CSCRF 2.4"]
    },
    {
        "control_id": "CTRL-03",
        "name": "Zero-Trust Network Segmentation",
        "category": "Network Security",
        "description": "Isolating Core Banking & Payment DBs into private micro-segments with WAF inspection.",
        "cost_inr": 4000000,          # ₹40 Lakhs
        "expected_risk_reduction_inr": 6000000, # ₹60 Lakhs saved
        "annual_maintenance_inr": 500000,
        "implementation_days": 45,
        "framework_mapping": ["NIST CSF: PR.AC-5", "CIS Control 12", "RBI Sec 5.3", "ISO 27001 A.13.1.3"]
    },
    {
        "control_id": "CTRL-04",
        "name": "EDR Enterprise Expansion",
        "category": "Endpoint Detection & Response",
        "description": "Deploying behavioral AI endpoint detection and automated quarantine on all 150 assets.",
        "cost_inr": 3000000,          # ₹30 Lakhs
        "expected_risk_reduction_inr": 4200000, # ₹42 Lakhs saved
        "annual_maintenance_inr": 450000,
        "implementation_days": 30,
        "framework_mapping": ["NIST CSF: DE.CM-4", "CIS Control 10", "SEBI CSCRF 3.2", "ISO 27001 A.12.2.1"]
    },
    {
        "control_id": "CTRL-05",
        "name": "Cloud WAF & DDoS Shield",
        "category": "Cloud Protection",
        "description": "Deploying Layer 7 rate-limiting and anti-bot protection on all internet-facing APIs.",
        "cost_inr": 1500000,          # ₹15 Lakhs
        "expected_risk_reduction_inr": 1800000, # ₹18 Lakhs saved
        "annual_maintenance_inr": 250000,
        "implementation_days": 10,
        "framework_mapping": ["NIST CSF: PR.PT-4", "CIS Control 13", "RBI Sec 6.1"]
    },
    {
        "control_id": "CTRL-06",
        "name": "Immutable Backup Vault",
        "category": "Disaster Recovery",
        "description": "Air-gapped, write-once-read-many (WORM) storage for instant ransomware recovery.",
        "cost_inr": 2500000,          # ₹25 Lakhs
        "expected_risk_reduction_inr": 3200000, # ₹32 Lakhs saved
        "annual_maintenance_inr": 300000,
        "implementation_days": 20,
        "framework_mapping": ["NIST CSF: RC.RP-1", "CIS Control 11", "RBI Sec 8.4", "ISO 27001 A.12.3.1"]
    }
]

print(f"[OK] Generated {len(controls)} security control options with framework mappings.")

# ==============================================================================
# 4. GENERATE THREAT INTELLIGENCE SCENARIOS
# ==============================================================================

threats = [
    {"threat_id": "THR-01", "name": "Ransomware Data Extortion", "target": "Database", "annual_base_likelihood": 0.28, "typical_impact": "High"},
    {"threat_id": "THR-02", "name": "Credential Stuffing & Account Takeover", "target": "Web Portal", "annual_base_likelihood": 0.42, "typical_impact": "Medium"},
    {"threat_id": "THR-03", "name": "API Abuse & BOLA Exploit", "target": "API Server", "annual_base_likelihood": 0.35, "typical_impact": "High"},
    {"threat_id": "THR-04", "name": "Insider Privilege Escalation", "target": "IAM Server", "annual_base_likelihood": 0.15, "typical_impact": "Critical"},
    {"threat_id": "THR-05", "name": "Supply-Chain Dependency Poisoning", "target": "Application", "annual_base_likelihood": 0.22, "typical_impact": "High"},
]

# ==============================================================================
# 5. SUMMARY STATS
# ==============================================================================

total_asset_value = sum(a["asset_value_inr"] for a in assets)
total_vulns = len(vulnerabilities)
critical_vulns = len([v for v in vulnerabilities if v["severity"] == "Critical"])

summary = {
    "generated_at": datetime.now().isoformat(),
    "organization_profile": "Mid-Tier Fintech & Digital Lending Institution",
    "total_monitored_assets": len(assets),
    "total_asset_valuation_inr": total_asset_value,
    "total_vulnerabilities": total_vulns,
    "critical_vulnerabilities": critical_vulns,
    "security_controls_available": len(controls),
    "active_threat_vectors": len(threats)
}

# ==============================================================================
# 6. WRITE ALL FILES TO DISK
# ==============================================================================

files_to_write = {
    "assets.json": assets,
    "vulnerabilities.json": vulnerabilities,
    "controls.json": controls,
    "threats.json": threats,
    "summary.json": summary
}

for filename, data in files_to_write.items():
    file_path = os.path.join(OUTPUT_DIR, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"[SAVED] {file_path}")

# Also copy the generator code to project folder as generate_data.py
project_script_path = os.path.join(WORKSPACE_DIR, "generate_data.py")
with open(__file__, "r", encoding="utf-8") as src, open(project_script_path, "w", encoding="utf-8") as dst:
    dst.write(src.read())
print(f"[SAVED] Project Script: {project_script_path}")

print("\n" + "="*70)
print(f"DAY 1 TASK COMPLETE!")
print(f"Total Assets Created:         {len(assets)} (Valuation: INR {total_asset_value / 10000000:.2f} Crores)")
print(f"Total Vulnerabilities Mapped: {total_vulns} ({critical_vulns} Critical)")
print(f"Security Controls Defined:    {len(controls)}")
print(f"Output Folder:               data/generated/")
print("="*70)
