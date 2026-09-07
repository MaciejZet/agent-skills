#!/usr/bin/env bash
# Install the CometWeb agent skills plus the external design stack.
#
# Usage:
#   bash scripts/install-design-stack.sh codex
#   bash scripts/install-design-stack.sh claude --project /path/to/project
#   bash scripts/install-design-stack.sh cursor --project /path/to/project
#
# Global-capable installs:
#   - MaciejZet/agent-skills
#   - Anthropic frontend-design
#   - Impeccable (global when --project is omitted)
#   - UI UX Pro Max CLI
#
# Project-aware installs when --project is provided:
#   - Impeccable project install (including native hooks where supported)
#   - UI UX Pro Max project initialization
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PROVIDER="${1:-codex}"
shift || true

PROJECT=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --project)
      [[ $# -ge 2 ]] || { echo "FAIL: --project requires a path" >&2; exit 2; }
      PROJECT="$2"
      shift 2
      ;;
    -h|--help)
      sed -n '1,22p' "$0"
      exit 0
      ;;
    *)
      echo "FAIL: unknown argument: $1" >&2
      exit 2
      ;;
  esac
done

case "$PROVIDER" in
  codex|claude|cursor) ;;
  *)
    echo "FAIL: provider must be one of: codex, claude, cursor" >&2
    exit 2
    ;;
esac

if [[ -n "$PROJECT" ]]; then
  PROJECT="$(cd "$PROJECT" && pwd)" || {
    echo "FAIL: project path does not exist: $PROJECT" >&2
    exit 2
  }
fi

need() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "FAIL: required command not found: $1" >&2
    exit 1
  }
}

provider_skills_dir() {
  case "$PROVIDER" in
    codex) printf '%s\n' "${CODEX_SKILLS_DIR:-$HOME/.codex/skills}" ;;
    claude) printf '%s\n' "${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}" ;;
    cursor) printf '%s\n' "${CURSOR_SKILLS_DIR:-$HOME/.cursor/skills}" ;;
  esac
}

install_own_skills() {
  echo "==> Installing MaciejZet/agent-skills for $PROVIDER"
  case "$PROVIDER" in
    codex) bash "$ROOT/scripts/install-codex.sh" ;;
    claude) bash "$ROOT/scripts/install-claude.sh" ;;
    cursor) bash "$ROOT/scripts/install-cursor.sh" ;;
  esac
}

install_frontend_design() {
  need git
  local data_home source_root source_skill target
  data_home="${XDG_DATA_HOME:-$HOME/.local/share}"
  source_root="$data_home/cometweb-agent-skills/upstreams/claude-plugins-official"
  source_skill="$source_root/plugins/frontend-design/skills/frontend-design"
  target="$(provider_skills_dir)/frontend-design"

  echo "==> Installing Anthropic frontend-design from upstream"
  mkdir -p "$(dirname "$source_root")"

  if [[ -d "$source_root/.git" ]]; then
    git -C "$source_root" fetch --depth 1 origin main
    git -C "$source_root" reset --hard origin/main
  else
    rm -rf "$source_root"
    git clone --depth 1 --filter=blob:none --sparse \
      https://github.com/anthropics/claude-plugins-official.git "$source_root"
  fi
  git -C "$source_root" sparse-checkout set plugins/frontend-design

  [[ -d "$source_skill" ]] || {
    echo "FAIL: frontend-design skill not found after checkout: $source_skill" >&2
    exit 1
  }

  mkdir -p "$(dirname "$target")"
  if [[ -L "$target" ]]; then
    rm "$target"
  elif [[ -e "$target" ]]; then
    echo "FAIL: $target already exists and is not a symlink; move it aside first" >&2
    exit 1
  fi
  ln -s "$source_skill" "$target"
  echo "linked frontend-design -> $source_skill"
}

install_impeccable() {
  need npx
  echo "==> Installing Impeccable"
  if [[ -n "$PROJECT" ]]; then
    (
      cd "$PROJECT"
      npx -y impeccable install --providers="$PROVIDER" --scope=project
    )
  else
    npx -y impeccable install --providers="$PROVIDER" --scope=global
  fi
}

install_uiux_pro_max() {
  need npm
  echo "==> Installing UI UX Pro Max CLI"
  if ! command -v uipro >/dev/null 2>&1; then
    npm install -g ui-ux-pro-max-cli
  fi

  if [[ -n "$PROJECT" ]]; then
    echo "==> Initializing UI UX Pro Max in $PROJECT for $PROVIDER"
    (
      cd "$PROJECT"
      uipro init --ai "$PROVIDER"
    )
  else
    echo "NOTE: UI UX Pro Max is project-scoped. CLI installed, but no project was modified."
    echo "      Run: bash scripts/install-design-stack.sh $PROVIDER --project /path/to/project"
  fi
}

install_own_skills
install_frontend_design
install_impeccable
install_uiux_pro_max

echo
echo "OK: design skill stack installed for $PROVIDER"
if [[ "$PROVIDER" == "codex" ]]; then
  echo "Codex: open /hooks in each project and approve Impeccable's project hook when prompted."
fi
