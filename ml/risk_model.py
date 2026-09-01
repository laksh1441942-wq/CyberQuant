"""Explainable risk-score model for CyberQuant.

This implementation keeps the project grounded in an interpretable workflow while
adding a scikit-learn predictive layer for richer portfolio scoring. It falls back
cleanly to the deterministic logic if the ML dependency is unavailable.
"""

from __future__ import annotations

import json
from pathlib import Path
from statistics import mean
from typing import Any

try:  # pragma: no cover - exercised when sklearn is installed in the selected environment.
    import pandas as pd
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import OneHotEncoder
    from sklearn.compose import ColumnTransformer
except Exception:  # pragma: no cover - fallback path for minimal environments.
    pd = None
    RandomForestRegressor = None
    Pipeline = None
    OneHotEncoder = None
    ColumnTransformer = None


CRITICALITY_WEIGHT = {
    "Critical": 1.0,
    "High": 0.75,
    "Medium": 0.45,
    "Low": 0.2,
}

RISK_BANDS = (
    (0.80, "Critical"),
    (0.60, "High"),
    (0.35, "Medium"),
    (0.0, "Low"),
)


def load_enterprise_dataset(data_dir: str | Path) -> dict[str, list[dict[str, Any]]]:
    """Load the generated enterprise datasets for model training and scoring."""
    base_dir = Path(data_dir)
    required = [
        "assets.json",
        "vulnerabilities.json",
        "threats.json",
    ]

    missing = [name for name in required if not (base_dir / name).exists()]
    if missing:
        raise FileNotFoundError(f"Missing required dataset files: {', '.join(missing)}")

    with (base_dir / "assets.json").open("r", encoding="utf-8") as file_handle:
        assets = json.load(file_handle)
    with (base_dir / "vulnerabilities.json").open("r", encoding="utf-8") as file_handle:
        vulnerabilities = json.load(file_handle)
    with (base_dir / "threats.json").open("r", encoding="utf-8") as file_handle:
        threats = json.load(file_handle)

    controls = []
    controls_path = base_dir / "controls.json"
    if controls_path.exists():
        with controls_path.open("r", encoding="utf-8") as file_handle:
            controls = json.load(file_handle)

    return {
        "assets": assets,
        "vulnerabilities": vulnerabilities,
        "threats": threats,
        "controls": controls,
    }


