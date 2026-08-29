from pydantic import BaseModel, Field
from typing import List

class RecommendedControl(BaseModel):
    control_id: str
    name: str
    cost_inr: float
    risk_reduction_inr: float
    framework_mappings: str

class OptimizeRequest(BaseModel):
    budget_inr: float = Field(..., ge=0, example=10000000.0, description="Available security budget in INR (must be non-negative)")

class OptimizeResponse(BaseModel):
    budget_inr: float
    total_investment_inr: float
    expected_risk_reduction_inr: float
    net_benefit_inr: float
    rosi_percentage: float
    recommended_controls: List[RecommendedControl]
    unallocated_budget_inr: float
