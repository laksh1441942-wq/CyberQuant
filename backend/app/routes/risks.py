from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.services.risk_service import evaluate_all_risks

router = APIRouter(prefix="/api/risks", tags=["Risks"])

@router.get("")
@router.get("/")
def get_all_risks(db: Session = Depends(get_db)):
    """Returns all evaluated enterprise cyber risks."""
    return evaluate_all_risks(db)

@router.get("/top")
def get_top_risk_assets(limit: int = Query(5, ge=1, le=20), db: Session = Depends(get_db)):
    """Returns top N highest financial risk contributor assets."""
    results = evaluate_all_risks(db)
    top_items = results["top_5_risk_contributors"][:limit]
    return {
        "count": len(top_items),
        "top_contributors": top_items
    }
