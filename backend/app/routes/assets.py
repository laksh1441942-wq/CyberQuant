from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from backend.app.database import get_db
from backend.app.models.vulnerability import Vulnerability
from backend.app.services.risk_service import evaluate_all_risks
from backend.app.schemas.asset import AssetListResponse, AssetResponse, AssetDetailResponse
from backend.app.schemas.vulnerability import VulnerabilityResponse

router = APIRouter(prefix="/api/assets", tags=["Assets"])

@router.get("", response_model=AssetListResponse)
def list_assets(
    department: Optional[str] = Query(None, description="Filter by department (e.g. Core Banking, Payments)"),
    criticality: Optional[str] = Query(None, description="Filter by business criticality (Critical, High, Medium, Low)"),
    is_internet_exposed: Optional[bool] = Query(None, description="Filter by internet exposure"),
    skip: int = Query(0, ge=0, description="Pagination offset"),
    limit: Optional[int] = Query(None, ge=1, le=500, description="Max assets to return"),
    db: Session = Depends(get_db)
):
    """Returns evaluated enterprise assets with EAL calculations and rich filters."""
    results = evaluate_all_risks(db)
    assets = results["all_assets"]

    if department:
        dept_clean = department.strip().lower()
        assets = [a for a in assets if a["department"].strip().lower() == dept_clean]
    if criticality:
        crit_clean = criticality.strip().lower()
        assets = [a for a in assets if a["criticality"].strip().lower() == crit_clean]
    if is_internet_exposed is not None:
        assets = [a for a in assets if a["is_internet_exposed"] == is_internet_exposed]

    total_filtered = len(assets)
    if skip > 0:
        assets = assets[skip:]
    if limit is not None:
        assets = assets[:limit]

    return AssetListResponse(
        total_count=total_filtered,
        returned_count=len(assets),
        assets=[AssetResponse(**a) for a in assets]
    )

@router.get("/{asset_id}", response_model=AssetDetailResponse)
def get_asset_by_id(asset_id: str, db: Session = Depends(get_db)):
    """Retrieves specific asset risk details including associated CVE vulnerabilities."""
    results = evaluate_all_risks(db)
    target_id = asset_id.strip().lower()

    found_asset = None
    for a in results["all_assets"]:
        if a["asset_id"].strip().lower() == target_id:
            found_asset = a
            break

    if not found_asset:
        raise HTTPException(status_code=404, detail=f"Asset '{asset_id}' not found.")

    # Fetch associated vulnerabilities for deep drill-down (Section 30 of SIH spec)
    vulns = db.query(Vulnerability).filter(Vulnerability.asset_id.ilike(target_id)).all()
    vuln_dtos = [
        VulnerabilityResponse(
            vuln_id=v.vuln_id,
            asset_id=v.asset_id,
            cve_id=v.cve_id,
            title=v.title,
            severity=v.severity,
            cvss_score=v.cvss_score,
            exploit_available=v.exploit_available,
            patch_cost_inr=v.patch_cost_inr
        ) for v in vulns
    ]

    return AssetDetailResponse(**found_asset, vulnerabilities=vuln_dtos)
