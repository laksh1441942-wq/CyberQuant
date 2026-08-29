from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.services.risk_service import evaluate_all_risks
from backend.app.schemas.scenario import ScenarioRequest, ScenarioResponse

router = APIRouter(prefix="/api/scenario", tags=["Scenarios"])

@router.post("", response_model=ScenarioResponse)
def run_scenario(req: ScenarioRequest, db: Session = Depends(get_db)):
    """Simulates What-If remediation action with custom coverage (Section 24, 44, 47 of SIH Spec)."""
    baseline = evaluate_all_risks(db)
    base_eal = baseline["total_expected_annual_loss_inr"]
    cov_ratio = (req.coverage or 100) / 100.0
    action_clean = req.action.strip().lower()

    if action_clean in ["enable_mfa", "enable_mfa_all"]:
        scenario = evaluate_all_risks(db, mfa_override=True)
        cost = 2000000.0 * cov_ratio
        desc = f"Deploy Hardware Token MFA across {req.coverage or 100}% of accounts"
    elif action_clean in ["enable_edr", "enable_edr_all"]:
        scenario = evaluate_all_risks(db, edr_override=True)
        cost = 3000000.0 * cov_ratio
        desc = f"Deploy behavioral EDR agent across {req.coverage or 100}% of endpoints"
    elif action_clean in ["enable_both", "mfa_and_edr"]:
        scenario = evaluate_all_risks(db, mfa_override=True, edr_override=True)
        cost = 5000000.0 * cov_ratio
        desc = f"Deploy both MFA and EDR enterprise-wide ({req.coverage or 100}% coverage)"
    elif action_clean in ["patch_critical", "patch_vulnerabilities"]:
        # Patching eliminates critical flaws, modeling ~60% loss reduction
        cost = 1000000.0
        desc = "Execute Critical Patch Program across exposed internet-facing servers"
        scenario = evaluate_all_risks(db, mfa_override=False, edr_override=False)
        # Scaled scenario
        reduced_eal = base_eal * (1.0 - (0.45 * cov_ratio))
        risk_reduced = base_eal - reduced_eal
        rosi = ((risk_reduced - cost) / cost * 100) if cost > 0 else 0.0
        return ScenarioResponse(
            scenario_action=req.action,
            description=desc,
            baseline_eal_inr=base_eal,
            scenario_eal_inr=round(reduced_eal, 2),
            risk_reduction_inr=round(risk_reduced, 2),
            implementation_cost_inr=cost,
            rosi_percentage=round(rosi, 1),
            new_enterprise_risk_score=max(18, baseline["enterprise_risk_score"] - 14)
        )
    elif action_clean in ["delay_remediation", "delay_30_days"]:
        # Delaying remediation increases attack window and risk by 25% (Section 24 of spec)
        cost = 0.0
        desc = "Hypothetical Scenario: Delay security remediation by 30 days"
        increased_eal = base_eal * 1.25
        risk_increased = increased_eal - base_eal
        return ScenarioResponse(
            scenario_action=req.action,
            description=desc,
            baseline_eal_inr=base_eal,
            scenario_eal_inr=round(increased_eal, 2),
            risk_reduction_inr=-round(risk_increased, 2),
            implementation_cost_inr=cost,
            rosi_percentage=0.0,
            new_enterprise_risk_score=min(95, baseline["enterprise_risk_score"] + 15)
        )
    else:
        valid_actions = "enable_mfa, enable_edr, enable_both, patch_critical, delay_remediation"
        raise HTTPException(status_code=400, detail=f"Unsupported scenario action: '{req.action}'. Valid options: {valid_actions}")

    new_eal = scenario["total_expected_annual_loss_inr"]
    risk_reduced = max(0.0, base_eal - new_eal) * cov_ratio
    actual_scenario_eal = base_eal - risk_reduced
    rosi = ((risk_reduced - cost) / cost * 100) if cost > 0 else 0.0

    return ScenarioResponse(
        scenario_action=req.action,
        description=desc,
        baseline_eal_inr=base_eal,
        scenario_eal_inr=round(actual_scenario_eal, 2),
        risk_reduction_inr=round(risk_reduced, 2),
        implementation_cost_inr=round(cost, 2),
        rosi_percentage=round(rosi, 1),
        new_enterprise_risk_score=scenario["enterprise_risk_score"]
    )
