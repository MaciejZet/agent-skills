## Agent scope

Public OSS repo: `MaciejZet/agent-skills`. Skill product + engineering only.

## Do not commit here

- GTM / promotion playbooks, outreach step plans, Council GTM memos
- Founder-brand strategy, sales sequences, private metrics targets
- Anything that reads like internal ops or “how to get stars”

**Canonical private location:** `personal/gtm-cometweb/cometweb/agent-skills/` (centrum path; repo `MaciejZet/gtm-cometweb`).

## Allowed in public repo

- `SKILL.md`, kernels, tests, routing evals, CW-AIP protocol
- `CONTRIBUTING.md`, `INSTALL.md`, technical `docs/` (demo, protocol pointers)
- User-facing README install/release instructions (no campaign strategy)

CI runs `scripts/public-safety-check.sh`, which fails if GTM-style docs reappear.
