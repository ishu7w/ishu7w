"""Build the Spider-Verse artwork used by the GitHub profile README."""
from pathlib import Path
import math
import random

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "assets" / "spider" / "references"
OUT = ROOT / "assets" / "spider"
W, H = 1200, 520


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(f"/System/Library/Fonts/Supplemental/{name}.ttf", size)


def cover(path: Path, size: tuple[int, int], centering=(0.5, 0.5)) -> Image.Image:
    im = Image.open(path).convert("RGB")
    return ImageOps.fit(im, size, Image.Resampling.LANCZOS, centering=centering)


def draw_web(draw: ImageDraw.ImageDraw, color, width=1, offset=0):
    # Fine radial silk with subtly bowed cross threads.
    cx, cy = 1175, -38
    for i in range(12):
        angle = math.radians(112 + i * 8.5)
        ex, ey = cx + 750 * math.cos(angle), cy + 750 * math.sin(angle)
        draw.line((cx, cy, ex, ey), fill=color, width=width)
    for radius in (74, 122, 176, 238, 310, 390, 478, 565):
        pts = []
        for i in range(121):
            a = math.radians(112 + 93 * i / 120)
            wobble = math.sin(a * 3 + offset) * 2.4
            pts.append((cx + (radius + wobble) * math.cos(a), cy + (radius + wobble) * math.sin(a)))
        draw.line(pts, fill=color, width=width, joint="curve")


def hero():
    # The noir image supplies the main figure; the neon and blossom references
    # are sampled as texture, with the chrome image reduced to a glint.
    base = Image.new("RGB", (W, H), (5, 7, 12))
    neon = cover(REF / "neon-glitch.jpeg", (W, H), (0.52, 0.43))
    neon = ImageEnhance.Color(neon).enhance(1.45)
    neon = ImageEnhance.Brightness(neon).enhance(0.46)
    base = Image.blend(base, neon, 0.36)

    # Scarlet bloom texture enters from the margins, never competing with copy.
    bloom = cover(REF / "red-sakura.jpeg", (440, H), (0.5, 0.5))
    bloom = ImageEnhance.Color(bloom).enhance(1.5)
    bloom = ImageEnhance.Brightness(bloom).enhance(0.42)
    bloom_layer = Image.new("RGB", (W, H), (0, 0, 0))
    bloom_layer.paste(bloom, (W - 440, 0))
    bloom_layer = bloom_layer.filter(ImageFilter.GaussianBlur(0.5))
    base = Image.blend(base, bloom_layer, 0.56)

    # Noir figure is masked in from the right, then graded into the scene.
    noir = cover(REF / "spider-noir.jpeg", (610, H), (0.53, 0.34))
    noir = ImageOps.grayscale(noir).convert("RGB")
    noir = ImageEnhance.Contrast(noir).enhance(1.15)
    noir = ImageEnhance.Brightness(noir).enhance(0.75)
    mask = Image.new("L", (610, H), 0)
    md = ImageDraw.Draw(mask)
    for x in range(610):
        alpha = int(255 * min(1, max(0, (x - 25) / 235)))
        md.line((x, 0, x, H), fill=alpha)
    base.paste(noir, (590, 0), mask)

    # Deep ink gradient protects left-side typography and integrates source art.
    grad = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grad)
    for x in range(760):
        a = int(242 * max(0, 1 - x / 800) ** 1.8)
        gd.line((x, 0, x, H), fill=(4, 7, 13, a))
    base = Image.alpha_composite(base.convert("RGBA"), grad)

    # Halftone in the shadow field, plus a subtle red edge vignette.
    dots = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dd = ImageDraw.Draw(dots)
    for y in range(8, H, 13):
        for x in range(8, W, 13):
            if (x * 3 + y) % 5 == 0:
                dd.ellipse((x, y, x + 1.4, y + 1.4), fill=(255, 220, 235, 28))
    base = Image.alpha_composite(base, dots)

    web = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(web)
    draw_web(wd, (255, 37, 80, 38), 2, 0.4)
    base = Image.alpha_composite(base, web)
    d = ImageDraw.Draw(base)

    # White spider emblem used as a small signature mark.
    emblem = Image.open(REF / "white-spider-emblem.jpeg").convert("RGB")
    emblem = ImageOps.fit(emblem, (110, 110), Image.Resampling.LANCZOS)
    # The supplied mark is luminous white on smoke; a rounded display tile retains its glow.
    emblem = ImageEnhance.Brightness(emblem).enhance(1.5)
    em_mask = Image.new("L", (110, 110), 0)
    ImageDraw.Draw(em_mask).rounded_rectangle((0, 0, 109, 109), 55, fill=220)
    base.paste(emblem, (57, 54), em_mask)
    d = ImageDraw.Draw(base)
    d.rounded_rectangle((57, 54, 167, 164), radius=55, outline=(255, 59, 96, 180), width=2)

    x = 62
    d.text((188, 70), "ISHU PATEL", font=font("DIN Condensed Bold", 50), fill=(250, 247, 248, 255), stroke_width=0)
    d.text((190, 127), "FRIENDLY NEIGHBORHOOD DEVELOPER", font=font("Arial Bold", 13), fill=(255, 61, 105, 255))
    d.line((190, 158, 506, 158), fill=(255, 63, 103, 205), width=2)
    d.text((x, 212), "BUILDING THE", font=font("DIN Condensed Bold", 55), fill=(245, 245, 248, 255))
    d.text((x - 2, 258), "NEXT WEB", font=font("DIN Condensed Bold", 80), fill=(255, 39, 84, 255), stroke_width=1, stroke_fill=(255, 165, 185, 130))
    d.text((x + 2, 354), "JAVA  /  FULL-STACK  /  PRACTICAL AI", font=font("Arial Bold", 16), fill=(229, 225, 233, 255))
    d.text((x + 2, 389), "OPEN SOURCE  ·  BUILD WITH PURPOSE", font=font("Arial", 13), fill=(177, 177, 193, 255))

    # A chrome Y2K star glint traces the fourth reference image.
    chrome = Image.open(REF / "chrome-y2k.jpeg").convert("RGB")
    chrome = ImageOps.fit(chrome, (92, 92), Image.Resampling.LANCZOS, centering=(0.5, 0.5))
    chrome = ImageOps.grayscale(chrome).convert("RGBA")
    # Lighten the metallic center; keep the black wallpaper transparent.
    px = chrome.load()
    for yy in range(92):
        for xx in range(92):
            r, g, b, _ = px[xx, yy]
            lum = max(r, g, b)
            px[xx, yy] = (205, 220, 238, max(0, int((lum - 15) * 1.05)))
    base.alpha_composite(chrome, (1060, 35))

    # Border and compact tag line.
    d = ImageDraw.Draw(base)
    d.line((42, 486, W - 42, 486), fill=(255, 50, 95, 155), width=1)
    d.text((52, 496), "EARTH-616  /  OPEN-SOURCE CONTRIBUTOR  /  ALWAYS IN YOUR CORNER", font=font("Arial Bold", 10), fill=(227, 220, 231, 210))
    base.convert("RGB").save(OUT / "hero.jpg", quality=91, optimize=True)


