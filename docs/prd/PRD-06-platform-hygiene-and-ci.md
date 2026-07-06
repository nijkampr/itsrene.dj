# PRD-06 · Platform Hygiene, SEO & CI

**Problem:** shipped defects (broken FAQ JSON-LD, ~40MB payload, stale claims) prove the real gap: nothing verifies the site. **Outcome:** defects fixed, measurement on, and CI that makes this class of bug impossible to ship again.

**Depends on:** ADR-0003, ADR-0006. The quick fixes below are **Block 0** in the backlog — they land *before* the redesign, on the current site, because they're live bugs.

## Scope

**Immediate fixes (current site, no redesign needed):**
1. FAQ JSON-LD: add the missing `}` closing the last Question object (~line 233 `index.html`). Verify all four JSON-LD blocks parse; run Google Rich Results Test.
2. Delete unused `images/53799373426_94907c72b4_o.jpg` (11MB) and `images/gotoams_2024.jpg` if unreferenced; archive originals off-repo.
3. Run the ADR-0003 script over the four referenced action shots + headshot (40MB → ~1.5MB); add `loading="lazy"`, `width`/`height`.
4. Copy triage: person-switch in bio, 270 vs 300 viewers, footer year → remove the year entirely, drop the stale "LATEST/August 2025/most recent banger" framing, remove `twitter:creator` (account not surfaced anywhere).

**Structured data (redesign-aligned):**
5. Consolidate four JSON-LD blocks → two: `Person` (musician, sameAs, memberOf) and `MusicGroup`/`LocalBusiness` — decide once, delete FAQ schema (Google largely stopped showing FAQ rich results for non-authority sites in 2023; it's dead weight). ContactPoint folds into Person.
6. Dedicated OG image (1200×630, poster-style, from the design system) instead of the raw headshot.

**CI & measurement:**
7. `.github/workflows/checks.yml`: Lighthouse CI (budgets per ADR-0006), html-validate, JSON-LD parse check, image-size guard.
8. `.github/workflows/sync-sets.yml`: weekly SoundCloud RSS → `sets.json` merge (ADR-0004), plus decapi → `stats.json` refresh.
9. GoatCounter with the five funnel events (view, book-click, presskit-download, twitch-out, soundcloud-out).
10. README refresh: what this repo is, badges, pointer to `docs/`.

## Acceptance

- Rich Results Test: zero errors. PageSpeed Insights mobile ≥ 95 performance **before** the redesign lands (fixes 1–4 alone should get close).
- Both workflows green; sync workflow proven by a manual dispatch producing a correct `sets.json` diff.
- A deliberately broken JSON-LD block in a test branch fails CI.
