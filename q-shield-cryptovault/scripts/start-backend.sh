#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/../backend"
if [ ! -d ".venv" ]; then
  python -m venv .venv
fi
./.venv/Scripts/python.exe -m pip install -r requirements.txt -q
./.venv/Scripts/python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
