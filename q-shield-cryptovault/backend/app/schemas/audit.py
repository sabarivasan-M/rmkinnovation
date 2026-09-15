from datetime import datetime

from pydantic import BaseModel


class AuditLogOut(BaseModel):
    event: str
    transaction_id: str
    risk_score: float
    decision: str
    blockchain_reference: str
    blockchain_status: str
    block_number: int
    timestamp: datetime

    class Config:
        from_attributes = True
