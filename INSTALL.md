# Install CometWeb Agent Skills

Fourteen standalone skills for **Cursor**, **Claude Code**, **ChatGPT**, **Codex**, and compatible hosts, including **Skill Orchestrator** (single thread) and **Skill Orchestrator Multiagent** (Task per step).

## Quick install (Claude Code plugin marketplace)

The shortest path — nothing to clone, and `/plugin update` keeps it current:

```text
/plugin marketplace add MaciejZet/agent-skills
/plugin install cometweb-agent-skills@cometweb-agent-skills
```

Restart Claude Code or start a new session. Prefer a symlinked clone if you intend to
edit the skills locally — see below.

## Quick install (Cursor)

```bash
git clone https://github.com/MaciejZet/agent-skills.git
cd agent-skills
./scripts/install-cursor.sh
```

This symlinks all skills to `~/.cursor/skills/` and installs the routing rule at
`~/.cursor/rules/cometweb-agent-skills.mdc`.

Restart Cursor (or open a new chat) and invoke e.g. `@web-app-auditor`.

## Quick install (Claude Code)

```bash
git clone https://github.com/MaciejZet/agent-skills.git
cd agent-skills
./scripts/install-claude.sh
```

Symlinks all skills to `~/.claude/skills/`. Restart Claude Code or start a new session, then invoke the skill by name.

## Quick install (Codex)

```bash
git clone https://github.com/MaciejZet/agent-skills.git
cd agent-skills
./scripts/install-codex.sh
```

Symlinks all skills to `~/.codex/skills/`. Existing CometWeb skill **directories** there are replaced with symlinks to the repo. Restart Codex or start a new session.

## Optional design stack: Impeccable + frontend-design + UI UX Pro Max

To install this repository together with the external frontend/design skills used alongside it:

```bash
# Codex
bash scripts/install-design-stack.sh codex

# Claude Code
bash scripts/install-design-stack.sh claude

# Cursor
bash scripts/install-design-stack.sh cursor
```

For project-aware setup (Impeccable project hooks + UI UX Pro Max initialization):

```bash
bash scripts/install-design-stack.sh codex --project /path/to/project
```

The external projects stay upstream rather than being vendored into this repository. See [`docs/design-skill-stack.md`](docs/design-skill-stack.md) for routing, overlap and update behavior.

## CometWeb centrum (Claude relative paths)

```bash
git clone https://github.com/MaciejZet/agent-skills.git
cd agent-skills
./scripts/install-claude-centrum.sh   # CometWeb/.claude/skills
```

## Single skill

```bash
ln -s "$(pwd)/skills/web-app-auditor" ~/.cursor/skills/web-app-auditor
```

Each skill folder contains its own [`INSTALL.md`](skills/web-app-auditor/INSTALL.md) with host-specific notes.

## Download ZIP (no git)

Releases ship per-skill ZIPs plus a full bundle:
https://github.com/MaciejZet/agent-skills/releases/latest

Unpack, then run `./scripts/install-cursor.sh` from the bundle root.

## Start with Web App Auditor

Recommended first skill — evidence-driven click-through QA:

```text
@web-app-auditor Audit cometweb.io/pricing — area mode, standard depth.
```

Demo: [`docs/demo/web-app-auditor-demo.gif`](docs/demo/web-app-auditor-demo.gif) ·
sample report: [`docs/demo/sample-audit-report.json`](docs/demo/sample-audit-report.json)

## Optional: AI Council Notion bindings

```bash
mkdir -p ~/.config/cometweb
cp skills/ai-council/references/notion-bindings.example.json \
   ~/.config/cometweb/ai-council-notion.json
chmod 600 ~/.config/cometweb/ai-council-notion.json
```

See [`skills/ai-council/references/notion-memory.md`](skills/ai-council/references/notion-memory.md).

## Verify install

```bash
./scripts/run_all_checks.sh
ls ~/.cursor/skills/ | grep -E 'web-app-auditor|product-operator|ai-council'
```

Questions: [GitHub Discussions](https://github.com/MaciejZet/agent-skills/discussions).