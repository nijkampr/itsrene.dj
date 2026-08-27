# CLAUDE.md

Guidance for working in this repo. Read the README first for the human-facing tour; this file is the operational contract.

## What this is

The DJ portfolio for **IT'S RENÉ** (Amsterdam), served at **www.itsrene.dj** (see `CNAME`). It is a hand-built **static site on GitHub Pages**: no framework, no bundler, no build step, no cookies, no backend. What is in the repo is exactly what ships. Two pages only: `index.html` (the site) and `press/index.html` (the press kit).

The architecture is deliberate and documented as ADRs in `docs/adr/`. Do not reach for a framework, a build tool, npm dependencies in the site, or a server — every one of those has a written decision against it. If you think one is warranted, say so and point at the ADR you'd be overturning.

## Layout

```
index.html            the site (single page, 5 sections: hero, listen, live, played, book)
press/index.html      the press kit + press/itsrene-presskit.zip
css/style.css         all styles, hand-written, budget ≤20KB
js/main.js            all client JS, ~180 lines vanilla, IIFE, progressive enhancement
data/*.json           content as data (see below)
scripts/sync_sets.py  refreshes data/ from SoundCloud RSS + Twitch (stdlib only)
scripts/optimize-images.sh  regenerates image derivatives with sips
docs/                 the redesign program: BRIEF, ADRs, PRDs, DESIGN-DIRECTION, BACKLOG
.github/workflows/    checks.yml (CI gates) + sync-sets.yml (weekly data sync)
```

## Content is data

Sets and gigs are data, rendered client-side by `js/main.js`. Never hand-edit rendered markup for a set or gig — edit the JSON.

- **`data/sets.json`** — one entry per SoundCloud set. Keys: `date`, `title`, `permalink`, `vibe`, `featured`, `note`. `vibe` is one of `melodic`, `house`, `techno`, `hard`, `chaos` (or `null` until curated); it drives the Listen filter and the "hot" tag (`hard`/`chaos`). `permalink` is the SoundCloud URL and doubles as the identity key.
- **`data/gigs.json`** — one entry per gig. Keys: `date`, `name`, `city`, `type` (`irl` or `stream`), `label`.
- **`data/stats.json`** — public numbers: `twitchFollowers`, `hoursStreamed`, `sets`, `streamingSince`. The HTML bakes fallback values into `data-stat` attributes; JS overwrites them from this file if the fetch succeeds. Suffix formatting (`500+`, `yearsStreaming` from `streamingSince`) happens in JS, not the data.

### The sync never clobbers curation

`scripts/sync_sets.py` merges the SoundCloud RSS feed and Twitch follower count into `data/`. **Curated fields always win** — an existing set entry is kept wholesale (its human-set `vibe`, `featured`, `note`, and date fixes are never overwritten); only genuinely new uploads get appended with `vibe: null`. When editing the sync, preserve this invariant. It runs weekly via `.github/workflows/sync-sets.yml` and on push locally is safe (exit 0 always; prints `CHANGED`/`UNCHANGED`).

## Design: "The Build"

Full spec in `docs/design/DESIGN-DIRECTION.md`. The constraints that CI and reviewers actually enforce:

- **One accent color:** `#4DD6FF` (from the logo). Don't introduce a second accent.
- Hairline structure, duotone photography, generous space up top that tightens toward the booking CTA — the page is staged like a DJ set.
- CSS is hand-written and kept **≤20KB**. No CSS framework, no utility classes from a CDN (ADR-0002 killed the Tailwind CDN).
- JS is **progressive enhancement only**: every dynamic feature has a designed static fallback already in the HTML (offline is the *default* live state; baked stat numbers stay if the fetch fails; a noscript note covers the set list). Preserve that — a feature may add, never subtract when JS or a third party is down. Always `escapeHtml()` any string that reaches `innerHTML`.

## Local workflow

```bash
python3 -m http.server 8000          # serve at http://localhost:8000
python3 scripts/sync_sets.py         # refresh data/ from SoundCloud + Twitch
./scripts/optimize-images.sh         # regenerate image derivatives (originals live off-repo)
```

Tooling on this machine: **Python 3** (system, 3.9) and **Node** (via Homebrew — the CI checks use it) are installed; `sips` is macOS built-in. The site itself has **zero runtime dependencies**; Node is only for the linters below.

Image originals live **off-repo** at `/Users/nijkampr/stuff/itsrene.dj-originals/` (ADR-0003) — `optimize-images.sh` reads from there and writes derivatives into `images/`.

## CI gates (`.github/workflows/checks.yml`) — run these before pushing

Every push to `main` and every PR must pass:

1. **JSON-LD parses** — the `application/ld+json` blocks in both HTML pages must be valid JSON.
2. **Image budget** — every file in `images/` ≤ 250KB, total ≤ 5MB.
3. **Referenced assets exist** — every root-relative `src`/`href` in the HTML resolves to a real file.
4. **html-validate** — `npx html-validate@8 index.html press/index.html` (recommended ruleset, with `no-trailing-whitespace`, `long-title`, `no-inline-style` off).

Lighthouse also runs but is warn-only (`continue-on-error`). Reproduce the linters locally:

```bash
npx html-validate@8 index.html press/index.html
python3 - <<'EOF'
import json, re
for p in ["index.html","press/index.html"]:
    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', open(p).read(), re.S):
        json.loads(b)
print("JSON-LD OK")
EOF
```

## Conventions

- Match the surrounding hand-written style: the CSS and JS have a distinct voice and comment density — read the neighbors before adding.
- Keep JSON diffs minimal and stable; the sync writes with `indent=1, ensure_ascii=False` and a trailing newline — match it so machine and human edits don't fight.
- Deploy is automatic: merging to `main` publishes via GitHub Pages. There is no staging — the checks *are* the safety net.
- Pick up backlog work from `docs/BACKLOG.md`.
