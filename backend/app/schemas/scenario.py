from pydantic import BaseModel, Field

class ScenarioRequest(BaseModel):
    action: str = Field(
        ...,
        description="Action name: 'enable_mfa_all', 'enable_edr_all', or 'enable_both'",
        examples=["enable_mfa_all"]
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
