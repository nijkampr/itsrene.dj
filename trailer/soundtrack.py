#!/usr/bin/env python3
"""
IT'S RENÉ · trailer soundtrack. 59 seconds, one set, 120 -> 175 BPM.

Everything is synthesised here from numpy noise and sine waves: no samples,
no loops, no licences. This script is also the master clock: it writes
timeline.json (every beat, section and hit) and the renderer cuts on it,
so picture and sound can't drift apart.

    python3 trailer/soundtrack.py      # -> trailer/build/soundtrack.wav + trailer/timeline.json
"""
import json
import os

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, fftconvolve, sosfilt

SR = 48000
DUR = 59.0
N = int(SR * DUR)
HERE = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(1529)  # the follower count, obviously

# ---------------------------------------------------------------- tempo map
# The site's energy rail, compressed: 00:00 120 · 01:00 128 · 02:00 140 · 03:00 150 · 04:00 175.
beats, sections = [], []
_t = 0.0


def section(name, label, marker, bpms):
    global _t
    start = _t
    for i, bpm in enumerate(bpms):
        beats.append({"t": round(_t, 5), "bpm": round(bpm, 2), "sec": name, "i": i})
        _t += 60.0 / bpm
    sections.append({"name": name, "label": label, "marker": marker, "start": round(start, 5),
                     "end": round(_t, 5), "bpm0": bpms[0], "bpm1": bpms[-1]})


section("A", "Opener", "00:00", [120] * 16)
section("B", "Listen", "01:00", [128] * 16)
section("C", "Live", "02:00", [140] * 24)
section("D", "Played", "03:00", [150] * 24)
section("E", "Build", "03:30", [150 + 25 * (i / 15) ** 1.6 for i in range(16)])
section("GAP", "", "", [175])
section("F", "Book", "04:00", [175] * 32)
sections.append({"name": "G", "label": "", "marker": "", "start": round(_t, 5), "end": DUR,
                 "bpm0": 175, "bpm1": 175})
G0 = _t


def sec(name):
    return next(s for s in sections if s["name"] == name)


def sbeats(name):
    return [b for b in beats if b["sec"] == name]


# named hits the picture also needs
hits = {
    "brace_l": G0 + 0.62,
    "brace_r": G0 + 0.74,
    "word": G0 + 1.05,
    "url": G0 + 2.30,
    "shut": G0 + 5.05,
}

# ---------------------------------------------------------------- dsp bits
def sos(kind, f, order=2):
    return butter(order, f, kind, fs=SR, output="sos")


def lp(x, f, o=2): return sosfilt(sos("low", f, o), x)
def hp(x, f, o=2): return sosfilt(sos("high", f, o), x)
def bp(x, lo, hi, o=2): return sosfilt(sos("band", [lo, hi], o), x)


def tt(d): return np.arange(int(d * SR)) / SR
def noise(d): return rng.standard_normal(int(d * SR))
def saw(f, t): return 2.0 * ((f * t) % 1.0) - 1.0


def sweep_sine(f_of_t):
    return np.sin(2 * np.pi * np.cumsum(f_of_t) / SR)


def fade(x, a=0.002, r=0.01):
    x = x.copy()
    na, nr = int(a * SR), int(r * SR)
    if na: x[:na] *= np.linspace(0, 1, na)
    if nr: x[-nr:] *= np.linspace(1, 0, nr)
    return x


def norm(x, peak=1.0):
    m = np.max(np.abs(x))
    return x * (peak / m) if m else x


L = np.zeros(N + SR * 4)
R = np.zeros(N + SR * 4)
VL = np.zeros_like(L)  # reverb send
VR = np.zeros_like(L)


def put(sig, t, gain=1.0, pan=0.0, verb=0.0):
    i = int(round(t * SR))
    if i >= len(L): return
    sig = sig[: len(L) - i] * gain
    gl, gr = np.sqrt(0.5 * (1 - pan)), np.sqrt(0.5 * (1 + pan))
    L[i:i + len(sig)] += sig * gl
    R[i:i + len(sig)] += sig * gr
    if verb:
        VL[i:i + len(sig)] += sig * gl * verb
        VR[i:i + len(sig)] += sig * gr * verb


