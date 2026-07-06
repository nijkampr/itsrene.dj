# Backlog — dull-moment-sized blocks

Blocks are ordered; tickets inside a block are ordered too. Sizes: **S** ≈ 30–45 min, **M** ≈ 1.5–2h, **L** ≈ an evening. Every ticket ends with something shippable — no block leaves `main` broken.

Rule of thumb for a dull moment: got 30 minutes? Take the next S. Got an evening? Take the block's L or two Ms.

---

## Block 0 · Stop the bleeding *(live bugs, current site — do first, ~one evening total)*

| ID | Size | Ticket |
|---|---|---|
| ITR-001 | S | **Fix FAQ JSON-LD** — add missing `}` before `]` (~line 233). Validate all 5 blocks parse (`node -e` one-liner). Run Rich Results Test. |
| ITR-002 | S | **Delete dead weight** — remove unreferenced `images/53799373426_94907c72b4_o.jpg` (11MB); check `gotoams_2024.jpg` usage; archive originals outside the repo first. |
| ITR-003 | M | **Image emergency pass** — `scripts/optimize-images.sh` (ADR-0003) over headshot + 4 action shots; swap in derivatives; add `loading="lazy"` + `width`/`height`. Page goes ~40MB → ~2MB. |
| ITR-004 | S | **Copy triage** — fix his/me person switch, unify 270 vs 300 viewers, drop footer year, remove "LATEST … most recent banger" staleness, drop `twitter:creator`. |
| ITR-005 | S | **SoundCloud profile hygiene** (off-repo, phone-friendly) — bio + city on the SC profile (currently empty), link back to itsrene.dj. |

**Exit:** PageSpeed mobile re-run; expect the single biggest jump of the whole program.

## Block 1 · Foundation *(PRD-01 starts; ~2 evenings)*

| ID | Size | Ticket |
|---|---|---|
| ITR-010 | M | **Design tokens + reset** — `css/style.css` with `:root` tokens from the design doc; base type/spacing; wire `<link>`; leave Tailwind in place for one commit (parallel-run). |
| ITR-011 | M | **Self-host fonts** — Archivo var, Inter, JetBrains Mono; subset woff2 (latin + É); `@font-face` with swap + fallback metrics; kill the Google Fonts import. |
| ITR-012 | L | **De-Tailwind the markup** — rewrite `index.html` classes onto the new stylesheet, section by section; delete the CDN script and the old `<style>` block. Kill list from PRD-01 executed here. |
| ITR-013 | S | **Reduced-motion + focus audit** — every animation guarded; focus ring = 2px `--itr`. |

## Block 2 · The poster hero *(~1 evening)*

| ID | Size | Ticket |
|---|---|---|
| ITR-020 | L | **Hero rebuild** — 8rem Archivo `IT'S RENÉ`, mono annotation line, duotone headshot, Book/Listen CTAs, typographic stat pair. Banner PNG retired; small SVG mark in header. |
| ITR-021 | S | **Duotone treatment** — CSS filter recipe (or baked variants via the image script) + hover color reveal; applied to headshot now, photo wall later. |
| ITR-022 | M | **Energy ramp v1** — scroll-driven 2px line + BPM section markers; rAF, reduced-motion guarded, hidden < 768px. |

## Block 3 · Listen hub *(PRD-02; ~2 evenings)*

| ID | Size | Ticket |
|---|---|---|
| ITR-030 | M | **Seed `data/sets.json`** — all 32 sets from the research snapshot; curate `vibe` + `featured` + notes (the curation pass is the real work). |
| ITR-031 | M | **Set list renderer** — fetch + table rows, newest first, computed "latest", `<noscript>` fallback. |
| ITR-032 | M | **Embed facade + vibe filter** — click-to-mount SC iframe (one at a time, `#4DD6FF` color param); ALL/MELODIC/TECHNO/HARD/CHAOS filter row. |

## Block 4 · Live + Played *(PRD-03 + PRD-05; ~2 evenings)*

| ID | Size | Ticket |
|---|---|---|
| ITR-040 | M | **LIVE section** — stat row from `data/stats.json`, teams links, rewritten copy, reserved badge space. |
| ITR-041 | S | **decapi live check** — 15 lines, 3s timeout, offline-is-default; test with request blocked. |
| ITR-042 | S | **Seed `data/gigs.json`** — brain-dump ≥ 12 gigs (ADE, GoToAms 2024, BB Summer, KonceptK, BwoB, ArtBeats, VFest, marathons…). Phone-friendly ticket. |
| ITR-043 | M | **PLAYED timeline + photo wall** — timetable rows from JSON; duotone wall with real alt texts; Sexbierum origin line. |

## Block 5 · Press kit *(PRD-04; ~2 evenings, half of it writing)*

| ID | Size | Ticket |
|---|---|---|
| ITR-050 | M | **Write the bios** — 1-liner / short / full, first-person + labeled third-person variants. Words, not code. |
| ITR-051 | M | **`press/index.html`** — facts block, rider, photos, logo assets, shared stylesheet. |
| ITR-052 | S | **Press bundle** — zip via GitHub Release; link from /press + BOOK section. |
| ITR-053 | S | **Ask for quotes** — message GoToAms/BB/Birdcage contacts for one-line testimonials (humans, not code; slot in when they land). |

## Block 6 · Automation & gates *(PRD-06; ~2 evenings, the engineering showcase)*

| ID | Size | Ticket |
|---|---|---|
| ITR-060 | M | **checks.yml** — Lighthouse CI budgets, html-validate, JSON-LD parse check, image-size guard; warn first, then required. |
| ITR-061 | M | **sync-sets.yml** — weekly RSS → `sets.json` merge (curated fields win), decapi → `stats.json`; idempotent commit; manual dispatch proof. |
| ITR-062 | S | **GoatCounter** — script + 5 funnel events; verify in dashboard. |
| ITR-063 | S | **Structured data v2** — consolidate to Person (+ business bits), delete FAQ schema, new OG image (1200×630 from design system); Rich Results zero errors. |
| ITR-064 | S | **README + badges** — repo as portfolio artifact; link `docs/`. |

## Icebox *(unscheduled, revisit after Block 6)*

- ITR-009 · Git history rewrite to shrink the 98MB repo (needs force-push comfort; cosmetic).
- Upcoming-gigs view once a pipeline of future bookings exists (a `gigs.json` filter).
- `.ics` stream schedule if Twitch cadence ever stabilizes.
- Characterful display-face upgrade if Archivo feels generic after living with it.
- Mix of the month automation: Action picks featured set by recency + play delta.
- itsrene.nl ↔ itsrene.dj cross-link footer ("also: I architect banking platforms" / "also: I play gabber").
