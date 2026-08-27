"""Prototype risk quantification model for the synthetic CyberQuant data."""

from typing import Any


CRITICALITY_FACTOR = {
    "Critical": 1.0,
    "High": 0.8,
    "Medium": 0.5,
    "Low": 0.25,
}


def _clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    return max(minimum, min(value, maximum))


def calculate_likelihood(
    asset: dict[str, Any], vulnerability: dict[str, Any], threat_likelihood: float
) -> float:
    """Estimate annual incident probability for one asset vulnerability pair."""
    cvss_factor = vulnerability["cvss_score"] / 10
    exposure_factor = 1.25 if asset["is_internet_exposed"] else 0.75
    exploit_factor = 1.2 if vulnerability["is_exploit_public"] else 0.9
    age_factor = min(1.25, 1 + vulnerability["days_unpatched"] / 365)
    control_effectiveness = 0.35
    control_effectiveness += 0.2 if asset["mfa_enabled"] else 0
    control_effectiveness += 0.2 if asset["edr_installed"] else 0

    raw_likelihood = (
        threat_likelihood
        * cvss_factor
        * exposure_factor
        * exploit_factor
        * age_factor
        * (1 - control_effectiveness)
    )
    return round(_clamp(raw_likelihood), 4)


def calculate_impact(asset: dict[str, Any]) -> float:
    """Estimate incident loss from asset value, downtime, and recovery costs."""
    asset_value = asset["asset_value_inr"]
    downtime_cost = asset["downtime_cost_per_hour_inr"] * 24
    recovery_and_regulatory_cost = asset_value * 0.25
    return round(asset_value + downtime_cost + recovery_and_regulatory_cost, 2)


def calculate_eal(likelihood: float, impact: float) -> float:
    """Calculate expected annual loss in INR."""
    return round(likelihood * impact, 2)


def calculate_asset_risks(
    assets: list[dict[str, Any]],
    vulnerabilities: list[dict[str, Any]],
    threats: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Return one quantified risk record for every open vulnerability."""
    assets_by_id = {asset["asset_id"]: asset for asset in assets}
    threats_by_target = {threat["target"]: threat for threat in threats}
    results = []

    for vulnerability in vulnerabilities:
        if vulnerability.get("status") != "OPEN":
            continue
        asset = assets_by_id[vulnerability["asset_id"]]
        threat = threats_by_target.get(asset["asset_type"])
        if threat is None:
            threat = min(
                threats,
                key=lambda candidate: abs(
                    CRITICALITY_FACTOR[asset["business_criticality"]]
                    - {"Critical": 1.0, "High": 0.8, "Medium": 0.5}[candidate["typical_impact"]]
                ),
            )

        likelihood = calculate_likelihood(asset, vulnerability, threat["annual_base_likelihood"])
        impact = calculate_impact(asset)
        results.append(
            {
                "risk_id": f"RISK-{vulnerability['vuln_id']}",
                "asset_id": asset["asset_id"],
                "asset_name": asset["asset_name"],
                "vulnerability_id": vulnerability["vuln_id"],
                "threat_id": threat["threat_id"],
                "likelihood": likelihood,
                "impact_inr": impact,
                "annualized_loss_inr": calculate_eal(likelihood, impact),
                "risk_score": round(likelihood * 100, 2),
                "confidence": "prototype estimate",
            }
        )

    return sorted(results, key=lambda risk: risk["annualized_loss_inr"], reverse=True)