def project_panel():
    # Compact illustrated project lineup; links and descriptions remain native text.
    content = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 340" role="img" aria-labelledby="title desc">
<title id="title">Ishu Patel's featured projects</title><desc id="desc">Four project cards connected by fine red web strands: Parkwise, Credence, Scholarship and Aid, and SmartHealth.</desc>
<defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#10151f"/><stop offset="1" stop-color="#190d16"/></linearGradient><linearGradient id="red"><stop stop-color="#ff315f"/><stop offset="1" stop-color="#ff7d9a"/></linearGradient><filter id="glow"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
<rect width="1200" height="340" rx="24" fill="url(#bg)"/><path d="M0 60 C180 180 260 35 410 140 S690 245 820 120 1040 25 1200 160" fill="none" stroke="#ff315f" stroke-opacity=".27" stroke-width="1.5"/><path d="M0 250 C150 130 270 280 410 190 S700 65 850 195 1050 290 1200 190" fill="none" stroke="#ec4e81" stroke-opacity=".19"/>
<g font-family="Arial,sans-serif"><text x="42" y="48" fill="#ff6285" font-size="13" font-weight="700" letter-spacing="4">FIELD NOTES  /  SELECTED BUILDS</text>
<g transform="translate(38 84)"><rect width="270" height="208" rx="18" fill="#121a25" stroke="#b32b4f"/><circle cx="227" cy="42" r="19" fill="#4a1829"/><path d="M216 42h22M227 31v22" stroke="#ff6987" stroke-width="2"/><text x="22" y="48" fill="#fff" font-size="23" font-weight="700">PARKWISE</text><text x="22" y="82" fill="#c8c5ce" font-size="14">Parking operations</text><text x="22" y="110" fill="#ff6686" font-size="12">REACT · TYPESCRIPT · VITE</text><path d="M22 146h208" stroke="#733047"/><text x="22" y="176" fill="#aaaab4" font-size="12">Allocation · holds · reporting</text></g>
<g transform="translate(333 84)"><rect width="270" height="208" rx="18" fill="#121a25" stroke="#b32b4f"/><circle cx="227" cy="42" r="19" fill="#4a1829"/><path d="M218 42l6 6 12-14" fill="none" stroke="#ff6987" stroke-width="2"/><text x="22" y="48" fill="#fff" font-size="23" font-weight="700">CREDENCE</text><text x="22" y="82" fill="#c8c5ce" font-size="14">Certificate verification</text><text x="22" y="110" fill="#ff6686" font-size="12">REACT · EXPRESS · SQLITE</text><path d="M22 146h208" stroke="#733047"/><text x="22" y="176" fill="#aaaab4" font-size="12">HMAC integrity · audit trail</text></g>
<g transform="translate(628 84)"><rect width="270" height="208" rx="18" fill="#121a25" stroke="#b32b4f"/><circle cx="227" cy="42" r="19" fill="#4a1829"/><path d="M216 36h22v13h-22zM220 32v22M234 32v22" fill="none" stroke="#ff6987" stroke-width="2"/><text x="22" y="48" fill="#fff" font-size="20" font-weight="700">SCHOLARSHIP &amp; AID</text><text x="22" y="82" fill="#c8c5ce" font-size="14">Eligibility &amp; applications</text><text x="22" y="110" fill="#ff6686" font-size="12">JAVA · NEXT.JS · JDBC</text><path d="M22 146h208" stroke="#733047"/><text x="22" y="176" fill="#aaaab4" font-size="12">Decisions · financial aid</text></g>
<g transform="translate(923 84)"><rect width="239" height="208" rx="18" fill="#121a25" stroke="#b32b4f"/><circle cx="196" cy="42" r="19" fill="#4a1829"/><path d="M186 42h20M196 32v20M190 36l12 12M202 36l-12 12" stroke="#ff6987" stroke-width="1.5"/><text x="22" y="48" fill="#fff" font-size="23" font-weight="700">SMARTHEALTH</text><text x="22" y="82" fill="#c8c5ce" font-size="14">Patient records</text><text x="22" y="110" fill="#ff6686" font-size="12">JAVA · SPRING · REACT</text><path d="M22 146h195" stroke="#733047"/><text x="22" y="176" fill="#aaaab4" font-size="12">Thread-pool benchmarks</text></g>
</g></svg>'''
    (OUT / "projects.svg").write_text(content)


def divider():
    # Render a subtle 2.5 s silk loop; all filaments remain hairline-thin.
    width, height, count = 1100, 82, 30
    frames = []
    random.seed(14)
    for frame in range(count):
        phase = 2 * math.pi * frame / count
        im = Image.new("RGBA", (width, height), (7, 9, 15, 255))
        # Soft red/magenta ambient haze.
        haze = Image.new("RGBA", im.size, (0, 0, 0, 0))
        hd = ImageDraw.Draw(haze)
        hd.ellipse((250, 6, 840, 78), fill=(110, 8, 36, 30))
        haze = haze.filter(ImageFilter.GaussianBlur(24))
        im = Image.alpha_composite(im, haze)
        for j in range(7):
            y0 = 15 + j * 8.5
            amp = 8 + (j % 3) * 2
            points = []
            for x in range(0, width + 1, 5):
                y = y0 + amp * math.sin(x / 105 + phase + j * 0.8) + 2.2 * math.sin(x / 47 - phase * 0.7 + j)
                points.append((x, y))
            # glow then fine colored core
            for color, stroke in (((255, 22, 75, 32), 7), ((255, 43, 92, 130), 2), ((255, 177, 195, 175), 1)):
                layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
                ImageDraw.Draw(layer).line(points, fill=color, width=stroke, joint="curve")
                if stroke == 7:
                    layer = layer.filter(ImageFilter.GaussianBlur(4))
                im = Image.alpha_composite(im, layer)
        d = ImageDraw.Draw(im)
        # Traveling glint points along the web.
        for k in range(3):
            x = int((frame / count + k / 3) % 1 * width)
            y = int(40 + 17 * math.sin(x / 120 + phase))
            d.ellipse((x - 3, y - 3, x + 3, y + 3), fill=(255, 160, 190, 210))
        frames.append(im.convert("RGB"))
    frames[0].save(OUT / "web-divider.gif", save_all=True, append_images=frames[1:], duration=85, loop=0, optimize=True)
    (OUT / "web-divider-still.svg").write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 82"><rect width="1100" height="82" fill="#07090f"/><g fill="none" stroke-linecap="round"><path d="M0 18 Q100 4 200 21T400 18 600 20 800 18 1000 17 1100 19M0 29Q120 42 220 26T420 32 620 28 820 31 1020 25 1100 28M0 42Q100 31 220 46T420 39 620 46 820 40 1020 45 1100 41M0 54Q100 64 220 50T420 56 620 51 820 56 1020 51 1100 54M0 68Q120 56 220 70T420 65 620 70 820 65 1020 68 1100 64" stroke="#ff315f" stroke-opacity=".68" stroke-width="1.5"/><path d="M0 18 Q100 4 200 21T400 18 600 20 800 18 1000 17 1100 19M0 42Q100 31 220 46T420 39 620 46 820 40 1020 45 1100 41" stroke="#ffc2d0" stroke-opacity=".56" stroke-width=".7"/></g></svg>''')


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    hero()
    project_panel()
    divider()
    print("Generated Spider-Verse profile artwork")
