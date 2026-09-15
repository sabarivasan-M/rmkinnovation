from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.engines.quantum.engine import assess_quantum_exposure
from app.models.quantum_assessment import QuantumAssessment

router = APIRouter()


@router.get("/quantum/status")
def quantum_status():
    demo = assess_quantum_exposure("HIGH")
    return {
        "engine": "Qiskit (qiskit-aer AerSimulator)",
        "mode": "LOCAL SIMULATION",
        "status": demo.simulation_status,
        "qubits": demo.qubit_count,
        "circuit_depth": demo.circuit_depth,
        "interpretation": demo.security_interpretation,
    }


@router.get("/quantum")
def list_quantum_assessments(limit: int = 20, db: Session = Depends(get_db)):
    return db.query(QuantumAssessment).order_by(QuantumAssessment.id.desc()).limit(limit).all()


@router.get("/quantum/{transaction_id}")
def get_quantum_assessment(transaction_id: str, db: Session = Depends(get_db)):
    quantum = db.query(QuantumAssessment).filter(QuantumAssessment.transaction_id == transaction_id).first()
    if quantum is None:
        raise HTTPException(status_code=404, detail="Quantum assessment not found")
    return quantum
