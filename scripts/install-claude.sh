#!/usr/bin/env bash
# Symlink CometWeb Agent Skills into Claude Code (~/.claude/skills/).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TARGET="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
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
  skill-orchestrator
  skill-orchestrator-multiagent
  web-app-auditor
)

mkdir -p "$TARGET"

for name in "${SKILLS[@]}"; do
  src="$ROOT/skills/$name"
  dest="$TARGET/$name"
  if [[ ! -d "$src" ]]; then
    echo "FAIL: missing skill directory $src" >&2
    exit 1
  fi
  if [[ -L "$dest" ]]; then
    rm "$dest"
  elif [[ -e "$dest" ]]; then
    echo "FAIL: $dest exists and is not a symlink — move it aside first" >&2
    exit 1
  fi
  ln -s "$src" "$dest"
  echo "linked $name -> $src"
done

echo "OK: ${#SKILLS[@]} Claude Code skills installed in $TARGET"
