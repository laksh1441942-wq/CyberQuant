from pathlib import Path

from sqlalchemy.orm import Session

from backend.app.config import PROJECT_ROOT
from backend.app.models.asset import Asset
from backend.app.models.vulnerability import Vulnerability
from ml.risk_model import RiskModel, load_enterprise_dataset


def _get_ml_model() -> RiskModel:
    dataset = load_enterprise_dataset(Path(PROJECT_ROOT) / "data" / "generated")
    return RiskModel().train(dataset)


def calculate_asset_likelihood(asset: Asset, vulns: list, mfa_override=None, edr_override=None) -> float:
    """Calculates breach likelihood (0.02 to 0.95)."""
    max_cvss = max((v.cvss_score for v in vulns), default=2.0)
    base_likelihood = (max_cvss / 10.0) * 0.45

    if asset.is_internet_exposed:
        base_likelihood += 0.30

    has_mfa = mfa_override if mfa_override is not None else asset.mfa_enabled
    has_edr = edr_override if edr_override is not None else asset.edr_installed

    defense = (0.35 if has_mfa else 0.0) + (0.25 if has_edr else 0.0)
    return round(max(0.02, min(0.95, base_likelihood - defense)), 3)


def calculate_asset_impact(asset: Asset) -> float:
    """
    Calculates potential monetary impact in INR specifically calibrated for the
    given Fintech Enterprise / Banking Organization (Section 8, 9, 14 of SIH 2026 Spec).
    Impact = Direct Asset Valuation + Downtime Cost + Incident Recovery + Regulatory Exposure (RBI / SEBI).
    """
    downtime_hours = 12 if asset.business_criticality in ["Critical", "High"] else 4
    downtime_loss = asset.downtime_cost_per_hour_inr * downtime_hours
    recovery_cost = 500000.0 if asset.business_criticality == "Critical" else 100000.0
    # Regulatory penalty & audit risk under RBI Cyber Security Framework for critical banking nodes
    regulatory_cost = 2500000.0 if asset.business_criticality == "Critical" and asset.is_internet_exposed else 0.0
    return asset.asset_value_inr + downtime_loss + recovery_cost + regulatory_cost


def evaluate_all_risks(db: Session, mfa_override=None, edr_override=None):
    """Evaluates EAL across all assets using the explainable ML risk model."""
    assets = db.query(Asset).all()
    vulns = db.query(Vulnerability).all()

    model = _get_ml_model()
    ml_predictions = {}
    for asset in assets:
        asset_dict = {
            "asset_id": asset.asset_id,
            "asset_name": asset.asset_name,
            "asset_type": asset.asset_type,
            "department": asset.department,
            "business_criticality": asset.business_criticality,
            "asset_value_inr": asset.asset_value_inr,
            "downtime_cost_per_hour_inr": asset.downtime_cost_per_hour_inr,
            "is_internet_exposed": asset.is_internet_exposed,
            "mfa_enabled": mfa_override if mfa_override is not None else asset.mfa_enabled,
            "edr_installed": edr_override if edr_override is not None else asset.edr_installed,
        }
        prediction = model.predict_asset_risk(
            asset_dict,
            [
                {
                    "asset_id": v.asset_id,
                    "cvss_score": v.cvss_score,
                    "severity": v.severity,
                    "days_unpatched": 30,
                }
                for v in vulns
                if v.asset_id == asset.asset_id
            ],
            [
                {"target": "Database", "annual_base_likelihood": 0.28, "name": "Ransomware Data Extortion"},
                {"target": "API Server", "annual_base_likelihood": 0.35, "name": "API Abuse & BOLA Exploit"},
                {"target": "IAM Server", "annual_base_likelihood": 0.15, "name": "Insider Privilege Escalation"},
                {"target": "Web Portal", "annual_base_likelihood": 0.42, "name": "Credential Stuffing"},
                {"target": "Application", "annual_base_likelihood": 0.22, "name": "Supply Chain Poisoning"},
            ],
        )
        ml_predictions[asset.asset_id] = prediction

    evaluated = []
    total_eal = 0.0
    total_exposure = 0.0

    for a in assets:
        prediction = ml_predictions.get(a.asset_id, {})
        likelihood = float(prediction.get("risk_probability", calculate_asset_likelihood(a, [], mfa_override, edr_override)))
        impact = float(prediction.get("financial_impact_inr", calculate_asset_impact(a)))
        eal = float(prediction.get("expected_annual_loss_inr", likelihood * impact))

        total_eal += eal
        total_exposure += impact

        evaluated.append({
            "asset_id": a.asset_id,
            "asset_name": a.asset_name,
            "asset_type": a.asset_type,
            "department": a.department,
            "criticality": a.business_criticality,
            "asset_value_inr": a.asset_value_inr,
            "is_internet_exposed": a.is_internet_exposed,
            "mfa_enabled": mfa_override if mfa_override is not None else a.mfa_enabled,
            "edr_installed": edr_override if edr_override is not None else a.edr_installed,
            "vulnerability_count": sum(1 for v in vulns if v.asset_id == a.asset_id),
            "max_cvss": max((v.cvss_score for v in vulns if v.asset_id == a.asset_id), default=0.0),
            "likelihood_pct": round(likelihood * 100, 1),
            "financial_impact_inr": round(impact, 2),
            "expected_annual_loss_inr": round(eal, 2),
            "top_drivers": prediction.get("top_drivers", []),
        })

    evaluated.sort(key=lambda x: x["expected_annual_loss_inr"], reverse=True)
    avg_l = sum(a["likelihood_pct"] for a in evaluated) / len(evaluated) if evaluated else 20.0
    score = min(98, max(15, round(avg_l * 2.2)))

    return {
        "enterprise_risk_score": score,
        "total_expected_annual_loss_inr": round(total_eal, 2),
        "total_potential_exposure_inr": round(total_exposure, 2),
        "total_assets_evaluated": len(evaluated),
        "top_5_risk_contributors": evaluated[:5],
        "all_assets": evaluated
    }
