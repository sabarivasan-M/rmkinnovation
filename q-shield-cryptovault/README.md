# Q-Shield CryptoVault

Post-quantum-aware cryptocurrency transaction security decision layer — a local, fully working prototype.

**CAPTURE → ANALYSE → QUANTIFY → DECIDE → LOG**, combining cyber, behavioural, anomaly, cryptographic, and
quantum-readiness signals into one **Unified Quantum-Cyber Risk Score** and an explainable
APPROVE / FLAG / REJECT decision, logged to a local blockchain audit trail.

> This is a security decision-support **prototype**, not a production security product. See
> [docs/security-model.md](docs/security-model.md) for an explicit list of what is implemented, simulated, or
> assessment-only — including the honest statement that no real quantum attack, no broken cryptography, and no
> real blockchain migration ever occurs here.

## Features

- Real FastAPI backend with 6 independent, unit-tested engines: behaviour, anomaly (scikit-learn IsolationForest),
  cryptographic assessment, quantum simulation (Qiskit, local), unified risk scoring, and decision policy.
- A deployed Solidity contract (`QShieldSecurityLog.sol`) on a local Hardhat chain, written to via `web3.py`,
  with a documented fail-safe: if the chain is unavailable, the system never fabricates a confirmation.
- A React + TypeScript security dashboard: live system status, risk activity chart, transaction investigation
  page with a full risk breakdown and analyst human-in-the-loop review, Quantum Security Center, and Blockchain
  Audit Trail — all driven by real API data, no hard-coded numbers.
- 4 seeded demo scenarios (normal / suspicious / quantum-exposed / authentication-failure) that run through the
  real pipeline and calculate their score live.

## Architecture

```
frontend/   React + TypeScript + Vite + Tailwind — talks only to the backend API
backend/    FastAPI + SQLAlchemy + scikit-learn + Qiskit + web3.py
blockchain/ Hardhat + Solidity + ethers.js — local Ethereum-compatible chain
data/       Reference copies of seeded demo wallets & scenarios (documentation)
docs/       architecture.md, security-model.md, api.md, demo-guide.md
scripts/    start-backend.sh, start-frontend.sh, start-blockchain.sh, deploy-contract.sh
```

See [docs/architecture.md](docs/architecture.md) for the full data-flow diagram and design rationale.

## Deploy

One-click Render deployment (frontend + backend + local blockchain, one URL, free
tier): see [docs/deployment.md](docs/deployment.md).

## Quick start

Requires: Python 3.10+, Node.js 18+, npm.

**On Windows Git Bash, `COMSPEC` must be set** (needed by esbuild/Hardhat's native postinstall steps):
```bash
export COMSPEC="C:\\Windows\\System32\\cmd.exe"
```

Run in four terminals, in order:

```bash
# 1. Local blockchain
scripts/start-blockchain.sh

# 2. Deploy the contract (after the node above is listening)
scripts/deploy-contract.sh

# 3. Backend API (installs its own venv on first run)
scripts/start-backend.sh

# 4. Frontend
scripts/start-frontend.sh
```

Open **http://localhost:5173**.

If you skip steps 1-2, the app still works fully — the Blockchain Audit page and system status will honestly
report the blockchain as `UNAVAILABLE` rather than faking a confirmation.

## Database

Defaults to SQLite (zero setup). To use Postgres instead, set in `backend/.env` (copy from `.env.example`):
```
DATABASE_URL=postgresql://user:password@localhost:5432/qshield
```

## Testing

```bash
cd backend && ./.venv/Scripts/python.exe -m pytest tests/ -v      # 31 tests: engines, API, failure injection, E2E pipeline
cd blockchain && npx hardhat test                                  # 5 tests: contract behaviour
```

## Demo

See [docs/demo-guide.md](docs/demo-guide.md) for a step-by-step walkthrough and expected outcomes per scenario.

## Limitations (see docs/security-model.md for the full list)

- Quantum simulation is local (Qiskit `AerSimulator`, 4 qubits) — not real quantum hardware, not a real attack.
- PQC migration priority is a readiness assessment, not automatic migration.
- Blockchain runs on local Hardhat, not any public network.
- DB schema uses SQLAlchemy `create_all()`, not a full Alembic migration chain (acceptable for this local prototype).
- Dashboard "live" updates are polling-based, not WebSocket push — labelled accordingly, never claimed otherwise.
- Risk-level thresholds (LOW/MODERATE/HIGH/CRITICAL bands) are Q-Shield prototype policy, not an industry standard.
