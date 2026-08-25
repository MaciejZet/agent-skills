#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "==> public-safety-check"
./scripts/public-safety-check.sh

echo "==> validate skills + routing evals"
python3 scripts/validate_skills.py
python3 scripts/run_routing_evals.py

echo "==> python compileall"
python3 -m compileall -q skills

echo "==> pytest (all skill tests)"
./scripts/run_all_tests.sh

echo "==> ai-humanize release check"
python3 skills/ai-humanize/scripts/release_check.py

echo "OK: all checks passed"
