# Q-Shield CryptoVault — Security Model & Honest Limitations

Q-Shield CryptoVault is a **security decision-support prototype**. This document states plainly what is
implemented, what is simulated, and what is out of scope — deliberately, per the project's honesty requirements.

## IMPLEMENTED vs SIMULATED vs ASSESSMENT vs DEMO DATA

| Component | Label | What it actually does |
|---|---|---|
| FastAPI backend, SQLAlchemy models, REST API | **IMPLEMENTED** | Real, runs locally, fully tested. |
| Behaviour / Anomaly / Risk / Decision engines | **IMPLEMENTED** | Real deterministic logic and a real scikit-learn IsolationForest, trained on seeded synthetic data. |
| Cryptographic profile assessment | **ASSESSMENT** | Classifies a wallet's algorithm (ECDSA/RSA/PQC) and its quantum-exposure category. Does **not** claim any algorithm is currently broken. |
| Qiskit quantum circuit | **SIMULATED (LOCAL)** | A small (4-qubit) circuit run on `qiskit-aer`'s `AerSimulator` on this machine. **Not** real quantum hardware, **not** a real attack on RSA/ECC/Bitcoin/Ethereum. |
| PQC migration priority | **ASSESSMENT** | A readiness/priority label (LOW–CRITICAL). No automatic migration of any wallet or chain occurs. |
| Blockchain audit log | **LOCAL BLOCKCHAIN** | Hardhat local Ethereum-compatible node + a real deployed Solidity contract. Not mainnet, not testnet. |
| Demo wallets / scenarios | **SEEDED DEMONSTRATION DATA** | Fixed, documented, non-real wallet profiles (`backend/app/database/seed.py`). |

## Explicit non-claims

Q-Shield CryptoVault does **not** claim to have:
- broken Bitcoin, Ethereum, RSA, or ECC;
- performed a real-world quantum attack;
- run on real quantum hardware (IBM Quantum or otherwise);
- automatically migrated any chain or wallet to post-quantum cryptography;
- produced a universally standard / industry-accepted risk score. The 0–24 / 25–49 / 50–74 / 75–100 bands in
  `app/core/config.py` are **Q-Shield prototype policy thresholds**, chosen for this demonstration.
- guaranteed cryptocurrency security. This is a decision-support layer, not a guarantee.

## Fail-safe policy (implemented, tested in `backend/tests/test_failure_injection.py`)

- **Authentication failure always overrides the computed risk score** and forces `REJECT`
  (`app/engines/decision/engine.py`, policy_trigger `AUTHENTICATION_FAILURE_OVERRIDE`).
- **Blockchain unavailable → the system never fabricates a `CONFIRMED` status.** The decision and risk score
  remain visible and fully persisted in the database; only the blockchain audit field reports `UNAVAILABLE`.
- **Malformed input (missing fields, non-positive amount, invalid authentication_status) is rejected by Pydantic
  validation (HTTP 422)** before it ever reaches an engine — see `app/schemas/transaction.py`.
- **An unknown transaction/scenario ID returns HTTP 404**, never a silently-fabricated result.

## Risk score determinism

`calculate_unified_risk()` (`app/engines/risk/engine.py`) is a pure function of its five input scores and the
configured weights — no randomness, no I/O. `backend/tests/test_risk_engine.py` asserts the same inputs always
produce the same `unified_score` and `risk_level`, and checks every threshold boundary explicitly.

The anomaly engine's IsolationForest is fit once, at process start, on a fixed-seed synthetic baseline
(`random_state=42`), so the same input transaction always produces the same anomaly score for the life of a
running backend process (and across restarts, since the training data and seed are both fixed).
