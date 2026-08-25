#!/usr/bin/env bash
# Symlink CometWeb Agent Skills into Cursor (~/.cursor/skills/).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TARGET="${CURSOR_SKILLS_DIR:-$HOME/.cursor/skills}"
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

RULE_SRC="$ROOT/extras/cursor-routing.mdc"
RULE_DEST="${CURSOR_RULES_DIR:-$HOME/.cursor/rules}/cometweb-agent-skills.mdc"
if [[ -f "$RULE_SRC" ]]; then
  mkdir -p "$(dirname "$RULE_DEST")"
  if [[ -L "$RULE_DEST" || ! -e "$RULE_DEST" ]]; then
    ln -sf "$RULE_SRC" "$RULE_DEST"
    echo "linked routing rule -> $RULE_DEST"
  else
    echo "skip routing rule: $RULE_DEST already exists"
  fi
fi

echo "OK: ${#SKILLS[@]} Cursor skills installed in $TARGET"
