from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.services.risk_service import evaluate_all_risks
from backend.app.schemas.dashboard import DashboardSummary, TopRiskAsset

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

@router.get("", response_model=DashboardSummary)
def get_dashboard_summary(db: Session = Depends(get_db)):
    """Executive overview metrics: Risk Score, Total EAL, Exposure."""
    results = evaluate_all_risks(db)
    top_item = results["top_5_risk_contributors"][0] if results["top_5_risk_contributors"] else None

    # Calculate potential reduction if MFA enabled
    mfa_scenario = evaluate_all_risks(db, mfa_override=True)
    potential_savings = max(0.0, results["total_expected_annual_loss_inr"] - mfa_scenario["total_expected_annual_loss_inr"])

    top_risk_dto = TopRiskAsset(
        asset_id=top_item["asset_id"],
        asset_name=top_item["asset_name"],
        criticality=top_item["criticality"],
        expected_annual_loss_inr=top_item["expected_annual_loss_inr"],
        likelihood_pct=top_item["likelihood_pct"],
        top_drivers=top_item.get("top_drivers", [])
    ) if top_item else None

    return DashboardSummary(
        enterprise_risk_score=results["enterprise_risk_score"],
        expected_annual_loss_inr=results["total_expected_annual_loss_inr"],
        total_potential_exposure_inr=results["total_potential_exposure_inr"],
        total_monitored_assets=results["total_assets_evaluated"],
        top_risk_asset=top_risk_dto,
        potential_risk_reduction_inr=potential_savings,
        currency="INR",
        model_name="CyberQuant ML Risk Model"
    )
