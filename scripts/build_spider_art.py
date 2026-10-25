"""Build the Spider-Man hero and restrained GitHub-native project panels."""
from html import escape
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "assets" / "spider" / "references"
OUT = ROOT / "assets" / "spider"
W, H = 1200, 500
BG = "#0d1117"
FG = "#e6edf3"
MUTED = "#8b949e"
LINE = "#30363d"
RED = "#f04452"


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(f"/System/Library/Fonts/Supplemental/{name}.ttf", size)


def cover(path: Path, size: tuple[int, int], centering=(0.5, 0.5)) -> Image.Image:
    image = Image.open(path).convert("RGB")
    return ImageOps.fit(image, size, Image.Resampling.LANCZOS, centering=centering)


def draw_web(draw: ImageDraw.ImageDraw):
    cx, cy = 1190, -80
    for i in range(12):
        angle = math.radians(110 + i * 8)
        draw.line((cx, cy, cx + 760 * math.cos(angle), cy + 760 * math.sin(angle)), fill=(240, 68, 82, 25), width=1)
    for radius in (90, 155, 235, 330, 440, 560):
        points = []
        for i in range(100):
            angle = math.radians(110 + 94 * i / 99)
            points.append((cx + radius * math.cos(angle), cy + radius * math.sin(angle)))
        draw.line(points, fill=(240, 68, 82, 24), width=1)


def hero():
    base = Image.new("RGBA", (W, H), (13, 17, 23, 255))
    # Preserve the supplied Spider-Man image as the sole character artwork.
    figure = cover(REF / "spider-noir.jpeg", (600, H), (0.53, 0.34))
    figure = ImageOps.grayscale(figure).convert("RGB")
    figure = ImageEnhance.Contrast(figure).enhance(1.12)
    figure = ImageEnhance.Brightness(figure).enhance(0.68)
    mask = Image.new("L", (600, H), 0)
    md = ImageDraw.Draw(mask)
    for x in range(600):
        alpha = int(245 * min(1, max(0, (x - 20) / 240)))
        md.line((x, 0, x, H), fill=alpha)
    base.paste(figure, (600, 0), mask)

    # GitHub-like canvas with a quiet halftone field and static web geometry.
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shade)
    for x in range(760):
        alpha = int(238 * max(0, 1 - x / 820) ** 1.8)
        sd.line((x, 0, x, H), fill=(13, 17, 23, alpha))
    base = Image.alpha_composite(base, shade)
    texture = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    td = ImageDraw.Draw(texture)
    for y in range(10, H, 14):
        for x in range(10, W, 14):
            if (x * 3 + y) % 7 == 0:
                td.ellipse((x, y, x + 1, y + 1), fill=(230, 237, 243, 14))
    draw_web(td)
    base = Image.alpha_composite(base, texture)
    d = ImageDraw.Draw(base)
    d.rounded_rectangle((28, 28, W - 28, H - 28), radius=6, outline=(48, 54, 61, 255), width=1)
    d.text((64, 84), "ISHU PATEL", font=font("Arial Bold", 46), fill=(230, 237, 243, 255))
    d.text((66, 140), "COMPUTER SCIENCE & ENGINEERING", font=font("Arial Bold", 16), fill=(240, 68, 82, 255))
    d.line((66, 165, 442, 165), fill=(48, 54, 61, 255), width=1)
    d.text((63, 220), "JAVA + FULL-STACK", font=font("Arial Bold", 33), fill=(230, 237, 243, 255))
    d.text((63, 266), "Practical software, built and tested in public.", font=font("Arial", 20), fill=(201, 209, 217, 255))
    d.rounded_rectangle((64, 318, 190, 352), radius=4, outline=(240, 68, 82, 190), width=1)
    d.text((77, 327), "OPEN SOURCE", font=font("Arial Bold", 14), fill=(230, 237, 243, 255))
    d.text((65, 436), "JAVA  ·  TYPESCRIPT  ·  JAVASCRIPT  ·  AI", font=font("Arial Bold", 14), fill=(175, 184, 193, 255))
    base.convert("RGB").save(OUT / "hero.jpg", quality=91, optimize=True)


