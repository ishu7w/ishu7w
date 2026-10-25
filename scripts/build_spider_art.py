"""Build the Spider-Man hero and restrained GitHub-native project panels."""
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "assets" / "spider" / "references"
OUT = ROOT / "assets" / "spider"
W, H = 1200, 520


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(f"/System/Library/Fonts/Supplemental/{name}.ttf", size)


def cover(path: Path, size: tuple[int, int], centering=(0.5, 0.5)) -> Image.Image:
    image = Image.open(path).convert("RGB")
    return ImageOps.fit(image, size, Image.Resampling.LANCZOS, centering=centering)


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
    neon = cover(REF / "glitch-spider.jpeg", (W, H), (0.52, 0.43))
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
    d.text((190, 127), "FRIENDLY NEIGHBORHOOD DEVELOPER", font=font("Arial Bold", 16), fill=(255, 61, 105, 255))
    d.line((190, 158, 506, 158), fill=(255, 63, 103, 205), width=2)
    d.text((x, 212), "BUILDING THE", font=font("DIN Condensed Bold", 55), fill=(245, 245, 248, 255))
    d.text((x - 2, 258), "NEXT WEB", font=font("DIN Condensed Bold", 80), fill=(255, 39, 84, 255), stroke_width=1, stroke_fill=(255, 165, 185, 130))
    d.text((x + 2, 354), "JAVA  /  FULL-STACK  /  PRACTICAL AI", font=font("Arial Bold", 16), fill=(229, 225, 233, 255))
    d.text((x + 2, 389), "OPEN SOURCE  ·  BUILD WITH PURPOSE", font=font("Arial", 16), fill=(195, 187, 200, 255))

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
    d.text((52, 496), "EARTH-616  /  OPEN-SOURCE CONTRIBUTOR  /  ALWAYS IN YOUR CORNER", font=font("Arial Bold", 14), fill=(227, 220, 231, 230))
    base.convert("RGB").save(OUT / "hero.jpg", quality=91, optimize=True)



def hero_glitch():
    """Glitch the Spider-Man figure and the white spider emblem in the hero."""
    source = Image.open(OUT / "hero.jpg").convert("RGB")
    frames, durations = [], []
    # Mostly hold the approved hero still; short red-channel shears interrupt it.
    sequence = [None, None, None,
                ((116, 18, 46), (160, 10, -29)),
                ((248, 22, -48), (299, 16, 34), (347, 11, -26)),
                None, None, None,
                ((177, 13, 38), (219, 9, -25)),
                ((321, 22, -42), (353, 10, 28)), None]
    for frame_index, item in enumerate(sequence):
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
            if frame_index in (3, 4, 8, 9):
                # Brief white cuts hit the emblem too, while leaving its outline clear.
                y = 98 + (frame_index % 2) * 15
                shift = 11 if frame_index % 2 else -9
                emblem_slice = source.crop((57, y, 167, y + 8))
                frame.paste(emblem_slice, (57 + shift, y))
                ImageDraw.Draw(frame).line((65, y + 2, 150, y + 2), fill=(255, 237, 245), width=1)
        frames.append(frame)
        durations.append(110 if item else 1150)

    palette = frames[0].quantize(colors=160, method=Image.Quantize.MEDIANCUT)
    indexed = [frames[0].quantize(palette=palette)]
    indexed.extend(frame.quantize(palette=palette) for frame in frames[1:])
    indexed[0].save(OUT / "hero-glitch.gif", save_all=True, append_images=indexed[1:],
                    duration=durations, loop=0, optimize=True, disposal=2)


PROJECTS = [
    ("parkwise", "Parkwise", "Parking operations", "Allocation · visitor holds · maintenance reports", "React · TypeScript · Vite"),
    ("credence", "Credence", "Certificate issue and verification", "HMAC integrity · audit history", "React · Express · SQLite"),
    ("scholarship-aid", "Scholarship & Aid", "Scholarship and financial aid workflows", "Eligibility · applications · institutional decisions", "Java · Next.js · JDBC"),
    ("smarthealth", "SmartHealth", "Educational patient records", "Java thread-pool benchmarks", "Java · Spring Boot · React"),
]


