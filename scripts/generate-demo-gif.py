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
MARGIN = 40
HEADER_H = 64
CONTENT_TOP = HEADER_H + 16
CONTENT_BOTTOM = H - 24
CONTENT_W = W - 2 * MARGIN

# CometWeb tokens
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


def blend(c1: tuple[int, int, int], c2: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2, strict=True))


def load_fonts() -> dict[str, ImageFont.FreeTypeFont | ImageFont.ImageFont]:
    regular = ASSETS / "nunito-sans-regular.ttf"
    semibold = ASSETS / "nunito-sans-600.ttf"
    bold = ASSETS / "nunito-sans-700.ttf"
    fb = "/System/Library/Fonts/Supplemental/Arial.ttf"
    fbb = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

    def ft(path: Path, size: int, fallback: str) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
        try:
            return ImageFont.truetype(str(path if path.exists() else fallback), size)
        except OSError:
            return ImageFont.load_default()

    return {
        "display": ft(bold, 40, fbb),
        "title": ft(bold, 28, fbb),
        "section": ft(semibold, 20, fbb),
        "body": ft(regular, 16, fb),
        "small": ft(regular, 13, fb),
        "mono": ft(regular, 14, fb),
        "chip": ft(semibold, 11, fbb),
        "badge": ft(bold, 11, fbb),
    }


def load_logo(size: int = 72) -> Image.Image:
    svg = ASSETS / "cometweb-logo.svg"
    png = cairosvg.svg2png(url=str(svg), output_width=size)
    return Image.open(BytesIO(png)).convert("RGBA")


