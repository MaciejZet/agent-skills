# Agent Skills for Claude Code, Cursor and Codex

Fourteen specialist skills for research, product operations, QA, release gates and
strategic decisions — from [CometWeb Labs](https://cometweb.io), MIT-licensed.

Most skill collections are folders of prompts. These ship with CI, **336 unit tests**
and a **75-case routing eval suite**, because a skill whose job is to check something
has to be checked itself. Fourteen skills that pass their own tests, rather than a
catalogue of hundreds that nobody runs.

[![CI](https://github.com/MaciejZet/agent-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/MaciejZet/agent-skills/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/MaciejZet/agent-skills?label=release)](https://github.com/MaciejZet/agent-skills/releases/latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

![Web App Auditor demo](docs/demo/web-app-auditor-demo.gif)

## What is an agent skill?

A skill is a folder with a `SKILL.md` entrypoint that an AI coding agent loads when the
task matches its description. It carries the instructions — and usually scripts and
schemas — for one kind of work, so the agent follows a defined procedure instead of
improvising one. Claude Code, Cursor and Codex each read skills from their own
directory; [`INSTALL.md`](INSTALL.md) covers all three plus ChatGPT.

What separates one collection from another is whether that procedure actually holds.
Here every behavioural claim a skill makes is covered by a test, and routing between
skills is measured against 75 labelled cases instead of assumed:

```bash
./scripts/run_all_tests.sh            # 336 unit tests across 14 skills
python3 scripts/run_routing_evals.py  # 75 routing cases
```

## Start here

Claude Code, in two lines — no clone:

```text
/plugin marketplace add MaciejZet/agent-skills
/plugin install cometweb-agent-skills@cometweb-agent-skills
```

1. **Install** — [`INSTALL.md`](INSTALL.md): the plugin marketplace above, Cursor, Codex, or a ZIP from [Releases](https://github.com/MaciejZet/agent-skills/releases/latest)
2. **First skill** — `@web-app-auditor` (evidence-backed QA; smallest useful demo)
3. **Questions** — [GitHub Discussions](https://github.com/MaciejZet/agent-skills/discussions)

Sample audit report: [`docs/demo/sample-audit-report.json`](docs/demo/sample-audit-report.json)

## Architecture

Fourteen skills that can run alone, but share one evidence and handoff model (CW-AIP v1).
Typical flow:

```text
                         EVIDENCE
                ┌─────────────────────┐
                │ Evidence Researcher │
                └──────────┬──────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
 Competitive        Product Teardown   Design Partner
 Intelligence                              Finder
        │                  │                  │
        └──────────────────┼──────────────────┘
                           ▼
                    Product Operator
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
       Customer Ops  Repo to Roadmap  Specialists
                                      │
                         ┌────────────┴────────────┐
                         ▼                         ▼
                Web App Auditor           SEO / GEO / AEO
                         │
                         └──────────┬──────────────┘
                                    ▼
                          Release Readiness
                                    │
                                    ▼
                              AI Council
                                    │
                                    ▼
                              decision / action

                     AI Humanize → communication layer
```

Real work loops back and branches; the diagram shows default dependencies, not a
single pipeline.

### Evidence before decisions

```text
question → Evidence Researcher → Evidence Pack → specialist / operator / Council → action
```

**Evidence Researcher** builds auditable claim/source/evidence graphs and stops there.
It does not issue GO/NO-GO or product priorities. Downstream skills apply their own
gates to what they accept from an Evidence Pack.

### How invocation works

| Mechanism | What it does |
| --- | --- |
| **`@skill-orchestrator`** | Multi-step flow in **one thread** (same agent, sequential SKILL.md) |
| **`@skill-orchestrator-multiagent`** | Same plan, but **one subagent per skill** (Cursor Task) — parent only merges |
| **Routing rule** (`install-cursor.sh`) | Maps intent from plain chat when you skip `@` tags |
| **Single specialist** | `@web-app-auditor`, `@product-operator`, … when one domain is enough |
| **Evidence Researcher alone** | Evidence Pack only — no GO/NO-GO, no auto-Council |
| **AI Council alone** | Explicit decision — re-verifies evidence even after research |

Example — one tag, full strategic flow:

```text
@skill-orchestrator — Verify our pricing claims, then Council on GO/NO-GO for the new tier.
```

## Skills (14)

| Layer | Skill | Role |
| --- | --- | --- |
| Orchestration | [Skill Orchestrator](skills/skill-orchestrator) | Multi-skill sequences in one thread with CW-AIP handoffs |
| Orchestration | [Skill Orchestrator Multiagent](skills/skill-orchestrator-multiagent) | One isolated subagent (Task) per specialist; parent plans/merges only |
| Evidence | [Evidence Researcher](skills/evidence-researcher) | Atomic claims, source lineage, falsifiers, freshness; Evidence Pack output; no decisions |
| Intelligence | [Competitive Intelligence](skills/competitive-intelligence) | Observation → normalized state → delta → implication; resists headline overreach |
| Intelligence | [Product Teardown](skills/product-teardown) | Transferable patterns from external products; ADOPT requires destination-side evidence |
| Intelligence | [Design Partner Finder](skills/design-partner-finder) | Design partner cohorts and learning contracts—not lead-gen prospecting |
| Product | [Repo to Roadmap](skills/repo-to-roadmap) | Whole-project baseline: topology, gaps, roadmap to a target state |
| Product | [Product Operator](skills/product-operator) | Weekly control loop on existing roadmap/state; lifecycle through Outcome |
| Customer | [Customer Ops](skills/customer-ops) | Support → incident → engineering handoff; closed ticket ≠ verified resolution |
| Quality | [Web App Auditor](skills/web-app-auditor) | Click-through QA with findings, evidence, and a validated report schema |
| Quality | [SEO GEO AEO Maxxing](skills/seo-geo-aeo-maxxing) | Live-verified search and AI-surface visibility audits |
| Release | [Release Readiness](skills/release-readiness) | Pinned RC/build + environment → GO / NO_GO / DEFER; score cannot override gates |
| Decision | [AI Council](skills/ai-council) | Multi-expert material decisions; **explicit invocation only** |
| Writing | [AI Humanize](skills/ai-humanize) | EN/PL prose editing with semantic-fidelity and invariant guards |

### Routing: three skills people confuse

| If the user asks… | Primary skill | Why |
| --- | --- | --- |
| Analyze the whole repo and map the path to a **target state** | **Repo to Roadmap** | Baseline and gap inventory, not a weekly sprint |
| We **already have** a roadmap—what should we do **this week**? | **Product Operator** | Control loop on current state and drift |
| Is **this build/RC** safe to ship to **this environment**? | **Release Readiness** | Requires pinned artifact + environment; gate verdict |

Ambiguous prompts like “analyze the repo for production readiness” are covered in
[`evals/routing/suite.json`](evals/routing/suite.json) (75 cases). Run:

```bash
python3 scripts/run_routing_evals.py
```

Other common routes:

| User intent | Primary skill |
| --- | --- |
| Verify claims → Evidence Pack | **Evidence Researcher** |
| Strategic GO/NO-GO / “przepuść przez Radę” | **AI Council** (explicit) |

## Example invocations

**Product Operator** — weekly reconciliation:

```text
@product-operator — reconcile GitHub + Notion for Insight. What are BLOCKER
and VERIFY NOW items this week?
```

Lifecycle states stay separate: `Intent → Planned → Implemented → Verified → Shipped → Outcome`.
A closed Notion task is not shipped proof.

**Web App Auditor** — bounded QA:

```text
@web-app-auditor — audit cometweb.io/pricing, area mode, standard depth.
```

**Release Readiness** — pinned candidate only:

```text
@release-readiness — RC v1.0.1 build 4821 on staging; run full gate set.
```

**Repo to Roadmap** — first-time or delta baseline:

```text
@repo-to-roadmap — whole-repo baseline for agent-skills; target: public OSS platform.
```

## Install

See **[INSTALL.md](INSTALL.md)** for details.

```bash
git clone https://github.com/MaciejZet/agent-skills.git
cd agent-skills
./scripts/install-cursor.sh          # ~/.cursor/skills + routing rule
./scripts/install-claude.sh          # ~/.claude/skills (Claude Code)
./scripts/install-codex.sh           # ~/.codex/skills (Codex)
./scripts/install-claude-centrum.sh  # CometWeb centrum .claude/skills
```

Single skill:

```bash
ln -s "$(pwd)/skills/web-app-auditor" ~/.cursor/skills/web-app-auditor
```

**AI Council** optional Notion bindings: copy
`skills/ai-council/references/notion-bindings.example.json` to
`~/.config/cometweb/ai-council-notion.json` (`chmod 600`). See
[`skills/ai-council/references/notion-memory.md`](skills/ai-council/references/notion-memory.md).

## Inter-skill protocol

Handoffs use **CometWeb Agent Interchange Protocol (CW-AIP) v1**:
[`protocol/cw-interchange-v1.md`](protocol/cw-interchange-v1.md) with JSON schemas under
`protocol/schemas/`. Envelope kinds include `EvidenceEnvelope`, `FindingEnvelope`,
`DecisionHandoff`, `SpecialistHandoff`, `ArtifactEnvelope`, and `SnapshotMetadata`.

Example chains the protocol supports:

- Evidence Researcher → Product Operator
- Web App Auditor → Release Readiness
- Competitive Intelligence → AI Council

## Quality and evals

```bash
./scripts/run_all_checks.sh           # safety + validate + routing + pytest + release_check
./scripts/public-safety-check.sh    # leak gate: secrets, Linear/Notion IDs, private paths
./scripts/public-safety-check.sh --history   # same rules across every commit ever made
python3 scripts/validate_skills.py    # metadata + routing suite shape
python3 scripts/run_routing_evals.py  # 75 routing cases
./scripts/run_all_tests.sh            # 336 unit tests across skills
```

Per-skill tools live under `skills/<name>/scripts/`. Bundle releases:

```bash
./scripts/package-releases.sh v1.0.2
```

See [CHANGELOG.md](CHANGELOG.md) and [CONTRIBUTING.md](CONTRIBUTING.md).

## Compatibility

| Host | Install path |
| --- | --- |
| **Cursor** | `./scripts/install-cursor.sh` |
| **Claude Code** | `./scripts/install-claude.sh` |
| **Codex** | `./scripts/install-codex.sh` |
| **ChatGPT / Atlas** | Upload per-skill ZIP from Releases; `agents/openai.yaml` metadata |
| **CometWeb centrum** | `./scripts/install-claude-centrum.sh` |

Multiagent smoke walkthrough: [`docs/multiagent-smoke-example.md`](docs/multiagent-smoke-example.md).

Implicit invocation is enabled for most skills. **AI Council** requires explicit
invocation for material decisions.

## License

MIT — see [LICENSE](LICENSE). Per-skill licenses in `skills/*/LICENSE`.
[NOTICE](NOTICE) covers private bindings and provenance.

Built alongside [CometWeb Insight](https://cometweb.io).