def save_gif(frames, path: Path, durations, disposal=2):
    palette = frames[0].convert("RGB").quantize(colors=160, method=Image.Quantize.MEDIANCUT)
    indexed = [frames[0].convert("RGB").quantize(palette=palette)]
    indexed.extend(frame.convert("RGB").quantize(palette=palette) for frame in frames[1:])
    indexed[0].save(path, save_all=True, append_images=indexed[1:], duration=durations,
                    loop=0, optimize=True, disposal=disposal)


def signal_poster(frame_index=0):
    """Composite a transparent neon-spider cutout with a moving hexadecimal field."""
    width, height = 1200, 380
    image = Image.new("RGB", (width, height), (7, 8, 14))
    d = ImageDraw.Draw(image)
    # Low-contrast dot texture ties this signal panel to the hero.
    for y in range(12, height, 12):
        for x in range(12, width, 12):
            if (x * 5 + y * 3) % 17 == 0:
                d.point((x, y), fill=(42, 20, 39))
    # A soft magenta haze anchors the cutout without a card or image frame.
    glow = Image.new("RGBA", image.size, (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse((850, -30, 1235, 410), fill=(106, 10, 57, 70))
    glow = glow.filter(ImageFilter.GaussianBlur(52))
    image = Image.alpha_composite(image.convert("RGBA"), glow).convert("RGB")

    # Matrix-like hexadecimal columns scroll behind the spider cutout.
    matrix = Image.new("RGBA", image.size, (0, 0, 0, 0))
    md = ImageDraw.Draw(matrix)
    code_font = font("Arial Bold", 17)
    glyphs = "0123456789ABCDEF"
    for col, x in enumerate(range(10, 1190, 29)):
        shift = (frame_index * (3 + col % 4)) % 420
        for row, y in enumerate(range(-24, 405, 22)):
            yy = (y - shift) % 420 - 18
            glyph = glyphs[(col * 11 + row * 7 + frame_index // 2) % len(glyphs)]
            alpha = 150 if (row + col + frame_index // 3) % 7 == 0 else 60
            md.text((x, yy), glyph, font=code_font, fill=(255, 56, 160, alpha))
    image = Image.alpha_composite(image.convert("RGBA"), matrix).convert("RGB")

    # Keep the left-side quote readable while the number field continues behind it.
    shade = Image.new("RGBA", image.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shade)
    for x in range(710):
        alpha = int(118 * max(0, 1 - x / 710) ** 1.5)
        sd.line((x, 0, x, height), fill=(7, 8, 14, alpha))
    image = Image.alpha_composite(image.convert("RGBA"), shade).convert("RGB")

    # Keep the Spider-Man line and its coding interpretation clear on the left.
    d = ImageDraw.Draw(image)
    d.text((55, 68), "WITH GREAT POWER", font=font("DIN Condensed Bold", 60), fill=(248, 245, 250))
    d.text((55, 125), "COMES GREAT RESPONSIBILITY", font=font("DIN Condensed Bold", 40), fill=(255, 49, 129), stroke_width=1, stroke_fill=(255, 205, 230))
    d.text((57, 192), "Write code that makes a difference.", font=font("Arial Bold", 21), fill=(235, 222, 234))
    d.text((57, 229), "Build with care. Use your skills to help.", font=font("Arial", 18), fill=(201, 184, 204))
    d.line((57, 279, 580, 279), fill=(255, 65, 139, 150), width=1)
    d.text((57, 318), "ISHU PATEL  ·  JAVA  ·  FULL-STACK  ·  OPEN SOURCE", font=font("Arial Bold", 15), fill=(201, 179, 202))

    source = Image.open(REF / "glitch-spider.jpeg").convert("RGB")
    portrait = ImageOps.fit(source, (250, 360), Image.Resampling.LANCZOS, centering=(0.5, 0.47))
    portrait = ImageEnhance.Color(portrait).enhance(1.12)
    portrait = ImageEnhance.Contrast(portrait).enhance(1.08)
    # Turn the source's near-black wallpaper transparent so the code field shows through.
    matte = Image.new("L", portrait.size)
    source_pixels, matte_pixels = portrait.load(), matte.load()
    for y in range(portrait.height):
        for x in range(portrait.width):
            red, green, blue = source_pixels[x, y]
            brightness = max(red, green, blue)
            matte_pixels[x, y] = min(255, max(0, int((brightness - 24) * 1.7)))
    # Occasional horizontal cuts break the image into deliberate digital slices.
    if frame_index in (6, 7, 18, 19, 20):
        y, band_h, shift = (88, 12, 19) if frame_index % 2 else (222, 17, -15)
        strip = portrait.crop((0, y, portrait.width, y + band_h))
        portrait.paste(strip, (shift, y))
        ImageDraw.Draw(portrait).line((0, y + band_h - 2, 70, y + band_h - 2), fill=(255, 230, 247), width=2)
    image.paste(portrait, (910, 10), matte)
    return image


def build_signal_animation():
    frames = [signal_poster(i) for i in range(32)]
    frames[0].save(OUT / "signal-poster.png", optimize=True)
    save_gif(frames, OUT / "signal-poster.gif", [180] * len(frames))



def project_frame(project, frame_index):
    slug, name, subtitle, details, stack = project
    width, height = 1200, 250
    image = Image.new("RGB", (width, height), (8, 9, 15))
    d = ImageDraw.Draw(image)

    # Sakura blooms frame the showcase, echoing the supplied reference image.
    sakura = Image.open(REF / "red-sakura.jpeg").convert("RGB")
    for box, target, xy, fade_direction in (
        ((0, 0, 360, 300), (350, 180), (-8, -16), "down"),
        ((255, 890, 675, 1200), (360, 220), (850, 54), "up"),
    ):
        bloom = sakura.crop(box).resize(target, Image.Resampling.LANCZOS)
        bloom = ImageEnhance.Color(bloom).enhance(1.6)
        bloom = ImageEnhance.Brightness(bloom).enhance(0.78)
        alpha = Image.new("L", target, 142)
        alpha_pixels = alpha.load()
        for by in range(target[1]):
            for bx in range(target[0]):
                if fade_direction == "down":
                    fade = max(0.12, 1 - by / target[1])
                else:
                    fade = max(0.12, bx / target[0])
                alpha_pixels[bx, by] = int(142 * fade)
        bloom = bloom.convert("RGBA")
        bloom.putalpha(alpha)
        image = Image.alpha_composite(image.convert("RGBA"), Image.new("RGBA", image.size))
        image.alpha_composite(bloom, xy)
        image = image.convert("RGB")

    # Low, animated magenta halos make the centerpiece and project mark glow.
    pulse = 0.88 + 0.12 * math.sin(frame_index * math.pi / 10)
    halo = Image.new("RGBA", image.size, (0, 0, 0, 0))
    hd = ImageDraw.Draw(halo)
    hd.ellipse((736, 18, 954, 238), fill=(255, 37, 115, int(58 * pulse)))
    hd.ellipse((988, 20, 1192, 224), fill=(255, 24, 86, int(64 * pulse)))
    halo = halo.filter(ImageFilter.GaussianBlur(28))
    image = Image.alpha_composite(image.convert("RGBA"), halo).convert("RGB")

    # Add the supplied chrome Y2K mark as the shared centerpiece of each panel.
    chrome = Image.open(REF / "chrome-y2k.jpeg").convert("RGB").crop((55, 290, 665, 1000))
    chrome = ImageOps.fit(chrome, (172, 172), Image.Resampling.LANCZOS)
    chrome_rgba = chrome.convert("RGBA")
    chrome_pixels = chrome_rgba.load()
    for cyi in range(chrome.height):
        for cxi in range(chrome.width):
            red, green, blue, _ = chrome_pixels[cxi, cyi]
            light = max(red, green, blue)
            chrome_pixels[cxi, cyi] = (red, green, blue, min(255, max(0, int((light - 16) * 1.35))))
    chrome_rgba = ImageEnhance.Brightness(chrome_rgba).enhance(1.08)
    image = image.convert("RGBA")
    image.alpha_composite(chrome_rgba, (760, 39))
    image = image.convert("RGB")

    # Glowing petals fall on a staggered loop with a small sideways sway.
    petals = Image.new("RGBA", image.size, (0, 0, 0, 0))
    pd = ImageDraw.Draw(petals)
    for index in range(7):
        phase = 2 * math.pi * (frame_index / 20 + index / 7)
        travel = height + 28
        x = 600 + index * 84 + 24 * math.sin(phase)
        y = (frame_index * travel / 20 + index * travel / 7) % travel - 14
        angle = 24 * math.sin(phase + index)
        scale = 4
        petal = Image.new("RGBA", (32 * scale, 19 * scale), (0, 0, 0, 0))
        pdraw = ImageDraw.Draw(petal)
        def bezier(p0, p1, p2, p3):
            points = []
            for step in range(33):
                t = step / 32
                u = 1 - t
                points.append(tuple(round(scale * (u**3 * p0[axis] + 3*u*u*t*p1[axis] + 3*u*t*t*p2[axis] + t**3*p3[axis])) for axis in (0, 1)))
            return points
        outline = bezier((1, 10), (7, 0), (23, -2), (31, 8)) + bezier((31, 8), (23, 16), (8, 22), (1, 10))[1:]
        pdraw.polygon(outline, fill=(205, 30, 70, 138))
        pdraw.line(((4*scale, 11*scale), (15*scale, 8*scale), (28*scale, 8*scale)), fill=(255, 115, 151, 145), width=scale)
        petal = petal.resize((32, 19), Image.Resampling.LANCZOS)
        petal = petal.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)
        petals.alpha_composite(petal, (int(x), int(y)))
    petal_glow_alpha = petals.getchannel("A").filter(ImageFilter.GaussianBlur(7))
    petal_glow = Image.new("RGBA", image.size, (255, 44, 120, 0))
    petal_glow.putalpha(petal_glow_alpha.point(lambda alpha: min(130, int(alpha * 1.5))))
    image = Image.alpha_composite(image.convert("RGBA"), petal_glow)
    image = Image.alpha_composite(image, petals).convert("RGB")

    # A soft ink wash keeps text crisp over the floral photography.
    wash = Image.new("RGBA", image.size, (0, 0, 0, 0))
    wd = ImageDraw.Draw(wash)
    for x in range(800):
        alpha = int(205 * max(0, 1 - x / 800) ** 1.5)
        wd.line((x, 0, x, height), fill=(7, 8, 14, alpha))
    image = Image.alpha_composite(image.convert("RGBA"), wash).convert("RGB")
    d = ImageDraw.Draw(image)
    # Sparse web geometry, confined to the right so content stays clear.
    cx, cy = 1090, 120
    for ray in range(12):
        angle = math.pi * 2 * ray / 12
        d.line((cx, cy, cx + 155 * math.cos(angle), cy + 155 * math.sin(angle)), fill=(53, 22, 43), width=1)
    for radius in (56, 84, 116):
        d.arc((cx-radius, cy-radius, cx+radius, cy+radius), 0, 360, fill=(61, 24, 47), width=1)
    for y in range(20, height, 12):
        for x in range(20, 970, 12):
            if (x * 2 + y * 3) % 23 == 0:
                d.point((x, y), fill=(25, 18, 29))

    # Divider and typography follow the older ink/scarlet Spider-Man styling.
    d.line((0, 228, width, 228), fill=(155, 32, 68), width=1)
    d.line((980, 0, 980, height), fill=(57, 37, 52), width=1)
    d.text((42, 30), "PROJECT  /  " + name.upper(), font=font("Arial Bold", 16), fill=(255, 99, 146))
    title_font = font("Arial Bold", 40 if len(name) < 17 else 34)
    d.text((40, 66), name, font=title_font, fill=(248, 245, 249))
    d.text((43, 121), subtitle, font=font("Arial", 20), fill=(220, 214, 223))
    d.text((43, 158), details, font=font("Arial", 16), fill=(185, 176, 190))
    d.text((43, 197), stack, font=font("Arial Bold", 16), fill=(255, 86, 139))

    if slug == "parkwise":
        x0, y0 = 1040, 65
        for i in range(12):
            x, y = x0 + (i % 3) * 36, y0 + (i // 3) * 34
            active = i == frame_index % 12
            box = (255, 59, 128) if active else (123, 48, 85)
            d.rounded_rectangle((x, y, x+25, y+25), radius=3, outline=box, width=2)
            if active:
                d.ellipse((x+8, y+8, x+17, y+17), fill=(255, 216, 237))
    elif slug == "credence":
        phase = frame_index * math.pi / 10
        d.ellipse((1043, 66, 1137, 160), outline=(143, 42, 81), width=2)
        r = 30
        pts = []
        for k in range(4):
            a = phase + math.pi / 4 + k * math.pi / 2
            pts.append((1090 + r * math.cos(a), 112 + r * math.sin(a)))
        d.polygon(pts, outline=(255, 73, 149))
        d.line((1072, 178, 1110, 178), fill=(255, 73, 149), width=2)
        d.line((1079, 188, 1103, 188), fill=(123, 48, 85), width=2)
    elif slug == "scholarship-aid":
        lift = round(3 * math.sin(frame_index * math.pi / 10))
        x, y = 1055, 58 + lift
        d.rounded_rectangle((x, y, x+78, y+108), radius=4, outline=(255, 73, 149), width=2)
        d.line((x+14, y+23, x+64, y+23), fill=(199, 72, 124), width=2)
        d.line((x+14, y+39, x+64, y+39), fill=(123, 48, 85), width=2)
        d.line((x+14, y+55, x+54, y+55), fill=(123, 48, 85), width=2)
        if frame_index % 20 > 8:
            d.line((x+17, y+79, x+29, y+91, x+57, y+66), fill=(255, 73, 149), width=3)
    else:
        points = [(1020, 122), (1040, 122), (1052, 98), (1068, 151), (1083, 111), (1094, 122), (1126, 122), (1143, 122)]
        d.line(points, fill=(191, 48, 105), width=3, joint="curve")
        phase = frame_index % 16
        point = points[min(phase // 2, len(points)-1)]
        radius = 7 + int(2 * math.sin(frame_index * math.pi / 4))
        d.ellipse((point[0]-radius, point[1]-radius, point[0]+radius, point[1]+radius), fill=(255, 88, 150))
        d.ellipse((point[0]-3, point[1]-3, point[0]+3, point[1]+3), fill=(255, 238, 246))
    return image


def build_project_animations():
    for project in PROJECTS:
        frames = [project_frame(project, i) for i in range(20)]
        frames[0].save(OUT / f"project-{project[0]}-static.png", optimize=True)
        save_gif(frames, OUT / f"project-{project[0]}.gif", [160] * len(frames), disposal=1)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    hero()
    hero_glitch()
    build_signal_animation()
    build_project_animations()
    print("Generated Spider-Man hero, glitch-spider signal, and animated project panels")
