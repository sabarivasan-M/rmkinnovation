# Q-Shield CryptoVault — Demo Guide

## Before you start

Run, in three terminals:

```bash
scripts/start-blockchain.sh   # Hardhat local node
scripts/deploy-contract.sh    # deploys QShieldSecurityLog.sol, writes blockchain/deployment.json
scripts/start-backend.sh      # FastAPI on http://127.0.0.1:8000
scripts/start-frontend.sh     # Vite dev server on http://127.0.0.1:5173
```

Open `http://127.0.0.1:5173`.

## Suggested walkthrough (Section 56)

1. **Dashboard** — point out the system status row (API / Database / Risk Engine / Quantum Simulator /
   Blockchain, each a real health check) and the empty-state messaging if nothing has run yet.
2. **Transactions → New Transaction** — open the "Demo Scenarios" list.
3. Click **Suspicious Transaction**. Watch the pipeline progress strip
   (CAPTURE → AUTHENTICATION → BEHAVIOUR → ANOMALY → CRYPTO → QUANTUM → RISK → DECISION → BLOCKCHAIN).
4. You land on the **Transaction Investigation** page: five risk-dimension cards, the Unified Quantum-Cyber Risk
   Score panel with its **Primary Contributors** (the actual triggered features, not canned text), and the
   Security Decision panel (APPROVE/FLAG/REJECT with a reason and a policy_trigger).
5. Scroll down to **Cryptographic Security Assessment** and **Quantum Assessment** — point out the "LOCAL
   SIMULATION" framing and the explicit non-claim sentence.
6. Go to **Quantum Security Center** — the roadmap (CURRENT → ASSESS → PRIORITISE → PREPARE) and the live table
   of quantum-exposure-by-transaction.
7. Go to **Blockchain Audit** — show the audit table with real block numbers / tx hashes from the local chain.
8. Run **Authentication Failure** scenario — show that it REJECTs regardless of how low the risk score is
   (`policy_trigger: AUTHENTICATION_FAILURE_OVERRIDE`) — the fail-safe override in action.
9. (Optional) Stop the Hardhat node, then run another scenario — show the Blockchain Audit page correctly
   reporting `UNAVAILABLE` rather than a fake confirmation, while risk/decision still work normally.

## Expected outcomes per scenario (Section 42-46)

| Scenario | Sender | Expected |
|---|---|---|
| `normal` | WALLET-ALPHA → WALLET-BETA, 0.85 ETH | LOW risk, APPROVE |
| `suspicious` | WALLET-GAMMA → new wallet, 6.5 ETH, 3am | HIGH/CRITICAL risk, FLAG/REJECT |
| `quantum_exposed` | WALLET-DELTA (RSA-2048) → WALLET-BETA | Elevated crypto/quantum dimensions specifically |
| `authentication_failure` | WALLET-ALPHA, auth FAILED | REJECT regardless of score |

Every number shown is calculated live by the backend engines — nothing in the frontend is hard-coded.
