from sqlalchemy import String, Float, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.database.session import Base


class RiskAssessment(Base):
    __tablename__ = "risk_assessments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    transaction_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    cyber_score: Mapped[float] = mapped_column(Float)
    behaviour_score: Mapped[float] = mapped_column(Float)
    anomaly_score: Mapped[float] = mapped_column(Float)
    crypto_score: Mapped[float] = mapped_column(Float)
    quantum_score: Mapped[float] = mapped_column(Float)
    unified_score: Mapped[float] = mapped_column(Float)
    risk_level: Mapped[str] = mapped_column(String(16))
    primary_contributors: Mapped[list] = mapped_column(JSON, default=list)
