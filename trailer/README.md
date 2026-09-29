# Trailer

A 59-second trailer for IT'S RENÉ, built the way the site is built: by hand, from the repo's own fonts, photos and `data/`. **Not linked from the site.** It is here to be looked at first.

The concept is the site's concept ("The Build"): the trailer *is* a set. The tempo ramps along the energy rail, 120 → 128 → 140 → 150 → 175 BPM, and every cut lands on the beat because picture and sound come from the same beat grid.

| Time | Set clock | BPM | Section | What happens |
|---|---|---|---|---|
| 0:00 | 00:00 | 120 | Opener | Coordinates typed into the dark. "It starts at the surface." A heartbeat. |
| 0:08 | 01:00 | 128 | Listen | FROM MAINSTREAM. The camera drops through the ground line (0.00 m NAP) and the music drops with it: TO UNDERGROUND. |
| 0:15 | 02:00 | 140 | Live | OFFLINE flips to LIVE. 500+ hours, 1,529 followers, 6 years, 32 sets, the two crews. |
| 0:26 | 03:00 | 150 | Played | Duotone rooms, the gig timetable, "Sexbierum, at 15. It escalated." |
| 0:35 | 03:30 | 150→175 | Build | One vibe per beat, melodic to chaos, BPM counter climbing. |
| 0:41 | 04:00 | — | | One beat of silence. |
| 0:42 | 04:00 | 175 | Book | The drop is the booking CTA. BOOK ME, the rooms, the facts, dj@itsrene.nl. |
| 0:53 | | | Ident | The braces snap in, the name flips up, the braces slam shut. Song requests: no. |

Numbers come from `data/stats.json` and the timetable from `data/gigs.json` at render time, so a re-render after the weekly sync stays true.

## Files

- `soundtrack.py`: synthesises the whole soundtrack from numpy sine waves and noise (no samples, no licences) and writes `timeline.json`, the beat grid everything else cuts on.
- `trailer.html`: the renderer. `render(t)` draws one frame on a 1920×1080 canvas. Opened in a browser it is also a preview player with the audio and a scrub bar.
- `capture.mjs`: steps `render(t)` at 30 fps in headless Chromium and pipes the frames into ffmpeg.
- `build/`: output, git-ignored.

## Render

```bash
pip install numpy scipy                      # soundtrack only
python3 trailer/soundtrack.py                # -> build/soundtrack.wav + timeline.json
python3 -m http.server 8000 &                # from the repo root
open http://localhost:8000/trailer/trailer.html   # preview with sound
node trailer/capture.mjs                     # -> build/itsrene-trailer.mp4 (needs playwright + ffmpeg with libx264)
node trailer/capture.mjs --stills 12.5 44    # single frames as PNG
```

`FFMPEG=/path/to/ffmpeg` and `PLAYWRIGHT=/path/to/playwright` override the defaults.
