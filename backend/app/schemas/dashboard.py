from pydantic import BaseModel
from typing import Optional

class TopRiskAsset(BaseModel):
    asset_id: str
    asset_name: str
    criticality: str
    expected_annual_loss_inr: float
    likelihood_pct: float

class DashboardSummary(BaseModel):
    enterprise_risk_score: int
    expected_annual_loss_inr: float
    total_potential_exposure_inr: float
    total_monitored_assets: int
    top_risk_asset: Optional[TopRiskAsset] = None
    potential_risk_reduction_inr: float
    currency: str = "INR"
