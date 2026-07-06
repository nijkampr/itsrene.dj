# Design Direction — "The Build"

**The concept in one sentence:** the page is structured like a René set — it opens clean and melodic, and gets harder, denser, and louder as you scroll, ending at full booking-CTA intensity.

"From mainstream to underground" stops being a tagline and becomes the information architecture. Every DJ site claims a journey; this one *is* one. That's the intriguing part — and it costs zero JavaScript.

## What we're leaving behind

The current aesthetic is 2024 AI-template: glow everything, animated grid, particles, cursor halo, emoji headers, pulsing text. The replacement is **club-poster editorial**: the visual language of festival lineups, Boiler Room stills, and Swiss typography. Flat, stark, typographic, confident.

## The Anti-Slop Contract

Hard rules. A PR that violates one gets rejected, including PRs from an AI.

1. No glows, no `box-shadow` halos, no `text-shadow`. Depth comes from contrast and scale.
2. No gradients — one exception: a single hairline energy-ramp element (see below).
3. No emoji in UI chrome. Iconography is text, numbers, or nothing.
4. No particles, grids, waveforms, or any ambient animated background.
5. No cursor effects. The cursor is the visitor's, not ours.
6. One accent color. If something else "needs" color, the answer is type scale or weight.
7. No stock phrases ("elevate your event"), no hype adjectives the data doesn't back.
8. Every number on the page is real and sourced (see `research/`).
9. Motion is meaning: something moves only when its state changed (live status, hover, reveal-on-first-scroll). Everything behind `prefers-reduced-motion`.
10. If a treatment would look at home on a SaaS pricing page, it's out.

## Color

The logo blue is the star, and it's used like a highlighter — scarce.

```css
:root {
  --ink:        #0A0B0D;  /* page background — near-black, flat, no gradient */
  --ink-2:      #121417;  /* raised surfaces: cards, panels */
  --line:       #23262B;  /* hairline borders, 1px, everywhere structure is needed */
  --paper:      #F2F3F5;  /* primary text — off-white, never pure #fff */
  --muted:      #8A9099;  /* metadata, captions */
  --itr:        #4DD6FF;  /* THE blue. Links, live state, key numbers, hover fills */
  --itr-deep:   #1E7FA6;  /* darker blue for large fills where #4DD6FF would scream */
}
```

**Usage discipline:** `--itr` covers well under ~5% of any viewport. It marks exactly: interactive affordances, the LIVE state, one key stat per section, and the energy ramp. Large blue areas use `--itr-deep`. The purple/orange/pink platform-brand buttons are gone — every external link is the same quiet style; the *destination* is labeled, not color-coded.

**Photo treatment:** all photography gets the **ITR duotone** — deep ink shadows to blue-tinted highlights (CSS `filter: grayscale(1)` + blend or pre-baked in the image script). Mixed-quality party photos become one cohesive, branded set. Full color only on hover/focus — a small reward, not a firework.

## Typography

Three voices, self-hosted woff2 (no Google Fonts request, no layout shift — `font-display: swap` + size-adjusted fallbacks):

| Voice | Face | Role |
|---|---|---|
| **Display** | Archivo (variable, using Expanded 700–900) | Headlines, the big poster type. Wide, industrial, reads like a lineup poster. |
| **Text** | Inter (400/600) | Body copy. Already on brand, kept. |
| **Data** | JetBrains Mono (400/700) | Dates, BPM, stats, genre tags, tracklists. The engineering wink. |

Fluid scale via `clamp()`: display runs from 2.5rem (mobile) to a genuinely oversized 8rem hero. Mono data type is always small (0.75–0.875rem), uppercase, letter-spaced +0.08em.

**The signature move:** big display type + tiny mono annotation. `IT'S RENÉ` at 8rem with `52.36°N / AMS · 120→200 BPM` in 13px mono underneath. That pairing is the brand, repeated everywhere: section titles annotated like a tracklist.

## The energy ramp (the one allowed gradient)

A 2px vertical line fixed to the left edge (desktop) that fills `--line` → `--itr` proportional to scroll depth, annotated at section boundaries with mono BPM markers. Sections are staged like a set:

| Section | Marker | Feel |
|---|---|---|
| Hero | `00:00 · 120 BPM` | Maximum whitespace, huge type, one photo, one CTA |
| Listen | `01:00 · 128 BPM` | Tracklist-style set list, tight rows |
| Live | `02:00 · 140 BPM` | Denser, mono-heavy, Twitch stats |
| Gigs / In Action | `03:00 · 150 BPM` | Duotone photo wall, edge-to-edge |
| Book | `04:00 · 175 BPM` | Near-full-bleed statement block, biggest type since the hero |

The density ramp is real, not decorative: section padding tightens progressively (e.g., `8rem → 5rem → 3rem`), type weight increases, hairlines multiply. Scroll the page fast and you *feel* the build. Engineers will find the scroll listener is ~10 lines with `requestAnimationFrame`; C-level just feels that the page has rhythm.

## Layout

- **12-col fluid grid, max-width 1280px**, generous gutters up top, tightening down the page.
- **Hairline structure:** 1px `--line` rules separate everything — the timetable/technical-drawing look. No rounded-corner card soup; corners are square or 2px.
- **Set list, not embed wall:** sets render as table rows (date mono · title display · vibe tag · play affordance), from `data/sets.json`. SoundCloud iframes only mount on click (a facade pattern) — one featured player max on initial load.
- **Numbers as graphics:** 1,531 followers, 6 years, 32 sets, 500+ hours — set in huge Archivo with mono captions. Real stats *are* the decoration.

## Voice & copy rules

First person, always. Confident-dry, one wink per section maximum ("No, I can't play it from your phone" earns its place; three jokes per scroll is a comedy site). Claims carry numbers or they're cut. Section titles are one word where possible: LISTEN. LIVE. PLAYED. BOOK.

## Accessibility baseline

Keep what's good (skip link, focus states — restyle to 2px `--itr` outline). Add: `prefers-reduced-motion` guards on everything that moves, `prefers-color-scheme` is moot (site is dark by identity, but contrast ratios must pass AA: `--paper` on `--ink` = 15.8:1 ✓, `--muted` on `--ink` = 5.7:1 ✓, `--itr` on `--ink` = 10.9:1 ✓).

## References (the shelf, not the template)

Festival lineup posters (Awakenings, Time Warp) · Boiler Room's stark chrome · Resident Advisor's editorial restraint · Swiss International Style · Teenage Engineering's mono-annotated hardware. Steal the *discipline*, not any specific page.
