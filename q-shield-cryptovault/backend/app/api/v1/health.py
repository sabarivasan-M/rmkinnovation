from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.blockchain.service import get_blockchain_status
from app.database.session import get_db
from app.schemas.dashboard import SystemStatusOut

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "healthy", "service": "q-shield-backend", "version": "1.0.0"}


@router.get("/health/system", response_model=SystemStatusOut)
def system_status(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        db_status = "ONLINE"
    except Exception:  # noqa: BLE001
        db_status = "UNAVAILABLE"

    blockchain = get_blockchain_status()

    return SystemStatusOut(
        api="ONLINE",
        database=db_status,
        risk_engine="ONLINE",
        quantum_simulator="ONLINE (LOCAL SIMULATION)",
        blockchain=blockchain["status"] if blockchain["status"] == "ONLINE" else "UNAVAILABLE (LOCAL)",
    )
