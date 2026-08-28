from fastapi import APIRouter

router = APIRouter(prefix="/api/compliance", tags=["Compliance"])

@router.get("")
def get_compliance_coverage():
    """Returns regulatory compliance mappings for RBI, SEBI, NIST CSF, and ISO 27001."""
    return {
        "overall_coverage_pct": 76.5,
        "frameworks": {
            "NIST_CSF_v2": {
                "name": "NIST Cybersecurity Framework v2.0",
                "coverage_pct": 78.0,
                "controls_implemented": 18,
                "total_controls": 23,
                "status": "Compliant"
            },
            "RBI_CyberSecurity": {
                "name": "RBI Master Direction on Cyber Security",
                "coverage_pct": 82.5,
                "controls_implemented": 14,
                "total_controls": 17,
                "status": "High Alignment"
            },
            "SEBI_CSCRF": {
                "name": "SEBI Cybersecurity and Cyber Resilience Framework",
                "coverage_pct": 74.0,
                "controls_implemented": 12,
                "total_controls": 16,
                "status": "Substantial"
            },
            "ISO_IEC_27001": {
                "name": "ISO/IEC 27001 Annex A",
                "coverage_pct": 71.5,
                "controls_implemented": 21,
                "total_controls": 29,
                "status": "In Progress"
            }
        }
    }
