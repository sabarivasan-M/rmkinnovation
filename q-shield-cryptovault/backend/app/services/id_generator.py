from datetime import datetime, timezone

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.transaction import Transaction


def generate_transaction_id(db: Session) -> str:
    year = datetime.now(timezone.utc).year
    count = db.query(func.count(Transaction.id)).scalar() or 0
    return f"TX-QS-{year}-{count + 1:04d}"
