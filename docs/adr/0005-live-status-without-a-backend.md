# ADR-0005: Twitch live status without a backend

**Status:** Accepted · 2026-07-06

## Context

The Twitch funnel is the strongest channel (1,531 followers), and "is he live right now?" is the one truly dynamic fact worth showing. The Twitch Helix API requires OAuth — impossible to do honestly from a static page without leaking credentials.

## Decision

Use **decapi.me** (public, CORS-friendly, plaintext Twitch proxy) from the client, wrapped in a strict progressive-enhancement pattern:

1. On load, `js/main.js` fires one request to `https://decapi.me/twitch/uptime/itsrene_nl` with a 3s timeout.
2. Response contains an uptime → swap the static "CATCH ME LIVE" block into a **LIVE NOW** state (accent treatment + direct link).
3. Response is "offline" / error / timeout → the default offline state stays. The default is fully designed; live is the bonus state.
4. No polling. One check per page load is enough for a portfolio.

## Consequences

- Zero secrets, zero backend, zero cost.
- decapi is a free third-party service and may die. Failure mode is explicitly the designed default state — visitors never see breakage. If it dies permanently, delete 15 lines of JS.
- A Twitch iframe embed was rejected: heavyweight, requires `parent` config, shows a grey box when offline (which is most of the time).
- A scheduled Action writing `live.json` was rejected: a 5-minute cron on a free runner to track a hobby stream schedule is waste, and 15-minute staleness makes "LIVE" a lie half the time.
