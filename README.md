# CometWeb Agent Skills

Public agent operating system from [CometWeb Labs](https://cometweb.io): twelve
standalone skills with deterministic kernels, evidence contracts, and cross-skill
handoffs. Each folder under `skills/` ships a `SKILL.md` entrypoint.

[![CI](https://github.com/MaciejZet/agent-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/MaciejZet/agent-skills/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## Problem

Agent skills often collapse into long prompts. CometWeb skills push **truth into
code**: registries, validators, invariant guards, scoring kernels, freshness gates,
and test harnesses — with LLM orchestration on top.

## Skills (12)

| Layer | Skill | Role |
| --- | --- | --- |
| Evidence | [Evidence Researcher](skills/evidence-researcher) | Claim/source/evidence packs; no decisions |
| Intelligence | [Competitive Intelligence](skills/competitive-intelligence) | Temporal competitor state + delta |
| Intelligence | [Product Teardown](skills/product-teardown) | External pattern → target adaptation |
| Intelligence | [Design Partner Finder](skills/design-partner-finder) | Design partner program, not lead gen |
| Product | [Repo to Roadmap](skills/repo-to-roadmap) | Whole-project baseline → roadmap |
| Product | [Product Operator](skills/product-operator) | Control loop: what to do next |
| Customer | [Customer Ops](skills/customer-ops) | Support → incident → engineering loop |
| Quality | [Web App Auditor](skills/web-app-auditor) | Evidence-driven click-through QA |
| Quality | [SEO GEO AEO Maxxing](skills/seo-geo-aeo-maxxing) | Search + AI visibility audit |
| Release | [Release Readiness](skills/release-readiness) | RC-specific GO / NO_GO / DEFER gate |
| Decision | [AI Council](skills/ai-council) | Multi-expert consequential decisions |
| Writing | [AI Humanize](skills/ai-humanize) | Voice-preserving prose editing |

### Routing quick guide

| User intent | Primary skill |
| --- | --- |
| Analyze whole repo → roadmap to target state | **Repo to Roadmap** |
| Weekly “what next?” on existing roadmap/state | **Product Operator** |
| Pin a build/RC → production gate | **Release Readiness** |
| Verify claims → Evidence Pack | **Evidence Researcher** |
| Strategic GO/NO-GO / “przepuść przez Radę” | **AI Council** (explicit) |

See [`evals/routing/suite.json`](evals/routing/suite.json) for cross-skill routing cases.

## Example invocation

```text
@Product Operator — reconcile GitHub + Notion for Insight. What are BLOCKER
and VERIFY NOW items this week?
```

The skill returns bounded actions with lifecycle states
(`Intent → Planned → Implemented → Verified → Shipped → Outcome`), drift flags,
and specialist handoffs — without treating a closed Notion task as shipped proof.

## Install

```bash
git clone https://github.com/MaciejZet/agent-skills.git
cd agent-skills
./scripts/install-cursor.sh          # ~/.cursor/skills + routing rule
./scripts/install-claude-centrum.sh  # CometWeb centrum .claude/skills
```

Manual symlink:

```bash
ln -s "$(pwd)/skills/product-operator" ~/.cursor/skills/product-operator
```

**AI Council** optional Notion bindings: copy
`skills/ai-council/references/notion-bindings.example.json` to
`~/.config/cometweb/ai-council-notion.json` (`chmod 600`). See
[`skills/ai-council/references/notion-memory.md`](skills/ai-council/references/notion-memory.md).

## Inter-skill protocol

Handoffs use **CometWeb Agent Interchange Protocol (CW-AIP) v1**:
[`protocol/cw-interchange-v1.md`](protocol/cw-interchange-v1.md) with JSON schemas
under `protocol/schemas/`. Envelope kinds: `EvidenceEnvelope`, `FindingEnvelope`,
`DecisionHandoff`, `SpecialistHandoff`, `ArtifactEnvelope`, `SnapshotMetadata`.

## Quality & evals

```bash
./scripts/public-safety-check.sh      # no leaked Notion IDs
python3 scripts/validate_skills.py    # metadata + routing suite
./scripts/run_all_tests.sh            # all skill unit tests
python3 skills/ai-humanize/scripts/release_check.py
```

Per-skill deterministic tools live under `skills/<name>/scripts/`. Release tags:
`<skill-name>-vX.Y.Z` (see each skill's `VERSION` file).

## Compatibility

Skills ship `agents/openai.yaml` for ChatGPT, Codex, Atlas, and API hosts that
support Agent Skills. Implicit invocation is enabled for most skills; **AI Council**
requires explicit invocation for material decisions.

## License & notice

MIT — see [LICENSE](LICENSE). Per-skill licenses in `skills/*/LICENSE`.
[NOTICE](NOTICE) covers private bindings and provenance.

## CometWeb Labs

Downstream product value over star count. Built alongside
[CometWeb Insight](https://cometweb.io) and the CometWeb agent toolchain.
