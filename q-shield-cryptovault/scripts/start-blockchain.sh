#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/../blockchain"
if [ ! -d "node_modules" ]; then
  npm install
fi
npx hardhat node
