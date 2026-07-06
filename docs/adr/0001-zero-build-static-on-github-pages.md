# ADR-0001: Zero-build static site on GitHub Pages

**Status:** Accepted · 2026-07-06

## Context

The site is a single-page portfolio on GitHub Pages with a custom domain (CNAME → itsrene.dj). The obvious "upgrade" paths are a static site generator (Astro, Eleventy) or a framework (Next). The site owner maintains it in short, irregular sessions and wants the repo itself to read as an engineering statement.

## Decision

Stay **zero-build**: hand-written HTML, one CSS file, one JS file, deployed by pushing to `main`. No SSG, no bundler, no `node_modules` for the site itself.

Structure target:

```
index.html          press/index.html (later)
css/style.css       js/main.js
data/sets.json      data/gigs.json
images/             docs/
```

CI (GitHub Actions) is allowed to **generate data files** (see ADR-0004) and **run checks** (Lighthouse CI, HTML validation), but never to compile pages. What's in the repo is what ships.

## Consequences

- Any dull-moment session starts with `git pull` and a text editor. Nothing to install, nothing to break in eighteen months.
- "View Source equals the repo" is itself the showcase: semantic HTML and lean CSS with no framework fingerprints.
- Multi-page growth (press kit, gig archive) is bounded — at roughly 5+ pages, shared header/footer duplication starts to hurt. Accepted: this site should never need that many pages. Revisit if it does.
- No templating means repeated markup (e.g., set cards) must be rendered client-side from JSON (ADR-0004) or duplicated by hand. We choose client-side rendering for lists, static HTML for everything else.

## Rejected

- **Astro/Eleventy:** better templating, but adds a toolchain to a one-page site and dilutes the "no magic" statement.
- **Next/React:** absurd overkill; also the exact aesthetic-of-tooling the brief wants to avoid.
