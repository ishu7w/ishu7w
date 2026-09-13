---
name: Ishu Patel — GitHub Profile
description: A restrained technical portfolio in ink navy with luminous build signals.
colors:
  ink-navy: "#0b1020"
  pale-text: "#f1f5ff"
  muted-text: "#b2c1d9"
  structural-line: "#24334e"
  signal-cyan: "#7dd9ed"
  geometry-blue: "#8caeff"
  restrained-violet: "#b7a0ff"
typography:
  display:
    fontFamily: "Arial, Helvetica, sans-serif"
    fontSize: "88px"
    fontWeight: 700
    letterSpacing: "-3px"
  title:
    fontFamily: "Arial, Helvetica, sans-serif"
    fontSize: "31px"
    fontWeight: 700
    letterSpacing: "-.8px"
  body:
    fontFamily: "Arial, Helvetica, sans-serif"
    fontSize: "18px"
  terminal:
    fontFamily: "ui-monospace, SFMono-Regular, Consolas, monospace"
    fontSize: "21px"
rounded:
  panel: "16px"
  link: "8px"
spacing:
  card-inset: "26px"
  mobile-inset: "24px"
components:
  panel:
    backgroundColor: "{colors.ink-navy}"
    textColor: "{colors.pale-text}"
    rounded: "{rounded.panel}"
  link-button:
    backgroundColor: "{colors.ink-navy}"
    textColor: "{colors.signal-cyan}"
    rounded: "{rounded.link}"
    height: "40px"
---

# Design System: Ishu Patel

## Overview

The visual metaphor is a **build signal** connecting learning, projects, and public contributions. This implements the user's premium technical portfolio brief: centered identity, dark navy SVG panels, restrained blue/cyan/violet accents, and compact evidence of real work. It remains a GitHub README, with native prose and disclosures between custom images.

## Colors

Cyan highlights roles, terminal prompts, and link labels; blue draws project motifs and signal paths; violet distinguishes terminal keys. Pale text carries names and data, while muted text carries descriptions and supporting labels. Structural lines separate content without heavy borders. Technology logos retain their original brand colors; analytics may use additional small categorical colors.

## Typography

Arial/Helvetica is intentional SVG portability; do not introduce remote fonts. Monospace identifies terminal prompts, keys, and the desktop filename. Native README text inherits GitHub's typography.

Token sizes are SVG source units, scaled with each image. Hero names use 88 desktop / 60 mobile, with 24 / 19 identity text and 28 / 23 animated roles. Cards use 31 / 30 titles and 18 / 19 descriptions. Analytics uses 35–36 numerals. SVG text has explicit coordinates rather than a CSS line-height system.

## Layout

The README is a single editorial flow. Hero and dividers span available width; terminal, analytics, and footer are centered at up to 640 display pixels. Project links use 400-pixel images and wrap from two columns to one as space narrows. Technology groups pair readable text with 32-pixel local icons.

Picture sources switch at 600px. Hero artboards are 960×410 and 480×360; terminal 640×276 and 480×348; cards 460×234 and 360×266; analytics 640×270 and 480×380. Mobile art changes composition: terminal entries stack, card motifs disappear, and metrics use a two-by-two arrangement. Do not rely only on shrinking desktop art.

## Elevation & Depth

Depth comes from navy panels, fine separators, and a soft radial glow behind the hero. There are no drop shadows or simulated raised controls. Decorative signal paths use the cyan-to-blue-to-violet gradient sparingly.

## Shapes

Panels share 16-unit rounded corners; outlined image links use 8-unit corners and one-unit borders. Project motifs use thin geometric strokes. The contribution calendar keeps its small square-cell vocabulary.

## Components

- **Hero:** centered name, student identity, cycling role subtitle, short statement, and symmetrical edge signal paths. The first role is the static fallback. Roles cycle over 24 seconds with reveal, hold, and exit phases.
- **Link buttons:** compact outlined SVG labels inside native anchors for projects, email, and GitHub. GitHub supplies link interaction and keyboard behavior; SVGs contain no custom hover states.
- **Terminal:** current learning, building, exploring, and contributing focus. Desktop includes window dots and filename; mobile stacks labels above values. The cursor blinks at 1.6 seconds. A native disclosure repeats the content in text.
- **Project cards:** project name, category, two-line description, stack, divider, and desktop geometric motif with outward arrow. The entire image links to source; demos and expanded text remain native README links.
- **Analytics:** four public metrics, language mix, and snapshot date. Desktop uses a segmented bar; mobile uses a readable list. The adjacent disclosure explains sources and scope.
- **Contribution snake:** animated public contribution calendar with light/dark assets, reduced-motion static calendar, and a native history link.
- **Dividers and footer:** fine moving signals separate sections and underline the centered closing statement. Signal motion uses a 12-second linear cycle.

## Do's and Don'ts

- **Do** maintain the user-pinned navy world, centered identity, and restrained accent hierarchy.
- **Do** preserve meaningful SVG titles, image alt text, native links, and plain-text details for substantive content.
- **Do** keep local static picture sources for reduced motion and useful defaults when animation is unavailable. Decorative movement must never carry unique information.
- **Do** update source data and `scripts/generate-assets.py`, then regenerate README and assets together; public numbers require dated, scoped evidence.
- **Don't** add JavaScript, remote fonts, unsupported README CSS, invented credentials, or visual controls that imply unavailable interaction.
- **Don't** turn every label into a badge or add glow, gradients, and animation indiscriminately.
