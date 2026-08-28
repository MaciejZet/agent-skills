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

CI runs `scripts/public-safety-check.sh`, which fails if private material reaches the
public tree. It scans **file contents and file names, every file type, the whole repo** —
secrets, Linear issue IDs and workspace URLs, Notion hub IDs, private vault paths and
absolute paths from a developer machine. Run `./scripts/public-safety-check.sh --history`
before a release: it applies the same rules to every commit ever made. History mode is
deliberately not in CI, because history only becomes clean after a `git filter-repo`
rewrite — until then it reports the known 2026-08-26 incident (see `docs/demo/README.md`).

Two rules that are not obvious:
- Demo artifacts are a leak surface. Anything under `docs/demo/` must be generated from
  fixtures or public data, never from a live workspace dump.
- The gate is fail-closed. It uses `grep`, not `rg`; the previous version wrapped `rg`
  in an `if`, so a runner without ripgrep made every check pass silently.
