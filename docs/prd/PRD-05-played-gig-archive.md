# PRD-05 · PLAYED — gig archive & photo wall

**Problem:** the strongest credibility signals (ADE, GoToAms 2024, conference closing parties, KonceptK, community marathons) are a throwaway caption line under four random photos. **Outcome:** a PLAYED section — part timeline, part duotone photo wall — that gives organisers instant "he's done this before" proof.

**Depends on:** PRD-01, ADR-0003 (images), ADR-0004 (`data/gigs.json`).

## Scope

1. **`data/gigs.json`:** `{date, name, venue?, city, type: club|festival|conference|party|stream-marathon, photo?, note?}`. Seed from `research/platform-snapshot-2026-07.md` plus René's memory — a 20-minute brain-dump ticket, this data lives nowhere else. SoundCloud titles help reconstruct (BwoB, ArtBeats, VFest, KonceptK, birthday marathons).
2. **Timeline render:** timetable rows (mono year · event · city · type tag), newest first, from JSON. The 2021→now arc *is* the story: bedroom streams → community slots → ADE/conference stages.
3. **Photo wall:** duotone-treated action shots, edge-to-edge grid, full color on hover/focus. Every photo has a real alt text naming the event. New derivatives via the ADR-0003 script; the 17MB originals leave the repo.
4. **Origin note:** one mono line at the timeline's foot: `first sets: Sexbierum, at 15` — the detail that makes the arc human. Keep it dry.

## Non-goals

Upcoming-events calendar (there's no reliable pipeline of future gigs yet — when there is, it's a `gigs.json` filter, not a new system), per-gig detail pages, lightbox library (native `<dialog>` if a lightbox is wanted at all).

## Acceptance

- ≥ 12 gigs seeded with dates and types; adding a gig = one JSON object.
- Photo wall ships only optimized derivatives (each ≤ 250KB, lazy-loaded, dimensions set — zero CLS).
- Timeline reads correctly with JS off (`<noscript>`: static fallback of the top 5 + "more on request").
