#!/usr/bin/env python3
"""Build loopable, cinematic TVA timeline filaments for the profile README."""
from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "tva"
FRAMES = 20
DELAY_MS = 95


def flowing_filament(width: int, lane: int, frame: int, height: int = 112) -> list[tuple[float, float]]:
    """Continuous cable paths avoid visible joins and drift gently over the loop."""
    phase = lane * 1.23
    points = []
    for x in range(-30, width + 31, 3):
        travel = frame / FRAMES * 2 * math.pi
        y = (height / 2 + 29 * math.sin(x / 132 + phase + travel * .24)
             + 13 * math.sin(x / 54 - phase * .45 + travel * .38)
             + 4.5 * math.sin(x / 23 + phase * .3 + travel * .6))
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

    # Keep the actual filament hair-thin; most of its apparent volume comes
    # from a restrained soft halo and a narrow moving specular edge.
    center = [(x * supersample, y * supersample)
              for x, y in offset_path(path, 0, frame, lane, 2.4 * scale)]
    px = scale * supersample
    cable = [(x * supersample, y * supersample)
             for x, y in offset_path(path, 0, frame, lane, 2.4 * scale)]
    bd.line(cable, fill=(42, 255, 110, 38), width=max(3, round(12 * px)))
    rd.line(cable, fill=(1, 24, 9, 145), width=max(2, round(6 * px)))
    rd.line(cable, fill=(10, 70, 29, 240), width=max(2, round(4.5 * px)))
    rd.line(cable, fill=(25, 142, 58, 245), width=max(1, round(2.4 * px)))
    rd.line(cable, fill=(112, 240, 132, 235), width=max(1, round(1.2 * px)))
    highlight = [(x * supersample, y * supersample) for x, y in
                 offset_path(path, -.8 * scale, frame, lane, 2.4 * scale)]
    rd.line(highlight, fill=(181, 247, 142, 190), width=max(1, round(.9 * px)))
    glint_path = [(x * supersample, y * supersample) for x, y in
                  offset_path(path, -1.5 * scale, frame, lane, 2.4 * scale)]
    rd.line(glint_path, fill=(228, 255, 188, 155), width=max(1, round(.65 * px)))

    # A soft reflection glides along each strand like light passing through translucent fiber.
    progress = (frame / FRAMES + lane * 0.21) % 1
    head = int(progress * (len(center) - 1))
    length = max(4, int(len(center) * .12))
    for i in range(max(1, head - length), head):
        p = (i - (head - length)) / length
        alpha = int(145 * p * min(1, progress * 7, (1 - progress) * 7))
        glint.line((center[i - 1], center[i]), fill=(222, 255, 180, alpha),
                   width=max(1, round((1.0 + .6 * p) * px)))

    bloom = bloom.filter(ImageFilter.GaussianBlur(max(2, round(5 * px))))
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
    w, h = 1200, 156
    base = Image.new("RGB", (w, h))
    px = base.load()
    for y in range(h):
        edge = abs(y - h / 2) / (h / 2)
        for x in range(w):
            core = max(0, 1 - math.hypot((x - w * .53) / 670, (y - h * .5) / 100))
            wash = max(0, 1 - abs(x - (w * .5 + 50 * math.sin(y / 31))) / 800)
            px[x, y] = (3 + int(3 * core), 26 + int(49 * core + 12 * wash - 5 * edge),
                        14 + int(29 * core + 8 * wash))
    random.seed(19)
    bokeh = [(random.randrange(w), random.randrange(8, h - 8), random.randrange(2, 8),
              random.randrange(32, 90)) for _ in range(42)]
    frames = []
    for frame in range(FRAMES):
        image = base.convert("RGBA")
        atmosphere = Image.new("RGBA", (w, h))
        haze = ImageDraw.Draw(atmosphere)
        sweep_x = int((frame / FRAMES) * (w + 500) - 250)
        haze.ellipse((sweep_x - 290, -170, sweep_x + 290, h + 170), fill=(31, 224, 91, 34))
        core_x = w * (.47 + .035 * math.sin(2 * math.pi * frame / FRAMES))
        haze.ellipse((core_x - 170, -70, core_x + 170, h + 70), fill=(57, 255, 111, 25))
        for x, y, radius, alpha in bokeh:
            shimmer = .55 + .45 * math.sin(2 * math.pi * frame / FRAMES + x * .018)
            r = radius * (.78 + .22 * shimmer)
            haze.ellipse((x-r, y-r, x+r, y+r), fill=(123, 255, 145, int(alpha * shimmer)))
        image.alpha_composite(atmosphere.filter(ImageFilter.GaussianBlur(24)))

        # A dim TVA loom halo and its gold measuring marks sit behind the strands.
        loom = Image.new("RGBA", (w, h))
        ld = ImageDraw.Draw(loom)
        cx, cy = int(core_x), h // 2
        pulse = 1 + .025 * math.sin(2 * math.pi * frame / FRAMES)
        for radius, alpha in ((56, 30), (73, 21), (91, 13)):
            r = radius * pulse
            ld.ellipse((cx-r, cy-r*.68, cx+r, cy+r*.68), outline=(208, 175, 73, alpha), width=1)
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            x1, y1 = cx + 80*math.cos(rad), cy + 57*math.sin(rad)
            x2, y2 = cx + 96*math.cos(rad), cy + 68*math.sin(rad)
            ld.line((x1, y1, x2, y2), fill=(242, 205, 106, 100), width=1)
        image.alpha_composite(loom.filter(ImageFilter.GaussianBlur(1.2)))
        image.alpha_composite(loom)

        depth = (.68, 1.16, .82, 1.32, .74, 1.08, .78, 1.22)
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
