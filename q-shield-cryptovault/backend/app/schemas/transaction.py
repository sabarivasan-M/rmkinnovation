from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class TransactionCreate(BaseModel):
    sender_address: str = Field(min_length=1)
    receiver_address: str = Field(min_length=1)
    amount: float
    currency: str = Field(min_length=1)
    transaction_type: str = "TRANSFER"
    authentication_status: str = "SUCCESS"
    simulated_hour_of_day: int | None = Field(
        default=None, ge=0, le=23, description="DEMO ONLY: override the hour-of-day used for behaviour analysis."
    )

    @field_validator("amount")
    @classmethod
    def amount_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("amount must be greater than 0")
        return v

    @field_validator("authentication_status")
    @classmethod
    def normalise_auth_status(cls, v: str) -> str:
        v = v.upper()
        if v not in ("SUCCESS", "FAILED"):
            raise ValueError("authentication_status must be SUCCESS or FAILED")
        return v


class TransactionOut(BaseModel):
    transaction_id: str
    sender_address: str
    receiver_address: str
    amount: float
    currency: str
    transaction_type: str
    authentication_status: str
    status: str
    is_new_recipient: bool
    timestamp: datetime

    class Config:
        from_attributes = True
