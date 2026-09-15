"""Demo scenarios (Section 42-46). Each scenario is real seeded input run
through the REAL pipeline - the resulting score is calculated by the engine,
never hard-coded (Section 44).
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.transaction import TransactionCreate
from app.services.pipeline import analyse_transaction

router = APIRouter()

_SCENARIOS = {
    "normal": dict(
        label="Normal Transaction",
        expected="LOW risk, APPROVE",
        payload=TransactionCreate(
            sender_address="WALLET-ALPHA",
            receiver_address="WALLET-BETA",
            amount=0.85,
            currency="ETH",
            authentication_status="SUCCESS",
            simulated_hour_of_day=14,
        ),
    ),
    "suspicious": dict(
        label="Suspicious Transaction",
        expected="HIGH/CRITICAL risk, FLAG/REJECT",
        payload=TransactionCreate(
            sender_address="WALLET-GAMMA",
            receiver_address="WALLET-UNKNOWN-01",
            amount=6.5,
            currency="ETH",
            authentication_status="SUCCESS",
            simulated_hour_of_day=3,
        ),
    ),
    "quantum_exposed": dict(
        label="Quantum-Exposed Profile",
        expected="Elevated crypto/quantum risk from legacy RSA-2048 profile",
        payload=TransactionCreate(
            sender_address="WALLET-DELTA",
            receiver_address="WALLET-BETA",
            amount=2.1,
            currency="USDT",
            authentication_status="SUCCESS",
            simulated_hour_of_day=15,
        ),
    ),
    "authentication_failure": dict(
        label="Authentication Failure",
        expected="REJECT via fail-safe override, independent of score",
        payload=TransactionCreate(
            sender_address="WALLET-ALPHA",
            receiver_address="WALLET-BETA",
            amount=0.9,
            currency="ETH",
            authentication_status="FAILED",
            simulated_hour_of_day=14,
        ),
    ),
}


@router.get("/scenarios")
def list_scenarios():
    return [{"key": key, "label": v["label"], "expected": v["expected"]} for key, v in _SCENARIOS.items()]


@router.post("/scenarios/{key}/run")
def run_scenario(key: str, db: Session = Depends(get_db)):
    scenario = _SCENARIOS.get(key)
    if scenario is None:
        raise HTTPException(status_code=404, detail="Unknown scenario")
    return analyse_transaction(db, scenario["payload"])
