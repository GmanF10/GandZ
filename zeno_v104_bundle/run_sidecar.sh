#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/zeno_sidecar"
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python app.py "$@"
