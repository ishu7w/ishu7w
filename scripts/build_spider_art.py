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


def save_gif(frames, path: Path, durations):
    palette = frames[0].convert("RGB").quantize(colors=160, method=Image.Quantize.MEDIANCUT)
    indexed = [frames[0].convert("RGB").quantize(palette=palette)]
    indexed.extend(frame.convert("RGB").quantize(palette=palette) for frame in frames[1:])
    indexed[0].save(path, save_all=True, append_images=indexed[1:], duration=durations,
                    loop=0, optimize=True, disposal=2)


def spider_code_mask():
    """Extract the magenta spider shape as a mask; render it with digits, not a photo tile."""
    source = Image.open(REF / "glitch-spider.jpeg").convert("RGB")
    source = source.crop((105, 95, 655, 1308))
    mask = Image.new("L", source.size, 0)
    src, dst = source.load(), mask.load()
    for y in range(source.height):
        for x in range(source.width):
            red, green, blue = src[x, y]
            if red > green * 1.15 and blue > green * 1.08:
                pink_signal = min(red, blue) - green
                dst[x, y] = max(0, min(255, int((pink_signal - 8) * 4.2)))
    mask = mask.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(0.7))
    return mask.resize((300, 365), Image.Resampling.LANCZOS)


def signal_poster(frame_index=0, spider_mask=None):
    """Render the supplied spider silhouette as part of the moving hexadecimal field."""
    width, height = 1200, 380
    image = Image.new("RGB", (width, height), (7, 8, 14))
    d = ImageDraw.Draw(image)
    # Low-contrast dot texture ties this signal panel to the hero.
    for y in range(12, height, 12):
        for x in range(12, width, 12):
            if (x * 5 + y * 3) % 17 == 0:
                d.point((x, y), fill=(42, 20, 39))
    # Ambient color sits beneath one continuous matrix; there is no portrait tile.
    glow = Image.new("RGBA", image.size, (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse((820, -30, 1200, 410), fill=(106, 10, 57, 60))
    glow = glow.filter(ImageFilter.GaussianBlur(52))
    image = Image.alpha_composite(image.convert("RGBA"), glow).convert("RGB")

    if spider_mask is None:
        spider_mask = spider_code_mask()
    spider_x, spider_y = 850, 7
    cell_w, cell_h = 13, 15
    code_font = font("Arial Bold", 14)
    glyphs = "0123456789ABCDEF"
    matrix = Image.new("RGBA", image.size, (0, 0, 0, 0))
    md = ImageDraw.Draw(matrix)
    for col, x in enumerate(range(690, 1195, cell_w)):
        column_phase = (frame_index * (1 + col % 3)) % 24
        for row, y in enumerate(range(8, 380, cell_h)):
            mask_x = x - spider_x
            mask_y = y - spider_y
            strength = 0
            if 0 <= mask_x < spider_mask.width and 0 <= mask_y < spider_mask.height:
                strength = spider_mask.getpixel((mask_x, mask_y))
            # Bright glyphs trace the supplied silhouette; subdued ones keep the
            # number field continuous around it. Values scroll independently by column.
            code_row = row + column_phase
            glyph = glyphs[(col * 11 + code_row * 7 + frame_index // 2) % len(glyphs)]
            if strength > 12:
                alpha = min(255, 150 + strength)
                color = (255, 238, 247, alpha) if strength > 92 and (row + col + frame_index) % 3 == 0 else (255, 56, 160, alpha)
            else:
                alpha = 28 + ((row + col * 3 + frame_index // 2) % 5) * 9
                color = (222, 48, 133, alpha)
            glitch_shift = 0
            if frame_index in (6, 7, 18, 19, 20) and row in range(8, 13):
                glitch_shift = 3 if frame_index % 2 else -2
            md.text((x + glitch_shift, y), glyph, font=code_font, fill=color)
            if strength > 120 and frame_index in (6, 7, 18, 19, 20) and row in (9, 10):
                md.line((x - 2, y + 5, x + 11, y + 5), fill=(255, 238, 247, 180), width=1)
    image = Image.alpha_composite(image.convert("RGBA"), matrix).convert("RGB")

    # Strong, readable type remains fixed while only the signal field moves.
    d = ImageDraw.Draw(image)
    d.text((55, 56), "SPIDER-SIGNAL  /  DIGITAL TRACE", font=font("Arial Bold", 17), fill=(255, 111, 176))
    d.text((50, 126), "GLITCH", font=font("DIN Condensed Bold", 76), fill=(248, 245, 250))
    d.text((48, 193), "SPIDER", font=font("DIN Condensed Bold", 84), fill=(255, 49, 129), stroke_width=1, stroke_fill=(255, 205, 230))
    d.text((55, 254), "The supplied spider image rebuilt as moving magenta code.", font=font("Arial", 19), fill=(214, 205, 217))
    d.text((55, 328), "ISHU PATEL  ·  JAVA  ·  FULL-STACK  ·  OPEN SOURCE", font=font("Arial Bold", 15), fill=(185, 164, 185))

    return image


def build_signal_animation():
    spider_mask = spider_code_mask()
    frames = [signal_poster(i, spider_mask) for i in range(32)]
    frames[0].save(OUT / "signal-poster.png", optimize=True)
    save_gif(frames, OUT / "signal-poster.gif", [180] * len(frames))


def project_frame(project, frame_index):
    slug, name, subtitle, details, stack = project
    width, height = 1200, 250
    image = Image.new("RGB", (width, height), (8, 9, 15))
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
        save_gif(frames, OUT / f"project-{project[0]}.gif", [160] * len(frames))


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    hero()
    hero_glitch()
    build_signal_animation()
    build_project_animations()
    print("Generated Spider-Man hero, glitch-spider signal, and animated project panels")
