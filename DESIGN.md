# Design plan: Spider-Verse signal

## Design brief

Turn the profile into a recognizable Spider-Man-inspired developer page while keeping it useful as a technical introduction. The visual language combines the five supplied references: noir comic contrast, red blossom and branching texture, neon-magenta glitch, chrome Y2K glints, and a luminous white spider emblem. Structurally, use Aoi-Todoo's profile as a reference for a concise navigation row followed by distinct visual project, skills, and contribution sections with readable text. The official Spider-Verse films' own description of a distinctive visual style and multiverse is a useful high-level reference for mixing comic, glitch, and noir techniques; the artwork here is composed from the user's references rather than copied promotional material.

Profile layout reference: [Aoi-Todoo](https://github.com/Aoi-Todoo).

Reference: [Sony Pictures Animation — Spider-Man: Into the Spider-Verse](https://www.sonypicturesanimation.com/projects/films/spider-man-spider-verse).

## Page plan

1. **Hero:** use the noir Spider-Man reference as the right-side focal image. Build the left-hand text area with a dark ink gradient and use the supplied emblem, neon glitch, red botanical image, and chrome image as smaller visual cues. Keep the name and core specialties readable at profile width.
2. **Feature panel:** use the supplied neon glitch spider as the focal image, with the scarlet blossom and chrome Y2K images in separate framed windows. Animate brief pixel-shear bursts on the glitch artwork only; provide a PNG still when reduced motion is preferred.
3. **Information hierarchy:** put current focus first, selected projects and their links next, technology after projects, and merged upstream contributions before contact. Use real Markdown for searchable, accessible copy and links.
4. **Projects panel:** create a restrained four-card visual summary of Parkwise, Credence, Scholarship & Aid, and SmartHealth. Pair it with native Markdown rows for source and demo links, plus prototype caveats.
5. **Publishing constraints:** GitHub profile READMEs cannot set the outer page CSS or run JavaScript. Motion is pre-rendered in a local GIF; no GSAP or Lenis runtime is applicable. GitHub controls the surrounding page background.

## Visual system

- **Palette:** ink black and midnight blue, scarlet red, hot magenta, paper white, and restrained chrome.
- **Texture:** comic halftone, a fine spider-web network, selected red botanical texture, and a soft glitch field.
- **Motion:** short, contained pixel-shear bursts on the glitch spider artwork; no moving line dividers. Project details remain still and readable.
- **Accessibility:** descriptive image alt text, native text for all important content, compact detail disclosures, and still art for reduced motion.

## Asset sources and generation

The five user-supplied JPEG references are kept in `assets/spider/references/`. `scripts/build_spider_art.py` uses those references to generate `assets/spider/hero.jpg`, `assets/spider/projects.svg`, `assets/spider/signal-poster.gif`, and `assets/spider/signal-poster.png`. Run `python3 scripts/build_spider_art.py` to rebuild these local assets.
