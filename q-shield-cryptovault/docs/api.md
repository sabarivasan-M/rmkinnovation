# Q-Shield CryptoVault — API Reference

Base URL: `http://127.0.0.1:8000/api/v1`

## Health

- `GET /health` — liveness check. `{status, service, version}`
- `GET /health/system` — per-component status: `api`, `database`, `risk_engine`, `quantum_simulator`, `blockchain`

## Transactions

- `POST /transactions` — capture + run the full pipeline. Body: `TransactionCreate` (see below). Returns
  `TransactionAnalysisOut` (behaviour, anomaly, crypto, quantum, risk, decision, blockchain).
- `GET /transactions?limit=50` — recent transactions with their risk level / decision, for tables.
- `GET /transactions/{transaction_id}` — full detail: transaction + every assessment + blockchain audit info.

`TransactionCreate`:
```json
{
  "sender_address": "WALLET-ALPHA",
  "receiver_address": "WALLET-BETA",
  "amount": 0.85,
  "currency": "ETH",
  "authentication_status": "SUCCESS",
  "simulated_hour_of_day": 14
}
```
`simulated_hour_of_day` (0-23, optional) is a DEMO-ONLY override so scenarios can deterministically show
"transaction at 3am" behaviour without waiting for real time to pass; omit it to use the current server hour.

## Risk

- `GET /risk/policy` — the configured weights, thresholds, and the "not an industry standard" disclaimer.
- `GET /risk/{transaction_id}` — persisted `RiskAssessment` row.

## Quantum

- `GET /quantum/status` — engine info + a fresh demo simulation run (qubits, circuit depth, interpretation).
- `GET /quantum` — recent quantum assessments across transactions.
- `GET /quantum/{transaction_id}` — quantum assessment for one transaction.

## Crypto

- `GET /crypto/{transaction_id}` — cryptographic profile assessment for one transaction.

## Decisions

- `GET /decisions/{transaction_id}` — the security decision.
- `POST /decisions/{transaction_id}/review` — analyst human-in-the-loop override. Body: `{"action": "APPROVE" | "REJECT" | "KEEP_FLAGGED"}`.

## Audit

- `GET /audit?limit=100` — blockchain audit log rows (event, risk score, decision, blockchain status/hash/block).

## Dashboard

- `GET /dashboard/summary` — top metrics + system status.
- `GET /dashboard/risk-activity` — time series of unified scores for the activity chart.
- `GET /dashboard/risk-distribution` — counts per risk level.
- `GET /dashboard/decision-distribution` — counts per decision.
- `GET /dashboard/alerts` — HIGH/CRITICAL transactions' triggers, for the alert panel.

## Wallets & Scenarios

- `GET /wallets` — seeded demo wallets.
- `GET /scenarios` — available demo scenarios (key, label, expected outcome).
- `POST /scenarios/{key}/run` — run one scenario through the real pipeline. Keys: `normal`, `suspicious`,
  `quantum_exposed`, `authentication_failure`.

## Error handling

- Validation errors (missing/invalid fields) → `422` with Pydantic's detail array.
- Unknown transaction / scenario → `404`.
- Any unhandled server error → `500` with a generic `{"detail": "Internal error. See server logs."}` (never a
  stack trace to the client — see `app/main.py`'s exception handler).
