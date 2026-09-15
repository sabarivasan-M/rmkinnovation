import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import audit, crypto, dashboard, decisions, health, quantum, risk, scenarios, transactions, wallets
from app.core.config import get_settings
from app.core.logging_config import setup_logging
from app.database.init_db import init_db
from app.database.seed import seed_demo_data
from app.database.session import SessionLocal

settings = get_settings()
setup_logging(settings.log_level)
logger = logging.getLogger("qshield.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    db = SessionLocal()
    try:
        seed_demo_data(db)
    finally:
        db.close()
    logger.info("Q-Shield backend startup complete")
    yield


app = FastAPI(
    title="Q-Shield CryptoVault API",
    description="Post-Quantum Secure Cryptocurrency Wallet & Blockchain Security System - backend API.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request, exc):
    from fastapi.responses import JSONResponse

    logger.error("Unhandled error on %s: %s", request.url.path, exc)
    return JSONResponse(status_code=500, content={"detail": "Internal error. See server logs."})


API_PREFIX = "/api/v1"
app.include_router(health.router, prefix=API_PREFIX, tags=["health"])
app.include_router(transactions.router, prefix=API_PREFIX, tags=["transactions"])
app.include_router(risk.router, prefix=API_PREFIX, tags=["risk"])
app.include_router(quantum.router, prefix=API_PREFIX, tags=["quantum"])
app.include_router(crypto.router, prefix=API_PREFIX, tags=["crypto"])
app.include_router(decisions.router, prefix=API_PREFIX, tags=["decisions"])
app.include_router(audit.router, prefix=API_PREFIX, tags=["audit"])
app.include_router(dashboard.router, prefix=API_PREFIX, tags=["dashboard"])
app.include_router(wallets.router, prefix=API_PREFIX, tags=["wallets"])
app.include_router(scenarios.router, prefix=API_PREFIX, tags=["scenarios"])
