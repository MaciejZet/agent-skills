---
name: skill-orchestrator
description: Plan and execute multi-skill CometWeb workflows with CW-AIP handoffs when the user wants one entry point instead of tagging each specialist. Use when the user asks to orchestrate, sequence, or run end-to-end flows (e.g. evidence then Council, audit then release, research then weekly ops), run everything needed for a goal, or chain Evidence Researcher with ai-council or other skills in order. Loads each step's SKILL.md, runs it fully, and passes envelopes between steps. Do not use for a single-domain task when one specialist skill is enough, for routing-only questions without execution, or to bypass AI Council decision policy or Release Readiness gate rules.
---

# Skill Orchestrator

Single entry point for **multi-skill workflows**. You plan the sequence, execute each
specialist skill in order, and hand off via CW-AIP v1 — without collapsing research
into decisions or skipping skill boundaries.

## Boundaries

**Owns:**

- workflow archetype selection,
- ordered execution plan with envelope types,
- loading each step's `SKILL.md` and running that skill's contract,
- handoff summaries between steps,
- final workflow result (artifacts produced, gaps, what remains).

**Does not own:**

- Evidence Pack construction (Evidence Researcher),
- GO/NO-GO / Council deliberation (AI Council),
- release gate verdicts (Release Readiness),
- weekly priority reconciliation (Product Operator),
- domain findings (auditors, CI, SEO, etc.).

Read `references/workflow-archetypes.md` and `references/sequencing-rules.md`.

## Workflow

### 1. Plan

Run the kernel when the host allows:

```bash
python3 scripts/orchestrate_kernel.py "<user goal>" --json
```

If scripts are unavailable, infer the same archetype from the goal using
`references/workflow-archetypes.md`.

Present the plan before step 1 unless the user asked to run immediately:

```text
Workflow plan (research_then_council)
  1. evidence-researcher — Evidence Pack
  2. ai-council — DecisionHandoff
```

### 2. Confirm scope (lightweight)

If the plan includes **ai-council** and the user did not mention a decision, ask once:
material decision in scope, or evidence-only?

If **release-readiness** is included without a pinned RC/build + environment, stop and
request the pin before gating.

### 3. Execute steps in order

For each step — see `references/sequencing-rules.md`:

1. Read that skill's `SKILL.md`.
2. Execute its full workflow (scripts, validators, output contract).
3. Emit the CW-AIP envelope for the step.
4. Handoff summary before the next step.

Protocol: [`protocol/cw-interchange-v1.md`](../../protocol/cw-interchange-v1.md).

### 4. Close

Emit **Workflow result**:

- archetype used,
- envelope IDs / hashes per step,
- accepted vs gap claims (if research ran),
- Council verdict if Council ran (otherwise explicitly `not run`),
- recommended next single skill if work continues.

## Archetype quick reference

| User intent | Steps |
| --- | --- |
| Verify claims → Council / Rada | evidence-researcher → ai-council |
| Evidence → weekly priorities | evidence-researcher → product-operator |
| QA audit → ship gate | web-app-auditor → release-readiness |
| Competitor delta → strategy | competitive-intelligence → (evidence-researcher?) → ai-council |
| Broad / "do everything" | evidence-researcher → optional operator → optional council |
| One skill only | delegate to that skill; do not orchestrate |

## Example invocations

```text
@skill-orchestrator — Verify our EU AI Act marketing claims, then run Council on
whether we can ship the current landing page copy.
```

```text
@skill-orchestrator — Audit app.cometweb.io/register, then release readiness for
RC 1.2.0 build 4910 on staging.
```

```text
@skill-orchestrator — Full workflow: what evidence do we need before this week's
Insight priorities?
```

## Output contract

Minimum sections:

1. **Workflow plan** — archetype + ordered steps
2. **Step outputs** — one subsection per step with envelope type and pointer
3. **Workflow result** — synthesis without overstepping skill boundaries
4. **CW-AIP handoff block** — JSON or structured list of envelope metadata when useful

Never fold Evidence Researcher synthesis into a Council GO/NO-GO in the same step.
