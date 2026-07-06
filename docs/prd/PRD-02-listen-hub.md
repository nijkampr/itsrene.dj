# PRD-02 · Listen Hub (data-driven set list)

**Problem:** four hand-picked, eagerly-loaded SoundCloud iframes; "LATEST" is 11 months stale; 28 of 32 sets are invisible. **Outcome:** the full catalog as a fast, filterable, tracklist-style section that can't go stale.

**Depends on:** PRD-01 (visual language), ADR-0004 (data model).

## Scope

1. **`data/sets.json`** seeded from `research/platform-snapshot-2026-07.md` (all 32 sets), with curated fields: `featured: bool`, `vibe: melodic|house|techno|hard|chaos`, optional `note` (the one-liner descriptions from the current site are good — keep those for featured sets).
2. **Renderer** in `js/main.js`: newest-first table rows (mono date · title · vibe tag · duration if available · play button). "Latest set" is computed from the data — the word "latest" never appears in HTML.
3. **Vibe filter:** one row of text-button filters (ALL / MELODIC / TECHNO / HARD / CHAOS) mirroring the mainstream→underground arc. No library; `data-vibe` attributes and 15 lines of JS.
4. **Embed facade:** clicking a row swaps in the SoundCloud iframe for that track (color param `#4DD6FF`). At most one live iframe at a time. One `featured: true` set may render its player eagerly *below the fold*, lazy-loaded.
5. **Fallbacks:** `<noscript>` → styled link list to SoundCloud profile. Fetch failure → same.

## Non-goals

The Actions sync workflow (PRD-06 owns CI; the ticket lands there), audio visualization, self-hosted audio.

## Acceptance

- Initial page load performs **zero** requests to soundcloud.com; first embed request happens on user click.
- All 32 sets render; filter and keyboard navigation work; rows are real `<button>`/`<a>` elements.
- Adding a set = adding one JSON object (until the sync automates it); page updates with no HTML edit.
- Vibe tags assigned for the full back catalog (30-minute curation pass, part of the seed ticket).
