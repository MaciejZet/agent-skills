# Changelog

All notable changes to the **CometWeb Agent Skills** bundle (public repo).

Format follows [Keep a Changelog](https://keepachangelog.com/). Version tags: `vMAJOR.MINOR.PATCH`.

## [1.0.2] - 2026-08-26

### Added

- [`scripts/install-claude.sh`](scripts/install-claude.sh) — symlink all skills to `~/.claude/skills/` (Claude Code)

### Changed

- README: architecture diagram, evidence flow, per-skill roles, routing collision guide (roadmap-aligned)
- INSTALL, demo GIF, and skill INSTALL docs list Claude Code alongside Cursor and ChatGPT

## [1.0.1] - 2026-08-26

### Added

- Branded README demo GIF (`docs/demo/web-app-auditor-demo.gif`, 4 frames, ~42 KB)
- Root [`INSTALL.md`](INSTALL.md) and GitHub issue / PR templates
- Welcome thread in GitHub Discussions
- Release bundle includes `scripts/`, `INSTALL.md`, and demo artifacts

### Changed

- README landing: demo GIF, release badge, install quick path
- Demo generator: CometWeb colors, simplified layout, lighter GIF weight

## [1.0.0] - 2026-08-25

### Added

- Twelve public skills with deterministic kernels and CI
- CW-AIP v1 interchange protocol and JSON schemas
- Routing eval suite (66 cases), `validate_skills.py`, install scripts
- GitHub Actions CI: safety check, validation, routing evals, pytest
- GitHub Release v1.0.0 with per-skill and bundle ZIPs

[1.0.2]: https://github.com/MaciejZet/agent-skills/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/MaciejZet/agent-skills/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/MaciejZet/agent-skills/releases/tag/v1.0.0
