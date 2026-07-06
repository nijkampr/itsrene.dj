# Platform Snapshot — July 2026

Raw numbers pulled from public sources on 2026-07-06. This grounds every claim in the brief and PRDs. Refresh when starting a new block of work.

## Twitch — twitch.tv/itsrene_nl

| Metric | Value | Source |
|---|---|---|
| Followers | 1,531 | decapi.me/twitch/followcount |
| Account age | 6 years, 3 months | decapi.me/twitch/accountage |
| Teams | Team Brisk, Birdcage Radio | site copy (verify on Twitch) |

**The takeaway:** 1,531 Twitch followers is the strongest public number René has. The current site hides it and leads with "270+ peak viewers" instead.

## SoundCloud — soundcloud.com/itsrene_nl (user id: 1009672477)

| Metric | Value |
|---|---|
| Tracks | 32 |
| Followers | 35 |
| Likes given | 16 |
| Profile bio | **empty** |
| Profile city/country | **not set** |

**Zero-auth data source:** `https://feeds.soundcloud.com/users/soundcloud:users:1009672477/sounds.rss` returns the full catalog as RSS. No API key needed. This powers the Listen hub automation (ADR-0004).

### Full catalog (RSS, newest first)

| Date | Title |
|---|---|
| 2025-08-17 | Loads of techno |
| 2024-05-11 | Mainframe May Edition |
| 2024-02-23 | Birdcage Mini - Thon - Birdie Love → Melodic & House |
| 2024-01-20 | TECNOOOOO |
| 2024-01-12 | Open Format Thursday Thumpers |
| 2023-10-07 | Just A Really Random Evening |
| 2023-10-06 | Lets Do Some House |
| 2023-08-18 | Melodic Dubss |
| 2023-06-28 | Potentially my hardest set ever |
| 2023-05-13 | Really Late Night Melodic Stuff |
| 2023-04-15 | Saturday Sounds |
| 2023-03-21 | Melodic To Tronce |
| 2023-02-13 | Flek C's 40 hour Funked up and Filthy 40th! |
| 2023-02-13 | Brisk's Big 51st Birthday Bash |
| 2023-01-30 | BwoB Presents: Mates and Crates — Techno n Stuff |
| 2023-01-30 | BwoB Presents: Mates and Crates — Melodic |
| 2022-12-30 | The Aphotic Zone vol4 |
| 2022-11-17 | ArtBeats 17-11-2022 |
| 2022-11-02 | Twitch DJ's Techno Raid Train |
| 2022-10-12 | Tech-Yes |
| 2022-08-19 | Friday In Between Meetings Techno |
| 2022-04-22 | Teknostorm2 Lets get banging |
| 2022-04-01 | The Aphotic Zone vol2 — Live on KonceptK |
| 2022-03-27 | TeknoStorm vol1 at KonceptK — The Aphotic Zone vol1 |
| 2022-03-21 | Guest Stream — Liona Stone — The First |
| 2022-03-20 | DJ Brisk 50th BDAY |
| 2022-03-20 | Tech-YES 2022-01-12 |
| 2022-03-20 | Guest Stream — Liona Stone — The Second |
| 2021-09-22 | TechYes VI |
| 2021-09-12 | (Dark) Techno for VFest |
| 2021-07-19 | CoxFest — The Chris Cox Megamix |
| 2021-07-19 | Late Night Set — Tekno |

## Ko-fi — ko-fi.com/itsrene_nl

Blocked from automated fetch (403). Linked from site; verify manually whether it's worth keeping front-and-center or demoting to footer.

## itsrene.nl (the day-job portfolio)

Live: "Product & Integration Architect" portfolio, 17+ years experience, mentions DJing under "Creative Edge." Cross-linking opportunity in both directions — the tech site already points at the creative side.

## Known IRL gigs (from site copy + images)

- ADE stages, Amsterdam
- GoToAms 2024 (conference closing party)
- BB Summer Party
- KonceptK (TeknoStorm vol1, Aphotic Zone vol2 — 2022)
- Conference closing parties, house parties, office events
- First sets at 15 in Sexbierum

**Gap worth knowing:** newest SoundCloud upload is 2025-08-17 — 11 months old at snapshot time. The site calls it "my most recent banger," which now reads stale. The redesign must not hard-code recency claims (see ADR-0004).
