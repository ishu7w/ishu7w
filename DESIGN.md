# Design plan: Spider-Man profile, native to GitHub

## Brief

- **Job and audience:** help recruiters, collaborators, and maintainers quickly understand Ishu's work and find a project or upstream contribution to explore. This profile is an experience/showcase.
- **Outcome and proof:** visitors see the Spider-Man identity, verified GitHub activity, four selected projects, and merged PRs, then can open the actual repositories and demos. Metrics come from `data/stats.json` and carry its update date.
- **Direction:** preserve the Spider-Man hero and scarlet/ink palette, but make the README artwork sit on GitHub's dark `#0d1117` surface with GitHub-like `#30363d` rules and restrained red accents. Remove the neon Spider art and replace its panel with a custom snapshot of Ishu's public GitHub account.
- **Page rhythm:** concise nav and factual introduction; GitHub account/activity snapshot; current focus; individually linked project panels; skills; merged open-source work; contact. Keep each item direct and useful, without cinematic slogans or invented personal branding.
- **Motion:** use one restrained reveal on the language composition bar in the account snapshot. The animation is embedded in its SVG and paired with a still version for reduced-motion preferences. No invented contribution graph or moving line dividers.
- **Boundaries:** preserve project facts, demos, contact, and upstream PR links. Do not add private activity or infer exact commit counts. GitHub owns the profile's outer background and README cannot run JavaScript or custom page CSS.

## Visual system

- **Surface:** GitHub dark canvas `#0d1117`; secondary surfaces only slightly lighter; GitHub-like borders `#30363d`.
- **Accent:** Spider-Man scarlet `#f04452` with one restrained magenta note, white text, and muted gray labels.
- **Motifs:** quiet comic halftone, fine static web geometry, and an accurate language composition bar. No neon character panels, glowing cards, excessive badges, or decorative copy.
- **Typography:** compact uppercase metadata, clear sans-serif headings, native Markdown for all searchable factual copy.

## Verification

Regenerate the local artwork; inspect the hero and account snapshot at profile width; run the README asset validator; confirm all README references resolve; publish and check the workflow. GitHub's browser surface remains responsible for its surrounding background.
