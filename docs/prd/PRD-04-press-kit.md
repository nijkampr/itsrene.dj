# PRD-04 · Press Kit / EPK (`/press`)

**Problem:** an organiser who's half-sold has nothing to forward to the co-decider, and every booking conversation restarts from zero (photos? bio? rider?). **Outcome:** `press/index.html` — a one-page electronic press kit that answers everything a booker or a venue's marketing person needs, plus a downloadable bundle.

**Depends on:** PRD-01 (shares `style.css`), ADR-0003 (photo derivatives).

## Scope

1. **Bios, three lengths,** written once and versioned here: one-liner (≤140 chars, for lineup posters), short (~60 words, for event pages), full (~200 words). First person for the site; third-person variants included because event pages need them — clearly labeled, no mid-sentence person-switching (current site bug).
2. **Facts block (mono, scannable):** genres with BPM ranges, based Amsterdam / travels EU, set lengths (1h warm-up → all-night), languages, contact.
3. **Tech rider (honest hobby-scale):** brings Traktor controller + USB backup, works any CDJ/mixer setup, needs: booth output + 1 channel, that's it. The simplicity *is* the sell — "no drama" as a rider.
4. **Photo section:** 4–6 approved photos in web resolution with a "download hi-res" link to a release-tagged zip (GitHub Releases hosts the bundle — free, versioned, off the Pages payload).
5. **Logo assets:** ITR mark as SVG, light/dark variants, plus a don't-do row (don't recolor, don't stretch).
6. **The bundle:** `itsrene-presskit.zip` (bios.txt, photos, logos, rider.pdf or .md) attached to a GitHub Release; the page links the latest.
7. **Discoverability:** linked from BOOK section ("Need the press kit?") and footer. `noindex` is **not** set — organisers Google names.

## Non-goals

Booking form (email is the funnel and it works), testimonials (collect first — backlog ticket to ask GoToAms/BB/Birdcage folks), a PDF replica of the whole page.

## Acceptance

- A booker can, in under a minute: read the short bio, see two photos, confirm gear needs, download the bundle, email — without leaving `/press` except to mail.
- Page shares the design system: same tokens, same header/footer, ≤ 1MB total.
- GoatCounter event on bundle download (funnel metric #2, per ADR-0006).
