from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from backend.app.database import get_db
from backend.app.services.risk_service import evaluate_all_risks
from backend.app.schemas.asset import AssetListResponse, AssetResponse

router = APIRouter(prefix="/api/assets", tags=["Assets"])

@router.get("", response_model=AssetListResponse)
def list_assets(
    limit: Optional[int] = Query(None, description="Limit number of returned assets"),
    department: Optional[str] = Query(None, description="Filter by department"),
    db: Session = Depends(get_db)
):
    """Returns evaluated enterprise assets with EAL calculations."""
    results = evaluate_all_risks(db)
    assets = results["all_assets"]

    if department:
        assets = [a for a in assets if a["department"].lower() == department.lower()]
    if limit:
        assets = assets[:limit]

    return AssetListResponse(
        total_count=len(results["all_assets"]),
        returned_count=len(assets),
        assets=[AssetResponse(**a) for a in assets]
    )

@router.get("/{asset_id}", response_model=AssetResponse)
def get_asset_by_id(asset_id: str, db: Session = Depends(get_db)):
    """Retrieves specific asset risk details."""
    results = evaluate_all_risks(db)
    target_id = asset_id.strip().lower()
    for a in results["all_assets"]:
        if a["asset_id"].strip().lower() == target_id:
            return AssetResponse(**a)
    raise HTTPException(status_code=404, detail=f"Asset '{asset_id}' not found.")
