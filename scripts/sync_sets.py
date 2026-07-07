#!/usr/bin/env python3
"""Sync data/sets.json from the SoundCloud RSS feed and refresh data/stats.json.

Zero-auth, stdlib only (see ADR-0004). Curated fields in sets.json
(vibe, featured, note) always win over feed data — the sync merges,
it never clobbers. New uploads arrive with vibe=null until curated.

Run from the repo root:  python3 scripts/sync_sets.py
Exit code 0 always; prints CHANGED or UNCHANGED for the workflow to read.
"""
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date, datetime
from email.utils import parsedate_to_datetime

RSS_URL = "https://feeds.soundcloud.com/users/soundcloud:users:1009672477/sounds.rss"
STATS_URL = "https://decapi.me/twitch/followcount/itsrene_nl"
SETS_PATH = "data/sets.json"
STATS_PATH = "data/stats.json"
TIMEOUT = 20


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "itsrene.dj sync (github actions)"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return r.read()


def clean_title(title, fallback_date):
    """Strip embedded dates from SoundCloud titles; prefer the title's own date."""
    t, d = title.strip(), fallback_date
    m = re.match(r"^(\d{4})\s*-\s*(\d{2})\s*-\s*(\d{2})[\s,.]*(.*)$", t)
    if m and m.group(4):
        d = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
        t = m.group(4).strip()
    m = re.search(r"[\s,]*\b(?:(\d{2})-(\d{2})-(\d{4})|(\d{4})\s*-\s*(\d{2})\s*-\s*(\d{2}))\s*$", t)
    if m:
        d = f"{m.group(3)}-{m.group(2)}-{m.group(1)}" if m.group(1) else f"{m.group(4)}-{m.group(5)}-{m.group(6)}"
        t = t[: m.start()].strip()
    t = t.replace("->", "→").rstrip(".").strip()
    return (t[0].upper() + t[1:] if t else t), d


def sync_sets():
    with open(SETS_PATH) as f:
        current = json.load(f)
    curated = {s["permalink"].rsplit("/", 1)[-1]: s for s in current["sets"]}

    feed = ET.fromstring(fetch(RSS_URL))
    merged = []
    for item in feed.findall(".//item"):
        link = item.findtext("link").strip()
        slug = link.rsplit("/", 1)[-1]
        pub = parsedate_to_datetime(item.findtext("pubDate")).strftime("%Y-%m-%d")
        title, when = clean_title(item.findtext("title"), pub)
        existing = curated.get(slug)
        if existing:
            # curated entry wins wholesale — date fixes and vibes are human decisions
            merged.append(existing)
        else:
            merged.append({"date": when, "title": title, "permalink": link, "vibe": None})

    merged.sort(key=lambda s: s["date"], reverse=True)
    changed = merged != current["sets"]
    if changed:
        current["sets"] = merged
        with open(SETS_PATH, "w") as f:
            json.dump(current, f, indent=1, ensure_ascii=False)
            f.write("\n")
    return changed, len(merged)


def sync_stats(set_count):
    with open(STATS_PATH) as f:
        stats = json.load(f)
    before = dict(stats)
    try:
        followers = int(fetch(STATS_URL).decode().strip())
        if followers > 0:
            stats["twitchFollowers"] = followers
    except (ValueError, OSError):
        pass  # decapi hiccup: keep the old number, never break the site
    stats["sets"] = set_count
    if stats != before:
        stats["updated"] = date.today().isoformat()
        with open(STATS_PATH, "w") as f:
            json.dump(stats, f, indent=1, ensure_ascii=False)
            f.write("\n")
        return True
    return False


if __name__ == "__main__":
    sets_changed, count = sync_sets()
    stats_changed = sync_stats(count)
    print("CHANGED" if (sets_changed or stats_changed) else "UNCHANGED")
    print(f"sets={count} sets_changed={sets_changed} stats_changed={stats_changed}", file=sys.stderr)