def gradient_bg(top: tuple[int, int, int], bottom: tuple[int, int, int], glow: tuple[int, int, int] | None = None) -> Image.Image:
    img = Image.new("RGB", (W, H), top)
    draw = ImageDraw.Draw(img)
    for y in range(H):
        draw.line([(0, y), (W, y)], fill=blend(top, bottom, y / max(H - 1, 1)))
    if glow:
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        od.ellipse((W // 2 - 240, -80, W // 2 + 240, 280), fill=(*glow, 32))
        img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
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


def text_center(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    text: str,
    font: ImageFont.ImageFont,
    fill: tuple[int, int, int],
    dy: int = 0,
) -> None:
    x0, y0, x1, y1 = box
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((x0 + (x1 - x0 - tw) // 2, y0 + (y1 - y0 - th) // 2 + dy), text, fill=fill, font=font)


def text_fit(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.ImageFont,
    max_w: int,
    min_size: int = 11,
) -> ImageFont.ImageFont:
    if not hasattr(font, "path"):
        return font
    size = font.size
    while size > min_size and draw.textlength(text, font=font) > max_w:
        size -= 1
        font = ImageFont.truetype(font.path, size)
    return font


def wrap_text(text: str, font: ImageFont.ImageFont, max_w: int, draw: ImageDraw.ImageDraw) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = words[0] if words else ""
    for word in words[1:]:
        trial = f"{current} {word}"
        if draw.textlength(trial, font=font) <= max_w:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def arrow_h(draw: ImageDraw.ImageDraw, y: int, x1: int, x2: int, color: tuple[int, int, int]) -> None:
    if x2 <= x1:
        return
    draw.line([(x1, y), (x2 - 8, y)], fill=color, width=2)
    draw.polygon([(x2, y), (x2 - 10, y - 5), (x2 - 10, y + 5)], fill=color)


def arrow_v(draw: ImageDraw.ImageDraw, x: int, y1: int, y2: int, color: tuple[int, int, int]) -> None:
    if y2 <= y1:
        return
    draw.line([(x, y1), (x, y2 - 8)], fill=color, width=2)
    draw.polygon([(x, y2), (x - 5, y2 - 10), (x + 5, y2 - 10)], fill=color)


def check_mark(draw: ImageDraw.ImageDraw, x: int, y: int, color: tuple[int, int, int]) -> None:
    draw.line([(x, y + 6), (x + 4, y + 10), (x + 11, y + 1)], fill=color, width=2)


def row_boxes(
    draw: ImageDraw.ImageDraw,
    items: list[tuple[str, str]],
    y: int,
    height: int,
    fonts: dict,
    *,
    gap: int = 14,
    accent_first: bool = False,
    accent_last: bool = False,
) -> None:
    n = len(items)
    box_w = (CONTENT_W - gap * (n - 1)) // n
    x = MARGIN
    cy = y + height // 2
    for i, (title, sub) in enumerate(items):
        accent = (i == 0 and accent_first) or (i == n - 1 and accent_last)
        outline = MINT if accent else BORDER
        rounded_rect(draw, (x, y, x + box_w, y + height), 12, CARD, outline=outline, width=2 if accent else 1)
        text_center(draw, (x, y + 8, x + box_w, y + height // 2 + 8), title, fonts["section"], TEXT)
        text_center(draw, (x, y + height // 2, x + box_w, y + height - 8), sub, fonts["small"], MUTED)
        if i < n - 1:
            arrow_h(draw, cy, x + box_w + 2, x + box_w + gap - 2, TRUST)
        x += box_w + gap


def header_bar(base: Image.Image, fonts: dict, title: str, subtitle: str = "") -> Image.Image:
    img = base.copy()
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, W, HEADER_H), fill=BG2)
    draw.line([(0, HEADER_H), (W, HEADER_H)], fill=BORDER, width=1)

    logo = load_logo(36)
    img.paste(logo, (MARGIN, 14), logo)
    draw.text((MARGIN + 48, 20), "Comet", fill=TEXT, font=fonts["section"])
    comet_w = draw.textlength("Comet", font=fonts["section"])
    draw.text((MARGIN + 48 + comet_w, 20), "Web", fill=MINT, font=fonts["section"])

    title_font = text_fit(draw, title, fonts["section"], 320, min_size=16)
    draw.text((W - MARGIN, 18), title, fill=MINT, font=title_font, anchor="ra")
    if subtitle:
        sub_font = text_fit(draw, subtitle, fonts["small"], 320, min_size=11)
        draw.text((W - MARGIN, 42), subtitle, fill=MUTED, font=sub_font, anchor="ra")
    return img


def panel(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    title: str,
    fonts: dict,
    *,
    outline: tuple[int, int, int] = BORDER,
) -> tuple[int, int, int, int]:
    rounded_rect(draw, box, 14, CARD, outline=outline, width=2 if outline != BORDER else 1)
    x0, y0, x1, _ = box
    draw.text((x0 + 16, y0 + 12), title, fill=MINT, font=fonts["section"])
    return (x0 + 16, y0 + 44, x1 - 16, box[3] - 12)


def draw_wordmark_centered(draw: ImageDraw.ImageDraw, y: int, font: ImageFont.ImageFont) -> None:
    comet, web = "Comet", "Web"
    total = draw.textlength(comet + web, font=font)
    x = (W - total) // 2
    draw.text((x, y), comet, fill=TEXT, font=font)
    draw.text((x + draw.textlength(comet, font=font), y), web, fill=MINT, font=font)


def frame_hero(fonts: dict) -> Image.Image:
    img = gradient_bg(DEPTH, BG, glow=MINT)
    draw = ImageDraw.Draw(img)

    logo = load_logo(120)
    img.paste(logo, (W // 2 - 60, 56), logo)

    draw_wordmark_centered(draw, 196, fonts["display"])
    draw.text((W // 2, 248), "Web App Auditor", fill=TEXT2, font=fonts["title"], anchor="mm")
    draw.text(
        (W // 2, 292),
        "Evidence-driven QA, protocol v1.1, deterministic validator",
        fill=MUTED,
        font=fonts["body"],
        anchor="mm",
    )

    pill = (W // 2 - 200, 330, W // 2 + 200, 368)
    rounded_rect(draw, pill, 18, CARD, outline=TRUST, width=2)
    text_center(draw, pill, "12 Agent Skills for Cursor and ChatGPT", fonts["small"], MINT)

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
    row_boxes(draw, steps, CONTENT_TOP + 8, 96, fonts, accent_first=True, accent_last=True)

    gate = (MARGIN, 300, W - MARGIN, CONTENT_BOTTOM)
    inner = panel(draw, gate, "Quality gate", fonts)
    x0, y0, x1, y1 = inner
    draw.text((x0, y0), "validate_report.py", fill=TEXT, font=fonts["mono"])
    draw.text((x0, y0 + 24), "schema + invariants + evidence links", fill=TEXT2, font=fonts["body"])
    draw.text((x0, y0 + 48), "PASS / FAIL without LLM guesswork", fill=MUTED, font=fonts["small"])

    badge = (x1 - 72, y0, x1, y0 + 56)
    rounded_rect(draw, badge, 28, DEPTH, outline=MINT, width=2)
    text_center(draw, badge, "CI", fonts["section"], MINT)
    return img


def frame_scope(fonts: dict) -> Image.Image:
    img = header_bar(gradient_bg(BG2, BG), fonts, "Scope", "cometweb.io/pricing")
    draw = ImageDraw.Draw(img)

    browser = (MARGIN, CONTENT_TOP, W - MARGIN, CONTENT_TOP + 200)
    rounded_rect(draw, browser, 14, CARD, outline=BORDER, width=1)
    bx0, by0, bx1, _ = browser
    draw.rectangle((bx0, by0, bx1, by0 + 36), fill=BG2)
    for i, color in enumerate((ERROR, WARNING, TRUST)):
        draw.ellipse((bx0 + 16 + i * 22, by0 + 10, bx0 + 28 + i * 22, by0 + 22), fill=color)
    url_box = (bx0 + 72, by0 + 8, bx1 - 16, by0 + 28)
    rounded_rect(draw, url_box, 6, BG, outline=BORDER)
    text_center(draw, url_box, "https://cometweb.io/pricing", fonts["small"], MINT)

    tiers = ["Free", "Growth", "Studio", "Scale"]
    gap = 12
    card_w = (bx1 - bx0 - 32 - gap * (len(tiers) - 1)) // len(tiers)
    tx = bx0 + 16
    ty = by0 + 52
    th = browser[3] - ty - 12
    for i, label in enumerate(tiers):
        box = (tx, ty, tx + card_w, ty + th)
        outline = MINT if label == "Studio" else BORDER
        rounded_rect(draw, box, 10, BG2, outline=outline, width=2 if label == "Studio" else 1)
        text_center(draw, (tx, ty + 8, tx + card_w, ty + th // 2), label, fonts["section"], TEXT)
        text_center(draw, (tx, ty + th // 2, tx + card_w, ty + th - 8), "PLN / USD", fonts["small"], MUTED)
        if label == "Studio":
            chip = (tx + 12, ty + th - 34, tx + card_w - 12, ty + th - 10)
            rounded_rect(draw, chip, 6, DEPTH, outline=MINT)
            text_center(draw, chip, "audit focus", fonts["chip"], MINT)
        tx += card_w + gap

    bottom_y = browser[3] + 16
    bottom_h = CONTENT_BOTTOM - bottom_y
    left_w = (CONTENT_W - 16) // 2
    right_x = MARGIN + left_w + 16

    left = (MARGIN, bottom_y, MARGIN + left_w, bottom_y + bottom_h)
    inner = panel(draw, left, "Scope parameters", fonts, outline=TRUST)
    x0, y0, _, _ = inner
    params = [
        ("target", "cometweb.io/pricing"),
        ("mode", "area"),
        ("depth", "standard"),
        ("persona", "prospect / PLN billing"),
    ]
    row_h = 28
    for i, (key, val) in enumerate(params):
        yy = y0 + i * row_h
        draw.text((x0, yy), key, fill=MUTED, font=fonts["mono"])
        draw.text((x0 + 110, yy), val, fill=TEXT2, font=fonts["mono"])

    right = (right_x, bottom_y, W - MARGIN, bottom_y + bottom_h)
    inner = panel(draw, right, "Navigation map", fonts)
    x0, y0, x1, y1 = inner
    node_w, node_h = 96, 32
    nodes = [("Home", 0), ("Pricing", 1), ("Register", 2)]
    row_y = y0 + 24
    total_w = len(nodes) * node_w + (len(nodes) - 1) * 28
    start_x = x0 + (x1 - x0 - total_w) // 2
    centers: list[tuple[int, str]] = []
    for i, (label, _) in enumerate(nodes):
        nx = start_x + i * (node_w + 28)
        box = (nx, row_y, nx + node_w, row_y + node_h)
        outline = MINT if label == "Pricing" else BORDER
        rounded_rect(draw, box, 8, BG2, outline=outline, width=2 if label == "Pricing" else 1)
        text_center(draw, box, label, fonts["chip"], TEXT if label == "Pricing" else MUTED)
        centers.append((nx + node_w // 2, label))
        if i < len(nodes) - 1:
            arrow_h(draw, row_y + node_h // 2, nx + node_w + 2, nx + node_w + 26, TRUST)

    checkout_y = row_y + node_h + 28
    cx = centers[1][0]
    checkout = (cx - node_w // 2, checkout_y, cx + node_w // 2, checkout_y + node_h)
    rounded_rect(draw, checkout, 8, BG2, outline=BORDER)
    text_center(draw, checkout, "Checkout", fonts["chip"], MUTED)
    arrow_v(draw, cx, row_y + node_h + 2, checkout_y - 2, TRUST)
    return img


def frame_finding(fonts: dict) -> Image.Image:
    img = header_bar(gradient_bg(BG, DEPTH), fonts, "Finding F-001", "MAJOR / billing UI")
    draw = ImageDraw.Draw(img)

    card = (MARGIN, CONTENT_TOP, W - MARGIN, CONTENT_TOP + 188)
    rounded_rect(draw, card, 14, CARD, outline=ERROR, width=2)
    badge = (MARGIN + 16, CONTENT_TOP + 16, MARGIN + 96, CONTENT_TOP + 44)
    rounded_rect(draw, badge, 8, ERROR)
    text_center(draw, badge, "MAJOR", fonts["badge"], TEXT)

    title = "Invoice count mismatch on billing dashboard"
    title_font = text_fit(draw, title, fonts["section"], CONTENT_W - 130, min_size=14)
    draw.text((MARGIN + 112, CONTENT_TOP + 18), title, fill=TEXT, font=title_font)

    body_box = (MARGIN + 16, CONTENT_TOP + 52, W - MARGIN - 16, CONTENT_TOP + 118)
    body = (
        "Badge shows 4 open invoices; table lists 3 rows. "
        "Arithmetic cross-check failed — user may miss a draft invoice."
    )
    y = body_box[1]
    for line in wrap_text(body, fonts["body"], body_box[2] - body_box[0], draw):
        draw.text((body_box[0], y), line, fill=TEXT2, font=fonts["body"])
        y += 22

    impacts = [("UX", 72, MUTED), ("Trust", 120, WARNING), ("Revenue", 168, ERROR)]
    bar_y = CONTENT_TOP + 132
    draw.text((MARGIN + 16, bar_y), "Impact", fill=MUTED, font=fonts["small"])
    bx = MARGIN + 72
    for label, width, color in impacts:
        rounded_rect(draw, (bx, bar_y - 2, bx + width, bar_y + 18), 5, color)
        draw.text((bx, bar_y + 22), label, fill=MUTED, font=fonts["chip"])
        bx += width + 20

    life = (MARGIN, CONTENT_TOP + 204, W - MARGIN, CONTENT_BOTTOM)
    inner = panel(draw, life, "Finding lifecycle", fonts)
    x0, y0, x1, _ = inner
    steps = ["Detected", "Evidence", "Validated", "Handoff"]
    n = len(steps)
    gap = 24
    circle = 44
    total = n * circle + (n - 1) * gap
    sx = x0 + (x1 - x0 - total) // 2
    cy = y0 + 36
    for i, step in enumerate(steps):
        cx = sx + i * (circle + gap) + circle // 2
        active = i >= 2
        fill = MINT if active else CARD_HOVER
        draw.ellipse((cx - circle // 2, cy - circle // 2, cx + circle // 2, cy + circle // 2), fill=fill, outline=MINT, width=2)
        num_color = BG if active else TEXT
        text_center(draw, (cx - circle // 2, cy - circle // 2, cx + circle // 2, cy + circle // 2), str(i + 1), fonts["section"], num_color)
        label_w = circle + 24
        text_center(draw, (cx - label_w // 2, cy + circle // 2 + 6, cx + label_w // 2, cy + circle // 2 + 30), step, fonts["small"], TEXT2)
        if i < n - 1:
            arrow_h(draw, cy, cx + circle // 2 + 4, cx + circle // 2 + gap - 4, TRUST)
    return img


def frame_evidence(fonts: dict) -> Image.Image:
    img = header_bar(gradient_bg(NIGHT, BG), fonts, "Evidence E-001", "confidence: HIGH")
    draw = ImageDraw.Draw(img)

    chain = [
        ("Screenshot", "badge + table"),
        ("Extract", "OCR + DOM"),
        ("Cross-check", "4 vs 3"),
        ("Verdict", "reproducible"),
    ]
    row_boxes(draw, chain, CONTENT_TOP, 88, fonts, accent_last=True)

    split_y = CONTENT_TOP + 104
    split_h = CONTENT_BOTTOM - split_y
    col_w = (CONTENT_W - 16) // 2

    left = (MARGIN, split_y, MARGIN + col_w, split_y + split_h)
    inner = panel(draw, left, "Captured state", fonts)
    x0, y0, x1, y1 = inner
    mock = (x0, y0, x1, y1)
    rounded_rect(draw, mock, 10, BG2, outline=BORDER)
    text_center(draw, (x0, y0 + 8, x1, y0 + 36), "Invoices (4)", fonts["section"], ERROR)
    for i, inv in enumerate(("INV-1042", "INV-1043", "INV-1044")):
        row = (x0 + 8, y0 + 40 + i * 34, x1 - 8, y0 + 68 + i * 34)
        rounded_rect(draw, row, 6, CARD)
        draw.text((row[0] + 10, row[1] + 8), inv, fill=TEXT2, font=fonts["mono"])
    text_center(draw, (x0, y1 - 28, x1, y1), "only 3 rows visible", fonts["small"], WARNING)

    right = (MARGIN + col_w + 16, split_y, W - MARGIN, split_y + split_h)
    inner = panel(draw, right, "Arithmetic proof", fonts, outline=TRUST)
    x0, y0, x1, y1 = inner
    lines = [
        ("badge_count", "= 4", TEXT2),
        ("table_rows", "= 3", TEXT2),
        ("delta", "= 1", ERROR),
        ("confidence", "= HIGH", MINT),
        ("source", "= screenshot + DOM", MUTED),
    ]
    row_h = (y1 - y0) // len(lines)
    for i, (key, val, color) in enumerate(lines):
        yy = y0 + i * row_h + 4
        draw.text((x0, yy), key, fill=MUTED, font=fonts["mono"])
        draw.text((x0 + 130, yy), val, fill=color, font=fonts["mono"])
    return img


def frame_validator(fonts: dict) -> Image.Image:
    img = header_bar(gradient_bg(BG2, NIGHT), fonts, "Validator", "deterministic PASS/FAIL")
    draw = ImageDraw.Draw(img)

    flow_y = CONTENT_TOP + 10
    flow_h = 150
    third = (CONTENT_W - 32) // 3
    boxes = [
        (MARGIN, flow_y, MARGIN + third, flow_y + flow_h),
        (MARGIN + third + 16, flow_y, MARGIN + 2 * third + 16, flow_y + flow_h),
        (MARGIN + 2 * third + 32, flow_y, W - MARGIN, flow_y + flow_h),
    ]

    rounded_rect(draw, boxes[0], 12, CARD, outline=BORDER)
    text_center(draw, boxes[0], "audit-report.json", fonts["section"], TEXT, dy=-16)
    text_center(draw, boxes[0], "schema v1.1", fonts["small"], MUTED, dy=8)

    rounded_rect(draw, boxes[1], 12, BG, outline=MINT, width=2)
    text_center(draw, (boxes[1][0], boxes[1][1] + 12, boxes[1][2], boxes[1][1] + 36), "python validate_report.py", fonts["mono"], MINT)
    checks = ["schema compliance", "finding IDs unique", "evidence linked", "severity enum valid"]
    cy = boxes[1][1] + 48
    for check in checks:
        check_mark(draw, boxes[1][0] + 16, cy, TRUST)
        draw.text((boxes[1][0] + 32, cy - 2), check, fill=TEXT2, font=fonts["small"])
        cy += 24

    rounded_rect(draw, boxes[2], 12, DEPTH, outline=MINT, width=2)
    text_center(draw, boxes[2], "VALID", fonts["title"], MINT, dy=-6)
    text_center(draw, boxes[2], "protocol v1.1", fonts["small"], TEXT2, dy=22)

    arrow_h(draw, flow_y + flow_h // 2, boxes[0][2] + 2, boxes[1][0] - 2, MINT)
    arrow_h(draw, flow_y + flow_h // 2, boxes[1][2] + 2, boxes[2][0] - 2, MINT)

    ci = (MARGIN, flow_y + flow_h + 24, W - MARGIN, CONTENT_BOTTOM)
    inner = panel(draw, ci, "CI / GitHub Actions", fonts)
    x0, y0, x1, y1 = inner
    steps = ["validate_skills.py", "routing evals (66)", "pytest (327+)", "public-safety-check"]
    gap = 12
    box_w = (x1 - x0 - gap * (len(steps) - 1)) // len(steps)
    cy = y0 + (y1 - y0 - 56) // 2
    for i, step in enumerate(steps):
        bx = x0 + i * (box_w + gap)
        box = (bx, cy, bx + box_w, cy + 56)
        outline = MINT if i == len(steps) - 1 else BORDER
        rounded_rect(draw, box, 10, BG2, outline=outline, width=2 if i == len(steps) - 1 else 1)
        font = text_fit(draw, step, fonts["small"], box_w - 12, min_size=10)
        text_center(draw, box, step, font, TEXT2)
        if i < len(steps) - 1:
            arrow_h(draw, cy + 28, bx + box_w + 2, bx + box_w + gap - 2, TRUST)
    return img


def frame_install(fonts: dict) -> Image.Image:
    img = gradient_bg(DEPTH, BG, glow=TRUST)
    draw = ImageDraw.Draw(img)

    logo = load_logo(64)
    img.paste(logo, (W // 2 - 32, 28), logo)
    draw.text((W // 2, 108), "Install 12 Agent Skills", fill=TEXT, font=fonts["title"], anchor="mm")

    skills = [
        "Evidence", "Competitive", "Teardown", "Design Partner",
        "Repo to Roadmap", "Product Operator", "Customer Ops", "Web Auditor",
        "SEO / AEO", "Release Readiness", "AI Council", "Humanize",
    ]
    grid = (MARGIN, 132, W - MARGIN, 388)
    cols, rows = 4, 3
    gap_x, gap_y = 12, 12
    cell_w = (grid[2] - grid[0] - gap_x * (cols - 1)) // cols
    cell_h = (grid[3] - grid[1] - gap_y * (rows - 1)) // rows
    for i, name in enumerate(skills):
        col = i % cols
        row = i // cols
        x = grid[0] + col * (cell_w + gap_x)
        y = grid[1] + row * (cell_h + gap_y)
        box = (x, y, x + cell_w, y + cell_h)
        highlight = "Auditor" in name
        rounded_rect(draw, box, 10, CARD, outline=MINT if highlight else BORDER, width=2 if highlight else 1)
        font = text_fit(draw, name, fonts["chip"], cell_w - 12, min_size=9)
        text_center(draw, box, name, font, MINT if highlight else TEXT2)

    hub = (W // 2 - 52, 404, W // 2 + 52, 428)
    rounded_rect(draw, hub, 12, DEPTH, outline=MINT, width=2)
    text_center(draw, hub, "CW-AIP handoffs", fonts["chip"], MINT)

    cmd = (MARGIN + 40, 444, W - MARGIN - 40, 492)
    rounded_rect(draw, cmd, 14, CARD, outline=MINT, width=2)
    text_center(draw, cmd, "./scripts/install-cursor.sh", fonts["mono"], MINT)

    draw.text((W // 2, H - 18), "CometWeb Labs  |  MIT  |  cometweb.io", fill=MUTED, font=fonts["small"], anchor="mm")
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


def ensure_assets() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    fonts_dir = ROOT.parent / "cometweb-io" / "static" / "fonts"
    for name in ("nunito-sans-regular.ttf", "nunito-sans-600.ttf", "nunito-sans-700.ttf"):
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
    images = build_frames(fonts)

    gif_path = OUT / "web-app-auditor-demo.gif"
    images[0].save(
        gif_path,
        save_all=True,
        append_images=images[1:],
        duration=2400,
        loop=0,
        optimize=True,
    )
    print(f"Wrote {gif_path} ({gif_path.stat().st_size} bytes, {len(images)} frames)")


if __name__ == "__main__":
    main()
