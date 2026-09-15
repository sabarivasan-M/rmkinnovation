from sqlalchemy import String, Float, Integer, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.database.session import Base


class AnomalyResult(Base):
    __tablename__ = "anomaly_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    transaction_id: Mapped[str] = mapped_column(String(64), index=True)
    anomaly_score: Mapped[float] = mapped_column(Float)
    is_anomalous: Mapped[bool] = mapped_column(Boolean)
    method: Mapped[str] = mapped_column(String(32), default="isolation_forest")
    triggers: Mapped[list] = mapped_column(JSON, default=list)
