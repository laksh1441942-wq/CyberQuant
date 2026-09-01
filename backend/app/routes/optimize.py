from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.services.optimizer_service import optimize_budget_knapsack
from backend.app.schemas.optimize import OptimizeRequest, OptimizeResponse

router = APIRouter(tags=["Investment Optimization"])

@router.post("/api/investment/optimize", response_model=OptimizeResponse)
@router.post("/api/optimize", response_model=OptimizeResponse)
def optimize_security_budget(req: OptimizeRequest, db: Session = Depends(get_db)):
    """Solves the Knapsack optimization problem for cybersecurity spending via POST."""
    result = optimize_budget_knapsack(db, req.budget_inr)
    return OptimizeResponse(**result)

@router.get("/api/investment/optimize", response_model=OptimizeResponse)
@router.get("/api/optimize", response_model=OptimizeResponse)
def optimize_security_budget_get(budget_inr: float = 10000000.0, db: Session = Depends(get_db)):
    """Solves the Knapsack optimization problem via GET query parameter."""
    result = optimize_budget_knapsack(db, budget_inr)
    return OptimizeResponse(**result)
