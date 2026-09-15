"""DB initialisation for the prototype.

Uses SQLAlchemy metadata.create_all() rather than a full migration tool
(Alembic) - a deliberate scope trade-off for a local demo prototype,
documented in docs/limitations. Safe to call repeatedly (idempotent).
"""
import logging

from app import models  # noqa: F401 - ensures all models are registered on Base
from app.database.session import Base, engine

logger = logging.getLogger("qshield.database")


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    logger.info("Database schema ready")
