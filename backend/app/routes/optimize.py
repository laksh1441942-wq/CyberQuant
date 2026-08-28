from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.services.optimizer_service import optimize_budget_knapsack
from backend.app.schemas.optimize import OptimizeRequest, OptimizeResponse

router = APIRouter(prefix="/api/investment", tags=["Investment Optimization"])

@router.post("/optimize", response_model=OptimizeResponse)
def optimize_security_budget(req: OptimizeRequest, db: Session = Depends(get_db)):
    """Solves the Knapsack optimization problem for cybersecurity spending."""
    result = optimize_budget_knapsack(db, req.budget_inr)
    return OptimizeResponse(**result)
