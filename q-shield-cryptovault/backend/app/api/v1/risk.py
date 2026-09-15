from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.database.session import get_db
from app.models.risk_assessment import RiskAssessment

router = APIRouter()


@router.get("/risk/policy")
def get_risk_policy():
    settings = get_settings()
    return {
        "weights": {
            "cyber": settings.risk_weight_cyber,
            "behaviour": settings.risk_weight_behaviour,
            "anomaly": settings.risk_weight_anomaly,
            "crypto": settings.risk_weight_crypto,
            "quantum": settings.risk_weight_quantum,
        },
        "thresholds": {
            "LOW": [0, settings.risk_threshold_low],
            "MODERATE": [settings.risk_threshold_low + 1, settings.risk_threshold_moderate],
            "HIGH": [settings.risk_threshold_moderate + 1, settings.risk_threshold_high],
            "CRITICAL": [settings.risk_threshold_high + 1, 100],
        },
        "disclaimer": "Q-Shield prototype policy thresholds, not an industry-standard universal scoring system.",
    }


@router.get("/risk/{transaction_id}")
def get_risk(transaction_id: str, db: Session = Depends(get_db)):
    risk = db.query(RiskAssessment).filter(RiskAssessment.transaction_id == transaction_id).first()
    if risk is None:
        raise HTTPException(status_code=404, detail="Risk assessment not found")
    return risk
