# Maintaining the profile

Edit **data/profile.json** for current focus, project descriptions, verified demos, or contact links. Empty LinkedIn/portfolio values deliberately publish no link. All public copy and SVGs are generated with `python3 scripts/generate-assets.py`. Commit the config to `main` and the workflow regenerates the profile automatically.

## Updates

`Refresh profile` runs daily at **02:23 UTC / 07:53 IST**, manually from Actions, and when config, generator, or workflow files change on `main`. It refreshes public statistics and upstream PR states, generates all custom assets and both snake themes, validates them, and commits changed outputs together. Scheduled runs can be delayed by GitHub. GitHub may disable scheduled workflows in public repositories after prolonged inactivity; re-enable the workflow from Actions if needed.

No custom secret, paid service, or personal access token is required. The workflow uses GitHub's built-in token with `contents: write` only in the publishing job. GitHub CLI and Python are included on the hosted Ubuntu runner. Locally, sign in with `gh auth login` and run `python3 scripts/generate-assets.py --refresh` to refresh stats. A failed API request fails the job and preserves the last committed snapshot rather than publishing zeroes. Dates are visible so stale data is identifiable.

The entire profile is on `main`, including `dist/`; no output branch or Pages deployment is needed. Keep the repository public and named `ishu7w` for GitHub to display the README on the profile.

## Data rules

Statistics come from GitHub REST APIs. Repository totals include public forks; stars and language bytes exclude forks. Language bytes measure repository composition, not ability. Merged PR totals use `author:ishu7w is:pr is:merged is:public -user:ishu7w`. No private repository records are stored. Contribution snakes are produced by the pinned Platane/snk action using GitHub's contribution calendar.

FocusX and WellTrack AI are labeled prototypes with demo/sample data. ScholarAI's matching is explainable weighted scoring; optional LLM support is not described as a deployed AI model. No coding-site identity, awards, profile views, LinkedIn, or portfolio URL has been invented. Upstream PR state is refreshed daily.

## Accessibility and reliability

All artwork is served from this repository. Native text, alt text, and expandable text equivalents preserve the important content. No script, custom CSS, iframe, or HTML table is used in the README. CSS exists only inside standalone SVG images. The hero, terminal, analytics, and project cards include phone compositions selected through `<picture>`. Every animated component has an explicit still source for reduced motion, in addition to its embedded SVG media rule. Project images wrap naturally instead of using a two-column table. Assets use viewBox dimensions and SVG animations with reduced-motion rules. The snake has a still calendar fallback selected through `<picture>`.

To validate: `python3 scripts/validate.py`. Devicon sources, pinned revision, and MIT notice live in `assets/icons/`. Platane/snk: https://github.com/Platane/snk (pinned revision in the workflow). Custom profile assets are generated from `scripts/generate-assets.py`.

Demo links were reachable when installed; availability is controlled by their hosts. The Render-hosted delivery demo can take time to wake up. GitHub may cache images briefly after a refresh. SVG animation behavior depends on the browser; static content remains readable when animation is unavailable.
