from datetime import datetime, timezone

from sqlalchemy import String, Float, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.database.session import Base


class Wallet(Base):
    __tablename__ = "wallets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    address: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    label: Mapped[str] = mapped_column(String(64), default="")
    crypto_algorithm: Mapped[str] = mapped_column(String(64), default="ECDSA-secp256k1")
    key_type: Mapped[str] = mapped_column(String(64), default="Classical Public-Key")
    wallet_age_days: Mapped[int] = mapped_column(Integer, default=0)
    avg_transaction_amount: Mapped[float] = mapped_column(Float, default=0.0)
    usual_transactions_per_day: Mapped[float] = mapped_column(Float, default=0.0)
    new_recipient_rate: Mapped[float] = mapped_column(Float, default=0.0)
    failed_auth_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
