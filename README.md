# CometWeb Agent Skills

Public hub for CometWeb Labs [Agent Skills](https://github.com/MaciejZet/agent-skills).
Each folder under `skills/` is a standalone skill (`SKILL.md`).

## Skills

| Skill | Path | Role | License |
|---|---|---|---|
| Web App Auditor | `skills/web-app-auditor` | Evidence-driven QA / click-through audits | MIT |
| SEO GEO AEO Maxxing | `skills/seo-geo-aeo-maxxing` | Search + AI visibility methodology | MIT |
| AI Humanize | `skills/ai-humanize` | Anti-pattern editing / writing fidelity | MIT |
| AI Council | `skills/ai-council` | Multi-expert decision protocol | MIT |

See `NOTICE` for provenance notes.

## Install

Copy or symlink a skill directory into your agent's skills path, or clone this
repo and point the agent at `skills/<name>`.

```bash
git clone https://github.com/MaciejZet/agent-skills.git
# then register skills/web-app-auditor, skills/seo-geo-aeo-maxxing, …
```

## AI Council setup

1. Copy `skills/ai-council/references/notion-bindings.example.json`
   to `~/.config/cometweb/ai-council-notion.json` (`chmod 600`).
2. Fill your Notion `collection://` IDs (never commit them).
3. Optional override in a clone: `references/notion-bindings.local.json` (gitignored).
4. Follow `skills/ai-council/references/notion-memory.md`.

## Public-safety check

```bash
./scripts/public-safety-check.sh
```

Fails if real Notion UUID bindings or hub page IDs leak into the tree.

## Status

Published for use and fork. KPI for CometWeb Labs is downstream product value,
not star count.
