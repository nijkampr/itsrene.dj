# itsrene.dj

DJ portfolio for **IT'S RENÉ** — Amsterdam, from mainstream to underground.

**Live:** [itsrene.dj](https://www.itsrene.dj) · **Press kit:** [/press](https://www.itsrene.dj/press/) · **Bookings:** dj@itsrene.nl

## How this site works

Hand-built static page on GitHub Pages. No framework, no build step, no cookies — what's in the repo is what ships. The interesting parts:

- **Content is data.** Sets and gigs live in `data/*.json`, rendered by ~180 lines of vanilla JS. A [weekly GitHub Action](.github/workflows/sync-sets.yml) syncs the set list from SoundCloud's RSS feed and follower stats from Twitch — curated fields (vibe tags, featured flags) always win over feed data, so nothing a human wrote gets clobbered and nothing on the page can go stale.
- **The design is "The Build":** the page is staged like a DJ set — opens melodic and spacious, tightens and hardens section by section, peaks at the booking CTA. One accent color (`#4DD6FF`, from the logo), hairline structure, duotone photography, ≤20KB of hand-written CSS. Full spec: [docs/design/DESIGN-DIRECTION.md](docs/design/DESIGN-DIRECTION.md).
- **CI keeps it honest.** Every push validates JSON-LD, HTML, image budgets and asset references; Lighthouse runs on top ([checks.yml](.github/workflows/checks.yml)).
- **Live status without a backend:** one client-side call to decapi with a 3s timeout; offline is the designed default state, so the feature can only ever add.

## Docs

The whole redesign was run as a documented program — brief, ADRs, PRDs, backlog: **[docs/](docs/)**. Start at [docs/BRIEF.md](docs/BRIEF.md).

## Working on it

```bash
python3 -m http.server 8000        # serve locally
python3 scripts/sync_sets.py       # refresh data from SoundCloud/Twitch
./scripts/optimize-images.sh       # regenerate image derivatives (originals live off-repo)
```

Pick up work from [docs/BACKLOG.md](docs/BACKLOG.md) — tickets are sized for dull moments.