def put_st(l, r, t=0.0, gain=1.0):
    i = int(round(t * SR))
    n = min(len(l), len(L) - i)
    L[i:i + n] += l[:n] * gain
    R[i:i + n] += r[:n] * gain


# ---------------------------------------------------------------- instruments
def kick_soft():
    t = tt(0.45)
    x = sweep_sine(48 + 62 * np.exp(-t / 0.035)) * np.exp(-t / 0.16)
    return fade(lp(x, 380))


def kick_techno():
    t = tt(0.42)
    body = sweep_sine(46 + 150 * np.exp(-t / 0.026)) * np.exp(-t / 0.19)
    click = hp(noise(0.42), 2500) * np.exp(-t / 0.003) * 0.35
    return fade(norm(np.tanh(2.2 * (body + click))), r=0.03)


def kick_hard():
    # gabber-ish: fast pitch dive into a tuned, driven tail
    t = tt(0.335)
    f = 54 + 520 * np.exp(-t / 0.009) + 70 * np.exp(-t / 0.05)
    body = sweep_sine(f) * np.where(t < 0.24, 1.0, np.exp(-(t - 0.24) / 0.03))
    x = np.tanh(7.5 * body)
    x = lp(x, 5200) + 0.35 * bp(x, 900, 2600)
    x += hp(noise(0.335), 3000) * np.exp(-t / 0.004) * 0.6
    return fade(norm(x), r=0.02)


def hat(d=0.02, length=0.12):
    t = tt(length)
    return fade(hp(noise(length), 7500, 4) * np.exp(-t / d))


def clap():
    t = tt(0.5)
    n = bp(noise(0.5), 900, 3200)
    env = sum(np.where(t >= o, np.exp(-(t - o) / 0.006), 0) for o in (0, 0.011, 0.023))
    env += np.where(t >= 0.03, np.exp(-(t - 0.03) / 0.09), 0) * 0.6
    return fade(n * env)


def snare():
    t = tt(0.3)
    tone = np.sin(2 * np.pi * 185 * t) * np.exp(-t / 0.05) * 0.6
    n = bp(noise(0.3), 1400, 9000) * np.exp(-t / 0.09)
    return fade(tone + n)


def crash(d=2.4):
    t = tt(d)
    return fade(hp(noise(d), 4500, 3) * np.exp(-t / 0.7), r=0.3)


def boom(d=2.2, f0=62, f1=28):
    t = tt(d)
    return fade(sweep_sine(f1 + (f0 - f1) * np.exp(-t / 0.35)) * np.exp(-t / 0.7), r=0.3)


def clack():
    # the brace snapping in: inharmonic metal + a knuckle of low end
    t = tt(0.25)
    m = (np.sin(2 * np.pi * 1730 * t) + 0.7 * np.sin(2 * np.pi * 2610 * t) + 0.4 * np.sin(2 * np.pi * 4150 * t))
    x = m * np.exp(-t / 0.018) * 0.5 + bp(noise(0.25), 1200, 6000) * np.exp(-t / 0.008)
    x += np.sin(2 * np.pi * 70 * t) * np.exp(-t / 0.05)
    return fade(x)


def reverse_swell(d):
    t = tt(d)
    return fade(hp(noise(d), 3000, 2) * (t / d) ** 3, a=0.05, r=0.004)


def note(n):  # midi -> Hz
    return 440.0 * 2 ** ((n - 69) / 12)


D1, D2, Eb2, F2, A2, D3, Eb3, F3, A3, C4, D4, E4, F4, Eb4, A4, C5, D5, E5 = (
    26, 38, 39, 41, 45, 50, 51, 53, 57, 60, 62, 64, 65, 63, 69, 72, 74, 76)

# ---------------------------------------------------------------- sidechain curve
kick_times = []  # (t, kind)
for b in beats:
    s = b["sec"]
    if s == "A" and b["i"] >= 8 and b["i"] % 2 == 0: kick_times.append((b["t"], "heart"))
    elif s == "B": kick_times.append((b["t"], "soft"))
    elif s in ("C", "D"): kick_times.append((b["t"], "techno"))
    elif s == "E" and b["i"] < 12: kick_times.append((b["t"], "techno"))
    elif s == "F": kick_times.append((b["t"], "hard"))
