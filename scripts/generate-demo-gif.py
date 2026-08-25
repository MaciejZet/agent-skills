#!/usr/bin/env python3
"""Generate a light, simple CometWeb Web App Auditor demo GIF."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path

import cairosvg
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "demo"
ASSETS = OUT / "assets"

W, H = 800, 450
MARGIN = 56
HEADER_H = 52
GAP = 28

BG = (15, 15, 15)
BG2 = (26, 26, 26)
CARD = (31, 31, 35)
MINT = (5, 242, 155)
TRUST = (4, 194, 124)
DEPTH = (3, 76, 50)
TEXT = (255, 255, 255)
TEXT2 = (209, 213, 219)
MUTED = (156, 163, 175)
BORDER = (45, 45, 45)
ERROR = (239, 68, 68)

CONTENT_W = W - 2 * MARGIN
CONTENT_TOP = HEADER_H + GAP
CONTENT_BOTTOM = H - MARGIN


def load_fonts() -> dict[str, ImageFont.FreeTypeFont | ImageFont.ImageFont]:
    bold = ASSETS / "nunito-sans-700.ttf"
    regular = ASSETS / "nunito-sans-regular.ttf"
    fb, fbb = "/System/Library/Fonts/Supplemental/Arial.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

    def ft(path: Path, size: int, fallback: str) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
        try:
            return ImageFont.truetype(str(path if path.exists() else fallback), size)
        except OSError:
            return ImageFont.load_default()

    return {
        "display": ft(bold, 34, fbb),
        "title": ft(bold, 24, fbb),
        "section": ft(bold, 18, fbb),
        "body": ft(regular, 15, fb),
        "small": ft(regular, 13, fb),
        "mono": ft(regular, 14, fb),
    }


def load_logo(size: int = 72) -> Image.Image:
    png = cairosvg.svg2png(url=str(ASSETS / "cometweb-logo.svg"), output_width=size)
    return Image.open(BytesIO(png)).convert("RGBA")


def canvas() -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGB", (W, H), BG)
    return img, ImageDraw.Draw(img)


def rounded_rect(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    radius: int,
    fill: tuple[int, int, int],
    outline: tuple[int, int, int] | None = None,
    width: int = 1,
) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def text_center(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    text: str,
    font: ImageFont.ImageFont,
    fill: tuple[int, int, int],
) -> None:
    x0, y0, x1, y1 = box
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((x0 + (x1 - x0 - tw) // 2, y0 + (y1 - y0 - th) // 2), text, fill=fill, font=font)


def wordmark_centered(draw: ImageDraw.ImageDraw, y: int, font: ImageFont.ImageFont) -> None:
    comet_w = draw.textlength("Comet", font=font)
    web_w = draw.textlength("Web", font=font)
    x = (W - comet_w - web_w) // 2
    draw.text((x, y), "Comet", fill=TEXT, font=font)
    draw.text((x + comet_w, y), "Web", fill=MINT, font=font)


def header(img: Image.Image, draw: ImageDraw.ImageDraw, fonts: dict, right: str) -> None:
    draw.rectangle((0, 0, W, HEADER_H), fill=BG2)
    draw.line([(0, HEADER_H), (W, HEADER_H)], fill=BORDER, width=1)
    logo = load_logo(30)
    img.paste(logo, (MARGIN, 11), logo)
    draw.text((MARGIN + 40, 14), "Comet", fill=TEXT, font=fonts["section"])
    cw = draw.textlength("Comet", font=fonts["section"])
    draw.text((MARGIN + 40 + cw, 14), "Web", fill=MINT, font=fonts["section"])
    draw.text((W - MARGIN, 16), right, fill=MINT, font=fonts["section"], anchor="ra")


def frame_hero(fonts: dict) -> Image.Image:
    img, draw = canvas()

    logo = load_logo(96)
    img.paste(logo, (W // 2 - 48, 72), logo)
    wordmark_centered(draw, 188, fonts["display"])

    draw.text((W // 2, 236), "Web App Auditor", fill=TEXT2, font=fonts["title"], anchor="mm")
    draw.text((W // 2, 278), "Evidence-driven QA for Cursor", fill=MUTED, font=fonts["body"], anchor="mm")

    pill = (MARGIN + 80, 320, W - MARGIN - 80, 360)
    rounded_rect(draw, pill, 16, CARD, outline=TRUST, width=2)
    text_center(draw, pill, "12 skills · protocol v1.1 · pytest + CI", fonts["small"], MINT)

    draw.text((W // 2, CONTENT_BOTTOM - 8), "github.com/MaciejZet/agent-skills", fill=MUTED, font=fonts["small"], anchor="mm")
    return img


def frame_flow(fonts: dict) -> Image.Image:
    img, draw = canvas()
    header(img, draw, fonts, "How it works")

    steps = [("Scope", "URL + mode"), ("Audit", "click + observe"), ("Report", "JSON v1.1")]
    gap = 36
    box_w = (CONTENT_W - gap * (len(steps) - 1)) // len(steps)
    box_h = 120
    y = CONTENT_TOP + 40

    for i, (title, sub) in enumerate(steps):
        x = MARGIN + i * (box_w + gap)
        accent = i == 0 or i == len(steps) - 1
        rounded_rect(draw, (x, y, x + box_w, y + box_h), 14, CARD, outline=MINT if accent else BORDER, width=2 if accent else 1)
        text_center(draw, (x, y + 24, x + box_w, y + 68), title, fonts["title"], TEXT)
        text_center(draw, (x, y + 68, x + box_w, y + box_h - 20), sub, fonts["small"], MUTED)
        if i < len(steps) - 1:
            ax = x + box_w + 8
            bx = x + box_w + gap - 8
            mid = y + box_h // 2
            draw.line([(ax, mid), (bx - 10, mid)], fill=TRUST, width=2)
            draw.polygon([(bx, mid), (bx - 9, mid - 5), (bx - 9, mid + 5)], fill=TRUST)

    note = (MARGIN, y + box_h + GAP + 24, W - MARGIN, y + box_h + GAP + 88)
    rounded_rect(draw, note, 14, CARD, outline=BORDER)
    text_center(draw, note, "validate_report.py - deterministic PASS / FAIL", fonts["mono"], TEXT2)
    return img


def frame_finding(fonts: dict) -> Image.Image:
    img, draw = canvas()
    header(img, draw, fonts, "Sample finding")

    card = (MARGIN, CONTENT_TOP + 24, W - MARGIN, CONTENT_BOTTOM - 24)
    rounded_rect(draw, card, 16, CARD, outline=ERROR, width=2)

    badge = (MARGIN + 32, CONTENT_TOP + 48, MARGIN + 120, CONTENT_TOP + 80)
    rounded_rect(draw, badge, 8, ERROR)
    text_center(draw, badge, "MAJOR", fonts["section"], TEXT)

    draw.text((MARGIN + 144, CONTENT_TOP + 52), "Invoice count mismatch", fill=TEXT, font=fonts["title"])

    body_y = CONTENT_TOP + 100
    for line in (
        "Badge shows 4 invoices. Table lists 3 rows.",
        "Cross-check failed - reproducible with screenshot + DOM.",
    ):
        draw.text((MARGIN + 32, body_y), line, fill=TEXT2, font=fonts["body"])
        body_y += 32

    proof = (MARGIN + 32, body_y + 24, W - MARGIN - 32, body_y + 88)
    rounded_rect(draw, proof, 12, BG2, outline=TRUST, width=2)
    text_center(draw, proof, "badge_count=4   table_rows=3   confidence=HIGH", fonts["mono"], MINT)
    return img


def frame_install(fonts: dict) -> Image.Image:
    img, draw = canvas()

    logo = load_logo(72)
    img.paste(logo, (W // 2 - 36, 80), logo)
    wordmark_centered(draw, 168, fonts["title"])

    draw.text((W // 2, 220), "Install in Cursor", fill=TEXT2, font=fonts["section"], anchor="mm")

    cmd = (MARGIN + 48, 260, W - MARGIN - 48, 312)
    rounded_rect(draw, cmd, 14, CARD, outline=MINT, width=2)
    text_center(draw, cmd, "./scripts/install-cursor.sh", fonts["mono"], MINT)

    draw.text((W // 2, 352), "Web App Auditor + 11 more skills", fill=MUTED, font=fonts["body"], anchor="mm")
    draw.text((W // 2, CONTENT_BOTTOM - 8), "CometWeb Labs · cometweb.io", fill=MUTED, font=fonts["small"], anchor="mm")
    return img


def build_frames(fonts: dict) -> list[Image.Image]:
    return [frame_hero(fonts), frame_flow(fonts), frame_finding(fonts), frame_install(fonts)]


def save_gif(frames: list[Image.Image], path: Path) -> None:
    paletted = [frame.quantize(colors=48, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE) for frame in frames]
    paletted[0].save(
        path,
        save_all=True,
        append_images=paletted[1:],
        duration=2800,
        loop=0,
        optimize=True,
    )


def ensure_assets() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    fonts_dir = ROOT.parent / "cometweb-io" / "static" / "fonts"
    for name in ("nunito-sans-regular.ttf", "nunito-sans-700.ttf"):
        src, dst = fonts_dir / name, ASSETS / name
        if src.exists() and not dst.exists():
            dst.write_bytes(src.read_bytes())
    logo_src = ROOT.parent / "cometweb-io" / "static" / "logo.svg"
    logo_dst = ASSETS / "cometweb-logo.svg"
    if logo_src.exists() and not logo_dst.exists():
        logo_dst.write_bytes(logo_src.read_bytes())


def main() -> None:
    ensure_assets()
    OUT.mkdir(parents=True, exist_ok=True)
    fonts = load_fonts()
    frames = build_frames(fonts)
    gif_path = OUT / "web-app-auditor-demo.gif"
    save_gif(frames, gif_path)
    print(f"Wrote {gif_path} ({gif_path.stat().st_size} bytes, {len(frames)} frames, {W}x{H})")


if __name__ == "__main__":
    main()
