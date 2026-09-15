from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.security_decision import SecurityDecision

router = APIRouter()


class AnalystReview(BaseModel):
    action: str  # APPROVE | REJECT | KEEP_FLAGGED


@router.get("/decisions/{transaction_id}")
def get_decision(transaction_id: str, db: Session = Depends(get_db)):
    decision = db.query(SecurityDecision).filter(SecurityDecision.transaction_id == transaction_id).first()
    if decision is None:
        raise HTTPException(status_code=404, detail="Decision not found")
    return decision


@router.post("/decisions/{transaction_id}/review")
def review_decision(transaction_id: str, payload: AnalystReview, db: Session = Depends(get_db)):
    decision = db.query(SecurityDecision).filter(SecurityDecision.transaction_id == transaction_id).first()
    if decision is None:
        raise HTTPException(status_code=404, detail="Decision not found")

    action = payload.action.upper()
    if action not in ("APPROVE", "REJECT", "KEEP_FLAGGED"):
        raise HTTPException(status_code=400, detail="action must be APPROVE, REJECT, or KEEP_FLAGGED")

    decision.analyst_override = action
    db.commit()
    db.refresh(decision)
    return decision
