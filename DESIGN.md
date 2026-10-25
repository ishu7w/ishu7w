# Design plan: Spider-Man profile, native to GitHub

## Brief

- **Job and audience:** help recruiters, collaborators, and maintainers quickly understand Ishu's work and find a project or upstream contribution to explore. This profile is an experience/showcase.
- **Outcome and proof:** visitors see the Spider-Man identity, verified GitHub activity, four selected projects, and merged PRs, then can open the actual repositories and demos. Metrics come from `data/stats.json` and carry its update date.
- **Direction:** preserve the Spider-Man hero and scarlet/ink palette, but make the README artwork sit on GitHub's dark `#0d1117` surface with GitHub-like `#30363d` rules and restrained red accents. Remove the neon Spider art and replace its panel with a custom snapshot of Ishu's public GitHub account.
- **Page rhythm:** concise nav and factual introduction; GitHub account/activity snapshot; current focus; individually linked project panels; skills; merged open-source work; contact. Keep each item direct and useful, without cinematic slogans or invented personal branding.
- **Motion:** hold the Spider-Man hero still most of the time, with brief scarlet pixel-shear bursts. Add a slow language-bar reveal and small staggered pulses on project marks and account values. Keep motion inside local GIF/SVG assets and show still assets for reduced-motion preferences.
- **Boundaries:** preserve project facts, demos, contact, and upstream PR links. Do not add private activity or infer exact commit counts. GitHub owns the profile's outer background and README cannot run JavaScript or custom page CSS.

## Visual system

- **Surface:** GitHub dark canvas `#0d1117`; secondary surfaces only slightly lighter; GitHub-like borders `#30363d`.
- **Accent:** Spider-Man scarlet `#f04452` with one restrained magenta note, white text, and muted gray labels.
- **Motifs:** quiet comic halftone, fine static web geometry, and an accurate language composition bar. No neon character panels, glowing cards, excessive badges, or decorative copy.
- **Typography:** enlarge labels and body copy inside artwork; use high-contrast GitHub-like sans-serif text and native Markdown for all searchable facts.

## Verification

Regenerate the local artwork; inspect hero, project cards, and the account snapshot at profile width; run the README asset validator; confirm all README references resolve; publish and check the workflow. GitHub's browser surface remains responsible for its surrounding background.
