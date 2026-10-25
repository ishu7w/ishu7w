"""Build the Spider-Verse artwork used by the GitHub profile README."""
from pathlib import Path
import math

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
    # Keep the Spider-Man reference as the hero figure; the neon image provides
    # a restrained magenta digital texture behind him.
    base = Image.new("RGB", (W, H), (5, 7, 12))
    neon = cover(REF / "neon-glitch.jpeg", (W, H), (0.52, 0.43))
    neon = ImageEnhance.Color(neon).enhance(1.45)
    neon = ImageEnhance.Brightness(neon).enhance(0.46)
    base = Image.blend(base, neon, 0.36)

    # Spider-Man is masked in from the right, then graded into the scene.
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
<g transform="translate(628 84)"><rect width="270" height="208" rx="18" fill="#121a25" stroke="#b32b4f"/><circle cx="227" cy="42" r="19" fill="#4a1829"/><path d="M216 36h22v13h-22zM220 32v22M234 32v22" fill="none" stroke="#ff6987" stroke-width="2"/><text x="22" y="48" fill="#fff" font-size="17" font-weight="700">SCHOLARSHIP &amp; AID</text><text x="22" y="82" fill="#c8c5ce" font-size="14">Eligibility &amp; applications</text><text x="22" y="110" fill="#ff6686" font-size="12">JAVA · NEXT.JS · JDBC</text><path d="M22 146h208" stroke="#733047"/><text x="22" y="176" fill="#aaaab4" font-size="12">Decisions · financial aid</text></g>
<g transform="translate(923 84)"><rect width="239" height="208" rx="18" fill="#121a25" stroke="#b32b4f"/><circle cx="196" cy="42" r="19" fill="#4a1829"/><path d="M186 42h20M196 32v20M190 36l12 12M202 36l-12 12" stroke="#ff6987" stroke-width="1.5"/><text x="22" y="48" fill="#fff" font-size="19" font-weight="700">SMARTHEALTH</text><text x="22" y="82" fill="#c8c5ce" font-size="14">Patient records</text><text x="22" y="110" fill="#ff6686" font-size="12">JAVA · SPRING · REACT</text><path d="M22 146h195" stroke="#733047"/><text x="22" y="176" fill="#aaaab4" font-size="12">Thread-pool benchmarks</text></g>
</g></svg>'''
    (OUT / "projects.svg").write_text(content)


def detail_panels():
    """Build the matching armory, contribution, and contact panels."""
    (OUT / "skills.svg").write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 230" role="img" aria-labelledby="t d"><title id="t">Developer toolkit</title><desc id="d">Four themed cards group languages, interface tools, backend and data, and workflow tools.</desc><defs><linearGradient id="b" x2="1" y2="1"><stop stop-color="#10151f"/><stop offset="1" stop-color="#190d16"/></linearGradient></defs><rect width="1200" height="230" rx="22" fill="url(#b)"/><text x="34" y="42" fill="#ff6686" font-family="Arial,sans-serif" font-size="13" font-weight="700" letter-spacing="4">THE ARMORY  /  TOOLS I BUILD WITH</text><g font-family="Arial,sans-serif"><g transform="translate(32 66)"><rect width="270" height="132" rx="16" fill="#121a25" stroke="#87304a"/><text x="18" y="34" fill="#ff6686" font-size="12" font-weight="700">01 / LANGUAGES</text><text x="18" y="72" fill="#f5f2f5" font-size="20" font-weight="700">Java</text><text x="18" y="101" fill="#c5bec9" font-size="14">TypeScript · JavaScript</text></g><g transform="translate(324 66)"><rect width="270" height="132" rx="16" fill="#121a25" stroke="#87304a"/><text x="18" y="34" fill="#ff6686" font-size="12" font-weight="700">02 / INTERFACE</text><text x="18" y="72" fill="#f5f2f5" font-size="18" font-weight="700">React · Next.js</text><text x="18" y="101" fill="#c5bec9" font-size="14">Vite · HTML · CSS</text></g><g transform="translate(616 66)"><rect width="270" height="132" rx="16" fill="#121a25" stroke="#87304a"/><text x="18" y="34" fill="#ff6686" font-size="12" font-weight="700">03 / SERVER &amp; DATA</text><text x="18" y="72" fill="#f5f2f5" font-size="18" font-weight="700">Node.js · Supabase</text><text x="18" y="101" fill="#c5bec9" font-size="14">PostgreSQL</text></g><g transform="translate(908 66)"><rect width="260" height="132" rx="16" fill="#121a25" stroke="#87304a"/><text x="18" y="34" fill="#ff6686" font-size="12" font-weight="700">04 / WORKFLOW</text><text x="18" y="72" fill="#f5f2f5" font-size="20" font-weight="700">Git · GitHub</text><text x="18" y="101" fill="#c5bec9" font-size="14">Build · review · repeat</text></g></g></svg>''')
    (OUT / "contributions.svg").write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 220" role="img" aria-labelledby="t d"><title id="t">Selected open-source contributions</title><desc id="d">Three merged pull request cards for Checkstyle, Gson, and Java Pathfinder.</desc><defs><linearGradient id="b" x2="1" y2="0"><stop stop-color="#11151d"/><stop offset=".55" stop-color="#1b0d16"/><stop offset="1" stop-color="#101321"/></linearGradient></defs><rect width="1200" height="220" rx="22" fill="url(#b)"/><text x="34" y="42" fill="#ff6686" font-family="Arial,sans-serif" font-size="13" font-weight="700" letter-spacing="4">UPSTREAM MISSIONS  /  MERGED</text><g font-family="Arial,sans-serif"><g transform="translate(32 64)"><rect width="360" height="122" rx="15" fill="#121a25" stroke="#9b3150"/><text x="18" y="33" fill="#ff6f8f" font-size="12" font-weight="700">CHECKSTYLE  ·  #21518</text><text x="18" y="64" fill="#f4f0f4" font-size="14" font-weight="700">Dotted-directory extension parsing</text><rect x="18" y="82" width="78" height="23" rx="11" fill="#17372c"/><text x="33" y="98" fill="#8cf0bc" font-size="10" font-weight="700">MERGED</text></g><g transform="translate(420 64)"><rect width="360" height="122" rx="15" fill="#121a25" stroke="#9b3150"/><text x="18" y="33" fill="#ff6f8f" font-size="12" font-weight="700">GSON  ·  #3115</text><text x="18" y="64" fill="#f4f0f4" font-size="14" font-weight="700">Faster JsonArray list-view removal</text><rect x="18" y="82" width="78" height="23" rx="11" fill="#17372c"/><text x="33" y="98" fill="#8cf0bc" font-size="10" font-weight="700">MERGED</text></g><g transform="translate(808 64)"><rect width="360" height="122" rx="15" fill="#121a25" stroke="#9b3150"/><text x="18" y="33" fill="#ff6f8f" font-size="12" font-weight="700">JAVA PATHFINDER  ·  #641</text><text x="18" y="64" fill="#f4f0f4" font-size="14" font-weight="700">Clamp position when buffer limit changes</text><rect x="18" y="82" width="78" height="23" rx="11" fill="#17372c"/><text x="33" y="98" fill="#8cf0bc" font-size="10" font-weight="700">MERGED</text></g></g></svg>''')
    (OUT / "contact.svg").write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 150" role="img" aria-labelledby="t d"><title id="t">Send Ishu a signal</title><desc id="d">Contact Ishu about practical AI, open-source Java, and hackathon collaboration.</desc><defs><linearGradient id="b"><stop stop-color="#30101f"/><stop offset=".55" stop-color="#131621"/><stop offset="1" stop-color="#10151e"/></linearGradient></defs><rect width="1200" height="150" rx="22" fill="url(#b)" stroke="#87304a"/><path d="M0 112 Q300 70 600 112T1200 108" fill="none" stroke="#ff3d70" stroke-opacity=".3"/><text x="38" y="53" fill="#fff" font-family="Arial,sans-serif" font-size="29" font-weight="700">GOOD IDEAS DESERVE DAYLIGHT.</text><text x="40" y="88" fill="#c9c1cd" font-family="Arial,sans-serif" font-size="15">Practical AI · Open-source Java · Hackathon builds</text><text x="1030" y="78" fill="#ff6686" font-family="Arial,sans-serif" font-size="15" font-weight="700">SEND A SIGNAL  ↗</text></svg>''')


