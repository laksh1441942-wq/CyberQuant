from pydantic import BaseModel, Field
from typing import Optional

class ScenarioRequest(BaseModel):
    action: str = Field(
        ...,
        description="Action: 'enable_mfa', 'enable_edr', 'enable_both', 'patch_critical', 'delay_remediation'",
        examples=["enable_mfa"]
    )
    coverage: Optional[int] = Field(
        100,
        ge=1,
        le=100,
        description="Coverage percentage (1-100%)",
        examples=[100]
    )

class ScenarioResponse(BaseModel):
    scenario_action: str
    description: str
    baseline_eal_inr: float
    scenario_eal_inr: float
    risk_reduction_inr: float
    implementation_cost_inr: float
    rosi_percentage: float
    new_enterprise_risk_score: int
