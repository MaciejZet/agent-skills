# Design Skill Stack

This repository can be used as the entry point for a four-part design stack:

1. **MaciejZet/agent-skills** — product, research, audit, release and orchestration skills.
2. **Impeccable** — primary frontend design execution workflow: shape, craft, critique, audit, polish, harden and related commands.
3. **Anthropic frontend-design** — lightweight aesthetic direction for distinctive frontend work.
4. **UI UX Pro Max** — design-system and recommendation engine with styles, palettes, typography, UX guidance and stack-specific references.

The external projects remain upstream dependencies. Their contents are not copied into this repository, which avoids stale forks and makes updates explicit.

## Recommended routing

Do not treat all three external design systems as equal instructions on every task. They overlap.

Use this order:

- **Implementation or redesign:** Impeccable first.
- **Fast visual direction or a small component:** Anthropic `frontend-design` is sufficient.
- **Choosing a design system, visual family, palette, typography, chart type or framework-specific UI guidance:** UI UX Pro Max first, then implement through Impeccable.
- **Product/UX audit, release readiness, evidence gathering, prioritization or multi-agent work:** use the relevant skill from `MaciejZet/agent-skills`; bring in Impeccable only for the visual/UI part.

For a large frontend task, a useful sequence is:

```text
product context -> UI UX Pro Max recommendation -> Impeccable shape/craft -> frontend-design sanity check -> Impeccable audit/polish -> release-readiness
```

`frontend-design` and Impeccable share some ancestry and aesthetic principles, so invoking both continuously usually adds noise rather than quality.

## One-command bootstrap

From a clone of this repository:

```bash
# Global-capable stack for Codex
bash scripts/install-design-stack.sh codex

# Same for Claude Code
bash scripts/install-design-stack.sh claude

# Same for Cursor
bash scripts/install-design-stack.sh cursor
```

The command installs:

- this repository's skills using the existing provider installer;
- Anthropic `frontend-design` from a sparse checkout of its official repository;
- Impeccable using its official installer;
- the UI UX Pro Max CLI.

UI UX Pro Max is initialized per project. To also configure the project-aware parts of the stack:

```bash
bash scripts/install-design-stack.sh codex --project /path/to/project
```

With `--project`, Impeccable is installed project-locally (including native project hooks where supported) and `uipro init --ai <provider>` is run in that project.

## Updating

Re-run the same command. The Anthropic sparse checkout is fast-forwarded to current `main`, Impeccable runs through its official installer, and the local CometWeb skills remain symlinked to this repository.

UI UX Pro Max CLI updates are intentionally not forced on every run. Update it explicitly when needed:

```bash
npm install -g ui-ux-pro-max-cli@latest
```

For reproducible CI or team environments, pin external versions/commits instead of following mutable upstream branches.

## Codex hook trust

After a project-scoped Impeccable install or update, Codex may require approval for the project hook. Open `/hooks` in Codex and approve the Impeccable hook when prompted.

## Upstreams

- Impeccable: https://github.com/pbakaus/impeccable
- Anthropic frontend-design: https://github.com/anthropics/claude-plugins-official/tree/main/plugins/frontend-design
- UI UX Pro Max: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
- CometWeb agent skills: https://github.com/MaciejZet/agent-skills
