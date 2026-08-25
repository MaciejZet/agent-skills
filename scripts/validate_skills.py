#!/usr/bin/env python3
"""Validate repo-level skill metadata and routing eval suite structure."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
EVALS = ROOT / "evals" / "routing" / "suite.json"
SKILL_NAMES = {
    "ai-council",
    "ai-humanize",
    "competitive-intelligence",
    "customer-ops",
    "design-partner-finder",
    "evidence-researcher",
    "product-operator",
    "product-teardown",
    "release-readiness",
    "repo-to-roadmap",
    "seo-geo-aeo-maxxing",
    "web-app-auditor",
}
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        fail(f"missing YAML frontmatter: {path}")
    block = match.group(1)
    result: dict[str, str] = {}
    key: str | None = None
    buf: list[str] = []
    for line in block.splitlines():
        if line.startswith("  ") and key:
            buf.append(line.strip())
            continue
        if key:
            result[key] = " ".join(buf).strip()
            buf = []
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip()
            if val in (">", ">-", "|"):
                buf = []
            else:
                result[key] = val
                key = None
    if key:
        result[key] = " ".join(buf).strip()
    return result


def validate_skills() -> None:
    found = {p.name for p in SKILLS.iterdir() if p.is_dir() and not p.name.startswith(".")}
    missing = SKILL_NAMES - found
    extra = found - SKILL_NAMES
    if missing:
        fail(f"missing skill dirs: {sorted(missing)}")
    if extra:
        fail(f"unexpected skill dirs: {sorted(extra)}")

    for name in sorted(SKILL_NAMES):
        skill_dir = SKILLS / name
        for rel in ("SKILL.md", "agents/openai.yaml", "LICENSE", "VERSION"):
            if not (skill_dir / rel).is_file():
                fail(f"{name}: missing {rel}")
        fm = parse_frontmatter(skill_dir / "SKILL.md")
        if fm.get("name") != name:
            fail(f"{name}: frontmatter name mismatch ({fm.get('name')!r})")
        desc = fm.get("description", "")
        if len(desc) < 80:
            fail(f"{name}: description too short for routing ({len(desc)} chars)")


def validate_routing_suite() -> None:
    if not EVALS.is_file():
        fail(f"missing routing suite: {EVALS}")
    data = json.loads(EVALS.read_text(encoding="utf-8"))
    cases = data.get("cases")
    if not isinstance(cases, list) or len(cases) < 40:
        fail(f"routing suite needs >= 40 cases, got {len(cases) if isinstance(cases, list) else 0}")

    ids: set[str] = set()
    for i, case in enumerate(cases):
        cid = case.get("id")
        if not cid or cid in ids:
            fail(f"case {i}: duplicate or missing id")
        ids.add(cid)
        for field in ("prompt", "expected_primary_skill", "reason"):
            if not case.get(field):
                fail(f"{cid}: missing {field}")
        primary = case["expected_primary_skill"]
        if primary not in SKILL_NAMES:
            fail(f"{cid}: unknown primary skill {primary!r}")
        for key in ("allowed_secondary_skills", "must_not_trigger"):
            for skill in case.get(key, []):
                if skill not in SKILL_NAMES:
                    fail(f"{cid}: unknown skill in {key}: {skill!r}")

    collision_ids = {
        c["id"]
        for c in cases
        if c.get("expected_primary_skill")
        in {"product-operator", "repo-to-roadmap", "release-readiness"}
    }
    if len(collision_ids) < 12:
        fail(f"expected >= 12 routing cases for operator/roadmap/readiness trio, got {len(collision_ids)}")


def main() -> None:
    validate_skills()
    validate_routing_suite()
    print("OK: skill metadata and routing suite validated")


if __name__ == "__main__":
    main()
