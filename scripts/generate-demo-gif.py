#!/usr/bin/env python3
"""Generate docs/demo/web-app-auditor-demo.gif for README and social posts."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "demo"
W, H = 960, 540
BG = (15, 23, 42)
ACCENT = (56, 189, 248)
TEXT = (241, 245, 249)
MUTED = (148, 163, 184)

FRAMES = [
    ("Web App Auditor", "Evidence-driven QA for Cursor & ChatGPT"),
    ("Scope", "Target: cometweb.io/pricing · mode: area · depth: standard"),
    ("Finding F-001 · MAJOR", "Invoice badge shows 4 while table lists 3 invoices"),
    ("Evidence E-001", "Screenshot + arithmetic cross-check · confidence: high"),
    ("Validator", "python scripts/validate_report.py → VALID (protocol v1.1)"),
    ("Install", "github.com/MaciejZet/agent-skills · ./scripts/install-cursor.sh"),
]


def load_fonts() -> tuple[ImageFont.FreeTypeFont | ImageFont.ImageFont, ...]:
    try:
        return (
            ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 42),
            ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 26),
            ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 20),
        )
    except OSError:
        default = ImageFont.load_default()
        return default, default, default


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    title_font, body_font, small_font = load_fonts()
    images: list[Image.Image] = []

    for i, (title, body) in enumerate(FRAMES):
        img = Image.new("RGB", (W, H), BG)
        draw = ImageDraw.Draw(img)
        draw.rounded_rectangle((40, 40, W - 40, H - 40), radius=16, outline=ACCENT, width=2)
        draw.text((80, 100), title, fill=ACCENT, font=title_font)
        draw.text((80, 200), body, fill=TEXT, font=body_font)
        draw.text(
            (80, H - 80),
            f"CometWeb Labs · frame {i + 1}/{len(FRAMES)}",
            fill=MUTED,
            font=small_font,
        )
        images.append(img)

    gif_path = OUT / "web-app-auditor-demo.gif"
    images[0].save(
        gif_path,
        save_all=True,
        append_images=images[1:],
        duration=1800,
        loop=0,
        optimize=True,
    )
    print(f"Wrote {gif_path} ({gif_path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
