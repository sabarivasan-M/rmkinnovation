from sqlalchemy import String, Float, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.database.session import Base


class QuantumAssessment(Base):
    __tablename__ = "quantum_assessments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    transaction_id: Mapped[str] = mapped_column(String(64), index=True)
    simulation_status: Mapped[str] = mapped_column(String(32))
    qubit_count: Mapped[int] = mapped_column(Integer)
    circuit_depth: Mapped[int] = mapped_column(Integer)
    simulation_result: Mapped[dict] = mapped_column(JSON, default=dict)
    security_interpretation: Mapped[str] = mapped_column(String(512))
    quantum_score: Mapped[float] = mapped_column(Float)
    migration_priority: Mapped[str] = mapped_column(String(16))
