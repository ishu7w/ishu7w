#!/usr/bin/env python3
"""Compose the shared Loki throne artwork into the profile's branded hero."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "tva"
SOURCE = ASSETS / "loki-throne-source.jpg"
OUTPUT = ASSETS / "loki-throne-hero.jpg"
WIDTH, HEIGHT = 1440, 810


def load_font(size: int, *, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    filename = "Georgia Bold.ttf" if bold else "Arial.ttf"
    candidates = [
        Path("/System/Library/Fonts/Supplemental") / filename,
        Path("/usr/share/fonts/truetype/liberation2") / ("LiberationSerif-Bold.ttf" if bold else "LiberationSans-Regular.ttf"),
        Path("/usr/share/fonts/truetype/dejavu") / ("DejaVuSerif-Bold.ttf" if bold else "DejaVuSans.ttf"),
    ]
    for candidate in candidates:
        if candidate.is_file():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default(size=size)


def main() -> None:
    with Image.open(SOURCE) as source:
        image = source.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)

    # Keep the original throne scene visible while giving the left-side type a
    # calm, deep-green reading zone that fades naturally into the image.
    rgba = image.convert("RGBA")
    overlay = Image.new("RGBA", (WIDTH, HEIGHT))
    pixels = overlay.load()
    for x in range(WIDTH):
        left = max(0.0, 1 - x / 960) ** 1.35
        for y in range(HEIGHT):
            lower = max(0.0, (y / HEIGHT - .52) / .48) * 34
            alpha = min(205, int(188 * left + lower))
            pixels[x, y] = (3, 24, 13, alpha)
    rgba.alpha_composite(overlay)
    draw = ImageDraw.Draw(rgba)

    label_font = load_font(16)
    title_font = load_font(70, bold=True)
    detail_font = load_font(18)

    gold = (227, 190, 90, 255)
    parchment = (249, 242, 220, 255)
    pale_green = (211, 234, 211, 245)

    # Fine TVA-style registration marks; all text stays inside the open left
    # portion of the shared artwork, away from Loki and the golden throne.
    draw.line((72, 446, 390, 446), fill=(219, 183, 82, 190), width=2)
    draw.text((72, 466), "ISHU PATEL  /  DEVELOPER PROFILE", font=label_font, fill=gold,
              stroke_width=0)
    draw.text((69, 520), "Mischief,", font=title_font, fill=parchment,
              stroke_width=1, stroke_fill=(6, 25, 14, 150))
    draw.text((69, 601), "made useful.", font=title_font, fill=parchment,
              stroke_width=1, stroke_fill=(6, 25, 14, 150))
    draw.line((72, 704, 128, 704), fill=gold, width=3)
    draw.text((148, 692), "JAVA  ·  FULL-STACK  ·  PRACTICAL AI", font=detail_font,
              fill=pale_green, stroke_width=1, stroke_fill=(5, 24, 14, 180))

    rgba.convert("RGB").save(OUTPUT, "JPEG", quality=91, optimize=True,
                              progressive=True, subsampling=0)
    print(f"{OUTPUT.relative_to(ROOT)}: {OUTPUT.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
