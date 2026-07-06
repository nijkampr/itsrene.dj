# PRD-03 · Live Presence (Twitch)

**Problem:** Twitch is the strongest channel (1,531 followers, two teams) but the site treats it as a paragraph and hides the numbers. There's no signal when a stream is actually happening. **Outcome:** a LIVE section that leads with real stats, states the schedule honestly, and lights up when streaming.

**Depends on:** PRD-01, ADR-0005.

## Scope

1. **Stat row:** followers (1,531 — update from data, see open question), 6+ years streaming, 500+ hours, 270+ peak viewers — Archivo numerals, mono captions, consistent with hero treatment. Fix the 270/300 inconsistency: one number, sourced.
2. **Live check:** the decapi pattern from ADR-0005. Offline (default, fully designed): "Usually evenings CET · no fixed schedule · follow for the ping" + follow link. Live: section header gains `--itr` LIVE badge + uptime, CTA becomes "WATCHING NOW →".
3. **Teams:** Team Brisk and Birdcage Radio as quiet mono links with one-line context (community credibility for the co-DJ audience).
4. **What-to-expect copy:** rewrite of the current two-card block into one tight paragraph, first person, one wink max.

## Non-goals

Twitch iframe embeds, VOD listings, schedule calendar/.ics (backlog candidate if streaming cadence ever stabilizes), viewer counts via polling.

## Acceptance

- Offline state is indistinguishable from a designed static section (no spinner, no layout shift when the check resolves — badge space is reserved).
- decapi timeout/failure = offline state, verified by blocking the request in DevTools.
- Follower count doesn't hard-code drift: rendered from `data/stats.json` (hand-updated or Action-updated later), not from HTML.

## Open question

Whether the sync Action (ADR-0004) should also refresh `stats.json` weekly via decapi — cheap to add, keeps the strongest number honest. Recommended: yes, same workflow, second job step.
