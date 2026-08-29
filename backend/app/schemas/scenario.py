from typing import Optional
from pydantic import BaseModel, Field

class ScenarioRequest(BaseModel):
    action: str = Field(
        ...,
        description="Action name: 'enable_mfa', 'enable_edr', 'enable_both', or 'patch_critical'",
        example="enable_mfa"
    )
    coverage: Optional[float] = Field(100.0, description="Coverage percentage (0-100%)", example=100.0)

class ScenarioResponse(BaseModel):
    scenario_action: str
    description: str
    baseline_eal_inr: float
    scenario_eal_inr: float
    risk_reduction_inr: float
    implementation_cost_inr: float
    rosi_percentage: float
    new_enterprise_risk_score: int