def hero_glitch():
    """Make an occasional, localized Spider-Man pixel-shear loop for the README hero."""
    source = Image.open(OUT / "hero.jpg").convert("RGB")
    frames, durations = [], []
    # Mostly hold the approved hero still; short red-channel shears interrupt it.
    sequence = [None, None, None,
                ((116, 18, 46), (160, 10, -29)),
                ((248, 22, -48), (299, 16, 34), (347, 11, -26)),
                None, None, None,
                ((177, 13, 38), (219, 9, -25)),
                ((321, 22, -42), (353, 10, 28)), None]
    for item in sequence:
        frame = source.copy()
        if item:
            draw = ImageDraw.Draw(frame)
            for y, height, shift in item:
                left, right = 615, 1200
                strip = source.crop((left, y, right, y + height))
                frame.paste(strip, (left + shift, y))
                # Short scarlet fragments trace the displaced slice, then disappear.
                fragment_x = max(left, min(1150, 760 + (y * 7) % 290))
                draw.rectangle((fragment_x, y + 2, fragment_x + 42, y + 4), fill=(240, 68, 82))
        frames.append(frame)
        durations.append(110 if item else 1150)

    palette = frames[0].quantize(colors=160, method=Image.Quantize.MEDIANCUT)
    indexed = [frames[0].quantize(palette=palette)]
    indexed.extend(frame.quantize(palette=palette) for frame in frames[1:])
    indexed[0].save(OUT / "hero-glitch.gif", save_all=True, append_images=indexed[1:],
                    duration=durations, loop=0, optimize=True, disposal=2)


PROJECTS = [
    ("parkwise", "Parkwise", "Parking operations", "Allocation · visitor holds · maintenance reports", "React · TypeScript · Vite", "M 0 195 H1200", '<rect x="1051" y="78" width="82" height="82" rx="4"/><path d="M1070 99h44v40h-44zM1082 99v40M1102 99v40M1070 119h44"/><text x="1089" y="191" text-anchor="middle" font-size="12" fill="#f04452">P</text>'),
    ("credence", "Credence", "Certificate issue and verification", "HMAC integrity · audit history", "React · Express · SQLite", "M 20 205 H1180", '<path d="M1059 78h66v74h-66zM1071 96h42M1071 108h42M1071 120h29M1075 152l-5 24 14-8 14 8-5-24"/><circle cx="1092" cy="139" r="14"/>'),
    ("scholarship-aid", "Scholarship & Aid", "Scholarship and financial aid workflows", "Eligibility · applications · institutional decisions", "Java · Next.js · JDBC", "M 0 215 H1200", '<path d="M1065 77h47l19 19v74h-66zM1112 77v20h19M1077 116h42M1077 129h42M1077 142h31"/><path d="M1070 96h38"/>'),
    ("smarthealth", "SmartHealth", "Educational patient records", "Java thread-pool benchmarks", "Java · Spring Boot · React", "M 25 205 H1175", '<path d="M1046 120h25l12-25 21 51 14-30 10 4h35"/><circle cx="1046" cy="120" r="3" fill="#f04452"/><circle cx="1163" cy="120" r="3" fill="#f04452"/>'),
]


def project_panel():
    for index, (slug, name, title, details, stack, rule, motif) in enumerate(PROJECTS):
        panel = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 240" role="img" aria-labelledby="title desc">
<title id="title">{escape(name)} project</title><desc id="desc">{escape(title)}. {escape(details)}. Built with {escape(stack)}.</desc>
<rect width="1200" height="240" rx="6" fill="{BG}"/><rect x=".5" y=".5" width="1199" height="239" rx="6" fill="none" stroke="{LINE}"/>
<path d="{rule}" stroke="{RED}" stroke-opacity=".58"/>
<path d="M985 0v240M1000 0v240" stroke="{LINE}"/>
<g class="project-mark" style="animation-delay:{index*.7:.1f}s" fill="none" stroke="{RED}" stroke-opacity=".82" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" font-family="system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif">{motif}</g>
<g font-family="system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif"><text x="40" y="49" fill="{MUTED}" font-size="15" font-weight="600" letter-spacing="1.2">SELECTED PROJECT</text>
<text x="38" y="107" fill="{FG}" font-size="42" font-weight="700">{escape(name)}</text><text x="40" y="147" fill="#c9d1d9" font-size="20">{escape(title)}</text>
<text x="40" y="181" fill="{MUTED}" font-size="17">{escape(details)}</text><text x="40" y="218" fill="{RED}" font-size="16" font-weight="600">{escape(stack)}</text>
<text x="1005" y="213" fill="{MUTED}" font-size="14" font-weight="600" letter-spacing=".5">REPOSITORY</text></g>
<style>.project-mark{{transform-box:fill-box;transform-origin:center;animation:mark-breathe 7s ease-in-out infinite}}@keyframes mark-breathe{{0%,76%,100%{{transform:scale(1);opacity:.82}}82%{{transform:scale(1.06);opacity:1}}88%{{transform:scale(.99);opacity:.88}}}}@media(prefers-reduced-motion:reduce){{.project-mark{{animation:none}}}}</style></svg>'''
        (OUT / f"project-{slug}.svg").write_text(panel)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    hero()
    hero_glitch()
    project_panel()
    print("Generated Spider-Man hero and GitHub-native project panels")
