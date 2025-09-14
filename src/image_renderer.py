from __future__ import annotations

from pathlib import Path
from typing import Tuple, Optional
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import winreg
import textwrap


def load_font(font_path: Optional[Path], size: int) -> ImageFont.ImageFont:
    if font_path and Path(font_path).exists():
        try:
            return ImageFont.truetype(str(font_path), size=size)  # type: ignore
        except Exception:
            pass
    # Fallback to default font
    try:
        return ImageFont.truetype("segoeui.ttf", size=size)  # type: ignore
    except Exception:
        return ImageFont.load_default()  # type: ignore


def draw_text_with_outline(draw: ImageDraw.ImageDraw, xy: Tuple[int, int], text: str, font: ImageFont.ImageFont, fill=(255, 255, 255), outline=(0, 0, 0), outline_width: int = 2, align="center", max_width: int = 1000):
    x, y = xy
    # Shadow/outline by drawing multiple offset copies
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx == 0 and dy == 0:
                continue
            draw.multiline_text((x + dx, y + dy), text, font=font, fill=outline, align=align, spacing=6)
    draw.multiline_text((x, y), text, font=font, fill=fill, align=align, spacing=6)


def wrap_text(text: str, font: ImageFont.ImageFont, max_width_px: int) -> str:
    # Binary search wrap width by characters to fit max_width_px
    words = text.split()
    if not words:
        return ""
    low, high = 10, max(10, max(len(w) for w in words)) * 4
    best = 40
    # Try to estimate characters per line
    while low <= high:
        mid = (low + high) // 2
        lines = textwrap.wrap(text, width=mid)
        line_w = max(font.getlength(line) for line in lines) if lines else 0
        if line_w <= max_width_px:
            best = mid
            low = mid + 1
        else:
            high = mid - 1
    wrapped = textwrap.fill(text, width=best)
    return wrapped


def render_wallpaper(verse_text: str, verse_ref: str, size: Tuple[int, int], out_path: Path, font_path: Optional[Path] = None) -> Path:
    width, height = size
    # Try to get current wallpaper path from registry
    def get_current_wallpaper_path() -> Optional[str]:
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                r"Control Panel\Desktop", 0, winreg.KEY_READ) as key:
                value, _ = winreg.QueryValueEx(key, "WallPaper")
                if value and Path(value).exists():
                    return value
        except Exception:
            pass
        return None


    # Always start from a fresh background image (never use the last generated wallpaper)
    # TEST PATCH: Always use a solid color background to ensure no previous verses are present
    img = Image.new("RGB", (width, height), color=(20, 24, 28))

    draw = ImageDraw.Draw(img)

    # Use a system-like font size (approx 14pt for body, 16pt for ref)
    # 1pt ≈ 1.33px, so 14pt ≈ 18px, 16pt ≈ 21px
    body_font_size = 18
    ref_font_size = 21
    title_font = load_font(font_path, size=ref_font_size)
    body_font = load_font(font_path, size=body_font_size)

    margin_top = int(height * 0.04)
    margin_right = int(width * 0.04)
    max_text_width = int(width * 0.38)  # About 1/3 screen width for realistic line length

    wrapped_body = wrap_text(verse_text, body_font, max_text_width)

    # Measure multiline text height using bbox
    body_bbox = draw.multiline_textbbox((0, 0), wrapped_body, font=body_font, align="left", spacing=6)
    body_w = body_bbox[2] - body_bbox[0]
    body_h = body_bbox[3] - body_bbox[1]

    # Reference text
    ref_text = f"— {verse_ref}"
    ref_bbox = draw.textbbox((0, 0), ref_text, font=title_font)
    ref_w = ref_bbox[2] - ref_bbox[0]
    ref_h = ref_bbox[3] - ref_bbox[1]

    # Draw only one verse and reference per image
    body_x = width - body_w - margin_right
    body_y = margin_top
    draw_text_with_outline(draw, (int(body_x), int(body_y)), wrapped_body, body_font, outline_width=2, align="left")

    ref_x = width - ref_w - margin_right
    ref_y = body_y + body_h + int(ref_h * 0.3)
    draw_text_with_outline(draw, (int(ref_x), int(ref_y)), ref_text, title_font, outline_width=2, align="left")

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, format="JPEG", quality=92)
    return out_path
