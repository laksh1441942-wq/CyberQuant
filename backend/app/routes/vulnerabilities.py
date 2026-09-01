from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from backend.app.database import get_db
from backend.app.models.vulnerability import Vulnerability
from backend.app.schemas.vulnerability import VulnerabilityListResponse, VulnerabilityResponse

router = APIRouter(prefix="/api/vulnerabilities", tags=["Vulnerabilities"])

@router.get("", response_model=VulnerabilityListResponse)
def list_vulnerabilities(
    severity: Optional[str] = Query(None, description="Filter by severity (Critical, High, Medium, Low)"),
    min_cvss: Optional[float] = Query(None, ge=0.0, le=10.0, description="Filter by minimum CVSS score"),
    exploit_available: Optional[bool] = Query(None, description="Filter by public exploit availability"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: Optional[int] = Query(None, ge=1, le=500, description="Max number of records to return"),
    db: Session = Depends(get_db)
):
    """Lists CVE vulnerabilities with optional filters for severity, CVSS, and exploits."""
    query = db.query(Vulnerability)

    if severity:
        query = query.filter(Vulnerability.severity.ilike(severity.strip()))
    if min_cvss is not None:
        query = query.filter(Vulnerability.cvss_score >= min_cvss)
    if exploit_available is not None:
        query = query.filter(Vulnerability.exploit_available == exploit_available)

    total_count = query.count()
    if skip > 0:
        query = query.offset(skip)
    if limit is not None:
        query = query.limit(limit)

    vulns = query.all()

    return VulnerabilityListResponse(
        total_count=total_count,
        returned_count=len(vulns),
        vulnerabilities=[
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
    )

@router.get("/{vuln_id}", response_model=VulnerabilityResponse)
def get_vulnerability_by_id(vuln_id: str, db: Session = Depends(get_db)):
    """Retrieves specific vulnerability by vuln_id or cve_id."""
    clean_id = vuln_id.strip().lower()
    vuln = db.query(Vulnerability).filter(
        (Vulnerability.vuln_id.ilike(clean_id)) | (Vulnerability.cve_id.ilike(clean_id))
    ).first()

    if not vuln:
        raise HTTPException(status_code=404, detail=f"Vulnerability '{vuln_id}' not found.")

    return VulnerabilityResponse(
        vuln_id=vuln.vuln_id,
        asset_id=vuln.asset_id,
        cve_id=vuln.cve_id,
        title=vuln.title,
        severity=vuln.severity,
        cvss_score=vuln.cvss_score,
        exploit_available=vuln.exploit_available,
        patch_cost_inr=vuln.patch_cost_inr
    )
