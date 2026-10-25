"""Build the Spider-Verse artwork used by the GitHub profile README."""
from pathlib import Path
from html import escape
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
    # One wide, directly linked-style showcase panel per project, as in the reference profile.
    projects = [
        ("01", "PARKWISE", "Parking operations, mapped clearly.", "ALLOCATION  /  VISITOR HOLDS  /  REPORTING", "REACT  ·  TYPESCRIPT  ·  VITE", "#ff3d69", "M 850 20 L 1120 20 L 1010 215 L 780 215 Z"),
        ("02", "CREDENCE", "A trustworthy path from issue to verify.", "HMAC INTEGRITY  /  AUDIT HISTORY", "REACT  ·  EXPRESS  ·  SQLITE", "#ff497b", "M 920 20 L 1170 20 L 1040 215 L 800 215 Z"),
        ("03", "SCHOLARSHIP & AID", "Make eligibility and decisions easier to follow.", "APPLICATIONS  /  INSTITUTIONAL REVIEW", "JAVA  ·  NEXT.JS  ·  JDBC", "#f23d64", "M 840 20 L 1115 20 L 995 215 L 765 215 Z"),
        ("04", "SMARTHEALTH", "Patient records meet measured concurrency.", "EDUCATIONAL RECORDS  /  THREAD-POOL BENCHMARKS", "JAVA  ·  SPRING BOOT  ·  REACT", "#ff5778", "M 900 20 L 1160 20 L 1040 215 L 800 215 Z"),
    ]
    for number, name, hook, scope, stack, accent, shard in projects:
        safe_id = name.lower().replace(" & ", "-").replace(" ", "-")
        title, hook_svg, scope_svg, stack_svg = map(escape, (name, hook, scope, stack))
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 240" role="img" aria-labelledby="title desc">
<title id="title">{title} project showcase</title><desc id="desc">{hook_svg} {scope_svg}. Built with {stack_svg}.</desc>
<defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#10151f"/><stop offset=".52" stop-color="#20101a"/><stop offset="1" stop-color="#10131d"/></linearGradient><radialGradient id="glow"><stop stop-color="{accent}" stop-opacity=".24"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient></defs>
<rect width="1200" height="240" rx="22" fill="url(#bg)"/><ellipse cx="990" cy="115" rx="330" ry="190" fill="url(#glow)"/><path d="{shard}" fill="{accent}" fill-opacity=".07" stroke="{accent}" stroke-opacity=".24"/><path d="M0 194 C210 164 380 226 580 189 S920 164 1200 199" fill="none" stroke="{accent}" stroke-opacity=".28"/><g fill="none" stroke="{accent}" stroke-opacity=".16"><circle cx="1060" cy="112" r="64"/><circle cx="1060" cy="112" r="91"/><path d="M967 112h186M1060 19v186M994 46l132 132M1126 46L994 178"/></g><g font-family="Arial,sans-serif"><text x="42" y="52" fill="{accent}" font-size="13" font-weight="700" letter-spacing="4">CASE FILE  /  {number}</text><text x="40" y="113" fill="#fff" font-size="44" font-weight="700">{title}</text><text x="43" y="150" fill="#e3dce5" font-size="18">{hook_svg}</text><text x="43" y="190" fill="#ff91a9" font-size="12" font-weight="700" letter-spacing="1.4">{scope_svg}</text><rect x="822" y="173" width="334" height="34" rx="17" fill="#180d16" stroke="{accent}" stroke-opacity=".45"/><text x="844" y="195" fill="#f4e9ef" font-size="12" font-weight="700">{stack_svg}</text><text x="1012" y="148" fill="{accent}" font-size="12" font-weight="700" letter-spacing="2">OPEN REPOSITORY  ↗</text></g></svg>'''
        (OUT / f"project-{safe_id}.svg").write_text(svg)


def detail_panels():
    """Build the matching armory, contribution, and contact panels."""
    (OUT / "skills.svg").write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 230" role="img" aria-labelledby="t d"><title id="t">Developer toolkit</title><desc id="d">Four themed cards group languages, interface tools, backend and data, and workflow tools.</desc><defs><linearGradient id="b" x2="1" y2="1"><stop stop-color="#10151f"/><stop offset="1" stop-color="#190d16"/></linearGradient></defs><rect width="1200" height="230" rx="22" fill="url(#b)"/><text x="34" y="42" fill="#ff6686" font-family="Arial,sans-serif" font-size="13" font-weight="700" letter-spacing="4">THE ARMORY  /  TOOLS I BUILD WITH</text><g font-family="Arial,sans-serif"><g transform="translate(32 66)"><rect width="270" height="132" rx="16" fill="#121a25" stroke="#87304a"/><text x="18" y="34" fill="#ff6686" font-size="12" font-weight="700">01 / LANGUAGES</text><text x="18" y="72" fill="#f5f2f5" font-size="20" font-weight="700">Java</text><text x="18" y="101" fill="#c5bec9" font-size="14">TypeScript · JavaScript</text></g><g transform="translate(324 66)"><rect width="270" height="132" rx="16" fill="#121a25" stroke="#87304a"/><text x="18" y="34" fill="#ff6686" font-size="12" font-weight="700">02 / INTERFACE</text><text x="18" y="72" fill="#f5f2f5" font-size="18" font-weight="700">React · Next.js</text><text x="18" y="101" fill="#c5bec9" font-size="14">Vite · HTML · CSS</text></g><g transform="translate(616 66)"><rect width="270" height="132" rx="16" fill="#121a25" stroke="#87304a"/><text x="18" y="34" fill="#ff6686" font-size="12" font-weight="700">03 / SERVER &amp; DATA</text><text x="18" y="72" fill="#f5f2f5" font-size="18" font-weight="700">Node.js · Supabase</text><text x="18" y="101" fill="#c5bec9" font-size="14">PostgreSQL</text></g><g transform="translate(908 66)"><rect width="260" height="132" rx="16" fill="#121a25" stroke="#87304a"/><text x="18" y="34" fill="#ff6686" font-size="12" font-weight="700">04 / WORKFLOW</text><text x="18" y="72" fill="#f5f2f5" font-size="20" font-weight="700">Git · GitHub</text><text x="18" y="101" fill="#c5bec9" font-size="14">Build · review · repeat</text></g></g></svg>''')
    (OUT / "contributions.svg").write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 220" role="img" aria-labelledby="t d"><title id="t">Selected open-source contributions</title><desc id="d">Three merged pull request cards for Checkstyle, Gson, and Java Pathfinder.</desc><defs><linearGradient id="b" x2="1" y2="0"><stop stop-color="#11151d"/><stop offset=".55" stop-color="#1b0d16"/><stop offset="1" stop-color="#101321"/></linearGradient></defs><rect width="1200" height="220" rx="22" fill="url(#b)"/><text x="34" y="42" fill="#ff6686" font-family="Arial,sans-serif" font-size="13" font-weight="700" letter-spacing="4">UPSTREAM MISSIONS  /  MERGED</text><g font-family="Arial,sans-serif"><g transform="translate(32 64)"><rect width="360" height="122" rx="15" fill="#121a25" stroke="#9b3150"/><text x="18" y="33" fill="#ff6f8f" font-size="12" font-weight="700">CHECKSTYLE  ·  #21518</text><text x="18" y="64" fill="#f4f0f4" font-size="14" font-weight="700">Dotted-directory extension parsing</text><rect x="18" y="82" width="78" height="23" rx="11" fill="#17372c"/><text x="33" y="98" fill="#8cf0bc" font-size="10" font-weight="700">MERGED</text></g><g transform="translate(420 64)"><rect width="360" height="122" rx="15" fill="#121a25" stroke="#9b3150"/><text x="18" y="33" fill="#ff6f8f" font-size="12" font-weight="700">GSON  ·  #3115</text><text x="18" y="64" fill="#f4f0f4" font-size="14" font-weight="700">Faster JsonArray list-view removal</text><rect x="18" y="82" width="78" height="23" rx="11" fill="#17372c"/><text x="33" y="98" fill="#8cf0bc" font-size="10" font-weight="700">MERGED</text></g><g transform="translate(808 64)"><rect width="360" height="122" rx="15" fill="#121a25" stroke="#9b3150"/><text x="18" y="33" fill="#ff6f8f" font-size="12" font-weight="700">JAVA PATHFINDER  ·  #641</text><text x="18" y="64" fill="#f4f0f4" font-size="14" font-weight="700">Clamp position when buffer limit changes</text><rect x="18" y="82" width="78" height="23" rx="11" fill="#17372c"/><text x="33" y="98" fill="#8cf0bc" font-size="10" font-weight="700">MERGED</text></g></g></svg>''')
    (OUT / "contact.svg").write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 150" role="img" aria-labelledby="t d"><title id="t">Send Ishu a signal</title><desc id="d">Contact Ishu about practical AI, open-source Java, and hackathon collaboration.</desc><defs><linearGradient id="b"><stop stop-color="#30101f"/><stop offset=".55" stop-color="#131621"/><stop offset="1" stop-color="#10151e"/></linearGradient></defs><rect width="1200" height="150" rx="22" fill="url(#b)" stroke="#87304a"/><path d="M0 112 Q300 70 600 112T1200 108" fill="none" stroke="#ff3d70" stroke-opacity=".3"/><text x="38" y="53" fill="#fff" font-family="Arial,sans-serif" font-size="29" font-weight="700">GOOD IDEAS DESERVE DAYLIGHT.</text><text x="40" y="88" fill="#c9c1cd" font-family="Arial,sans-serif" font-size="15">Practical AI · Open-source Java · Hackathon builds</text><text x="1030" y="78" fill="#ff6686" font-family="Arial,sans-serif" font-size="15" font-weight="700">SEND A SIGNAL  ↗</text></svg>''')


def card_image(source: Path, size: tuple[int, int], centering=(0.5, 0.5)) -> Image.Image:
    image = Image.open(source).convert("RGB")
    return ImageOps.fit(image, size, Image.Resampling.LANCZOS, centering=centering)


def signal_poster(frame: int | None = None) -> Image.Image:
    """Build the glitch-signal panel with the glitch Spider as its only character image."""
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
