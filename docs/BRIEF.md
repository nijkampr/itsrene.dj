# itsrene.dj — Project Brief

**One line:** Rebuild itsrene.dj from an AI-flavored template into a sharp, credible DJ presence that books gigs, feeds the Twitch funnel, and quietly doubles as an engineering showcase.

This is the north-star document. Everything else hangs off it:

- **Decisions** → `adr/` (why the stack is what it is)
- **What to build** → `prd/` (one PRD per logical block)
- **How it should look** → `design/DESIGN-DIRECTION.md`
- **What to pick up in a dull moment** → `BACKLOG.md`
- **Real numbers** → `research/platform-snapshot-2026-07.md`

## Here's the reality: the current site audit

The site works, ranks, and has solid SEO bones. It also has real defects and it looks like every other 2024-era AI-generated landing page. Both problems are fixable.

**Broken structured data.** The FAQPage JSON-LD block is invalid JSON — the last Question object is never closed (missing `}` before the closing `]`, around line 233 of `index.html`). Google silently drops the entire FAQ block. It's been shipping broken since the "CRITICAL FIXES" commit.

**~40MB page weight.** Two action shots are 17MB and 16MB (5,700px wide, displayed at ~300px). The headshot is 3.3MB. One 11MB image (`images/53799373426_94907c72b4_o.jpg`) isn't referenced anywhere. Four SoundCloud iframes load eagerly on top. Mobile visitors on 4G are gone before the hero renders.

**Tailwind via CDN `<script>`.** Runtime-compiled Tailwind in production: ~110KB of JS, a console warning, a flash of unstyled content, and a hard dependency on a third-party CDN for *all* styling. For a single-page site this buys nothing.

**The AI-slop tells** (the things that make it "look like any other AI generated website"):
cursor-glow div chasing the mouse • animated background grid • floating particles • pulsing text-shadow on the hero • fake CSS waveform bars • glow on every hover • emoji as section iconography (🔥🎧📅🎛️📍🎵) • a Tailwind color literally named `neon-red` that renders cyan • every section the same card-grid-with-border pattern.

**Stale and inconsistent copy.** "LATEST … my most recent banger" pinned to an August 2025 upload (11 months old). Footer says © 2025. Hero says "270+ peak viewers," the quote section says "300+ viewer Twitch streams." Bio switches person mid-sentence ("Started DJing at 15 in *his* hometown, COVID brought *me* back"). `twitter:creator` points at an X account that isn't in the socials.

**The strongest number is hidden.** 1,531 Twitch followers across 6+ years — nowhere on the page. Meanwhile SoundCloud (35 followers) gets four embeds. Lead with the strong signal.

## Who this site is for

**Organisers & venue bookers** (primary). They decide in 30 seconds: does this person look professional, what do they sound like, can I reach them. They need: one representative set, real gig history (ADE, GoToAms, conference parties), gear/rider facts, a working email. Eventually: a press kit they can forward.

**Fellow DJs & the Twitch scene** (community). Team Brisk, Birdcage Radio, raid trains, b2b partners. They need: the catalog, the live schedule, proof of craft.

**Fans → future groupies** (growth). They need: where to listen, when the next stream is, one click to follow.

**C-level & engineers** (the stealth audience). This site is linked from a Product & Integration Architect's world. Executives should read *taste and judgment*. Engineers should View Source and nod: hand-rolled CSS, no framework, data-driven content, CI on a static page. The repo and these docs are part of the portfolio — that's deliberate.

## Positioning

**"From mainstream to underground"** stays — it's genuinely differentiating and it's true (progressive house warm-ups → gabber chaos). The redesign turns it from a tagline into the *organizing principle* of the whole site: the page itself builds like a set. See `design/DESIGN-DIRECTION.md` ("The Build").

Tone: confident, direct, a little dry. The "no, I can't play it from your phone" energy survives. Zero corporate speak, zero hype-words, zero emoji in UI chrome.

## What success looks like

1. **Lighthouse ≥ 95 across the board** on mobile, enforced by CI (currently: performance would be catastrophic — ~40MB payload).
2. **Valid structured data** — Rich Results Test passes with zero errors.
3. **Nothing on the page can go stale by itself.** Latest set, gig list, live status: all data-driven, no hard-coded "latest."
4. **A booker can go from landing to "email sent + press kit downloaded" in under a minute.**
5. **The View Source test:** an engineer inspecting the page finds hand-written CSS under 20KB, semantic HTML, and a GitHub Action doing something clever.
6. **The squint test:** at arm's length it reads as a club poster, not a SaaS landing page.

## Constraints

- **GitHub Pages, static, no paid services.** No backend, no secrets in the repo, free-tier everything.
- **The blue stays.** `#4DD6FF` comes from the ITR logo and is the brand. It becomes the *only* accent color (the purple/orange/pink/blue social buttons go).
- **No frameworks, no build step** for the site itself (ADR-0001). CI may generate *data*, never *pages*.
- **Effort is delivered in dull-moment-sized blocks.** Every ticket in `BACKLOG.md` is sized so a session produces something shippable.
