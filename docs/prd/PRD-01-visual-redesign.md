# PRD-01 · Visual Redesign Core ("The Build")

**Problem:** the site reads as AI-template, contradicting both the brand ("no AI slop") and the stealth-portfolio goal. **Outcome:** the page implements the design language in `../design/DESIGN-DIRECTION.md` end-to-end.

**Depends on:** ADR-0001, ADR-0002. Blocks: PRD-02 through PRD-05 (they build sections *in* this language).

## Scope

1. **Foundation:** `css/style.css` with the token set from the design doc; self-hosted Archivo + Inter + JetBrains Mono (woff2, subset to latin + `É`); delete the Tailwind CDN script and all inline `<style>`.
2. **Hero:** poster-type `IT'S RENÉ`, mono annotation line, duotone headshot, two CTAs (Book / Listen), real stat pair (Twitch followers, hours streamed) as typographic elements — no floating cards.
3. **Section scaffold:** the five staged sections with energy-ramp markers, progressive density (padding/weight ramp), hairline structure.
4. **Energy ramp element:** scroll-driven 2px line, ~10 lines of JS, `prefers-reduced-motion` guarded, hidden on mobile (<768px).
5. **Footer:** quiet, mono, with the one joke.
6. **Kill list:** cursor glow, grid/particle backgrounds, waveform bars, all `box-shadow`/`text-shadow` glows, emoji headers, platform-colored buttons, `neon-red` naming.

## Non-goals

Content sections' *data* behavior (PRD-02/03/05), press kit (PRD-04), copy rewrite beyond what sections need to render (tracked as its own ticket).

## Acceptance

- Zero external CSS/JS requests except GoatCounter (once ADR-0006 lands) and click-mounted SoundCloud embeds.
- `style.css` ≤ 20KB; no `!important` (sole exception: the `prefers-reduced-motion` kill switch); tokens only — no raw hex outside `:root`.
- Anti-Slop Contract audit passes (checklist in design doc, run manually pre-merge).
- Lighthouse A11y ≥ 95; AA contrast on all text; keyboard-only walkthrough works.
- The squint test: at 25% zoom the page reads as a poster with a visible density ramp.

## Open questions

- Archivo Expanded vs. licensing a characterful display face later — start free, revisit if the poster type feels generic.
- Whether the banner PNG survives — recommendation: no; the logo mark moves to a small SVG in the header, the hero *is* the banner.
