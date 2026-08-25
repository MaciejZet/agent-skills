# Web App Auditor — demo artifacts

Public demo for GitHub README and social posts (no GTM strategy here).

| File | Description |
| --- | --- |
| [sample-audit-report.json](./sample-audit-report.json) | Valid v1.1 audit report fixture |
| [web-app-auditor-demo.gif](./web-app-auditor-demo.gif) | Animated walkthrough of scope → finding → validator |

Validate the JSON locally:

```bash
python skills/web-app-auditor/scripts/validate_report.py docs/demo/sample-audit-report.json
```

Regenerate GIF after copy changes:

```bash
source .venv/bin/activate && pip install pillow
python scripts/generate-demo-gif.py
```

Note: the GIF illustrates the **audit protocol output**, not a screen recording of Cursor IDE.
