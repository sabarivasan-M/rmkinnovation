from sqlalchemy import String, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database.session import Base


class CryptoAssessment(Base):
    __tablename__ = "crypto_assessments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    transaction_id: Mapped[str] = mapped_column(String(64), index=True)
    algorithm: Mapped[str] = mapped_column(String(64))
    key_type: Mapped[str] = mapped_column(String(64))
    signature_type: Mapped[str] = mapped_column(String(64))
    security_category: Mapped[str] = mapped_column(String(32))
    quantum_exposure: Mapped[str] = mapped_column(String(16))
    migration_status: Mapped[str] = mapped_column(String(32))
    crypto_score: Mapped[float] = mapped_column(Float)
