from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.crypto_assessment import CryptoAssessment

router = APIRouter()


@router.get("/crypto/{transaction_id}")
def get_crypto_assessment(transaction_id: str, db: Session = Depends(get_db)):
    crypto = db.query(CryptoAssessment).filter(CryptoAssessment.transaction_id == transaction_id).first()
    if crypto is None:
        raise HTTPException(status_code=404, detail="Crypto assessment not found")
    return crypto
