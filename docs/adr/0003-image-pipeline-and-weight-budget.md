# ADR-0003: Image pipeline and page-weight budget

**Status:** Accepted · 2026-07-06

## Context

`images/` holds ~48MB. Two action shots are 16–17MB at 5,700px, displayed at card size. The headshot is 3.3MB. An 11MB image is committed but unused. The repo is 98MB for a one-page site, and the page ships roughly 40MB of pixels. This is the single biggest performance defect.

## Decision

**Originals leave the repo; the repo holds only web-ready derivatives.**

1. **Derivative format:** AVIF with JPEG fallback via `<picture>`, `srcset` at 480/960/1600w. Every `<img>` gets `width`/`height` attributes and `loading="lazy"` (except the LCP hero image, which gets `fetchpriority="high"`).
2. **Hard budgets, enforced by a CI check:** no single image file > 250KB; total `images/` ≤ 4MB; initial-viewport payload ≤ 1MB.
3. **Tooling:** a checked-in script (`scripts/optimize-images.sh`) wrapping `sips`/ImageMagick + `avifenc`, so regenerating derivatives is one command on macOS. No npm image pipeline.
4. **Originals** move to `originals/` in a private location (external drive / cloud album), referenced by name in `docs/` so they're findable. Git history still contains the big blobs — accepted; history rewrite is optional ticket ITR-009, not a blocker.

## Consequences

- Expect the biggest single Lighthouse jump of the whole program from this ADR alone.
- New photos require running the script — friction is one command, documented in the script header.
- JPEG fallback keeps ancient browsers fine; AVIF covers evergreen at roughly half of WebP size for these photo types.
