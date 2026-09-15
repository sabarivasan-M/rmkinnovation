from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.anomaly_result import AnomalyResult
from app.models.audit_log import AuditLog
from app.models.behaviour_profile import BehaviourProfile
from app.models.crypto_assessment import CryptoAssessment
from app.models.quantum_assessment import QuantumAssessment
from app.models.risk_assessment import RiskAssessment
from app.models.security_decision import SecurityDecision
from app.models.transaction import Transaction
from app.schemas.analysis import TransactionAnalysisOut
from app.schemas.transaction import TransactionCreate, TransactionOut
from app.services.pipeline import analyse_transaction

router = APIRouter()


@router.post("/transactions", response_model=TransactionAnalysisOut)
def create_and_analyse_transaction(payload: TransactionCreate, db: Session = Depends(get_db)):
    return analyse_transaction(db, payload)


@router.get("/transactions")
def list_transactions(limit: int = 50, db: Session = Depends(get_db)):
    transactions = db.query(Transaction).order_by(Transaction.id.desc()).limit(limit).all()
    results = []
    for tx in transactions:
        risk = db.query(RiskAssessment).filter(RiskAssessment.transaction_id == tx.transaction_id).first()
        decision = db.query(SecurityDecision).filter(SecurityDecision.transaction_id == tx.transaction_id).first()
        results.append(
            {
                "transaction_id": tx.transaction_id,
                "sender_address": tx.sender_address,
                "receiver_address": tx.receiver_address,
                "amount": tx.amount,
                "currency": tx.currency,
                "status": tx.status,
                "timestamp": tx.timestamp,
                "unified_score": risk.unified_score if risk else None,
                "risk_level": risk.risk_level if risk else None,
                "decision": decision.decision if decision else None,
            }
        )
    return results


@router.get("/transactions/{transaction_id}")
def get_transaction_detail(transaction_id: str, db: Session = Depends(get_db)):
    tx = db.query(Transaction).filter(Transaction.transaction_id == transaction_id).first()
    if tx is None:
        raise HTTPException(status_code=404, detail="Transaction not found")

    behaviour = db.query(BehaviourProfile).filter(BehaviourProfile.transaction_id == transaction_id).first()
    anomaly = db.query(AnomalyResult).filter(AnomalyResult.transaction_id == transaction_id).first()
    crypto = db.query(CryptoAssessment).filter(CryptoAssessment.transaction_id == transaction_id).first()
    quantum = db.query(QuantumAssessment).filter(QuantumAssessment.transaction_id == transaction_id).first()
    risk = db.query(RiskAssessment).filter(RiskAssessment.transaction_id == transaction_id).first()
    decision = db.query(SecurityDecision).filter(SecurityDecision.transaction_id == transaction_id).first()
    # AuditLog has no unique constraint on transaction_id (an audit trail can in principle gain more than
    # one event per transaction) - always take the most recent row so this never shows a stale entry.
    audit = (
        db.query(AuditLog)
        .filter(AuditLog.transaction_id == transaction_id)
        .order_by(AuditLog.id.desc())
        .first()
    )

    return {
        "transaction": TransactionOut.model_validate(tx),
        "behaviour": behaviour,
        "anomaly": anomaly,
        "crypto": crypto,
        "quantum": quantum,
        "risk": risk,
        "decision": decision,
        "blockchain": {
            "status": audit.blockchain_status if audit else "UNAVAILABLE",
            "tx_hash": audit.blockchain_reference if audit else "",
            "block_number": audit.block_number if audit else 0,
            "network": "LOCAL HARDHAT",
        },
    }
