from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.v1.health import system_status
from app.database.session import get_db
from app.models.audit_log import AuditLog
from app.models.crypto_assessment import CryptoAssessment
from app.models.risk_assessment import RiskAssessment
from app.models.security_decision import SecurityDecision
from app.models.transaction import Transaction

router = APIRouter()


@router.get("/dashboard/summary")
def dashboard_summary(db: Session = Depends(get_db)):
    total = db.query(func.count(Transaction.id)).scalar() or 0
    high_risk = db.query(func.count(RiskAssessment.id)).filter(RiskAssessment.risk_level == "HIGH").scalar() or 0
    critical = db.query(func.count(RiskAssessment.id)).filter(RiskAssessment.risk_level == "CRITICAL").scalar() or 0
    quantum_exposed = (
        db.query(func.count(CryptoAssessment.id))
        .filter(CryptoAssessment.quantum_exposure.in_(["HIGH", "CRITICAL"]))
        .scalar()
        or 0
    )

    return {
        "transactions_analysed": total,
        "high_risk_count": high_risk,
        "critical_count": critical,
        "quantum_exposed_count": quantum_exposed,
        "system_status": system_status(db),
    }


@router.get("/dashboard/risk-activity")
def risk_activity(db: Session = Depends(get_db)):
    rows = (
        db.query(Transaction.timestamp, RiskAssessment.unified_score, RiskAssessment.risk_level)
        .join(RiskAssessment, RiskAssessment.transaction_id == Transaction.transaction_id)
        .order_by(Transaction.id.asc())
        .all()
    )
    return [
        {"timestamp": ts.isoformat(), "unified_score": score, "risk_level": level} for ts, score, level in rows
    ]


@router.get("/dashboard/risk-distribution")
def risk_distribution(db: Session = Depends(get_db)):
    rows = db.query(RiskAssessment.risk_level, func.count(RiskAssessment.id)).group_by(RiskAssessment.risk_level).all()
    counts = {level: count for level, count in rows}
    return {level: counts.get(level, 0) for level in ["LOW", "MODERATE", "HIGH", "CRITICAL"]}


@router.get("/dashboard/decision-distribution")
def decision_distribution(db: Session = Depends(get_db)):
    rows = (
        db.query(SecurityDecision.decision, func.count(SecurityDecision.id))
        .group_by(SecurityDecision.decision)
        .all()
    )
    counts = {decision: count for decision, count in rows}
    return {d: counts.get(d, 0) for d in ["APPROVE", "FLAG", "REJECT"]}


@router.get("/dashboard/alerts")
def security_alerts(limit: int = 20, db: Session = Depends(get_db)):
    rows = (
        db.query(RiskAssessment, Transaction)
        .join(Transaction, Transaction.transaction_id == RiskAssessment.transaction_id)
        .filter(RiskAssessment.risk_level.in_(["HIGH", "CRITICAL"]))
        .order_by(RiskAssessment.id.desc())
        .limit(limit)
        .all()
    )
    alerts = []
    for risk, tx in rows:
        for trigger in risk.primary_contributors:
            alerts.append(
                {
                    "severity": risk.risk_level,
                    "message": trigger,
                    "transaction_id": tx.transaction_id,
                    "timestamp": tx.timestamp.isoformat(),
                }
            )
    return alerts[:limit]