kick_times.append((G0, "final"))

T = np.arange(len(L)) / SR
duck = np.ones_like(T)
for kt, kind in kick_times:
    if kind in ("techno", "hard", "final"):
        i = int(kt * SR)
        n = int(0.3 * SR)
        seg = T[i:i + n] - kt
        duck[i:i + n] = np.minimum(duck[i:i + n], 1 - (0.75 if kind != "techno" else 0.6) * np.exp(-seg / 0.09))


def envelope(points):
    """piecewise-linear gain over the whole timeline: [(t, g), ...]"""
    ts, gs = zip(*points)
    return np.interp(T, ts, gs)


A, B, C, Dd, E, GAP, F = (sec(n) for n in ("A", "B", "C", "D", "E", "GAP", "F"))

# ---------------------------------------------------------------- the drone (the gloom)
dt = T
drone = np.zeros_like(T)
for f, g in ((note(D2), 1.0), (note(D2) * 1.003, 0.8), (note(A2), 0.45), (note(D1), 0.9)):
    drone += saw(f, dt) * g
drone_dark = lp(drone, 220, 2)
drone_air = lp(drone, 900, 2) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.07 * dt))
rub = lp(saw(note(Eb2), dt) + saw(note(Eb2) * 1.004, dt), 500)  # the minor second: pure dread
drone_env = envelope([(0, 0), (1.5, 0.35), (6, 0.8), (B["start"], 0.7), (C["start"], 0.35), (E["start"], 0.35),
                      (GAP["start"] - 0.01, 0.6), (GAP["start"], 0), (F["start"], 0), (F["start"] + 0.01, 0.22),
                      (G0 - 0.01, 0.22), (G0, 0.7), (57.8, 0.6), (DUR, 0)])
rub_env = envelope([(0, 0), (4, 0), (7.5, 0.25), (B["start"] + 1, 0), (G0 + 0.5, 0), (G0 + 2.5, 0.2), (57.8, 0.15),
                    (DUR, 0)])
mono = (drone_dark + 0.25 * drone_air) * drone_env * duck + rub * rub_env
put_st(mono * 0.16, np.roll(mono, 180) * 0.16)

# rain / room air: pink-ish noise, only when the room is empty
air = lp(hp(np.cumsum(rng.standard_normal(len(T))) * 0.02 + rng.standard_normal(len(T)) * 0.3, 350), 2800)
air_env = envelope([(0, 0), (0.8, 0.6), (C["start"], 0.25), (C["start"] + 0.5, 0), (G0 + 0.3, 0), (G0 + 1.5, 0.5),
                    (58.3, 0.4), (DUR, 0)])
put_st(air * air_env * 0.05, np.roll(air, 2400) * air_env * 0.05)

# ---------------------------------------------------------------- A · opener: heartbeat in the dark
ks, kt_, kh = kick_soft(), kick_techno(), kick_hard()
for kt, kind in kick_times:
    if kind == "heart":
        put(ks, kt, 0.55); put(ks, kt + 0.2, 0.3)
put(reverse_swell(1.2), B["start"] - 1.2, 0.18, verb=0.4)

# ---------------------------------------------------------------- B · listen: melodic, then underground
bus_l = np.zeros_like(L); bus_r = np.zeros_like(L)
bd = sbeats("B")
beat = 60 / 128


def bput(sig, t, gain=1.0, pan=0.0):
    i = int(t * SR)
    n = min(len(sig), len(bus_l) - i)
    bus_l[i:i + n] += sig[:n] * gain * np.sqrt(0.5 * (1 - pan))
    bus_r[i:i + n] += sig[:n] * gain * np.sqrt(0.5 * (1 + pan))


for b in bd:
    bput(ks, b["t"], 0.9)
    bput(hat(0.03), b["t"] + beat / 2, 0.12, 0.3)
# pad: Dm9, slow and wide
pd = B["end"] - B["start"] + 0.8
t = tt(pd)
for k, n in enumerate((D3, F3, A3, C4, E4)):
    for det, pan in ((0.997, -0.6), (1.003, 0.6)):
        s = lp(saw(note(n) * det, t), 1700) * np.minimum(t / 0.8, 1) * np.minimum((pd - t) / 0.6, 1)
        bput(s, B["start"], 0.035, pan)
