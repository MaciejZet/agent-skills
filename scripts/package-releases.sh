#!/usr/bin/env bash
# Package each skill as a release ZIP (skill-name-VERSION.zip).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TAG="${1:-}"
OUT="$ROOT/dist"

if [[ -z "$TAG" ]]; then
  echo "Usage: $0 <tag-or-version>" >&2
  echo "Example: $0 v1.0.0" >&2
  exit 1
fi

mkdir -p "$OUT"
rm -f "$OUT"/*.zip

for skill_dir in "$ROOT"/skills/*/; do
  name="$(basename "$skill_dir")"
  version="$(tr -d '[:space:]' < "$skill_dir/VERSION" 2>/dev/null || echo "1.0.0")"
  zip_name="${name}-${version}.zip"
  (
    cd "$ROOT/skills"
    zip -qr "$OUT/$zip_name" "$name" \
      -x "$name/**/__pycache__/*" \
      -x "$name/**/*.pyc" \
      -x "$name/**/.DS_Store"
  )
  echo "created $OUT/$zip_name"
done

# Bundle all skills + install path
(
  cd "$ROOT"
  zip -qr "$OUT/cometweb-agent-skills-${TAG#v}.zip" \
    skills protocol evals scripts docs/demo \
    README.md INSTALL.md CHANGELOG.md LICENSE NOTICE CONTRIBUTING.md VERSION \
    -x "skills/**/__pycache__/*" \
    -x "docs/demo/preview/*" \
    -x "docs/demo/assets/*.ttf" \
    -x "**/.DS_Store"
)
echo "created $OUT/cometweb-agent-skills-${TAG#v}.zip"
echo "OK: $(ls -1 "$OUT"/*.zip | wc -l | tr -d ' ') archives in $OUT"
