# Web App Auditor — demo artifacts

Public demo for GitHub README and social posts (no GTM strategy here).

> **Rule:** everything in this directory ends up on the public internet. Demo
> artifacts must be generated from fixtures or public data — never from a dump of
> a live workspace. On 2026-08-26 eight `linear-*` files were committed here
> containing 40 real Linear issues with working `linear.app` URLs and an absolute
> path from a developer machine. They were removed from `HEAD` on 2026-08-28 and
> `scripts/public-safety-check.sh` was rewritten to catch that class of file, but
> they remain in git history until it is rewritten. Treat anything published here
> before that date as disclosed.

| File | Description |
| --- | --- |
| [sample-audit-report.json](./sample-audit-report.json) | Valid v1.1 audit report fixture |
| [web-app-auditor-demo.gif](./web-app-auditor-demo.gif) | 4-frame intro: hero, flow, sample finding, install (~40 KB) |

Validate the JSON locally:

```bash
python skills/web-app-auditor/scripts/validate_report.py docs/demo/sample-audit-report.json
```

Regenerate GIF after copy changes:

```bash
source .venv/bin/activate
pip install pillow cairosvg
python scripts/generate-demo-gif.py
```

Branding assets live in [`assets/`](./assets/) (CometWeb logo SVG, Nunito Sans). Colors match `platforms/cometweb-io` tokens (`--cw-energy-mint`, `--cw-depth-green`, etc.).

Note: the GIF illustrates the **audit protocol and CometWeb brand**, not a screen recording of Cursor IDE.
