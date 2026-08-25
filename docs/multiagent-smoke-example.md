# Multiagent smoke example

Bounded workflow for validating `@skill-orchestrator-multiagent` end-to-end.

## Goal

Verify three pricing claims on https://cometweb.io/pricing, then Council GO/NO-GO on
whether current **Growth** tier copy can ship as-is.

## 1. Plan

```bash
cd platforms/agent-skills
python3 skills/skill-orchestrator-multiagent/scripts/orchestrate_multiagent_kernel.py \
  "Multiagent: verify 3 pricing claims on cometweb.io/pricing, then Council GO/NO-GO on Growth tier copy" \
  --json --workspace-root "$(pwd)/../.."
```

Expected archetype: `research_then_council` — 2 subagent tasks.

## 2. Step 1 — evidence-researcher (subagent)

Material claims (example):

1. Growth tier monthly price is stated in PLN and USD on `/pricing`.
2. Free plan CTA routes to register without billing query params.
3. Studio tier lists a concrete feature set distinct from Growth.

Subagent returns `EvidenceEnvelope` JSON. Validate:

```bash
python3 skills/skill-orchestrator-multiagent/scripts/validate_envelope.py \
  /tmp/step1-evidence.json --expect-type EvidenceEnvelope
```

## 3. Step 2 — ai-council (subagent)

Pass step 1 envelope in `prior_envelopes`. Decision question:

> Given verified pricing-page claims, GO/NO-GO/TEST/DEFER on shipping current Growth tier marketing copy?

Subagent returns `DecisionHandoff`. Validate:

```bash
python3 skills/skill-orchestrator-multiagent/scripts/validate_envelope.py \
  /tmp/step2-decision.json --expect-type DecisionHandoff
```

## 4. Parent merge

Emit **Workflow result** only — no second research pass, no verdict without step 2.

## Single-thread comparison

Same goal with `@skill-orchestrator` in a separate chat to compare handoff clarity.

## Hosts

| Host | Install | Multiagent |
| --- | --- | --- |
| Cursor | `./scripts/install-cursor.sh` | Task tool |
| Claude Code | `./scripts/install-claude.sh` | manual separate sessions + envelope paste |
| Codex | `./scripts/install-codex.sh` | manual separate sessions + envelope paste |
