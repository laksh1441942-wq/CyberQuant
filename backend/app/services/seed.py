import os
import json
from sqlalchemy.orm import Session
from backend.app.config import PROJECT_ROOT
from backend.app.models.asset import Asset
from backend.app.models.vulnerability import Vulnerability
from backend.app.models.control import Control

def seed_database_from_json(db: Session):
    """Loads Rajat's synthetic data from data/generated/ into database tables (cross-platform)."""
    data_dir = PROJECT_ROOT / "data" / "generated"
    assets_file = data_dir / "assets.json"
    vulns_file = data_dir / "vulnerabilities.json"
    controls_file = data_dir / "controls.json"

    # If assets already seeded, skip
    if db.query(Asset).first():
        return

    if assets_file.exists():
        with open(assets_file, "r", encoding="utf-8") as f:
            assets_data = json.load(f)
            for a in assets_data:
                db.add(Asset(
                    asset_id=a["asset_id"],
                    asset_name=a["asset_name"],
                    asset_type=a["asset_type"],
                    department=a["department"],
                    business_criticality=a["business_criticality"],
                    asset_value_inr=float(a["asset_value_inr"]),
                    is_internet_exposed=bool(a["is_internet_exposed"]),
                    downtime_cost_per_hour_inr=float(a.get("downtime_cost_per_hour_inr", 20000)),
                    mfa_enabled=bool(a.get("mfa_enabled", False)),
                    edr_installed=bool(a.get("edr_installed", False))
                ))
        db.commit()
        print(f"[SEED] Seeded {len(assets_data)} assets into database.")

    if vulns_file.exists():
        with open(vulns_file, "r", encoding="utf-8") as f:
            vulns_data = json.load(f)
            for v in vulns_data:
                db.add(Vulnerability(
                    vuln_id=v.get("vuln_id") or v.get("vulnerability_id"),
                    asset_id=v["asset_id"],
                    cve_id=v["cve_id"],
                    title=v.get("vulnerability_name") or v.get("title", ""),
                    severity=v["severity"],
                    cvss_score=float(v["cvss_score"]),
                    exploit_available=bool(v.get("is_exploit_public", v.get("exploit_available", False))),
                    patch_cost_inr=float(v.get("patch_cost_inr", 50000))
                ))
        db.commit()
        print(f"[SEED] Seeded {len(vulns_data)} vulnerabilities into database.")

    if controls_file.exists():
        with open(controls_file, "r", encoding="utf-8") as f:
            controls_data = json.load(f)
            for c in controls_data:
                mapping = c.get("framework_mapping") or c.get("frameworks", [])
                db.add(Control(
                    control_id=c["control_id"],
                    name=c["name"],
                    description=c.get("description", ""),
                    cost_inr=float(c["cost_inr"]),
                    risk_reduction_inr=float(c.get("expected_risk_reduction_inr") or c.get("risk_reduction_inr", 0)),
                    frameworks=", ".join(mapping) if isinstance(mapping, list) else str(mapping)
                ))
        db.commit()
        print(f"[SEED] Seeded {len(controls_data)} controls into database.")