def card_image(source: Path, size: tuple[int, int], centering=(0.5, 0.5)) -> Image.Image:
    image = Image.open(source).convert("RGB")
    return ImageOps.fit(image, size, Image.Resampling.LANCZOS, centering=centering)


def signal_poster(frame: int | None = None) -> Image.Image:
    """Show all three requested references in a restrained neon signal board."""
    width, height = 1200, 410
    poster = Image.new("RGB", (width, height), (5, 7, 13))
    # Low, static pools of color give this section its own backdrop.
    haze = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    h = ImageDraw.Draw(haze)
    h.ellipse((270, -80, 890, 480), fill=(94, 8, 39, 90))
    h.ellipse((810, -100, 1280, 430), fill=(19, 24, 78, 72))
    poster = Image.alpha_composite(poster.convert("RGBA"), haze.filter(ImageFilter.GaussianBlur(66)))
    d = ImageDraw.Draw(poster)

    # Fine static grain/grid, as in a cyberpunk monitor. Nothing sweeps or moves.
    for x in range(20, width, 32):
        d.line((x, 20, x, height - 20), fill=(255, 255, 255, 9), width=1)
    for y in range(20, height, 32):
        d.line((20, y, width - 20, y), fill=(255, 255, 255, 9), width=1)
    for y in range(27, height - 20, 10):
        for x in range(27, width - 20, 10):
            if (x * 7 + y * 3) % 11 == 0:
                d.ellipse((x, y, x + 1, y + 1), fill=(255, 74, 127, 27))

    d.rounded_rectangle((18, 18, width - 18, height - 18), radius=22, outline=(255, 55, 103, 115), width=1)
    d.text((43, 47), "ISHU PATEL  /  SPIDER-SIGNAL", font=font("Arial Bold", 12), fill=(255, 121, 159, 255))
    d.text((40, 102), "NEON", font=font("DIN Condensed Bold", 62), fill=(250, 247, 251, 255))
    d.text((38, 153), "SPIDER", font=font("DIN Condensed Bold", 75), fill=(255, 43, 93, 255), stroke_width=1, stroke_fill=(255, 186, 204, 160))
    d.text((44, 244), "SIGNAL UNSTABLE", font=font("Arial Bold", 13), fill=(239, 228, 236, 245))
    d.text((44, 272), "GLITCH MODE // ACTIVE", font=font("Arial", 12), fill=(188, 166, 185, 245))
    d.text((44, 337), "FRIENDLY NEIGHBORHOOD DEVELOPER  ·  EARTH-616", font=font("Arial Bold", 9), fill=(255, 121, 159, 230))

    # The glitching Spider-Man reference is the sole image in this feature panel.
    x, y, w, image_h = 905, 40, 250, 330
    image = card_image(REF / "neon-glitch.jpeg", (w, image_h), (0.5, 0.34))
    poster.paste(image, (x, y))
    d = ImageDraw.Draw(poster)
    d.rounded_rectangle((x - 4, y - 4, x + w + 4, y + image_h + 4), radius=12, outline=(255, 95, 139, 210), width=1)
    d.text((x, y + image_h + 13), "GLITCH SIGNAL  /  ACTIVE", font=font("Arial Bold", 10), fill=(242, 224, 236, 235))
    image_region = (x, y, w, image_h)

    # Short, contained pixel-shear bursts on the glitch spider only.
    # Most frames are stable; bursts read as digital signal corruption, not moving lines.
    if frame is not None and image_region and frame in {3, 4, 5, 12, 13, 21, 22}:
        x, y, w, h = image_region
        offsets = {3: (40, -7), 4: (92, 8), 5: (172, -6), 12: (58, 7), 13: (212, -8), 21: (118, 6), 22: (25, -9)}
        band_y, shift = offsets[frame]
        band_h = 19 if frame % 2 else 12
        crop_x = max(0, -shift)
        crop_end = min(w, w - shift)
        strip = poster.crop((x + crop_x, y + band_y, x + crop_end, y + band_y + band_h))
        poster.paste(strip, (x + crop_x + shift, y + band_y))
        d = ImageDraw.Draw(poster)
        # A few short magenta/cyan fragments add chromatic aberration without scanlines.
        d.rectangle((x + (frame * 17) % (w - 30), y + band_y + 2, x + (frame * 17) % (w - 30) + 26, y + band_y + 4), fill=(255, 49, 129, 240))
        d.rectangle((x + (frame * 31) % (w - 22), y + band_y + 10, x + (frame * 31) % (w - 22) + 18, y + band_y + 12), fill=(80, 241, 255, 210))
    # Flatten translucent grid, glows, and type onto the dark plate before RGB export.
    opaque = Image.new("RGBA", poster.size, (5, 7, 13, 255))
    return Image.alpha_composite(opaque, poster).convert("RGB")


def make_signal_art():
    frames = [signal_poster(frame) for frame in range(24)]
    frames[0].save(OUT / "signal-poster.png", optimize=True)
    frames[0].save(OUT / "signal-poster.gif", save_all=True, append_images=frames[1:], duration=95, loop=0, optimize=True)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    hero()
    project_panel()
    detail_panels()
    make_signal_art()
    print("Generated Spider-Verse profile artwork")
