#!/usr/bin/env bash
# Fail if private Notion bindings or hub IDs leak into the public tree.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

failures=0

if rg -n 'collection://[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}' skills README.md NOTICE LICENSE 2>/dev/null; then
  echo "FAIL: real Notion collection UUID found" >&2
  failures=1
fi

if rg -n 'app\.notion\.com/p/[0-9a-f]{20,}|notion\.so/[0-9a-f]{32}' skills README.md NOTICE 2>/dev/null; then
  echo "FAIL: Notion hub/page ID found" >&2
  failures=1
fi

if [[ -f skills/ai-council/references/notion-bindings.local.json ]]; then
  echo "FAIL: notion-bindings.local.json must not be tracked/present in release tree" >&2
  failures=1
fi

if [[ "$failures" -ne 0 ]]; then
  exit 1
fi

echo "OK: public-safety check passed"
