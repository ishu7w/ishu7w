#!/usr/bin/env python3
"""Build subtle, loopable emerald filament animations for the profile README."""
from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "tva"
FRAMES = 24
DELAY_MS = 110


def flowing_filament(width: int, lane: int, frame: int, height: int = 112) -> list[tuple[float, float]]:
    """Continuous cable paths avoid visible joins and drift gently over the loop."""
    phase = lane * 1.23
    points = []
    for x in range(-30, width + 31, 3):
        travel = frame / FRAMES * 2 * math.pi
        y = (height / 2 + 17 * math.sin(x / 132 + phase + travel * .24)
             + 7 * math.sin(x / 54 - phase * .45 + travel * .38)
             + 2.5 * math.sin(x / 23 + phase * .3 + travel * .6))
        points.append((x, y))
    return points


def offset_path(points: list[tuple[float, float]], amount: float, frame: int,
                lane: int, wave: float) -> list[tuple[float, float]]:
    moved = []
    for i, (x, y) in enumerate(points):
        before = points[max(0, i - 1)]
        after = points[min(len(points) - 1, i + 1)]
        dx, dy = after[0] - before[0], after[1] - before[1]
        length = max(1, math.hypot(dx, dy))
        nx, ny = -dy / length, dx / length
        phase = 2 * math.pi * (i / (len(points) - 1) * 1.35 - frame / FRAMES + lane * .27)
        undulate = math.sin(phase) * wave
        moved.append((x + nx * (amount + undulate), y + ny * (amount + undulate)))
    return moved


def draw_strand(size: tuple[int, int], path: list[tuple[float, float]], frame: int,
                lane: int, scale: float) -> Image.Image:
    """A translucent braided filament: dark edge, green body, fine moving glint."""
    w, h = size
    supersample = 2
    canvas = (w * supersample, h * supersample)
    bloom = Image.new("RGBA", canvas)
    body = Image.new("RGBA", canvas)
    reflection = Image.new("RGBA", canvas)
    bd, rd = ImageDraw.Draw(bloom), ImageDraw.Draw(body)
    glint = ImageDraw.Draw(reflection)

    # A rounded, shaded cable with an offset specular edge reads as glass fiber,
    # while a small undulation and moving reflection keep it alive.
    center = [(x * supersample, y * supersample)
              for x, y in offset_path(path, 0, frame, lane, 2.4 * scale)]
    px = scale * supersample
    cable = [(x * supersample, y * supersample)
             for x, y in offset_path(path, 0, frame, lane, 2.4 * scale)]
    bd.line(cable, fill=(42, 255, 110, 45), width=max(5, round(34 * px)))
    rd.line(cable, fill=(1, 24, 9, 180), width=max(4, round(21 * px)))
    rd.line(cable, fill=(10, 70, 29, 245), width=max(3, round(16 * px)))
    rd.line(cable, fill=(25, 142, 58, 245), width=max(2, round(10 * px)))
    rd.line(cable, fill=(86, 211, 103, 225), width=max(1, round(5 * px)))
    highlight = [(x * supersample, y * supersample) for x, y in
                 offset_path(path, -3.5 * scale, frame, lane, 2.4 * scale)]
    rd.line(highlight, fill=(181, 247, 142, 215), width=max(1, round(2.3 * px)))
    glint_path = [(x * supersample, y * supersample) for x, y in
                  offset_path(path, -4.5 * scale, frame, lane, 2.4 * scale)]
    rd.line(glint_path, fill=(228, 255, 188, 175), width=max(1, round(1.0 * px)))

    # A soft reflection glides along each strand like light passing through translucent fiber.
    progress = (frame / FRAMES + lane * 0.21) % 1
    head = int(progress * (len(center) - 1))
    length = max(4, int(len(center) * .12))
    for i in range(max(1, head - length), head):
        p = (i - (head - length)) / length
        alpha = int(175 * p * min(1, progress * 7, (1 - progress) * 7))
        glint.line((center[i - 1], center[i]), fill=(222, 255, 180, alpha),
                   width=max(1, round((2.4 + 2.0 * p) * px)))

    bloom = bloom.filter(ImageFilter.GaussianBlur(max(3, round(9 * px))))
    body.alpha_composite(bloom)
    body.alpha_composite(reflection.filter(ImageFilter.GaussianBlur(max(1, round(2 * px)))))
    body.alpha_composite(reflection)
    return body.resize(size, Image.Resampling.LANCZOS)


def save_gif(frames: list[Image.Image], target: Path) -> None:
    palette = frames[0].convert("P", palette=Image.Palette.ADAPTIVE, colors=256)
    indexed = [frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in frames]
    indexed[0].save(target, save_all=True, append_images=indexed[1:], duration=DELAY_MS,
                    loop=0, optimize=True, disposal=2)


def make_divider() -> None:
    w, h = 1200, 112
    base = Image.new("RGB", (w, h))
    px = base.load()
    for y in range(h):
        edge = abs(y - h / 2) / (h / 2)
        for x in range(w):
            ambient = max(0, 1 - abs(x - (w * .5 + 40 * math.sin(y / 27))) / 750)
            px[x, y] = (5 + int(4 * ambient), 24 + int(22 * ambient - 7 * edge),
                        12 + int(15 * ambient))
    random.seed(19)
    bokeh = [(random.randrange(w), random.randrange(10, h - 10), random.randrange(2, 7),
              random.randrange(30, 75)) for _ in range(28)]
    frames = []
    for frame in range(FRAMES):
        image = base.convert("RGBA")
        atmosphere = Image.new("RGBA", (w, h))
        haze = ImageDraw.Draw(atmosphere)
        sweep_x = int((frame / FRAMES) * (w + 340) - 170)
        haze.ellipse((sweep_x - 240, -150, sweep_x + 240, h + 150), fill=(30, 190, 79, 22))
        for x, y, radius, alpha in bokeh:
            shimmer = .55 + .45 * math.sin(2 * math.pi * frame / FRAMES + x * .018)
            r = radius * (.78 + .22 * shimmer)
            haze.ellipse((x-r, y-r, x+r, y+r), fill=(99, 255, 129, int(alpha * shimmer)))
        image.alpha_composite(atmosphere.filter(ImageFilter.GaussianBlur(18)))
        depth = (.62, .88, .73, .96, .67, .82)
        for lane, scale in enumerate(depth):
            path = flowing_filament(w, lane, frame, h)
            image.alpha_composite(draw_strand((w, h), path, frame, lane, scale))
        frames.append(image.convert("RGB"))
    save_gif(frames, OUT / "divider.gif")

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    make_divider()
    path = OUT / "divider.gif"
    print(f"{path.relative_to(ROOT)}: {path.stat().st_size:,} bytes")
