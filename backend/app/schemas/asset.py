from pydantic import BaseModel
from typing import List, Optional
from backend.app.schemas.vulnerability import VulnerabilityResponse

class AssetResponse(BaseModel):
    asset_id: str
    asset_name: str
    asset_type: str
    department: str
    criticality: str
    asset_value_inr: float
    is_internet_exposed: bool
    mfa_enabled: bool
    edr_installed: bool
    vulnerability_count: int
    max_cvss: float
    likelihood_pct: float
    financial_impact_inr: float
    expected_annual_loss_inr: float

class AssetDetailResponse(AssetResponse):
    vulnerabilities: List[VulnerabilityResponse] = []

class AssetListResponse(BaseModel):
    total_count: int
    returned_count: int
    assets: List[AssetResponse]
