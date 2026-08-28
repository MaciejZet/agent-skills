#!/usr/bin/env bash
# Fail if private data leaks into the public tree.
#
# Design notes (2026-08-28 hardening):
#   * Uses grep, not rg. The previous version wrapped `rg` in `if`, so a missing
#     ripgrep on the runner made every check silently pass — a fail-open gate.
#   * Scans every file type, not just *.md / *.mdc. The 2026-08-26 leak was JSON.
#   * Scans file CONTENT, not just file names.
#   * Scans the whole repo, not just skills/ and docs/.
#   * `--history` additionally scans every blob ever committed. Not run in CI:
#     history is only clean after a filter-repo rewrite. Run it before releases
#     and after any rewrite.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

SCAN_HISTORY=0
[[ "${1:-}" == "--history" ]] && SCAN_HISTORY=1

command -v grep >/dev/null || { echo "FATAL: grep unavailable — gate cannot run" >&2; exit 2; }
command -v git  >/dev/null || { echo "FATAL: git unavailable — gate cannot run" >&2; exit 2; }

failures=0
SELF="scripts/public-safety-check.sh"
EXCLUDES=(--exclude-dir=.git --exclude-dir=node_modules --exclude-dir=dist
          --exclude-dir=.venv --exclude-dir=__pycache__ --exclude-dir=.mypy_cache)

# --- content rules: label|regex[|allowed-path-regex] ---------------------------
# Keep regexes narrow. A noisy gate gets disabled, which is worse than no gate.
# The third field allowlists paths where a match is legitimate guidance rather
# than leaked content (e.g. AGENTS.md telling contributors where private material
# belongs). Allowlist paths, never whole rules.
CONTENT_RULES=(
  "Notion collection UUID|collection://[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
  "Notion hub/page ID|app\.notion\.com/p/[0-9a-f]{20,}|notion\.so/[0-9a-f]{32}"
  "Linear workspace URL|linear\.app/"
  "Linear issue ID|(^|[^A-Za-z0-9])COM-[0-9]{1,5}([^A-Za-z0-9]|$)"
  "owner absolute path|/Users/maciejzet"
  "private vault path|personal/(gtm-cometweb|nauka)/|internal/cometbase/|^\./(AGENTS|CONTRIBUTING)\.md:"
  "CRM/infra hostname|app-eu1\.hubspot|api\.betterwebhub\.com|hpanel\.hostinger"
  "OpenAI-style key|sk-[A-Za-z0-9]{20,}"
  "GitHub token|gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}"
  "Slack token/webhook|xox[baprs]-[A-Za-z0-9-]{10,}|hooks\.slack\.com/services/[A-Z0-9]"
  "Google API key|AIza[0-9A-Za-z_-]{35}"
  "private key block|-----BEGIN [A-Z ]*PRIVATE KEY-----"
  "bearer token|Bearer [A-Za-z0-9._-]{30,}"
)

# --- filename rules -----------------------------------------------------------
NAME_RULES=(
  '*promotion-playbook*' '*GTM-COUNCIL*' '*gtm-council-memo*' '*KROKI-PROMOCJA*'
  '*linear-*' '*.local.json' '.env' '.env.*' '*client_secret*' '*credentials.json'
  '*boardroom*' '*pilot-queue*' '*evidence-register*'
)

scan_content() {
  local rule="$1" label pat allow hits
  label="${rule%%|*}"; rule="${rule#*|}"
  # A trailing "|^\./path:" field is an allowlist, not part of the pattern.
  if [[ "$rule" == *'|^\./'* ]]; then
    allow="${rule##*|}"; pat="${rule%|*}"
  else
    allow=""; pat="$rule"
  fi
  hits=$(grep -rEIn "$pat" . "${EXCLUDES[@]}" 2>/dev/null | grep -v "^\./$SELF:" || true)
  [[ -n "$allow" ]] && hits=$(printf '%s' "$hits" | grep -Ev "$allow" || true)
  if [[ -n "$hits" ]]; then
    echo "FAIL: $label in public tree:" >&2
    echo "$hits" | head -20 >&2
    failures=1
  fi
}

echo "==> content scan (working tree)"
for rule in "${CONTENT_RULES[@]}"; do scan_content "$rule"; done

echo "==> filename scan (working tree)"
while IFS= read -r f; do
  base=$(basename "$f")
  for pat in "${NAME_RULES[@]}"; do
    # shellcheck disable=SC2053
    if [[ "$base" == $pat ]]; then
      echo "FAIL: forbidden filename in public tree: $f — private material belongs in personal/gtm-cometweb/" >&2
      failures=1
    fi
  done
done < <(git ls-files)

if [[ -f skills/ai-council/references/notion-bindings.local.json ]]; then
  echo "FAIL: notion-bindings.local.json must not be present in the release tree" >&2
  failures=1
fi

if [[ "$SCAN_HISTORY" -eq 1 ]]; then
  echo "==> history scan (every commit ever)"
  revs=$(git rev-list --all)
  if [[ -n "$revs" ]]; then
    while IFS= read -r f; do
      base=$(basename "$f")
      for pat in "${NAME_RULES[@]}"; do
        # shellcheck disable=SC2053
        if [[ "$base" == $pat ]]; then
          echo "FAIL(history): file was committed at some point: $f" >&2
          failures=1
        fi
      done
    done < <(git log --all --diff-filter=A --name-only --format= | sort -u | grep -v '^$')

    for rule in "${CONTENT_RULES[@]}"; do
      label="${rule%%|*}"; pat="${rule#*|}"
      # shellcheck disable=SC2086
      if hits=$(git grep -IEn "$pat" $revs -- . ':!'"$SELF" 2>/dev/null) && [[ -n "$hits" ]]; then
        echo "FAIL(history): $label found in committed history:" >&2
        echo "$hits" | head -10 >&2
        failures=1
      fi
    done
  fi
fi

if [[ "$failures" -ne 0 ]]; then
  echo "" >&2
  echo "Public-safety check FAILED. Do not push. See AGENTS.md 'public repo' rules." >&2
  exit 1
fi

echo "OK: public-safety check passed$([[ "$SCAN_HISTORY" -eq 1 ]] && echo ' (incl. history)')"