class RiskModel:
    """Interpretable weighted scoring model for asset-level cyber risk."""

    def __init__(self) -> None:
        self.is_trained = False
        self.training_summary: dict[str, Any] = {}
        self.model = None
        self.feature_columns = [
            "asset_type",
            "business_criticality",
            "department",
            "asset_value_inr",
            "downtime_cost_per_hour_inr",
            "is_internet_exposed",
            "mfa_enabled",
            "edr_installed",
            "vuln_count",
            "max_cvss",
            "critical_vuln_count",
            "mean_unpatched_days",
            "threat_likelihood",
        ]

    def train(self, dataset: dict[str, list[dict[str, Any]]]) -> "RiskModel":
        """Train the model using enterprise telemetry + vulnerability data."""
        assets = dataset.get("assets", [])
        vulnerabilities = dataset.get("vulnerabilities", [])
        threats = dataset.get("threats", [])

        avg_cvss = 0.0
        if vulnerabilities:
            avg_cvss = mean(v.get("cvss_score", 0.0) for v in vulnerabilities)

        training_rows = []
        for asset in assets:
            asset_id = asset.get("asset_id")
            asset_vulns = [v for v in vulnerabilities if v.get("asset_id") == asset_id]
            threat = self._resolve_threat(asset, threats)
            features = self._asset_feature_summary(asset, asset_vulns, threat)
            target = self._target_probability(asset, features)
            row = {**features, "risk_probability": target}
            training_rows.append(row)

        self.training_summary = {
            "asset_count": len(assets),
            "vulnerability_count": len(vulnerabilities),
            "average_cvss": round(avg_cvss, 2),
            "critical_assets": sum(
                1 for asset in assets if asset.get("business_criticality") == "Critical"
            ),
            "internet_exposed_assets": sum(
                1 for asset in assets if asset.get("is_internet_exposed")
            ),
        }

        if RandomForestRegressor is not None and pd is not None and self.feature_columns:
            training_df = pd.DataFrame(training_rows)
            x = training_df[self.feature_columns]
            y = training_df["risk_probability"]

            categorical = [col for col in self.feature_columns if col in {"asset_type", "business_criticality", "department"}]
            numeric = [col for col in self.feature_columns if col not in categorical]

            preprocessor = ColumnTransformer(
                transformers=[
                    ("num", "passthrough", numeric),
                    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
                ]
            )
            self.model = Pipeline(
                steps=[
                    ("preprocess", preprocessor),
                    ("regressor", RandomForestRegressor(n_estimators=300, random_state=42, max_depth=12)),
                ]
            )
            self.model.fit(x, y)

        self.is_trained = True
        return self

    def _resolve_threat(self, asset: dict[str, Any], threats: list[dict[str, Any]]) -> dict[str, Any] | None:
        asset_type = asset.get("asset_type", "")
        for threat in threats:
            if str(threat.get("target", "")).lower() == str(asset_type).lower():
                return threat

        for threat in threats:
            if threat.get("typical_impact") in {"Critical", "High", "Medium", "Low"}:
                return threat
        return None

    def _risk_band(self, probability: float) -> str:
        for threshold, label in RISK_BANDS:
            if probability >= threshold:
                return label
        return "Low"

    def _target_probability(self, asset: dict[str, Any], features: dict[str, Any]) -> float:
        base = 0.10 + 0.25 * features["criticality_weight"]
        if features.get("is_internet_exposed"):
            base += 0.12
        if not features.get("mfa_enabled"):
            base += 0.10
        if not features.get("edr_installed"):
            base += 0.08
        base += min(0.18, features.get("mean_unpatched_days", 0.0) / 450.0)
        base += min(0.20, features.get("threat_likelihood", 0.15) / 1.5)
        base += min(0.15, features.get("max_cvss", 0.0) / 20.0)
        base = max(0.02, min(0.96, base))
        return round(base, 4)

    def _asset_feature_summary(
        self,
        asset: dict[str, Any],
        asset_vulns: list[dict[str, Any]],
        threat: dict[str, Any] | None,
    ) -> dict[str, Any]:
        max_cvss = max((v.get("cvss_score", 0.0) for v in asset_vulns), default=0.0)
        critical_vulns = sum(1 for v in asset_vulns if v.get("severity") == "Critical")
        mean_unpatched_days = 0.0
        if asset_vulns:
            mean_unpatched_days = mean(v.get("days_unpatched", 0) for v in asset_vulns)

        return {
            "asset_type": asset.get("asset_type", "Unknown"),
            "business_criticality": asset.get("business_criticality", "Medium"),
            "department": asset.get("department", "Unknown"),
            "asset_value_inr": float(asset.get("asset_value_inr", 0.0)),
            "downtime_cost_per_hour_inr": float(asset.get("downtime_cost_per_hour_inr", 20000.0)),
            "is_internet_exposed": bool(asset.get("is_internet_exposed", False)),
            "mfa_enabled": bool(asset.get("mfa_enabled", False)),
            "edr_installed": bool(asset.get("edr_installed", False)),
            "vuln_count": len(asset_vulns),
            "max_cvss": max_cvss,
            "critical_vuln_count": critical_vulns,
            "mean_unpatched_days": round(mean_unpatched_days, 1),
            "threat_likelihood": float(threat.get("annual_base_likelihood", 0.15)) if threat else 0.15,
            "criticality_weight": CRITICALITY_WEIGHT.get(asset.get("business_criticality", "Medium"), 0.45),
        }

    def _build_top_drivers(
        self,
        asset: dict[str, Any],
        features: dict[str, Any],
        threat: dict[str, Any] | None,
    ) -> list[str]:
        drivers: list[str] = []

        if features["is_internet_exposed"]:
            drivers.append("internet exposure")
        if features["critical_vuln_count"] > 0:
            drivers.append("critical CVEs")
        if not features["mfa_enabled"]:
            drivers.append("missing MFA")
        if not features["edr_installed"]:
            drivers.append("missing EDR")
        if features["criticality_weight"] >= 0.75:
            drivers.append("high asset criticality")
        if threat is not None:
            drivers.append(f"{threat.get('name', 'active threat')} activity")

        if not drivers:
            drivers = ["baseline operational posture"]
        return drivers[:5]

    def _prepare_feature_row(self, asset: dict[str, Any], all_vulnerabilities: list[dict[str, Any]], threats: list[dict[str, Any]]) -> dict[str, Any]:
        asset_id = asset.get("asset_id")
        asset_vulns = [v for v in all_vulnerabilities if v.get("asset_id") == asset_id]
        threat = self._resolve_threat(asset, threats)
        return self._asset_feature_summary(asset, asset_vulns, threat)

    def predict_asset_risk(
        self,
        asset: dict[str, Any],
        all_vulnerabilities: list[dict[str, Any]],
        threats: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Score a single asset and estimate its EAL with a model-driven score."""
        if not self.is_trained:
            raise ValueError("Model must be trained before predicting.")

        asset_id = asset.get("asset_id")
        asset_vulns = [v for v in all_vulnerabilities if v.get("asset_id") == asset_id]
        threat = self._resolve_threat(asset, threats)
        features = self._asset_feature_summary(asset, asset_vulns, threat)

        if self.model is not None:
            row = {
                key: features.get(key) for key in self.feature_columns
            }
            probability = float(self.model.predict(pd.DataFrame([row]))[0])
        else:
            probability = self._target_probability(asset, features)

        probability = max(0.02, min(0.98, probability))

        downtime_hours = 12 if asset.get("business_criticality") in {"Critical", "High"} else 4
        downtime_cost = float(asset.get("downtime_cost_per_hour_inr", 20000.0)) * downtime_hours
        recovery_cost = 500000.0 if asset.get("business_criticality") == "Critical" else 100000.0
        impact = float(asset.get("asset_value_inr", 0.0)) + downtime_cost + recovery_cost
        expected_loss = probability * impact

        return {
            "asset_id": asset_id,
            "asset_name": asset.get("asset_name"),
            "risk_probability": round(probability, 4),
            "risk_band": self._risk_band(probability),
            "expected_annual_loss_inr": round(expected_loss, 2),
            "financial_impact_inr": round(impact, 2),
            "top_drivers": self._build_top_drivers(asset, features, threat),
            "feature_summary": {
                "max_cvss": round(features["max_cvss"], 2),
                "critical_vuln_count": features["critical_vuln_count"],
                "mean_unpatched_days": features["mean_unpatched_days"],
                "threat_likelihood": round(features["threat_likelihood"], 3),
                "internet_exposed": features["is_internet_exposed"],
                "mfa_enabled": features["mfa_enabled"],
                "edr_installed": features["edr_installed"],
            },
        }

    def predict_enterprise_risk(
        self,
        dataset: dict[str, list[dict[str, Any]]],
    ) -> dict[str, Any]:
        """Predict risk across the whole portfolio and summarize enterprise exposure."""
        assets = dataset.get("assets", [])
        vulnerabilities = dataset.get("vulnerabilities", [])
        threats = dataset.get("threats", [])

        results = [
            self.predict_asset_risk(asset, vulnerabilities, threats)
            for asset in assets
        ]
        results.sort(key=lambda item: item["expected_annual_loss_inr"], reverse=True)
        total_eal = sum(item["expected_annual_loss_inr"] for item in results)

        return {
            "enterprise_risk_score": min(98, max(15, round(sum(item["risk_probability"] for item in results) / max(len(results), 1) * 100, 1))),
            "total_expected_annual_loss_inr": round(total_eal, 2),
            "top_5_risk_contributors": results[:5],
            "all_assets": results,
        }
