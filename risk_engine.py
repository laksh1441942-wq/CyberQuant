"""
================================================================================
CYBERQUANT — DAY 2 TASK: RISK QUANTIFICATION ENGINE (risk_engine.py)
================================================================================
Author: Backend Team
Purpose: Calculates Incident Likelihood, Financial Impact, and Expected Annual Loss (EAL)
         based on the globally recognized FAIR (Factor Analysis of Information Risk)
         framework for each asset and across the entire enterprise.

Core Formulas:
  1. Incident Likelihood (P): Probability (0.02 to 0.95) of an exploit this year
  2. Financial Impact (I): Monetary loss (Downtime + Recovery + Data Breach in INR)
  3. Expected Annual Loss (EAL) = Likelihood (P) × Financial Impact (I)
  4. Enterprise Risk Score = Normalized scale (0 to 100)
  5. What-If Scenario Simulations & Return on Security Investment (ROSI)
================================================================================
"""

import os
import sys
import json

# Ensure UTF-8 stdout on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Dynamic base directory resolution
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data", "generated")


def load_data():
    """Loads synthetic assets and vulnerabilities from Day 1."""
    assets_file = os.path.join(DATA_DIR, "assets.json")
    vulns_file = os.path.join(DATA_DIR, "vulnerabilities.json")
    
    if not os.path.exists(assets_file) or not os.path.exists(vulns_file):
        raise FileNotFoundError(
            f"Missing dataset files in {DATA_DIR}. Please run generate_data.py first!"
        )
        
    with open(assets_file, "r", encoding="utf-8") as f:
        assets = json.load(f)
    with open(vulns_file, "r", encoding="utf-8") as f:
        vulns = json.load(f)
        
    return assets, vulns


def calculate_asset_likelihood(asset, asset_vulns, mfa_override=None, edr_override=None):
    """
    Calculates the probability (0.02 to 0.95) that this asset will suffer a breach.
    Factors:
      + Max CVSS score among vulnerabilities on this asset (scale 0.0 to 0.45)
      + Internet exposure (+0.30 if exposed)
      - MFA Protection (-0.35 if enabled)
      - EDR Protection (-0.25 if installed)
    """
    if not asset_vulns:
        max_cvss = 2.0
    else:
        max_cvss = max(v["cvss_score"] for v in asset_vulns)
        
    # Base likelihood from vulnerability score (scale 0.0 to 0.45)
    base_likelihood = (max_cvss / 10.0) * 0.45
    
    # Internet exposure multiplier
    if asset["is_internet_exposed"]:
        base_likelihood += 0.30
        
    # Check security controls (allow overrides for What-If scenario simulations)
    has_mfa = mfa_override if mfa_override is not None else asset.get("mfa_enabled", False)
    has_edr = edr_override if edr_override is not None else asset.get("edr_installed", False)
    
    control_defense = 0.0
    if has_mfa:
        control_defense += 0.35
    if has_edr:
        control_defense += 0.25
        
    final_likelihood = base_likelihood - control_defense
    # Clamp between 2% (0.02) and 95% (0.95)
    return round(max(0.02, min(0.95, final_likelihood)), 3)


def calculate_asset_impact(asset):
    """
    Calculates the financial damage in Rupees (INR) if the asset is compromised.
    Impact = Direct Asset Value + (Downtime Cost/hr × Estimated Downtime Hours) + Incident Recovery
    """
    base_val = asset["asset_value_inr"]
    downtime_rate = asset.get("downtime_cost_per_hour_inr", 20000)
    
    # Critical and High tier assets take ~12 hours to recover; lower assets take ~4 hours
    downtime_hours = 12 if asset["business_criticality"] in ["Critical", "High"] else 4
    downtime_loss = downtime_rate * downtime_hours
    
    # Forensic analysis and recovery costs
    recovery_cost = 500000 if asset["business_criticality"] == "Critical" else 100000
    
    total_impact = base_val + downtime_loss + recovery_cost
    return total_impact


def quantify_all_risks(mfa_override=None, edr_override=None):
    """
    Calculates EAL across all 150 assets in the enterprise.
    Returns:
      - Full list of evaluated assets with their individual EAL
      - Total Enterprise EAL (INR)
      - Total Potential Exposure (INR)
      - Enterprise Risk Score (0 to 100)
      - Top 5 Highest Risk Contributor Assets
    """
    assets, vulns = load_data()
    
    # Group vulnerabilities by asset_id
    vuln_map = {}
    for v in vulns:
        aid = v["asset_id"]
        if aid not in vuln_map:
            vuln_map[aid] = []
        vuln_map[aid].append(v)
        
    evaluated_assets = []
    total_enterprise_eal = 0.0
    total_potential_loss = 0.0
    
    for a in assets:
        aid = a["asset_id"]
        a_vulns = vuln_map.get(aid, [])
        
        likelihood = calculate_asset_likelihood(a, a_vulns, mfa_override, edr_override)
        financial_impact = calculate_asset_impact(a)
        
        # FAIR Formula: EAL = Likelihood (P) × Financial Impact (I)
        asset_eal = likelihood * financial_impact
        
        total_enterprise_eal += asset_eal
        total_potential_loss += financial_impact
        
        evaluated_assets.append({
            "asset_id": aid,
            "asset_name": a["asset_name"],
            "asset_type": a["asset_type"],
            "department": a["department"],
            "criticality": a["business_criticality"],
            "asset_value_inr": a["asset_value_inr"],
            "is_internet_exposed": a["is_internet_exposed"],
            "mfa_enabled": a["mfa_enabled"] if mfa_override is None else mfa_override,
            "edr_installed": a["edr_installed"] if edr_override is None else edr_override,
            "vulnerability_count": len(a_vulns),
            "max_cvss": max((v["cvss_score"] for v in a_vulns), default=0.0),
            "likelihood_pct": round(likelihood * 100, 1),
            "financial_impact_inr": round(financial_impact, 2),
            "expected_annual_loss_inr": round(asset_eal, 2)
        })
        
    # Sort assets by highest Expected Annual Loss (EAL) descending
    evaluated_assets.sort(key=lambda x: x["expected_annual_loss_inr"], reverse=True)
    
    # Calculate 0-100 Enterprise Risk Score
    avg_likelihood = sum(a["likelihood_pct"] for a in evaluated_assets) / len(evaluated_assets)
    enterprise_score = min(98, max(15, round(avg_likelihood * 2.2)))
    
    return {
        "enterprise_risk_score": enterprise_score,
        "total_expected_annual_loss_inr": round(total_enterprise_eal, 2),
        "total_potential_exposure_inr": round(total_potential_loss, 2),
        "total_assets_evaluated": len(evaluated_assets),
        "top_5_risk_contributors": evaluated_assets[:5],
        "all_assets": evaluated_assets
    }


