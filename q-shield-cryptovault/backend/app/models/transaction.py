from datetime import datetime, timezone

from sqlalchemy import String, Float, DateTime, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database.session import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    transaction_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    sender_address: Mapped[str] = mapped_column(String(128), index=True)
    receiver_address: Mapped[str] = mapped_column(String(128), index=True)
    amount: Mapped[float] = mapped_column(Float)
    currency: Mapped[str] = mapped_column(String(16))
    transaction_type: Mapped[str] = mapped_column(String(32), default="TRANSFER")
    authentication_status: Mapped[str] = mapped_column(String(32), default="SUCCESS")
    status: Mapped[str] = mapped_column(String(32), default="PENDING")
    is_new_recipient: Mapped[bool] = mapped_column(Boolean, default=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
