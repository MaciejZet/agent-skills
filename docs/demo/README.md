# Web App Auditor — demo artifacts

Public demo for GitHub README and social posts (no GTM strategy here).

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
