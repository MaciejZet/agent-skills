---
name: skill-orchestrator-multiagent
description: Run multi-skill CometWeb workflows with one isolated subagent per specialist skill when the user wants enforced separation instead of single-thread orchestration. Use when the user asks for multiagent orchestration, separate agents per skill, Task/subagent per step, isolated skill runs, or strict boundaries between Evidence Researcher, AI Council, auditors, and other skills in one workflow. Builds CW-AIP handoff payloads and launches a dedicated subagent per step; parent thread plans and merges only. Do not use when a single specialist skill suffices, when the host has no subagent/Task API (use skill-orchestrator instead), for routing-only questions, or to bypass AI Council or Release Readiness policy.
---

# Skill Orchestrator — Multiagent

**Multiagent** variant of Skill Orchestrator. Same workflow **plan**; different
**execution model**: one isolated subagent (Cursor Task / cloud agent / equivalent)
per specialist skill.

Compare with `skill-orchestrator` (single-thread): same CW-AIP envelopes, but this
skill **forbids** running domain steps in the parent thread.

Read `references/multiagent-execution.md`, `references/subagent-prompt-template.md`,
and `references/workflow-archetypes.md`.

## Boundaries

**Parent orchestrator owns:**

- archetype / step plan (`orchestrate_kernel.py`),
- subagent task payloads (`orchestrate_multiagent_kernel.py`),
- launching and awaiting each subagent sequentially,
- envelope validation and workflow result merge.

**Parent must not:**

- execute Evidence Researcher, Council, audit, or release work inline,
- collapse two steps into one model pass,
- skip subagent launch when Task API is available.

**Each subagent owns:** one skill's full `SKILL.md` contract and one CW-AIP envelope.

## Workflow

### 1. Plan (parent)

```bash
python3 scripts/orchestrate_multiagent_kernel.py "<user goal>" --json --workspace-root "<abs workspace>"
```

Present plan + subagent count before launching step 1.

### 2. Confirm scope

Same as `skill-orchestrator`:

- Council in plan but no decision in goal → ask once.
- Release Readiness without pinned RC → stop and request pin.

### 3. Execute — one subagent per step

For each `subagent_tasks[]` entry:

1. Announce: `Launching subagent step i/N: <skill>`.
2. Call host subagent API (Cursor **Task** tool) with `subagent_type`, `description`, `prompt`.
3. Set `run_in_background: false` unless user requested parallel independent steps.
4. Parse subagent return → CW-AIP envelope; validate type matches plan.
5. Append envelope to `prior_envelopes` for the next task payload (re-build prompt or pass in Task prompt manually).

**Do not** re-run the specialist workflow in the parent thread after the subagent returns.

If Task/subagent API is **unavailable** → stop and recommend `@skill-orchestrator` or
separate chats. See `references/multiagent-execution.md`.

### 4. Close (parent)

Emit **Workflow result**:

- `execution_mode: multiagent`,
- subagent ID or turn reference per step (when host provides it),
- envelope IDs / types per step,
- Council verdict only if ai-council subagent ran,
- explicit note if any step used fallback (should be none when this skill is used correctly).

## Example invocations

```text
@skill-orchestrator-multiagent — Multiagent: verify EU AI Act claims, then Council on
landing page copy.
```

```text
@skill-orchestrator-multiagent — Separate agent per skill: audit register, then
release readiness RC 1.2.0 build 4910 staging.
```

## Output contract

1. **Workflow plan** — archetype + steps + subagent count
2. **Subagent log** — one line per launched subagent with status
3. **Step envelopes** — pointer or inline JSON per step
4. **Workflow result** — parent merge only; no domain re-execution

## Relation to skill-orchestrator

| | skill-orchestrator | skill-orchestrator-multiagent |
| --- | --- | --- |
| Plan | shared kernel | shared kernel |
| Execution | same thread, sequential SKILL.md | one subagent per step |
| Enforcement | procedural | structural (when Task available) |
| Host requirement | any | subagent / Task API |
