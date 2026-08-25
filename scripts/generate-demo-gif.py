#!/usr/bin/env python3
"""Generate branded CometWeb Web App Auditor demo GIF."""

from __future__ import annotations

import math
from io import BytesIO
from pathlib import Path

import cairosvg
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "demo"
ASSETS = OUT / "assets"

W, H = 960, 540

# CometWeb tokens — platforms/cometweb-io/src/lib/styles/tokens.css
NIGHT = (24, 24, 27)
MINT = (5, 242, 155)
TRUST = (4, 194, 124)
DEPTH = (3, 76, 50)
BG = (15, 15, 15)
BG2 = (26, 26, 26)
CARD = (31, 31, 35)
CARD_HOVER = (49, 49, 58)
TEXT = (255, 255, 255)
TEXT2 = (209, 213, 219)
MUTED = (156, 163, 175)
BORDER = (45, 45, 45)
WARNING = (245, 158, 11)
ERROR = (239, 68, 68)


def hex_rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def lerp(a: int, b: int, t: float) -> int:
    return int(a + (b - a) * t)


def blend(c1: tuple[int, int, int], c2: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    return (lerp(c1[0], c2[0], t), lerp(c1[1], c2[1], t), lerp(c1[2], c2[2], t))


def load_fonts() -> dict[str, ImageFont.FreeTypeFont | ImageFont.ImageFont]:
    regular = ASSETS / "nunito-sans-regular.ttf"
    semibold = ASSETS / "nunito-sans-600.ttf"
    bold = ASSETS / "nunito-sans-700.ttf"
    fallback = "/System/Library/Fonts/Supplemental/Arial.ttf"
    fallback_b = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

    def ft(path: Path, size: int, fb: str) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
        try:
            return ImageFont.truetype(str(path if path.exists() else fb), size)
        except OSError:
            return ImageFont.load_default()

    if not regular.exists():
        for src, dst in [
            (
                ROOT.parent / "cometweb-io" / "static" / "fonts" / "nunito-sans-regular.ttf",
                regular,
            ),
            (
                ROOT.parent / "cometweb-io" / "static" / "fonts" / "nunito-sans-600.ttf",
                semibold,
            ),
        ]:
            if src.exists():
                ASSETS.mkdir(parents=True, exist_ok=True)
                dst.write_bytes(src.read_bytes())

    return {
        "hero": ft(bold, 46, fallback_b),
        "title": ft(bold, 32, fallback_b),
        "subtitle": ft(semibold, 22, fallback_b),
        "body": ft(regular if regular.exists() else Path(fallback), 18, fallback),
        "small": ft(regular if regular.exists() else Path(fallback), 14, fallback),
        "mono": ft(regular if regular.exists() else Path(fallback), 15, fallback),
        "badge": ft(bold, 12, fallback_b),
        "label": ft(semibold, 11, fallback_b),
    }


def load_logo(size: int = 72) -> Image.Image:
    svg = ASSETS / "cometweb-logo.svg"
    if not svg.exists():
        alt = ROOT.parent / "cometweb-io" / "static" / "logo.svg"
        if alt.exists():
            ASSETS.mkdir(parents=True, exist_ok=True)
            svg.write_bytes(alt.read_bytes())
    png = cairosvg.svg2png(url=str(svg), output_width=size)
    return Image.open(BytesIO(png)).convert("RGBA")


def gradient_bg(top: tuple[int, int, int], bottom: tuple[int, int, int], glow: tuple[int, int, int] | None = None) -> Image.Image:
    img = Image.new("RGB", (W, H), top)
    draw = ImageDraw.Draw(img)
    for y in range(H):
        t = y / max(H - 1, 1)
        draw.line([(0, y), (W, y)], fill=blend(top, bottom, t))
    if glow:
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        od.ellipse((W // 2 - 280, -120, W // 2 + 280, 320), fill=(*glow, 38))
        od.ellipse((120, H - 200, 420, H + 80), fill=(*TRUST, 22))
        img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    return img


def draw_wordmark(draw: ImageDraw.ImageDraw, x: int, y: int, fonts: dict, size: str = "subtitle") -> None:
    f = fonts[size]
    draw.text((x, y), "Comet", fill=TEXT, font=f)
    w = draw.textlength("Comet", font=f)
    draw.text((x + w, y), "Web", fill=MINT, font=f)


def header_bar(base: Image.Image, fonts: dict, title: str, subtitle: str = "") -> Image.Image:
    img = base.copy()
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, W, 72), fill=(*BG2, 255))
    draw.line([(0, 72), (W, 72)], fill=BORDER, width=1)

    logo = load_logo(44)
    img.paste(logo, (24, 14), logo)
    draw_wordmark(draw, 78, 18, fonts, "subtitle")

    draw.text((W - 24, 22), title, fill=MINT, font=fonts["subtitle"], anchor="ra")
    if subtitle:
        draw.text((W - 24, 48), subtitle, fill=MUTED, font=fonts["small"], anchor="ra")
    return img


def rounded_rect(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    radius: int,
    fill: tuple[int, int, int],
    outline: tuple[int, int, int] | None = None,
    width: int = 1,
) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], color: tuple[int, int, int]) -> None:
    draw.line([start, end], fill=color, width=3)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    size = 10
    for da in (2.6, -2.6):
        ax = end[0] - size * math.cos(angle - da)
        ay = end[1] - size * math.sin(angle - da)
        draw.line([end, (ax, ay)], fill=color, width=3)


