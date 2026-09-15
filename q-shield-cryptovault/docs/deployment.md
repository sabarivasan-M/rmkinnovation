# Deploying Q-Shield CryptoVault to Render

This repo includes everything needed for a one-service deployment on
[Render](https://render.com)'s free tier: `Dockerfile` and `render.yaml` at the repo
root build and run the **frontend, backend, and a local Hardhat blockchain node all
in one container**, so the whole app is reachable behind a single URL.

## How it works

`Dockerfile` builds the React frontend to static files, installs the Python backend,
and installs + compiles the Solidity contract - all inside one image. On container
start, `q-shield-cryptovault/scripts/render-start.sh`:
1. starts `npx hardhat node` (the local chain) in the background,
2. waits for it to accept connections,
3. deploys `QShieldSecurityLog.sol` to it (writes `blockchain/deployment.json`),
4. starts the FastAPI backend, which also serves the built frontend from the same
   origin (see `backend/app/main.py`) - no CORS setup needed.

## Deploy steps (one-time, ~2 minutes of clicking)

1. Sign up / log in at [render.com](https://render.com) (free, no credit card required
   for the free tier).
2. Click **New → Blueprint**.
3. Connect your GitHub account and select this repository
   (`sabarivasan-M/rmkinnovation`).
4. Render reads `render.yaml` automatically and proposes one web service,
   `q-shield-cryptovault`, on the free plan. Click **Apply** / **Create**.
5. Wait for the build (several minutes the first time - it's compiling a Solidity
   contract and installing both a Python and a Node toolchain). Render gives you a
   permanent URL like `https://q-shield-cryptovault.onrender.com`.

That's it - no environment variables need to be set manually; `render.yaml` already
configures them.

## What to expect on the free tier

- **Cold starts**: the free plan spins the service down after 15 minutes of no
  traffic. The next request wakes it up, which re-runs the whole startup sequence
  (fresh Hardhat chain, fresh contract deploy, fresh seeded database) - expect the
  first request after a period of inactivity to take 20-60 seconds.
- **Ephemeral storage**: the SQLite database and the blockchain both reset on every
  cold start / redeploy (free web services have no persistent disk). This is
  actually consistent with the app's own "seeded demonstration data" design - it
  always starts from the same clean, documented state.
- **512MB RAM**: this is genuinely tight for qiskit-aer + scikit-learn + a Node
  Hardhat process running together. If the service crashes or fails health checks,
  check Render's logs first - the most likely cause is an out-of-memory kill, which
  would mean splitting the blockchain node into its own free service (or upgrading
  the plan) rather than a code bug.

## Redeploying after code changes

Render redeploys automatically on every push to the connected branch (`main`), since
`render.yaml` is a Blueprint - no extra steps needed.
