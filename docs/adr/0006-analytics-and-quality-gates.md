# ADR-0006: Privacy-first analytics and CI quality gates

**Status:** Accepted · 2026-07-06

## Context

There is zero measurement today — no way to know whether a redesign, a booking CTA, or a press kit does anything. Classic Google Analytics would demand a cookie banner (instant aesthetic and legal overhead in the EU) and contradicts the site's taste.

Separately, the site has shipped broken JSON-LD for months because nothing checks the page.

## Decision

**Analytics: GoatCounter** (free tier, no cookies, no consent banner needed, ~3KB script, EU-friendly). Events worth counting: page view, booking-email click, press-kit download, Twitch click-out, SoundCloud click-out. That's the entire funnel.

**Quality gates in CI on every push to `main`:**

1. **Lighthouse CI** (`treosh/lighthouse-ci-action`) with budgets: Performance/A11y/Best-Practices/SEO ≥ 95 (mobile), total-byte-weight ≤ 1.5MB.
2. **HTML validation** (`html-validate`) — catches malformed markup.
3. **JSON-LD validation** — a 20-line node script that extracts every `application/ld+json` block and `JSON.parse`s it. This alone would have caught the FAQ bug at commit time.
4. Budgets from ADR-0003 (max image size) as a shell check.

Checks warn-then-fail: first iteration reports, once green they become required.

## Consequences

- The funnel becomes measurable without a consent banner or a privacy policy rewrite.
- The badge row on the README (Lighthouse scores, checks passing) is itself signal for the engineering audience.
- GoatCounter's free tier is a dependency; failure mode is silent no-data, never breakage. Plausible ($) rejected on cost; GA4 rejected on cookies/banner/taste.
