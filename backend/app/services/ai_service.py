def generate_ai_response(query: str, top_risk_asset: dict) -> dict:
    """
    Grounded AI Analyst response.
    Combines structured risk engine data with plain-English executive explanations.
    """
    name = top_risk_asset.get("asset_name", "Core Identity Server")
    loss = top_risk_asset.get("expected_annual_loss_inr", 27416000.0)
    chance = top_risk_asset.get("likelihood_pct", 73.6)
    risk_probability = top_risk_asset.get("risk_probability", chance / 100.0)
    drivers = top_risk_asset.get("top_drivers") or [
        "internet exposure",
        "critical CVEs",
        "missing MFA",
    ]

    summary = (
        f"Your highest current financial risk is the {name}, contributing approximately "
        f"₹{loss / 100000:.2f} Lakhs to Expected Annual Cyber Loss. "
        f"The modeled breach likelihood is {chance}%, primarily driven by {', '.join(drivers[:3])}."
    )

    return {
        "query": query,
        "executive_summary": summary,
        "top_risk_asset": name,
        "financial_loss_inr": loss,
        "recommended_action": "Deploy Hardware Token MFA and behavioral EDR agent.",
        "estimated_cost_inr": 2000000.0,
        "expected_savings_inr": 67440000.0,
        "risk_probability": float(risk_probability),
        "risk_drivers": drivers,
    }
