from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.services.risk_service import evaluate_all_risks
from backend.app.services.ai_service import generate_ai_response
from backend.app.schemas.ai import AIQueryRequest, AIQueryResponse

router = APIRouter(prefix="/api/ai", tags=["AI Analyst"])

@router.post("/query", response_model=AIQueryResponse)
def query_ai_analyst(req: AIQueryRequest, db: Session = Depends(get_db)):
    """Ask CyberQuant plain-English questions about enterprise risk."""
    results = evaluate_all_risks(db)
    top_item = results["top_5_risk_contributors"][0] if results["top_5_risk_contributors"] else {}
    return generate_ai_response(req.query, top_item)
