"""Som do Big Bang: voz + trilha (Echoes of Time, Kevin MacLeod, CC-BY) + efeitos sintetizados nos instantes das cenas.
Junta com bigbang_visual.mp4 -> ../renders/bigbang_v3.mp4 (+ _share em crf 25)."""
import json, re, subprocess
from pathlib import Path
import numpy as np

D = Path(__file__).parent; ROOT = D.parents[2]; SR = 48000
raw = json.loads((D.parent / "assets" / "timing_raw.json").read_text(encoding="utf-8"))
W = [w for w in raw["words"] if any(c.isalnum() for c in w["w"])]
B = raw["blocks"]; vend = max(w["e"] for w in raw["words"]); dur = vend + 3.0


def wt(w, after=0):
    return next(x["s"] for x in W if x["s"] >= after and re.sub(r"[^a-z0-9]", "", x["w"].lower()) == w)


rng = np.random.default_rng(1)
def env(n, a, d): t = np.arange(n) / SR; return np.minimum(t / a, 1) * np.exp(-t / d)
def boom(d=3.0):
    n = int(d * SR); t = np.arange(n) / SR
    f = 30 + 70 * np.exp(-t * 3); s = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.005, 0.9)
    no = np.convolve(rng.standard_normal(n), np.ones(60) / 60, "same") * env(n, 0.002, 0.35)
    return s * 0.9 + no * 1.6
def whoosh(d=1.0, up=False):
    n = int(d * SR); t = np.arange(n) / SR
    no = rng.standard_normal(n); k = 8 + 40 * (t / d if up else 1 - t / d)
    out = np.zeros(n); y = 0.0
    for i in range(n): a = 1 / k[int(i)]; y += a * (no[i] - y); out[i] = y  # passa-baixa que varre
    shape = np.sin(np.pi * t / d) ** (1.5 if not up else 0.6)
    if up: shape *= (t / d) ** 2 + 0.1
    return out * shape * 3
def chime(d=2.5, f0=880):
    n = int(d * SR); t = np.arange(n) / SR
    return sum(np.sin(2 * np.pi * f0 * m * t) / m for m in (1, 2.01, 3.02)) * env(n, 0.004, 0.7) * 0.25
def thud(d=1.2): n = int(d * SR); t = np.arange(n) / SR; return np.sin(2 * np.pi * (55 + 40 * np.exp(-t * 8)) * t) * env(n, 0.003, 0.25)

ev = [(0.8 - 0.05, boom(), 1.0), (0.0, whoosh(0.85, up=True), 0.5)]
s2 = B[2]; tStr = wt("stretched", s2)
ev += [(tStr - 1.0, whoosh(1.1, up=True), 0.9), (tStr, boom(2.2), 0.6)]
ev += [(b - 0.35, whoosh(0.8), 0.45) for b in (B[1], B[3], B[4], B[5], B[6])]
ev += [(wt("hot", B[1]) - 0.1, thud(), 0.6), (wt("fuse", B[3]) + 0.5, thud(), 0.8), (wt("hydrogen", B[3]), chime(1.5, 660), 0.6),
       (wt("helium", B[3]), chime(1.5, 880), 0.6), (wt("light", B[4]), chime(3, 523), 0.9), (wt("detect", B[4]), whoosh(0.7), 0.4),
       (wt("ignited", B[5]), chime(2.5, 1047), 0.7), (vend - 0.4, thud(), 0.7)]
sfx = np.zeros(int((dur + 1) * SR))
for t, s, g in ev:
    i = int(max(0, t) * SR); s = s[: len(sfx) - i]; sfx[i:i + len(s)] += s / (np.abs(s).max() + 1e-9) * g
sfx = np.clip(sfx * 0.5, -1, 1)
st = np.stack([sfx, sfx], 1)
import wave
with wave.open(str(D / "sfx.wav"), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype("<i2").tobytes())

music = ROOT / "library" / "music" / "incompetech" / "echoes-of-time-v2.mp3"
out = D.parent / "renders" / "bigbang_v3.mp4"
fc = (f"[1:a]aresample={SR},asplit=2[v][vk];"
      f"[2:a]atrim=0:{dur:.2f},afade=t=in:d=1.5,afade=t=out:st={dur - 2.5:.2f}:d=2.5,volume=0.22[m];"
      f"[m][vk]sidechaincompress=threshold=0.05:ratio=4:attack=20:release=400[md];"
      f"[3:a]volume=0.9[s];[v][md][s]amix=inputs=3:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11[a]")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(D / "bigbang_visual.mp4"), "-i", str(D.parent / "assets" / "voice.wav"),
                "-i", str(music), "-i", str(D / "sfx.wav"), "-filter_complex", fc, "-map", "0:v", "-map", "[a]",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", str(out)], check=True)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(out), "-c:v", "libx264", "-crf", "25", "-preset", "slow", "-c:a", "copy",
                str(out.with_name("bigbang_v3_share.mp4"))], check=True)
print(out, len(ev), "efeitos")
