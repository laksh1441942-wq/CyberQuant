from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.services.risk_service import evaluate_all_risks
from backend.app.schemas.scenario import ScenarioRequest, ScenarioResponse

router = APIRouter(prefix="/api/scenario", tags=["Scenarios"])

@router.post("", response_model=ScenarioResponse)
def run_scenario(req: ScenarioRequest, db: Session = Depends(get_db)):
    """Simulates What-If remediation action."""
    baseline = evaluate_all_risks(db)
    base_eal = baseline["total_expected_annual_loss_inr"]

    action_normalized = req.action.lower().strip().replace("-", "_")
    
    if action_normalized in ["enable_mfa", "enable_mfa_all", "mfa"]:
        scenario = evaluate_all_risks(db, mfa_override=True)
        cost = 2000000.0
        desc = "Deploy Hardware Token MFA across 100% of accounts (RBI / NIST Compliant)"
    elif action_normalized in ["enable_edr", "enable_edr_all", "edr"]:
        scenario = evaluate_all_risks(db, edr_override=True)
        cost = 3000000.0
        desc = "Deploy behavioral EDR agent across all enterprise endpoints"
    elif action_normalized in ["enable_both", "both", "mfa_and_edr"]:
        scenario = evaluate_all_risks(db, mfa_override=True, edr_override=True)
        cost = 5000000.0
        desc = "Deploy both MFA and EDR enterprise-wide"
    elif action_normalized in ["patch_critical", "patching", "critical_patching"]:
        scenario = evaluate_all_risks(db, mfa_override=True)  # Remediation proxy
        cost = 1000000.0
        desc = "Deploy Critical Patch Program for high-severity CVE vulnerabilities"
    else:
        supported = "['enable_mfa', 'enable_edr', 'enable_both', 'patch_critical']"
        raise HTTPException(status_code=400, detail=f"Unsupported scenario action: '{req.action}'. Supported: {supported}")

    new_eal = scenario["total_expected_annual_loss_inr"]
    risk_reduced = max(0.0, base_eal - new_eal)
    rosi = ((risk_reduced - cost) / cost * 100) if cost > 0 else 0.0

    return ScenarioResponse(
        scenario_action=req.action,
        description=desc,
        baseline_eal_inr=base_eal,
        scenario_eal_inr=new_eal,
        risk_reduction_inr=risk_reduced,
        implementation_cost_inr=cost,
        rosi_percentage=round(rosi, 1),
        new_enterprise_risk_score=scenario["enterprise_risk_score"]
    )
