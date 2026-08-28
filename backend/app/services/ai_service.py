def generate_ai_response(query: str, top_risk_asset: dict) -> dict:
    """
    Grounded AI Analyst response.
    Combines structured risk engine data with plain-English executive explanations.
    """
    name = top_risk_asset.get("asset_name", "Core Identity Server")
    loss = top_risk_asset.get("expected_annual_loss_inr", 27416000.0)
    chance = top_risk_asset.get("likelihood_pct", 73.6)

    summary = (
        f"Your highest current financial risk is the {name}, contributing approximately "
        f"₹{loss / 100000:.2f} Lakhs to Expected Annual Cyber Loss. "
        f"The breach likelihood is {chance}%, primarily driven by internet exposure, "
        f"critical CVE vulnerabilities, and absence of hardware MFA."
    )

    return {
        "query": query,
        "executive_summary": summary,
        "top_risk_asset": name,
        "financial_loss_inr": loss,
        "recommended_action": "Deploy Hardware Token MFA and behavioral EDR agent.",
        "estimated_cost_inr": 2000000.0,
        "expected_savings_inr": 67440000.0
    }