# arp: a melodic-house pluck, echoing
arp = [D4, A4, F4, C5, A4, F4, E5, A4]
t = tt(0.4)
for j in range(64):
    ts = B["start"] + j * beat / 4
    p = lp(saw(note(arp[j % 8]), t), 2600) * np.exp(-t / 0.08)
    for e, g in ((0, 1), (3, 0.4), (6, 0.16)):
        bput(fade(p), ts + e * beat / 4, 0.07 * g, (-0.4, 0.4, 0)[e // 3 % 3])
# the descent: bars 3-4 go through the floor (open -> muffled)
dark_l, dark_r = lp(bus_l, 320, 4), lp(bus_r, 320, 4)
mix = envelope([(0, 0), (B["start"] + 2 * 4 * beat, 0), (B["start"] + 3 * 4 * beat, 1), (99, 1)])
put_st(bus_l * (1 - mix) + dark_l * mix * 1.5, bus_r * (1 - mix) + dark_r * mix * 1.5)
VL[: len(bus_l)] += bus_l * 0.25 * (1 - mix); VR[: len(bus_r)] += bus_r * 0.25 * (1 - mix)
put(boom(1.8, 70, 30), B["start"] + 2 * 4 * beat, 0.5)  # the floor gives
put(reverse_swell(1.0), C["start"] - 1.0, 0.25, verb=0.5)

# ---------------------------------------------------------------- C + D · techno: kick, rumble, hats, stabs
rumble_t = tt(0.16)
rumble = fade(lp(np.tanh(3 * np.sin(2 * np.pi * note(D2) * rumble_t)), 170) * np.exp(-rumble_t / 0.07))
stab_t = tt(0.16)
stab = sum(lp(saw(note(n) * d, stab_t), 2400) for n in (D3, Eb3, A3, D4) for d in (0.996, 1.004))
stab = fade(bp(stab, 300, 3500) * np.exp(-stab_t / 0.05))
for name in ("C", "D"):
    s = sec(name)
    bb = sbeats(name)
    q = 60 / s["bpm0"]
    for b in bb:
        bar, pos = divmod(b["i"], 4)
        put(kt_, b["t"], 0.7)
        for k in (1, 2, 3):
            put(rumble, b["t"] + k * q / 4, 0.4 * (0.6 if k == 2 else 1))
        put(hat(0.035), b["t"] + q / 2, 0.22, 0.25)
        if name == "D":
            for k in (1, 3):
                put(hat(0.012), b["t"] + k * q / 4, 0.1 + (0.08 if bar >= 4 else 0), -0.3)
        if pos in (1, 3) and (name == "D" or bar >= 1):
            put(clap(), b["t"], 0.3, verb=0.35)
    if name == "D":
        # industrial stab, syncopated, every bar
        for bar in range(6):
            t0 = s["start"] + bar * 4 * q
            for sx in (0, 3, 6, 10, 13):
                put(stab, t0 + sx * q / 4, 0.12, 0.2 * (1 if sx % 2 else -1), verb=0.5)
put(crash(1.4), Dd["start"], 0.12)

# ---------------------------------------------------------------- E · the build: accelerating roll + riser
eb = sbeats("E")
for b in eb:
    if b["i"] < 12: put(kt_, b["t"], 0.9)
    q = 60 / b["bpm"]
    div = 2 if b["i"] < 8 else 4 if b["i"] < 12 else 8
    for k in range(div):
        v = 0.12 + 0.5 * ((b["i"] + k / div) / 16) ** 1.4
        put(snare(), b["t"] + k * q / div, v, 0.0, verb=0.3)
e0, e1 = E["start"], GAP["start"]
n = int((e1 - e0) * SR)
wn = rng.standard_normal(n)
cut = 300 * (9000 / 300) ** (np.arange(n) / n)
alpha = 1 - np.exp(-2 * np.pi * cut / SR)
lo = np.empty(n); y = 0.0
for i in range(n):
    y += alpha[i] * (wn[i] - y); lo[i] = y
riser = (wn - lo) * np.linspace(0.05, 1, n) ** 2
put(fade(riser, r=0.003), e0, 0.22, verb=0.3)
tr = np.arange(n) / SR
pitch = note(D3) * 4 ** ((tr / tr[-1]) ** 2)
screamer = lp(saw(1, np.cumsum(pitch) / SR) + saw(1, np.cumsum(pitch * 1.01) / SR), 3000)
put(fade(screamer * np.linspace(0, 1, n) ** 2, r=0.003), e0, 0.06)
# GAP: nothing. Absolutely nothing. That's the point.

# ---------------------------------------------------------------- F · the drop, 175
fb = sbeats("F")
q = 60 / 175
put(crash(), F["start"], 0.3)
put(boom(1.6, 80, 32), F["start"], 0.7)
put(crash(1.2), F["start"] + 2 * q, 0.15)  # "ME"
lead_t = tt(0.13)
roots = [D4, D4, F4, Eb4]
for b in fb:
    bar, pos = divmod(b["i"], 4)
    put(kh, b["t"], 1.15)
    put(hat(0.05, 0.2), b["t"] + q / 2, 0.22, 0.2)
    if bar >= 4 and pos in (1, 3):
        put(clap(), b["t"], 0.35, verb=0.3)
    r = roots[bar % 4]
    for n_ in (r, r + 7):
        s = sum(saw(note(n_) * d, lead_t) for d in (0.99, 0.997, 1.0, 1.004, 1.011))
        s = fade(lp(np.tanh(2.5 * s), 3600) * np.exp(-lead_t / 0.07))
        put(s, b["t"] + q / 2, 0.075, 0.35 if n_ == r else -0.35, verb=0.25)
put(reverse_swell(q * 4), G0 - q * 4, 0.15)

# ---------------------------------------------------------------- G · the end card
put(kh, G0, 1.0, verb=0.6)
put(crash(3.0), G0, 0.3, verb=0.5)
put(boom(3.5, 58, 24), G0, 0.9)
put(clack(), hits["brace_l"], 0.5, -0.5, verb=0.5)
put(clack(), hits["brace_r"], 0.5, 0.5, verb=0.5)
put(reverse_swell(0.35), hits["word"] - 0.35, 0.12, verb=0.3)
put(clack(), hits["shut"], 0.6, 0, verb=0.8)
put(boom(2.5, 50, 26), hits["shut"], 0.6)

# ---------------------------------------------------------------- reverb + master
ir_t = tt(3.2)
ir_l = lp(rng.standard_normal(len(ir_t)), 5500) * np.exp(-ir_t / 0.55)
ir_r = lp(rng.standard_normal(len(ir_t)), 5500) * np.exp(-ir_t / 0.55)
pre = int(0.025 * SR)
ir_l = np.concatenate([np.zeros(pre), ir_l]) / np.sqrt(np.sum(ir_l ** 2))
ir_r = np.concatenate([np.zeros(pre), ir_r]) / np.sqrt(np.sum(ir_r ** 2))
wet_l = fftconvolve(VL, ir_l)[: len(L)] * duck
wet_r = fftconvolve(VR, ir_r)[: len(R)] * duck
ml, mr = L + wet_l * 0.5, R + wet_r * 0.5
ml, mr = hp(ml, 28), hp(mr, 28)
ml, mr = ml[:N], mr[:N]
peak = max(np.max(np.abs(ml)), np.max(np.abs(mr)))
ml, mr = np.tanh(1.6 * ml / peak) / np.tanh(1.6), np.tanh(1.6 * mr / peak) / np.tanh(1.6)
end = envelope([(0, 1), (DUR - 0.6, 1), (DUR, 0)])[:N]
out = np.stack([ml, mr], 1) * end[:, None] * 0.89
os.makedirs(os.path.join(HERE, "build"), exist_ok=True)
wavfile.write(os.path.join(HERE, "build", "soundtrack.wav"), SR, (out * 32767).astype(np.int16))

with open(os.path.join(HERE, "timeline.json"), "w", encoding="utf-8") as f:
    json.dump({"duration": DUR, "sections": sections, "beats": beats, "hits": hits,
               "kicks": [{"t": round(k, 5), "kind": kind} for k, kind in kick_times]},
              f, indent=1, ensure_ascii=False)
    f.write("\n")
print("soundtrack.wav + timeline.json written ·", " · ".join(f'{s["name"]} {s["start"]:.2f}' for s in sections))
