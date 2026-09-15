"""Seeded demonstration data (Section 12 / 42-46).

Creates deterministic demo wallets and a small amount of historical
transaction data so the "known recipient" scenarios behave as documented.
This is clearly SEEDED DEMONSTRATION DATA, not real-world statistics.
"""
import logging
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.models.transaction import Transaction
from app.models.wallet import Wallet

logger = logging.getLogger("qshield.database")

_WALLETS = [
    dict(
        address="WALLET-ALPHA",
        label="Alpha (established, normal)",
        crypto_algorithm="ECDSA-secp256k1",
        wallet_age_days=420,
        avg_transaction_amount=0.8,
        usual_transactions_per_day=3.0,
        failed_auth_count=0,
    ),
    dict(
        address="WALLET-BETA",
        label="Beta (established, normal)",
        crypto_algorithm="ECDSA-secp256k1",
        wallet_age_days=380,
        avg_transaction_amount=1.0,
        usual_transactions_per_day=2.0,
        failed_auth_count=0,
    ),
    dict(
        address="WALLET-GAMMA",
        label="Gamma (new, elevated risk history)",
        crypto_algorithm="ECDSA-secp256k1",
        wallet_age_days=2,
        avg_transaction_amount=0.5,
        usual_transactions_per_day=1.0,
        failed_auth_count=2,
    ),
    dict(
        address="WALLET-DELTA",
        label="Delta (legacy RSA profile)",
        crypto_algorithm="RSA-2048",
        wallet_age_days=600,
        avg_transaction_amount=2.0,
        usual_transactions_per_day=5.0,
        failed_auth_count=0,
    ),
]

# (sender, receiver) pairs with prior history, so they are NOT flagged as new-recipient.
_HISTORICAL_PAIRS = [
    ("WALLET-ALPHA", "WALLET-BETA"),
    ("WALLET-DELTA", "WALLET-BETA"),
]


def seed_demo_data(db: Session) -> None:
    if db.query(Wallet).count() > 0:
        logger.info("Seed data already present, skipping")
        return

    for wallet_data in _WALLETS:
        db.add(Wallet(**wallet_data))
    db.commit()

    historical_time = datetime.now(timezone.utc) - timedelta(days=30)
    for index, (sender, receiver) in enumerate(_HISTORICAL_PAIRS):
        db.add(
            Transaction(
                transaction_id=f"TX-QS-SEED-{index + 1:04d}",
                sender_address=sender,
                receiver_address=receiver,
                amount=1.0,
                currency="ETH",
                transaction_type="TRANSFER",
                authentication_status="SUCCESS",
                status="APPROVE",
                is_new_recipient=False,
                timestamp=historical_time,
            )
        )
    db.commit()
    logger.info("Seeded %d demo wallets and %d historical transactions", len(_WALLETS), len(_HISTORICAL_PAIRS))
