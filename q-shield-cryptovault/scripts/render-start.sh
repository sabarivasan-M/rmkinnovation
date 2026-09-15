#!/usr/bin/env bash
# Container entrypoint for the Render deployment (see ../../Dockerfile and
# ../../render.yaml). Starts the local Hardhat chain, deploys the audit-log
# contract to it, then starts the FastAPI backend (which also serves the
# built frontend from /app/frontend/dist - see backend/app/main.py).
set -e

cd /app/blockchain
npx hardhat node &
HARDHAT_PID=$!

echo "Waiting for local Hardhat node to accept connections..."
for i in $(seq 1 30); do
  if curl -s -X POST http://127.0.0.1:8545 \
      -H "Content-Type: application/json" \
      -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}' \
      > /dev/null 2>&1; then
    echo "Hardhat node is up."
    break
  fi
  sleep 1
done

npx hardhat run scripts/deploy.ts --network localhost

cd /app/backend
exec python -m uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"
