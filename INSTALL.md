# Install CometWeb Agent Skills

Twelve standalone skills for **Cursor**, **ChatGPT**, **Codex**, and compatible hosts.

## Quick install (Cursor)

```bash
git clone https://github.com/MaciejZet/agent-skills.git
cd agent-skills
./scripts/install-cursor.sh
```

This symlinks all skills to `~/.cursor/skills/` and installs the routing rule at
`~/.cursor/rules/cometweb-agent-skills.mdc`.

Restart Cursor (or open a new chat) and invoke e.g. `@web-app-auditor`.

## CometWeb centrum (Claude Code)

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
