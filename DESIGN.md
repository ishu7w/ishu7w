# Design plan: Spider-Verse signal

## Design brief

Build a Spider-Man-inspired developer profile that preserves the user's Spider-Man hero and makes the supplied magenta glitch Spider the only additional character artwork. Use a scarlet, ink, and magenta comic palette throughout the page. Follow [Mr-KnightCLI's README](https://github.com/Mr-KnightCLI/Mr-KnightCLI) for its editorial rhythm: concise navigation, visual intro and skills panels, individually linked full-width project showcases, contributions, and a direct contact close. The artwork and copy remain Ishu's own and use his verified projects and contributions.

## Page plan

1. **Hero and signal:** preserve the Spider-Man hero, followed by a single-image glitch feature. Animate short pixel-shear bursts only on the supplied glitch Spider; show a static PNG for reduced-motion preferences.
2. **Profile rhythm:** concise navigation and introduction, a visual armory panel, four individually linked project showcases, upstream contributions, and a strong contact panel.
3. **Project showcase:** replace the single four-up graphic and repeated table with one wide comic-style card per project. Each card links to its repository; native Markdown below provides exact descriptions and demo links.
4. **Full-page theme:** use ink panels, scarlet borders, magenta halftone, small web geometry, numbered case-file labels, and consistent typography across every section. Keep informational copy readable outside the artwork too.
5. **Publishing constraints:** GitHub profile READMEs cannot set the outer page CSS or run JavaScript. Motion is pre-rendered in a local GIF; no GSAP or Lenis runtime is applicable. GitHub controls the surrounding page background.

## Visual system

- **Palette:** ink black and midnight blue, scarlet red, hot magenta, paper white, and restrained chrome.
- **Texture:** comic halftone, fine static web geometry, and a soft glitch field; use restrained abstract geometry on project cards without additional character imagery.
- **Motion:** short, contained pixel-shear bursts on the glitch spider artwork; no moving line dividers. Project details remain still and readable.
- **Accessibility:** descriptive image alt text, native text for all important content, compact detail disclosures, and still art for reduced motion.

## Asset sources and generation

The user-supplied Spider-Man JPEG references are kept in `assets/spider/references/`. `scripts/build_spider_art.py` generates the Spider-Man hero, single-image glitch panel, individual case-file showcase cards, and matching skills, contribution, and contact panels. Run `python3 scripts/build_spider_art.py` to rebuild these local assets.
