from sqlalchemy.orm import Session
from backend.app.models.control import Control

def optimize_budget_knapsack(db: Session, budget_inr: float):
    """
    Greedy / 0-1 Knapsack budget optimizer.
    Selects security controls that maximize Risk Reduction within available budget.
    """
    controls = db.query(Control).all()

    # Sort controls by efficiency: (Risk Reduction / Cost) descending
    control_list = []
    for c in controls:
        efficiency = (c.risk_reduction_inr / c.cost_inr) if c.cost_inr > 0 else 0
        control_list.append({
            "control_id": c.control_id,
            "name": c.name,
            "cost_inr": c.cost_inr,
            "risk_reduction_inr": c.risk_reduction_inr,
            "framework_mappings": c.frameworks or "NIST CSF, RBI, ISO 27001",
            "efficiency": efficiency
        })

    control_list.sort(key=lambda x: x["efficiency"], reverse=True)

    selected = []
    remaining_budget = budget_inr
    total_invested = 0.0
    total_risk_reduced = 0.0

    for c in control_list:
        if c["cost_inr"] <= remaining_budget:
            selected.append(c)
            remaining_budget -= c["cost_inr"]
            total_invested += c["cost_inr"]
            total_risk_reduced += c["risk_reduction_inr"]

    net_benefit = total_risk_reduced - total_invested
    rosi = (net_benefit / total_invested * 100) if total_invested > 0 else 0.0

    return {
        "budget_inr": budget_inr,
        "total_investment_inr": total_invested,
        "expected_risk_reduction_inr": total_risk_reduced,
        "net_benefit_inr": net_benefit,
        "rosi_percentage": round(rosi, 1),
        "recommended_controls": selected,
        "unallocated_budget_inr": remaining_budget
    }
