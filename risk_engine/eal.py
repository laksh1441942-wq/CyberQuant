"""Deterministic prototype risk quantification for synthetic CyberQuant data."""

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
    asset: dict[str, Any],
    vulnerability: dict[str, Any],
    threat_likelihood: float,
    mfa_override: bool | None = None,
    edr_override: bool | None = None,
) -> float:
    """Estimate annual incident probability for one asset-vulnerability pair."""
    cvss_factor = _clamp(float(vulnerability.get("cvss_score", 0.0)) / 10.0)
    exposure_factor = 1.25 if asset.get("is_internet_exposed", False) else 0.75
    exploit_factor = 1.2 if vulnerability.get("is_exploit_public", False) else 0.9
    age_factor = min(1.25, 1 + max(0, vulnerability.get("days_unpatched", 0)) / 365)

    has_mfa = mfa_override if mfa_override is not None else asset.get("mfa_enabled", False)
    has_edr = edr_override if edr_override is not None else asset.get("edr_installed", False)
    control_effectiveness = 0.35 + (0.2 if has_mfa else 0) + (0.2 if has_edr else 0)

    raw_likelihood = (
        float(threat_likelihood)
        * cvss_factor
        * exposure_factor
        * exploit_factor
        * age_factor
        * (1 - min(control_effectiveness, 1.0))
    )
    return round(_clamp(raw_likelihood), 4)


def calculate_impact(asset: dict[str, Any]) -> float:
    """Estimate incident loss from asset value, downtime, and recovery costs."""
    asset_value = float(asset.get("asset_value_inr", 0.0))
    downtime_rate = float(asset.get("downtime_cost_per_hour_inr", 20000))
    downtime_cost = downtime_rate * 24
    recovery_and_regulatory_costs = asset_value * 0.25
    return round(asset_value + downtime_cost + recovery_and_regulatory_costs, 2)


def calculate_eal(likelihood: float, impact: float) -> float:
    """Calculate expected annual loss in INR."""
    return round(max(0.0, likelihood) * max(0.0, impact), 2)


def _fallback_threat(asset: dict[str, Any], threats: list[dict[str, Any]]) -> dict[str, Any] | None:
    if not threats:
        return None

    asset_criticality = CRITICALITY_FACTOR.get(asset.get("business_criticality"), 0.5)
    impact_factor = {"Critical": 1.0, "High": 0.8, "Medium": 0.5, "Low": 0.25}
    return min(
        threats,
        key=lambda candidate: abs(
            asset_criticality - impact_factor.get(candidate.get("typical_impact"), 0.5)
        ),
    )


def calculate_asset_risks(
    assets: list[dict[str, Any]],
    vulnerabilities: list[dict[str, Any]],
    threats: list[dict[str, Any]],
    mfa_override: bool | None = None,
    edr_override: bool | None = None,
) -> list[dict[str, Any]]:
    """Return one quantified risk record for every open vulnerability."""
    assets_by_id = {asset["asset_id"]: asset for asset in assets}
    threats_by_target = {threat.get("target"): threat for threat in threats}
    results = []

    for vulnerability in vulnerabilities:
        if vulnerability.get("status", "OPEN") != "OPEN":
            continue
        asset = assets_by_id.get(vulnerability.get("asset_id"))
        if asset is None:
            continue

        threat = threats_by_target.get(asset.get("asset_type")) or _fallback_threat(asset, threats)
        if threat is None:
            continue

        likelihood = calculate_likelihood(
            asset,
            vulnerability,
            threat.get("annual_base_likelihood", 0.0),
            mfa_override,
            edr_override,
        )
        impact = calculate_impact(asset)
        results.append(
            {
                "risk_id": f"RISK-{vulnerability['vuln_id']}",
                "asset_id": asset["asset_id"],
                "asset_name": asset.get("asset_name", asset["asset_id"]),
                "vulnerability_id": vulnerability["vuln_id"],
                "threat_id": threat.get("threat_id"),
                "likelihood": likelihood,
                "impact_inr": impact,
                "annualized_loss_inr": calculate_eal(likelihood, impact),
                "risk_score": round(likelihood * 100, 2),
                "confidence": "prototype estimate",
            }
        )

    return sorted(results, key=lambda risk: risk["annualized_loss_inr"], reverse=True)