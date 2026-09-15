from sqlalchemy import String, Float, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.database.session import Base


class BehaviourProfile(Base):
    __tablename__ = "behaviour_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    transaction_id: Mapped[str] = mapped_column(String(64), index=True)
    behaviour_score: Mapped[float] = mapped_column(Float)
    amount_deviation: Mapped[float] = mapped_column(Float)
    velocity_score: Mapped[float] = mapped_column(Float)
    new_recipient_penalty: Mapped[float] = mapped_column(Float)
    time_of_day_penalty: Mapped[float] = mapped_column(Float)
    auth_failure_penalty: Mapped[float] = mapped_column(Float)
    triggers: Mapped[list] = mapped_column(JSON, default=list)