def calculate_scenario(action_name):
    """
    Simulates 'What-If' remediation scenarios:
      - 'enable_mfa_all': Enables MFA across 100% of accounts
      - 'enable_edr_all': Deploys EDR across 100% of endpoints
      - 'enable_both': Deploys both MFA and EDR enterprise-wide
    """
    baseline = quantify_all_risks()
    base_eal = baseline["total_expected_annual_loss_inr"]
    
    if action_name == "enable_mfa_all":
        scenario = quantify_all_risks(mfa_override=True)
        cost = 2000000  # ₹20 Lakhs
        desc = "Deploy Hardware Token MFA across 100% of enterprise accounts"
    elif action_name == "enable_edr_all":
        scenario = quantify_all_risks(edr_override=True)
        cost = 3000000  # ₹30 Lakhs
        desc = "Deploy behavioral EDR agent across all endpoints"
    elif action_name == "enable_both":
        scenario = quantify_all_risks(mfa_override=True, edr_override=True)
        cost = 5000000  # ₹50 Lakhs
        desc = "Deploy both MFA and EDR across all assets"
    else:
        return {"error": f"Unknown scenario action: {action_name}"}
        
    new_eal = scenario["total_expected_annual_loss_inr"]
    risk_reduction = max(0.0, base_eal - new_eal)
    rosi = ((risk_reduction - cost) / cost) if cost > 0 else 0.0
    
    return {
        "scenario_action": action_name,
        "description": desc,
        "baseline_eal_inr": base_eal,
        "scenario_eal_inr": new_eal,
        "risk_reduction_inr": round(risk_reduction, 2),
        "implementation_cost_inr": cost,
        "rosi_percentage": round(rosi * 100, 1),
        "new_enterprise_risk_score": scenario["enterprise_risk_score"]
    }


if __name__ == "__main__":
    print("[DAY 2] Testing CyberQuant FAIR Risk Quantification Engine...\n")
    
    # 1. Run baseline quantification
    result = quantify_all_risks()
    
    print("=" * 70)
    print("📊 ENTERPRISE CYBER RISK QUANTIFICATION (FAIR FRAMEWORK)")
    print("=" * 70)
    print(f"Enterprise Risk Score:       {result['enterprise_risk_score']} / 100")
    print(f"Total Expected Annual Loss:  INR {result['total_expected_annual_loss_inr'] / 10000000:.2f} Crores (₹{result['total_expected_annual_loss_inr']:,.0f})")
    print(f"Total Maximum Exposure:      INR {result['total_potential_exposure_inr'] / 10000000:.2f} Crores (₹{result['total_potential_exposure_inr']:,.0f})")
    print(f"Total Monitored Assets:      {result['total_assets_evaluated']}")
    
    print("\n🔥 TOP 3 HIGHEST FINANCIAL RISK ASSETS:")
    for idx, top in enumerate(result["top_5_risk_contributors"][:3], 1):
        print(f"  {idx}. {top['asset_name']} [{top['criticality']} Tier]")
        print(f"     • Valuation: ₹{top['asset_value_inr']:,.0f} | Exploit Likelihood: {top['likelihood_pct']}%")
        print(f"     • Expected Annual Loss (EAL): INR {top['expected_annual_loss_inr'] / 100000:.2f} Lakhs (₹{top['expected_annual_loss_inr']:,.0f})")
        print(f"     • Internet Exposed: {'YES' if top['is_internet_exposed'] else 'NO'} | Max CVSS: {top['max_cvss']}")
    
    print("\n" + "=" * 70)
    print("🧪 WHAT-IF SCENARIO: 'Deploy Hardware MFA across 100% Accounts'")
    print("=" * 70)
    mfa_scenario = calculate_scenario("enable_mfa_all")
    print(f"Baseline EAL:       INR {mfa_scenario['baseline_eal_inr'] / 10000000:.2f} Crores")
    print(f"New EAL with MFA:   INR {mfa_scenario['scenario_eal_inr'] / 10000000:.2f} Crores")
    print(f"Risk Reduction:     INR {mfa_scenario['risk_reduction_inr'] / 100000:.2f} Lakhs saved!")
    print(f"Deployment Cost:    INR {mfa_scenario['implementation_cost_inr'] / 100000:.2f} Lakhs")
    print(f"Return on Invest:   {mfa_scenario['rosi_percentage']}% ROSI")
    print(f"New Risk Score:     {mfa_scenario['new_enterprise_risk_score']} / 100")
    print("=" * 70)
    print("\n[SUCCESS] Day 2 Risk Engine is fully functional!")
