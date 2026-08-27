"""
================================================================================
CYBERQUANT — DAY 3 TASK: FASTAPI BACKEND SERVER (main.py)
================================================================================
Author: Backend Team
Purpose: High-speed asynchronous REST API server connecting the FAIR Risk Engine
         and synthetic enterprise telemetry to the frontend dashboard and external clients.

Key Endpoints:
  1. GET  /                     - Health check and API metadata
  2. GET  /api/dashboard        - Enterprise summary: Risk Score, Total EAL, Exposure
  3. GET  /api/assets           - Detailed risk breakdown for all 150 enterprise assets
  4. GET  /api/risks/top        - Top 5 highest financial risk contributor assets
  5. POST /api/scenario         - What-If simulation engine (MFA, EDR, Remediation)

Interactive Documentation:
  Swagger UI: http://127.0.0.1:8000/docs
  ReDoc:      http://127.0.0.1:8000/redoc
================================================================================
"""

import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

# Ensure local imports work reliably
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from risk_engine import quantify_all_risks, calculate_scenario, load_data

# Initialize FastAPI application
app = FastAPI(
    title="CyberQuant Risk Engine API",
    description="AI-Powered Continuous Cyber Risk Quantification & Investment Optimization Platform (SIH 2026)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS (Cross-Origin Resource Sharing) so browsers & frontends can communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==============================================================================
# PYDANTIC DATA SCHEMAS (Request & Response Validation)
# ==============================================================================

class ScenarioRequest(BaseModel):
    action: str = Field(
        ...,
        description="Scenario action name: 'enable_mfa_all', 'enable_edr_all', or 'enable_both'",
        example="enable_mfa_all"
    )


# ==============================================================================
# REST API ROUTES
# ==============================================================================

@app.get("/", tags=["Health"])
def health_check():
    """Health check endpoint to verify backend status."""
    return {
        "status": "online",
        "service": "CyberQuant Risk Engine API",
        "version": "1.0.0",
        "framework": "FastAPI + Uvicorn",
        "docs_url": "/docs"
    }


@app.get("/api/dashboard", tags=["Dashboard"])
def get_dashboard_summary():
    """
    Returns executive summary metrics:
      - Enterprise Risk Score (0 to 100)
      - Total Expected Annual Loss (EAL in ₹)
      - Total Potential Exposure (₹)
      - Top risk asset and potential risk reduction opportunity
    """
    try:
        risk_data = quantify_all_risks()
        top_asset = risk_data["top_5_risk_contributors"][0] if risk_data["top_5_risk_contributors"] else None
        
        # Calculate potential risk reduction if MFA is enabled
        mfa_simulation = calculate_scenario("enable_mfa_all")
        potential_reduction = mfa_simulation.get("risk_reduction_inr", 0.0)
        
        return {
            "enterprise_risk_score": risk_data["enterprise_risk_score"],
            "expected_annual_loss_inr": risk_data["total_expected_annual_loss_inr"],
            "total_potential_exposure_inr": risk_data["total_potential_exposure_inr"],
            "total_monitored_assets": risk_data["total_assets_evaluated"],
            "top_risk_asset": {
                "asset_id": top_asset["asset_id"],
                "asset_name": top_asset["asset_name"],
                "criticality": top_asset["criticality"],
                "expected_annual_loss_inr": top_asset["expected_annual_loss_inr"],
                "likelihood_pct": top_asset["likelihood_pct"]
            } if top_asset else None,
            "potential_risk_reduction_inr": potential_reduction,
            "currency": "INR"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Risk calculation failed: {str(e)}")


@app.get("/api/assets", tags=["Assets"])
def get_evaluated_assets(limit: Optional[int] = None):
    """
    Returns the complete list of 150 evaluated enterprise assets with:
      - Asset valuation, criticality, department
      - Vulnerability counts and max CVSS severity
      - Attack likelihood (%) and Expected Annual Loss (₹)
    """
    try:
        risk_data = quantify_all_risks()
        assets = risk_data["all_assets"]
        if limit:
            assets = assets[:limit]
        return {
            "total_count": len(risk_data["all_assets"]),
            "returned_count": len(assets),
            "assets": assets
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch assets: {str(e)}")


@app.get("/api/risks/top", tags=["Risks"])
def get_top_risk_contributors(limit: int = 5):
    """Returns the top N highest financial risk contributor assets in the enterprise."""
    try:
        risk_data = quantify_all_risks()
        top_risks = risk_data["top_5_risk_contributors"][:limit]
        return {
            "top_contributors": top_risks,
            "count": len(top_risks)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch top risks: {str(e)}")


@app.post("/api/scenario", tags=["Scenarios"])
def run_scenario_simulation(req: ScenarioRequest):
    """
    Simulates a 'What-If' remediation scenario.
    Allowed actions:
      - 'enable_mfa_all': Enables MFA across 100% of accounts
      - 'enable_edr_all': Deploys EDR across 100% of endpoints
      - 'enable_both': Deploys both controls enterprise-wide
    """
    try:
        result = calculate_scenario(req.action)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scenario simulation failed: {str(e)}")


# ==============================================================================
# STANDALONE ENTRYPOINT
# ==============================================================================

if __name__ == "__main__":
    import uvicorn
    print("[DAY 3] Starting CyberQuant FastAPI Server on http://127.0.0.1:8000...")
    print("Swagger API Documentation available at: http://127.0.0.1:8000/docs")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