def frame_hero(fonts: dict) -> Image.Image:
    img = gradient_bg(DEPTH, BG, glow=MINT)
    draw = ImageDraw.Draw(img)

    logo = load_logo(140)
    img.paste(logo, (W // 2 - 70, 72), logo)
    draw_wordmark(draw, W // 2 - 95, 228, fonts, "hero")

    draw.text((W // 2, 292), "Web App Auditor", fill=TEXT, font=fonts["title"], anchor="mm")
    draw.text(
        (W // 2, 340),
        "Evidence-driven QA · protocol v1.1 · deterministic validator",
        fill=TEXT2,
        font=fonts["body"],
        anchor="mm",
    )

    pill = (W // 2 - 150, 390, W // 2 + 150, 430)
    rounded_rect(draw, pill, 20, CARD, outline=TRUST, width=2)
    draw.text((W // 2, 410), "12 Agent Skills · Cursor & ChatGPT", fill=MINT, font=fonts["small"], anchor="mm")

    draw.text((W // 2, H - 28), "github.com/MaciejZet/agent-skills", fill=MUTED, font=fonts["small"], anchor="mm")
    return img


def frame_pipeline(fonts: dict) -> Image.Image:
    img = header_bar(gradient_bg(BG, NIGHT), fonts, "Audit pipeline", "Deterministic kernel")
    draw = ImageDraw.Draw(img)

    steps = [
        ("Scope", "URL + mode"),
        ("Navigate", "Click path"),
        ("Observe", "DOM + UI"),
        ("Finding", "Severity"),
        ("Report", "JSON v1.1"),
    ]
    x0, y0 = 48, 130
    box_w, box_h, gap = 148, 88, 24
    for i, (title, sub) in enumerate(steps):
        x = x0 + i * (box_w + gap)
        y = y0 + 40
        accent = MINT if i == 0 else TRUST if i == len(steps) - 1 else CARD_HOVER
        rounded_rect(draw, (x, y, x + box_w, y + box_h), 14, CARD, outline=accent, width=2)
        draw.text((x + box_w // 2, y + 28), title, fill=TEXT, font=fonts["subtitle"], anchor="mm")
        draw.text((x + box_w // 2, y + 58), sub, fill=MUTED, font=fonts["small"], anchor="mm")
        if i < len(steps) - 1:
            arrow(draw, (x + box_w + 4, y + box_h // 2), (x + box_w + gap - 4, y + box_h // 2), MINT)

    # Loop-back quality gate
    rounded_rect(draw, (48, 380, W - 48, 470), 16, CARD, outline=BORDER)
    draw.text((72, 400), "Quality gate", fill=MINT, font=fonts["subtitle"])
    draw.text(
        (72, 432),
        "validate_report.py · schema + invariants · no LLM guesswork on PASS/FAIL",
        fill=TEXT2,
        font=fonts["body"],
    )
    draw.ellipse((W - 120, 396, W - 72, 444), outline=MINT, width=3)
    draw.text((W - 96, 420), "CI", fill=MINT, font=fonts["badge"], anchor="mm")
    return img


def frame_scope(fonts: dict) -> Image.Image:
    img = header_bar(gradient_bg(BG2, BG), fonts, "Scope", "cometweb.io/pricing")
    draw = ImageDraw.Draw(img)

    # Browser chrome
    browser = (60, 100, W - 60, 320)
    rounded_rect(draw, browser, 18, CARD, outline=BORDER, width=2)
    draw.rectangle((browser[0], browser[1], browser[2], browser[1] + 44), fill=BG2)
    for dx, color in [(82, ERROR), (104, WARNING), (126, TRUST)]:
        draw.ellipse((dx, 112, dx + 16, 128), fill=color)
    rounded_rect(draw, (150, 108, browser[2] - 24, 134), 8, BG, outline=BORDER)
    draw.text((162, 121), "https://cometweb.io/pricing", fill=MINT, font=fonts["small"])

    # Pricing mock blocks
    for i, label in enumerate(["Free", "Growth", "Studio", "Scale"]):
        bx = 90 + i * 195
        rounded_rect(draw, (bx, 170, bx + 165, 290), 12, BG2, outline=BORDER)
        draw.text((bx + 82, 195), label, fill=TEXT, font=fonts["subtitle"], anchor="mm")
        draw.text((bx + 82, 235), "PLN / USD", fill=MUTED, font=fonts["small"], anchor="mm")
        if i == 2:
            rounded_rect(draw, (bx + 40, 255, bx + 125, 278), 8, DEPTH, outline=MINT)
            draw.text((bx + 82, 266), "audit focus", fill=MINT, font=fonts["label"], anchor="mm")

    # Params panel
    rounded_rect(draw, (60, 350, 460, 500), 14, CARD, outline=TRUST, width=2)
    draw.text((84, 372), "Scope parameters", fill=MINT, font=fonts["subtitle"])
    params = [
        ("target", "cometweb.io/pricing"),
        ("mode", "area"),
        ("depth", "standard"),
        ("persona", "prospect · PLN billing"),
    ]
    for i, (k, v) in enumerate(params):
        y = 408 + i * 22
        draw.text((84, y), k, fill=MUTED, font=fonts["small"])
        draw.text((200, y), v, fill=TEXT2, font=fonts["small"])

    # Mini sitemap diagram
    rounded_rect(draw, (500, 350, W - 60, 500), 14, CARD, outline=BORDER)
    draw.text((524, 372), "Navigation map", fill=MINT, font=fonts["subtitle"])
    nodes = [("Home", 540, 420), ("Pricing", 660, 420), ("Register", 780, 420), ("Checkout", 660, 460)]
    for label, nx, ny in nodes:
        rounded_rect(draw, (nx, ny, nx + 90, ny + 36), 8, BG2, outline=TRUST if label == "Pricing" else BORDER)
        draw.text((nx + 45, ny + 18), label, fill=TEXT if label == "Pricing" else MUTED, font=fonts["label"], anchor="mm")
    arrow(draw, (630, 438), (660, 438), MINT)
    arrow(draw, (750, 438), (780, 438), MINT)
    arrow(draw, (705, 456), (705, 460), MINT)
    return img


def frame_finding(fonts: dict) -> Image.Image:
    img = header_bar(gradient_bg(BG, DEPTH), fonts, "Finding F-001", "MAJOR · billing UI")
    draw = ImageDraw.Draw(img)

    rounded_rect(draw, (60, 100, W - 60, 280), 18, CARD, outline=ERROR, width=2)
    draw.rounded_rectangle((84, 124, 170, 152), radius=8, fill=ERROR)
    draw.text((127, 138), "MAJOR", fill=TEXT, font=fonts["badge"], anchor="mm")
    draw.text((190, 130), "Invoice count mismatch on billing dashboard", fill=TEXT, font=fonts["subtitle"])
    draw.text(
        (84, 175),
        "Badge displays 4 open invoices while the table lists only 3 rows.\n"
        "User may overpay or miss a draft invoice — arithmetic cross-check failed.",
        fill=TEXT2,
        font=fonts["body"],
    )

    # Severity bar diagram
    draw.text((84, 230), "Impact", fill=MUTED, font=fonts["small"])
    for i, (label, color, w) in enumerate([("UX", MUTED, 80), ("Trust", WARNING, 140), ("Revenue", ERROR, 200)]):
        rounded_rect(draw, (150 + i * 210, 222, 150 + i * 210 + w, 246), 6, color)
        draw.text((150 + i * 210, 252), label, fill=MUTED, font=fonts["label"])

    # Finding lifecycle
    rounded_rect(draw, (60, 310, W - 60, 500), 16, CARD, outline=BORDER)
    draw.text((84, 332), "Finding lifecycle", fill=MINT, font=fonts["subtitle"])
    lifecycle = ["Detected", "Evidence", "Validated", "Handoff"]
    lx = 100
    for i, step in enumerate(lifecycle):
        cx = lx + i * 200
        cy = 400
        fill = MINT if i >= 2 else CARD_HOVER
        draw.ellipse((cx - 28, cy - 28, cx + 28, cy + 28), fill=fill, outline=MINT, width=2)
        draw.text((cx, cy), str(i + 1), fill=BG if i >= 2 else TEXT, font=fonts["subtitle"], anchor="mm")
        draw.text((cx, cy + 44), step, fill=TEXT2, font=fonts["small"], anchor="mm")
        if i < len(lifecycle) - 1:
            arrow(draw, (cx + 32, cy), (cx + 168, cy), TRUST)
    return img


def frame_evidence(fonts: dict) -> Image.Image:
    img = header_bar(gradient_bg(NIGHT, BG), fonts, "Evidence E-001", "confidence: HIGH")
    draw = ImageDraw.Draw(img)

    # Evidence chain diagram
    nodes = [
        ("Screenshot", "pricing · badge + table"),
        ("Extract", "OCR + DOM counts"),
        ("Cross-check", "4 ≠ 3 rows"),
        ("Verdict", "reproducible"),
    ]
    y = 130
    for i, (title, sub) in enumerate(nodes):
        x = 60 + i * 220
        rounded_rect(draw, (x, y, x + 190, y + 100), 14, CARD, outline=MINT if i == 3 else BORDER, width=2)
        draw.text((x + 95, y + 35), title, fill=MINT if i == 3 else TEXT, font=fonts["subtitle"], anchor="mm")
        draw.text((x + 95, y + 68), sub, fill=MUTED, font=fonts["small"], anchor="mm")
        if i < len(nodes) - 1:
            arrow(draw, (x + 192, y + 50), (x + 218, y + 50), TRUST)

    # Mock screenshot panel
    rounded_rect(draw, (60, 260, 420, 500), 14, CARD, outline=BORDER)
    draw.text((84, 282), "Captured state", fill=MINT, font=fonts["subtitle"])
    rounded_rect(draw, (84, 310, 396, 470), 10, BG2, outline=BORDER)
    draw.text((240, 340), "Invoices (4)", fill=ERROR, font=fonts["subtitle"], anchor="mm")
    for row, label in enumerate(["INV-1042", "INV-1043", "INV-1044"]):
        rounded_rect(draw, (100, 365 + row * 32, 380, 390 + row * 32), 6, CARD)
        draw.text((110, 377 + row * 32), label, fill=TEXT2, font=fonts["small"])
    draw.text((240, 455), "← only 3 rows visible", fill=WARNING, font=fonts["small"], anchor="mm")

    # Math diagram
    rounded_rect(draw, (450, 260, W - 60, 500), 14, CARD, outline=TRUST, width=2)
    draw.text((474, 282), "Arithmetic proof", fill=MINT, font=fonts["subtitle"])
    lines = [
        "badge_count  = 4",
        "table_rows   = 3",
        "delta        = 1  ⚠",
        "confidence   = HIGH",
        "source       = screenshot + DOM",
    ]
    for i, line in enumerate(lines):
        color = ERROR if "delta" in line else MINT if "HIGH" in line else TEXT2
        draw.text((474, 320 + i * 32), line, fill=color, font=fonts["mono"])
    return img


def frame_validator(fonts: dict) -> Image.Image:
    img = header_bar(gradient_bg(BG2, NIGHT), fonts, "Validator", "deterministic PASS/FAIL")
    draw = ImageDraw.Draw(img)

    # Flow: JSON → script → result
    rounded_rect(draw, (80, 140, 260, 260), 14, CARD, outline=BORDER)
    draw.text((170, 175), "audit-report.json", fill=TEXT, font=fonts["subtitle"], anchor="mm")
    draw.text((170, 210), "schema v1.1", fill=MUTED, font=fonts["small"], anchor="mm")
    draw.text((170, 235), "findings + evidence", fill=MUTED, font=fonts["small"], anchor="mm")

    arrow(draw, (268, 200), (320, 200), MINT)

    rounded_rect(draw, (328, 120, 632, 280), 14, BG, outline=MINT, width=2)
    draw.text((480, 150), "$ python validate_report.py", fill=MINT, font=fonts["mono"], anchor="mm")
    draw.text((480, 185), "✓ schema compliance", fill=TRUST, font=fonts["small"], anchor="mm")
    draw.text((480, 210), "✓ finding IDs unique", fill=TRUST, font=fonts["small"], anchor="mm")
    draw.text((480, 235), "✓ evidence linked", fill=TRUST, font=fonts["small"], anchor="mm")
    draw.text((480, 260), "✓ severity enum valid", fill=TRUST, font=fonts["small"], anchor="mm")

    arrow(draw, (640, 200), (692, 200), MINT)

    rounded_rect(draw, (700, 140, 880, 260), 14, DEPTH, outline=MINT, width=3)
    draw.text((790, 185), "VALID", fill=MINT, font=fonts["hero"], anchor="mm")
    draw.text((790, 230), "protocol v1.1", fill=TEXT2, font=fonts["small"], anchor="mm")

    # CI integration diagram
    rounded_rect(draw, (60, 320, W - 60, 500), 16, CARD, outline=BORDER)
    draw.text((84, 342), "CI · GitHub Actions", fill=MINT, font=fonts["subtitle"])
    ci_steps = ["validate_skills.py", "routing evals (66)", "pytest (327+)", "public-safety-check"]
    for i, step in enumerate(ci_steps):
        x = 84 + i * 210
        rounded_rect(draw, (x, 380, x + 190, 460), 12, BG2, outline=TRUST if i == 3 else BORDER)
        draw.text((x + 95, 420), step, fill=TEXT2, font=fonts["small"], anchor="mm")
        if i < len(ci_steps) - 1:
            arrow(draw, (x + 192, 420), (x + 208, 420), MINT)
    return img


def frame_install(fonts: dict) -> Image.Image:
    img = gradient_bg(DEPTH, BG, glow=TRUST)
    draw = ImageDraw.Draw(img)

    logo = load_logo(80)
    img.paste(logo, (W // 2 - 40, 48), logo)
    draw.text((W // 2, 140), "Install · 12 Agent Skills", fill=TEXT, font=fonts["title"], anchor="mm")

    # Skill constellation diagram
    skills = [
        "Evidence", "Competitive", "Teardown", "Design Partner",
        "Repo→Roadmap", "Product Op", "Customer Ops", "Web Auditor",
        "SEO/AEO", "Release", "AI Council", "Humanize",
    ]
    cx, cy, r = W // 2, 290, 150
    for i, name in enumerate(skills):
        angle = -math.pi / 2 + i * (2 * math.pi / len(skills))
        sx = int(cx + r * math.cos(angle))
        sy = int(cy + r * math.sin(angle))
        w = max(88, int(draw.textlength(name, font=fonts["label"])) + 20)
        rounded_rect(draw, (sx - w // 2, sy - 16, sx + w // 2, sy + 16), 10, CARD, outline=MINT if "Auditor" in name else BORDER)
        draw.text((sx, sy), name, fill=MINT if "Auditor" in name else TEXT2, font=fonts["label"], anchor="mm")
        draw.line([(cx, cy), (sx, sy)], fill=(*TRUST, 80), width=1)

    draw.ellipse((cx - 36, cy - 36, cx + 36, cy + 36), fill=DEPTH, outline=MINT, width=2)
    draw.text((cx, cy), "CW-AIP", fill=MINT, font=fonts["badge"], anchor="mm")

    cmd_box = (120, 430, W - 120, 490)
    rounded_rect(draw, cmd_box, 14, CARD, outline=MINT, width=2)
    draw.text(
        (W // 2, 460),
        "git clone …/agent-skills && ./scripts/install-cursor.sh",
        fill=MINT,
        font=fonts["mono"],
        anchor="mm",
    )
    draw.text((W // 2, H - 22), "CometWeb Labs · MIT · cometweb.io", fill=MUTED, font=fonts["small"], anchor="mm")
    return img


def build_frames(fonts: dict) -> list[Image.Image]:
    return [
        frame_hero(fonts),
        frame_pipeline(fonts),
        frame_scope(fonts),
        frame_finding(fonts),
        frame_evidence(fonts),
        frame_validator(fonts),
        frame_install(fonts),
    ]


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)

    fonts_dir = ROOT.parent / "cometweb-io" / "static" / "fonts"
    for name in ("nunito-sans-regular.ttf", "nunito-sans-600.ttf", "nunito-sans-700.ttf"):
        src = fonts_dir / name
        dst = ASSETS / name
        if src.exists() and not dst.exists():
            dst.write_bytes(src.read_bytes())

    logo_src = ROOT.parent / "cometweb-io" / "static" / "logo.svg"
    logo_dst = ASSETS / "cometweb-logo.svg"
    if logo_src.exists() and not logo_dst.exists():
        logo_dst.write_bytes(logo_src.read_bytes())

    fonts = load_fonts()
    images = build_frames(fonts)

    gif_path = OUT / "web-app-auditor-demo.gif"
    images[0].save(
        gif_path,
        save_all=True,
        append_images=images[1:],
        duration=2200,
        loop=0,
        optimize=True,
    )
    print(f"Wrote {gif_path} ({gif_path.stat().st_size} bytes, {len(images)} frames)")


if __name__ == "__main__":
    main()
