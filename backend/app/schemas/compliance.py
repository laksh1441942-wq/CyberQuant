from pydantic import BaseModel
from typing import Dict, Any

class ComplianceResponse(BaseModel):
    overall_coverage_pct: float
    frameworks: Dict[str, Any]
