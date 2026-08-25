#!/usr/bin/env bash
# Symlink CometWeb Agent Skills into CometWeb centrum .claude/skills (relative paths).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
AGENT_SKILLS_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CENTRUM_ROOT="$(cd "$AGENT_SKILLS_ROOT/../.." && pwd)"
TARGET="${CLAUDE_SKILLS_DIR:-$CENTRUM_ROOT/.claude/skills}"
REL_PREFIX="../../platforms/agent-skills/skills"

SKILLS=(
  ai-council
  ai-humanize
  competitive-intelligence
  customer-ops
  design-partner-finder
  evidence-researcher
  product-operator
  product-teardown
  release-readiness
  repo-to-roadmap
  seo-geo-aeo-maxxing
  web-app-auditor
)

mkdir -p "$TARGET"

for name in "${SKILLS[@]}"; do
  src="$AGENT_SKILLS_ROOT/skills/$name"
  dest="$TARGET/$name"
  if [[ ! -d "$src" ]]; then
    echo "FAIL: missing $src" >&2
    exit 1
  fi
  if [[ -L "$dest" ]]; then
    rm "$dest"
  elif [[ -e "$dest" ]]; then
    echo "FAIL: $dest exists and is not a symlink" >&2
    exit 1
  fi
  ln -s "$REL_PREFIX/$name" "$dest"
  echo "linked $name (relative) -> $REL_PREFIX/$name"
done

echo "OK: ${#SKILLS[@]} Claude/Codex skills in $TARGET"
