#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/../blockchain"
npx hardhat compile
npx hardhat run scripts/deploy.ts --network localhost
