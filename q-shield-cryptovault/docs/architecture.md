# Q-Shield CryptoVault — Architecture

## Data flow

```
React (Vite/TS) --HTTP--> FastAPI /api/v1 --> Pipeline Orchestrator (app/services/pipeline.py)
                                                 |
                     +---------------------------+---------------------------+
                     |         |          |          |          |            |
                Behaviour  Anomaly     Crypto     Quantum     Risk       Decision
                 Engine    Engine     Engine      Engine     Engine      Engine
                     |         |          |          |          |            |
                     +---------------------------+---------------------------+
                                                 |
                                          SQLAlchemy ORM
                                                 |
                                        SQLite (dev) / Postgres
                                                 |
                                    web3.py --JSON-RPC--> Local Hardhat node
                                                 |
                                     QShieldSecurityLog.sol (deployed contract)
```

## Why this shape

- **One orchestrator, many independent engines.** `app/services/pipeline.py` is the only module that calls
  every engine. Each engine (`app/engines/*`) is a pure function with no knowledge of the others, so each is
  independently unit-testable (see `backend/tests/test_*_engine.py`) and the pipeline stays inspectable.
- **Weights and thresholds live in one place.** `app/core/config.py` holds the five risk weights and the four
  risk-level thresholds. No engine hard-codes a weight.
- **Fail-safe by construction.** The blockchain service (`app/blockchain/service.py`) never raises out of the
  pipeline and never fabricates a `CONFIRMED` status — any RPC/deployment problem degrades to
  `blockchain_status = UNAVAILABLE` while the rest of the pipeline (risk score, decision, database audit row)
  keeps working.
- **SQLite by default, Postgres via one env var.** `DATABASE_URL` in `.env` switches the whole persistence layer;
  no code change required.

## Repository layout

See the top-level tree in `README.md`. Notable choices:

- `backend/app/engines/behaviour`, `.../anomaly`, `.../crypto`, `.../quantum`, `.../risk`, `.../decision` — one
  package per Section-4 pipeline stage. `engines/risk/cyber.py` computes the fifth risk dimension (cyber /
  authentication posture), since it doesn't warrant its own top-level engine package.
- `backend/app/blockchain/service.py` — the only backend module that talks to web3.py / the local chain.
- `blockchain/` — a self-contained Hardhat project (Solidity contract + deploy script + Mocha/Chai tests) that
  writes `deployment.json` (contract address + ABI) which the backend reads to connect.
- `frontend/src/services/api.ts` — the only module that calls the backend. Pages/components never call `axios`
  directly.

## Known scope trade-offs (see `docs/security-model.md` for the full list)

- DB schema is created with SQLAlchemy `metadata.create_all()`, not a full Alembic migration chain — acceptable
  for a local demo prototype, called out explicitly rather than hidden.
- Dashboard "live" updates are short-interval polling, not WebSocket push — labelled as such in the UI, never
  claimed as push-based real-time.
