from pydantic import BaseModel, Field
from typing import List, Optional

class AIQueryRequest(BaseModel):
    query: Optional[str] = Field(None, examples=["What is our highest financial cyber risk today?"])
    prompt: Optional[str] = Field(None, examples=["What is our highest financial cyber risk today?"])

class AIQueryResponse(BaseModel):
    query: str
    executive_summary: str
    top_risk_asset: str
    financial_loss_inr: float
    recommended_action: str
    estimated_cost_inr: float
    expected_savings_inr: float
    risk_probability: float = 0.0
    risk_drivers: List[str] = []
