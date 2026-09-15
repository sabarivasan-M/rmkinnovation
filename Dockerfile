# Single-service deployment image for Q-Shield CryptoVault.
# Runs the React frontend (built to static files), the FastAPI backend, and a
# local Hardhat blockchain node all in one container, so the whole app is
# reachable behind one URL on a single free Render web service.

FROM node:20-slim AS frontend-build
WORKDIR /frontend
COPY q-shield-cryptovault/frontend/package*.json ./
RUN npm install
COPY q-shield-cryptovault/frontend/ ./
RUN npm run build

FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates gnupg && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Backend
COPY q-shield-cryptovault/backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt
COPY q-shield-cryptovault/backend/ backend/

# Blockchain (install deps + compile contract inside the final image so native
# node modules match this container's architecture/glibc)
COPY q-shield-cryptovault/blockchain/package*.json blockchain/
RUN cd blockchain && npm install
COPY q-shield-cryptovault/blockchain/ blockchain/
RUN cd blockchain && npx hardhat compile

# Frontend build output (static files only - no native module concerns)
COPY --from=frontend-build /frontend/dist frontend/dist

COPY q-shield-cryptovault/scripts/render-start.sh render-start.sh
RUN chmod +x render-start.sh

ENV DATABASE_URL=sqlite:////app/backend/qshield.db
ENV BLOCKCHAIN_RPC_URL=http://127.0.0.1:8545
ENV BLOCKCHAIN_ENABLED=true

EXPOSE 8000
CMD ["./render-start.sh"]
