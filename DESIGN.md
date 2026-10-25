# Design plan: Spider-Verse signal

## Design brief

Turn the profile into a recognizable Spider-Man-inspired developer page while keeping it useful as a technical introduction. Keep the user's Spider-Man hero and make the supplied magenta glitch Spider the only additional character picture. Use the scarlet, ink, magenta, and halftone palette across the skills, project, contribution, and contact panels. Structurally, use Aoi-Todoo's profile as a reference for a concise navigation row followed by distinct visual sections with readable text. The artwork is composed from user-supplied images and custom vector panels.

Profile layout reference: [Aoi-Todoo](https://github.com/Aoi-Todoo).

## Page plan

1. **Hero:** preserve the Spider-Man hero artwork and headline; use a restrained dark and magenta grade with clear title space.
2. **Glitch feature:** show the supplied neon Spider image alone in its own framed panel. Animate brief pixel-shear bursts on that image only; provide a PNG still when reduced motion is preferred.
3. **Full-profile system:** carry the same palette and panel design through the skills, four-project, merged-contribution, and contact sections. Keep each panel paired with native Markdown links and explanatory text.
4. **Information hierarchy:** put current focus first, selected projects and their links next, technology after projects, and merged upstream contributions before contact.
5. **Publishing constraints:** GitHub profile READMEs cannot set the outer page CSS or run JavaScript. Motion is pre-rendered in a local GIF; no GSAP or Lenis runtime is applicable. GitHub controls the surrounding page background.

## Visual system

- **Palette:** ink black and midnight blue, scarlet red, hot magenta, paper white, and restrained chrome.
- **Texture:** comic halftone, fine static web geometry, and a soft glitch field.
- **Motion:** short, contained pixel-shear bursts on the glitch spider artwork; no moving line dividers. Project details remain still and readable.
- **Accessibility:** descriptive image alt text, native text for all important content, compact detail disclosures, and still art for reduced motion.

## Asset sources and generation

The user-supplied JPEG references are kept in `assets/spider/references/`. `scripts/build_spider_art.py` generates the Spider-Man hero, the single-image glitch panel, project cards, and matching skills, contribution, and contact panels. Run `python3 scripts/build_spider_art.py` to rebuild these local assets.
