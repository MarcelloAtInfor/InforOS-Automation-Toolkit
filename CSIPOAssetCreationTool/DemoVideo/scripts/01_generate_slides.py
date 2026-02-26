"""
01_generate_slides.py — Pillow-based slide renderer for Demo Video pipeline.

Reads video_script.json and generates one PNG per section:
  - title_card: gradient background, centered title/subtitle/footer
  - architecture_diagram: 6 colored boxes with arrow connectors
  - screenshot_frame: loads screenshot (or gray placeholder), title + caption bars
  - closing_card: 2x2 metrics grid, tagline, footer

Also generates gray placeholder PNGs for any missing screenshots.

Usage:
    python scripts/01_generate_slides.py
"""

import json
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
CONFIG_DIR = PROJECT_DIR / "config"
SLIDES_DIR = PROJECT_DIR / "assets" / "slides"
SCREENSHOTS_DIR = PROJECT_DIR / "assets" / "screenshots"

# ---------------------------------------------------------------------------
# Load configuration
# ---------------------------------------------------------------------------

def load_json(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


CONFIG = load_json(CONFIG_DIR / "video_script.json")
COLORS = load_json(CONFIG_DIR / "colors.json")
FONTS_CFG = load_json(CONFIG_DIR / "fonts.json")

WIDTH, HEIGHT = CONFIG["video"]["resolution"]

# ---------------------------------------------------------------------------
# Font loader (cached)
# ---------------------------------------------------------------------------
_font_cache: dict[str, ImageFont.FreeTypeFont] = {}


def get_font(key: str, size_override: int | None = None) -> ImageFont.FreeTypeFont:
    """Load a font from fonts.json by key, with optional size override."""
    cfg = FONTS_CFG[key]
    size = size_override or cfg["size"]
    cache_key = f"{cfg['family']}_{size}"
    if cache_key not in _font_cache:
        _font_cache[cache_key] = ImageFont.truetype(cfg["family"], size)
    return _font_cache[cache_key]


def color(key: str) -> str:
    """Look up a color from colors.json."""
    return COLORS[key]


# ---------------------------------------------------------------------------
# Drawing helpers
# ---------------------------------------------------------------------------

def draw_gradient(img: Image.Image, top_color: str, bottom_color: str):
    """Fill image with a vertical linear gradient."""
    draw = ImageDraw.Draw(img)
    r1, g1, b1 = _hex_to_rgb(top_color)
    r2, g2, b2 = _hex_to_rgb(bottom_color)
    for y in range(HEIGHT):
        t = y / HEIGHT
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))


def _hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    h = hex_color.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def draw_rounded_rect(draw: ImageDraw.Draw, xy: tuple, radius: int, fill: str,
                      outline: str | None = None, outline_width: int = 0):
    """Draw a rounded rectangle with optional outline."""
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill,
                           outline=outline, width=outline_width)


def _darken_hex(hex_color: str, factor: float = 0.35) -> str:
    """Darken a hex color by multiplying RGB channels by factor."""
    r, g, b = _hex_to_rgb(hex_color)
    r2 = int(r * factor)
    g2 = int(g * factor)
    b2 = int(b * factor)
    return f"#{r2:02x}{g2:02x}{b2:02x}"


def text_centered(draw: ImageDraw.Draw, y: int, text: str,
                  font: ImageFont.FreeTypeFont, fill: str):
    """Draw text horizontally centered at given y."""
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (WIDTH - tw) // 2
    draw.text((x, y), text, font=font, fill=fill)


def text_wrapped_centered(draw: ImageDraw.Draw, y: int, text: str,
                          font: ImageFont.FreeTypeFont, fill: str,
                          max_width: int, line_spacing: int = 8) -> int:
    """Draw multi-line text, each line horizontally centered. Returns final y."""
    words = text.split()
    lines: list[str] = []
    current_line = ""
    for word in words:
        test = f"{current_line} {word}".strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current_line = test
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        x = (WIDTH - tw) // 2
        draw.text((x, y), line, font=font, fill=fill)
        y += th + line_spacing
    return y


# ---------------------------------------------------------------------------
# Slide templates
# ---------------------------------------------------------------------------

