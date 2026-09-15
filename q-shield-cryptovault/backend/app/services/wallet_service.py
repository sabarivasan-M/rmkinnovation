from sqlalchemy.orm import Session

from app.models.wallet import Wallet


def get_or_create_wallet(db: Session, address: str) -> Wallet:
    wallet = db.query(Wallet).filter(Wallet.address == address).first()
    if wallet is None:
        wallet = Wallet(address=address, label=address[:16])
        db.add(wallet)
        db.commit()
        db.refresh(wallet)
    return wallet


def has_transacted_before(db: Session, sender_address: str, receiver_address: str) -> bool:
    from app.models.transaction import Transaction

    existing = (
        db.query(Transaction)
        .filter(Transaction.sender_address == sender_address, Transaction.receiver_address == receiver_address)
        .first()
    )
    return existing is not None


def count_transactions_today(db: Session, sender_address: str) -> int:
    from datetime import datetime, timezone

    from app.models.transaction import Transaction

    today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    return (
        db.query(Transaction)
        .filter(Transaction.sender_address == sender_address, Transaction.timestamp >= today_start)
        .count()
    )
