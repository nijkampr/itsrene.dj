# ADR-0002: Hand-rolled CSS replaces the Tailwind CDN script

**Status:** Accepted · 2026-07-06

## Context

The page loads `https://cdn.tailwindcss.com` — the runtime JIT compiler meant for prototyping. Costs: ~110KB of JS, style computation at runtime, a production console warning, FOUC, and a hard third-party dependency for all styling. On top of that sits ~300 lines of custom `<style>` (glows, animations) that fight the utility classes. The visual redesign (PRD-01) replaces the design language anyway.

## Decision

Write **one hand-authored stylesheet** (`css/style.css`) built on CSS custom properties as design tokens. No Tailwind (CDN or compiled), no preprocessor.

- **Budget: ≤ 20KB uncompressed.** The design direction is austere; this is achievable and the budget is the point.
- Tokens defined once in `:root`: color, type scale, spacing scale, borders (names specced in `design/DESIGN-DIRECTION.md`).
- Modern CSS is allowed and encouraged: nesting, `clamp()` fluid type, grid, `color-mix()`, container queries where useful. Target evergreen browsers only.
- All motion behind `@media (prefers-reduced-motion: no-preference)`.

## Consequences

- Removes the largest render-blocking dependency and the FOUC in one move.
- The stylesheet becomes part of the portfolio: an engineer reading 20KB of intentional CSS learns more about the author than any framework config.
- We give up utility-class iteration speed. Acceptable: the design is specced up front in PRD-01, not discovered in the browser.
- A compiled Tailwind build (standalone CLI) was considered and rejected — it solves the CDN problem but keeps utility soup in the markup and adds the build step ADR-0001 forbids.