def render_title_card(section: dict) -> Image.Image:
    """Dark gradient background, large centered title, accent subtitle, footer."""
    img = Image.new("RGB", (WIDTH, HEIGHT))
    draw_gradient(img, color("background_dark"), color("background_gradient_end"))
    draw = ImageDraw.Draw(img)

    # Title
    title_font = get_font("title", 68)
    text_wrapped_centered(draw, 300, section["title"], title_font,
                          color("text_primary"), max_width=1600)

    # Subtitle
    subtitle_font = get_font("subtitle", 36)
    text_wrapped_centered(draw, 430, section["subtitle"], subtitle_font,
                          color("accent"), max_width=1500)

    # Decorative line
    line_y = 510
    line_w = 200
    draw.line([(WIDTH // 2 - line_w, line_y), (WIDTH // 2 + line_w, line_y)],
              fill=color("accent"), width=3)

    # Footer
    footer_font = get_font("footer")
    text_centered(draw, 950, section.get("footer", ""), footer_font,
                  color("text_secondary"))

    return img


def render_architecture_diagram(section: dict,
                                highlight_boxes: list[int] | None = None) -> Image.Image:
    """6 colored rounded-rect boxes with arrow connectors.

    Args:
        section: Section config dict from video_script.json.
        highlight_boxes: If None, render all boxes at normal brightness (overview).
            If a list of box indices, spotlight those boxes and dim the rest.
    """
    img = Image.new("RGB", (WIDTH, HEIGHT))
    draw_gradient(img, color("background_dark"), color("background_gradient_end"))
    draw = ImageDraw.Draw(img)

    # Title at top
    title_font = get_font("title", 48)
    text_centered(draw, 60, section["title"], title_font, color("text_primary"))

    boxes = section["boxes"]
    n = len(boxes)
    box_w = 200
    box_h = 160
    gap = 40
    total_w = n * box_w + (n - 1) * gap
    start_x = (WIDTH - total_w) // 2
    center_y = HEIGHT // 2 - 20
    box_top = center_y - box_h // 2

    label_font = get_font("box_label")
    sublabel_font = get_font("box_sublabel")
    arrow_font = get_font("diagram_arrow")

    for i, box in enumerate(boxes):
        x = start_x + i * (box_w + gap)
        base_color = color(box["color_key"])

        # Determine if this box is highlighted, dimmed, or normal
        is_highlighted = highlight_boxes is not None and i in highlight_boxes
        is_dimmed = highlight_boxes is not None and i not in highlight_boxes

        if is_dimmed:
            box_color = _darken_hex(base_color, 0.35)
            text_fill = "#666666"
            sub_fill = "#444444"
        else:
            box_color = base_color
            text_fill = "#FFFFFF"
            sub_fill = "rgba(255,255,255,200)"

        # Box (with white glow border if highlighted)
        if is_highlighted:
            draw_rounded_rect(draw, (x, box_top, x + box_w, box_top + box_h),
                              radius=16, fill=box_color,
                              outline="#FFFFFF", outline_width=3)
        else:
            draw_rounded_rect(draw, (x, box_top, x + box_w, box_top + box_h),
                              radius=16, fill=box_color)

        # Label (centered in box)
        lbl = box["label"]
        bbox = draw.textbbox((0, 0), lbl, font=label_font)
        lw = bbox[2] - bbox[0]
        lx = x + (box_w - lw) // 2
        draw.text((lx, box_top + 40), lbl, font=label_font, fill=text_fill)

        # Sublabel
        slbl = box["sublabel"]
        bbox2 = draw.textbbox((0, 0), slbl, font=sublabel_font)
        sw = bbox2[2] - bbox2[0]
        sx = x + (box_w - sw) // 2
        draw.text((sx, box_top + 100), slbl, font=sublabel_font, fill=sub_fill)

        # Arrow between boxes (except after last)
        if i < n - 1:
            ax = x + box_w + 4
            ay = center_y - 10
            # Dim arrows not adjacent to highlighted boxes
            if highlight_boxes is not None:
                arrow_adjacent = (i in highlight_boxes or (i + 1) in highlight_boxes)
                arrow_fill = color("accent") if arrow_adjacent else _darken_hex(color("accent"), 0.35)
            else:
                arrow_fill = color("accent")
            draw.text((ax, ay), "\u2192", font=arrow_font, fill=arrow_fill)

    # Bottom caption
    caption_font = get_font("caption")
    caption_fill = color("text_secondary") if highlight_boxes is None else _darken_hex(color("text_secondary"), 0.5)
    text_centered(draw, 780, "Invoice PDF \u2192 RPA \u2192 IDP \u2192 GenAI \u2192 SyteLine \u2192 Pulse",
                  caption_font, caption_fill)

    return img


def render_screenshot_frame(section: dict) -> Image.Image:
    """Screenshot (or placeholder) with title bar and caption bar."""
    img = Image.new("RGB", (WIDTH, HEIGHT))
    draw_gradient(img, color("background_dark"), color("background_gradient_end"))
    draw = ImageDraw.Draw(img)

    # Layout constants
    title_bar_h = 70
    caption_bar_h = 60
    padding = 40
    screenshot_x = padding
    screenshot_y = title_bar_h
    screenshot_w = WIDTH - 2 * padding
    screenshot_h = HEIGHT - title_bar_h - caption_bar_h

    # Title bar
    draw.rectangle([0, 0, WIDTH, title_bar_h], fill=color("title_bar_bg"))
    title_font = get_font("subtitle", 30)
    draw.text((padding, 18), section["title"], font=title_font,
              fill=color("text_primary"))

    # Load screenshot or generate placeholder
    screenshot_path = PROJECT_DIR / section["screenshot"]
    if screenshot_path.exists():
        shot = Image.open(screenshot_path).convert("RGB")
        # Scale to fit within the screenshot area, maintaining aspect ratio
        scale = min(screenshot_w / shot.width, screenshot_h / shot.height)
        new_w = int(shot.width * scale)
        new_h = int(shot.height * scale)
        shot = shot.resize((new_w, new_h), Image.LANCZOS)
        # Center in the screenshot area
        sx = screenshot_x + (screenshot_w - new_w) // 2
        sy = screenshot_y + (screenshot_h - new_h) // 2
        img.paste(shot, (sx, sy))
    else:
        # Gray placeholder with filename text
        draw.rectangle([screenshot_x, screenshot_y,
                        screenshot_x + screenshot_w,
                        screenshot_y + screenshot_h],
                       fill=color("placeholder_bg"))
        ph_font = get_font("body")
        ph_text = f"[ {Path(section['screenshot']).name} ]"
        bbox = draw.textbbox((0, 0), ph_text, font=ph_font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text(
            (screenshot_x + (screenshot_w - tw) // 2,
             screenshot_y + (screenshot_h - th) // 2),
            ph_text, font=ph_font, fill=color("placeholder_text")
        )

    # Caption bar at bottom
    draw.rectangle([0, HEIGHT - caption_bar_h, WIDTH, HEIGHT],
                   fill=color("caption_bg"))
    caption_font = get_font("caption")
    draw.text((padding, HEIGHT - caption_bar_h + 16), section["caption"],
              font=caption_font, fill=color("text_secondary"))

    return img


def render_closing_card(section: dict) -> Image.Image:
    """2x2 metrics grid, tagline, footer."""
    img = Image.new("RGB", (WIDTH, HEIGHT))
    draw_gradient(img, color("background_dark"), color("background_gradient_end"))
    draw = ImageDraw.Draw(img)

    # Title
    title_font = get_font("title", 52)
    text_centered(draw, 60, section["title"], title_font, color("text_primary"))

    # Metrics 2x2 grid
    metrics = section["metrics"]
    val_font = get_font("metric_value")
    lbl_font = get_font("metric_label")

    grid_x_centers = [WIDTH // 2 - 300, WIDTH // 2 + 300]
    grid_y_centers = [320, 560]

    for i, metric in enumerate(metrics):
        col = i % 2
        row = i // 2
        cx = grid_x_centers[col]
        cy = grid_y_centers[row]

        # Value
        val_text = metric["value"]
        bbox = draw.textbbox((0, 0), val_text, font=val_font)
        vw = bbox[2] - bbox[0]
        draw.text((cx - vw // 2, cy - 50), val_text, font=val_font,
                  fill=color("metric_value"))

        # Label
        lbl_text = metric["label"]
        bbox2 = draw.textbbox((0, 0), lbl_text, font=lbl_font)
        lw = bbox2[2] - bbox2[0]
        draw.text((cx - lw // 2, cy + 40), lbl_text, font=lbl_font,
                  fill=color("metric_label"))

    # Divider line
    div_y = 700
    draw.line([(WIDTH // 2 - 300, div_y), (WIDTH // 2 + 300, div_y)],
              fill=color("accent"), width=2)

    # Tagline
    tagline_font = get_font("subtitle", 30)
    text_wrapped_centered(draw, 730, section.get("tagline", ""), tagline_font,
                          color("accent"), max_width=1400)

    # Footer
    footer_font = get_font("footer")
    text_centered(draw, 950, section.get("footer", ""), footer_font,
                  color("text_secondary"))

    return img


# ---------------------------------------------------------------------------
# Placeholder generator
# ---------------------------------------------------------------------------

PLACEHOLDER_SCREENSHOTS = [
    "rpa_watch.png",
    "idp_extract.png",
    "genai_agent.png",
    "syteline_po.png",
    "pulse_alert.png",
]


def generate_placeholders():
    """Create gray placeholder PNGs for screenshots that don't exist yet."""
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    ph_font = get_font("body")

    for filename in PLACEHOLDER_SCREENSHOTS:
        path = SCREENSHOTS_DIR / filename
        if path.exists():
            continue
        img = Image.new("RGB", (WIDTH, HEIGHT), color=color("placeholder_bg"))
        draw = ImageDraw.Draw(img)
        text = f"PLACEHOLDER: {filename}"
        bbox = draw.textbbox((0, 0), text, font=ph_font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(((WIDTH - tw) // 2, (HEIGHT - th) // 2), text,
                  font=ph_font, fill=color("placeholder_text"))
        # Border
        draw.rectangle([10, 10, WIDTH - 10, HEIGHT - 10],
                       outline=color("placeholder_text"), width=2)
        img.save(path, "PNG")
        print(f"  Created placeholder: {path.name}")


# ---------------------------------------------------------------------------
# Template dispatcher
# ---------------------------------------------------------------------------

TEMPLATE_MAP = {
    "title_card": render_title_card,
    "architecture_diagram": render_architecture_diagram,
    "screenshot_frame": render_screenshot_frame,
    "closing_card": render_closing_card,
}


def generate_all_slides():
    """Generate one PNG per section defined in video_script.json.

    For sections with a 'highlights' array, generates an overview slide plus
    one spotlight sub-slide per highlight entry (e.g., _h0.png, _h1.png, ...).
    """
    SLIDES_DIR.mkdir(parents=True, exist_ok=True)

    print("Generating placeholder screenshots...")
    generate_placeholders()
    print()

    print("Generating slides...")
    total_files = 0
    for i, section in enumerate(CONFIG["sections"]):
        section_id = section["id"]
        section_type = section["type"]
        renderer = TEMPLATE_MAP.get(section_type)
        if renderer is None:
            print(f"  WARNING: Unknown template '{section_type}' for section '{section_id}'")
            continue

        # Base slide (overview — no highlights)
        img = renderer(section)
        out_path = SLIDES_DIR / f"{i + 1:02d}_{section_id}.png"
        img.save(out_path, "PNG")
        total_files += 1
        print(f"  [{i + 1}/{len(CONFIG['sections'])}] {out_path.name}  ({section_type})")

        # Generate highlight sub-slides if section has highlights array
        highlights = section.get("highlights")
        if highlights and section_type == "architecture_diagram":
            for h_idx, highlight in enumerate(highlights):
                h_boxes = highlight["boxes"]
                if not h_boxes:
                    # Empty boxes = overview (already generated above), skip
                    continue
                h_img = render_architecture_diagram(section, highlight_boxes=h_boxes)
                h_path = SLIDES_DIR / f"{i + 1:02d}_{section_id}_h{h_idx}.png"
                h_img.save(h_path, "PNG")
                total_files += 1
                print(f"         +- {h_path.name}  (highlight boxes={h_boxes})")

    print(f"\nDone. {total_files} slide files written to {SLIDES_DIR}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    generate_all_slides()
