"""Monta um video do EffectCraft a partir de <projeto>/scenes.json + <projeto>/assets/timing_raw.json (voz Kokoro).

Uso (da raiz do repo):
  python puzzles/ec_lib/build.py <projeto>                      # so monta o .ecproj (confere se o JSON esta certo)
  python puzzles/ec_lib/build.py <projeto> --frames             # + 1 quadro a cada 1.5 s -> ec_build/sheet.png
  python puzzles/ec_lib/build.py <projeto> --frames 1,7.5,20    # + quadros nesses segundos
  python puzzles/ec_lib/build.py <projeto> --render             # + video (~12 min por minuto) + mixagem -> renders/<out>.mp4
  python puzzles/ec_lib/build.py <projeto> --mix                # so refaz a mixagem (usa o video ja renderizado)
  python puzzles/ec_lib/build.py <projeto> --sheet video.mp4    # folha de contato de um video a 2 quadros/s
Tudo que e gerado fica em <projeto>/ec_build/; o video final em <projeto>/renders/.
"""
import json, re, subprocess, sys, wave
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

LIB = Path(__file__).parent
ROOT = LIB.parents[1]
CLI = Path.home() / "AppData/Local/DarkStudio/effectcraft/effectcraft-cli.exe"
SR = 48000


def load_words(raw):
    """Palavras da voz; pontuacao gruda na palavra anterior."""
    words = []
    for w in raw["words"]:
        t = w["w"]
        if not any(c.isalnum() for c in t):
            if words: words[-1]["w"] += t; words[-1]["e"] = max(words[-1]["e"], w["e"])
            continue
        words.append({"w": t, "s": round(w["s"], 3), "e": round(w["e"], 3)})
    return words


def captions(words):
    """Legendas de ate 3 palavras; quebra em pontuacao ou pausa."""
    chunks, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        nxt = words[i + 1] if i + 1 < len(words) else None
        if len(cur) == 3 or w["w"][-1] in ".,:;!?" or not nxt or nxt["s"] - w["e"] > 0.35:
            chunks.append({"t": " ".join(x["w"] for x in cur).upper(), "s": cur[0]["s"],
                           "e": nxt["s"] if nxt and nxt["s"] - cur[-1]["e"] < 0.6 else cur[-1]["e"] + 0.25})
            cur = []
    assert all(c["e"] > c["s"] for c in chunks), "legenda com duracao zero"
    return chunks


def cli(*a, cwd):
    r = subprocess.run([str(CLI), *a], cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = (r.stdout + r.stderr).strip()
    if r.returncode: sys.exit(out)
    return out


# ---------------- efeitos sonoros sintetizados ----------------
rng = np.random.default_rng(1)
def env(n, a, d): t = np.arange(n) / SR; return np.minimum(t / a, 1) * np.exp(-t / d)
def boom(d=3.0, **_):
    n = int(d * SR); t = np.arange(n) / SR
    f = 30 + 70 * np.exp(-t * 3); s = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.005, 0.9)
    no = np.convolve(rng.standard_normal(n), np.ones(60) / 60, "same") * env(n, 0.002, 0.35)
    return s * 0.9 + no * 1.6
def whoosh(d=0.8, up=False, **_):
    n = int(d * SR); t = np.arange(n) / SR
    no = rng.standard_normal(n); k = 8 + 40 * (t / d if up else 1 - t / d)
    out = np.zeros(n); y = 0.0
    for i in range(n): y += (no[i] - y) / k[i]; out[i] = y  # passa-baixa que varre
    shape = np.sin(np.pi * t / d) ** (0.6 if up else 1.5)
    if up: shape *= (t / d) ** 2 + 0.1
    return out * shape * 3
def rise(d=1.0, **_): return whoosh(d, up=True)
def chime(d=2.5, f=880, **_):
    n = int(d * SR); t = np.arange(n) / SR
    return sum(np.sin(2 * np.pi * f * m * t) / m for m in (1, 2.01, 3.02)) * env(n, 0.004, 0.7) * 0.25
def thud(d=1.2, **_): n = int(d * SR); t = np.arange(n) / SR; return np.sin(2 * np.pi * (55 + 40 * np.exp(-t * 8)) * t) * env(n, 0.003, 0.25)
SFX = {"boom": boom, "whoosh": whoosh, "rise": rise, "chime": chime, "thud": thud}


def mix(P, B, spec, events, dur):
    sfx = np.zeros(int((dur + 1) * SR))
    for e in events:
        s = SFX[e["k"]](**{k: v for k, v in e.items() if k in ("d", "f")})
        i = int(max(0, e["t"]) * SR); s = s[: len(sfx) - i]
        sfx[i:i + len(s)] += s / (np.abs(s).max() + 1e-9) * e["g"]
    st = np.stack([np.clip(sfx * 0.5, -1, 1)] * 2, 1)
    with wave.open(str(B / "sfx.wav"), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype("<i2").tobytes())
    music = ROOT / spec.get("music", "library/music/incompetech/echoes-of-time-v2.mp3")
    out = P / "renders" / f"{spec['out']}.mp4"; out.parent.mkdir(exist_ok=True)
    fc = (f"[1:a]aresample={SR},asplit=2[v][vk];"
          f"[2:a]atrim=0:{dur:.2f},afade=t=in:d=1.5,afade=t=out:st={dur - 2.5:.2f}:d=2.5,volume={spec.get('music_gain', 0.22)}[m];"
          f"[m][vk]sidechaincompress=threshold=0.05:ratio=4:attack=20:release=400[md];"
          f"[3:a]volume=0.9[s];[v][md][s]amix=inputs=3:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11[a]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(B / "visual.mp4"), "-i", str(P / "assets" / "voice.wav"),
                    "-i", str(music), "-i", str(B / "sfx.wav"), "-filter_complex", fc, "-map", "0:v", "-map", "[a]",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", str(out)], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(out), "-c:v", "libx264", "-crf", "25", "-preset", "slow",
                    "-c:a", "copy", str(out.with_name(out.stem + "_share.mp4"))], check=True)
    print("video:", out, f"| {len(events)} efeitos sonoros")


def sheet(pngs, labels, dest, cols=8):
    ims = [Image.open(p).convert("RGB") for p in pngs]
    w, h = ims[0].size; rows = -(-len(ims) // cols)
    S = Image.new("RGB", (cols * w, rows * h)); d = ImageDraw.Draw(S)
    font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 22)
    for i, (im, lb) in enumerate(zip(ims, labels)):
        x, y = i % cols * w, i // cols * h; S.paste(im.resize((w, h)), (x, y)); d.text((x + 6, y + 4), lb, fill="yellow", font=font)
    S.save(dest); print("folha:", dest)


def video_sheet(video, dest, fps=2):
    tmp = Path(dest).with_suffix(""); tmp.mkdir(parents=True, exist_ok=True)
    for f in tmp.glob("*.png"): f.unlink()
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(video), "-vf", f"fps={fps},scale=-2:320", str(tmp / "%04d.png")], check=True)
    pngs = sorted(tmp.glob("*.png"))
    sheet(pngs, [f"{i / fps:.1f}" for i in range(len(pngs))], dest, cols=16)


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # o CLI imprime "→"; cp1252 quebrava o print
    a = sys.argv[1:]
    if not a or a[0].startswith("-"): sys.exit(__doc__)
    P = Path(a[0]).resolve(); B = P / "ec_build"; B.mkdir(exist_ok=True)
    if "--sheet" in a:
        v = Path(a[a.index("--sheet") + 1]); return video_sheet(v, B / f"sheet_{v.stem}.png")
    spec = json.loads((P / "scenes.json").read_text(encoding="utf-8"))
    raw = json.loads((P / "assets" / "timing_raw.json").read_text(encoding="utf-8"))
    words = load_words(raw)
    vend = max(w["e"] for w in words)
    blocks = raw["blocks"] + [round(vend + 0.3, 3)]
    if len(spec["blocks"]) != len(raw["blocks"]):
        sys.exit(f"scenes.json tem {len(spec['blocks'])} blocos, a voz tem {len(raw['blocks'])}")
    dur = round(vend + spec.get("tail", 3.0), 2)
    comp = spec.get("comp", "main")
    head = (f"var WORDS={json.dumps(words)};\nvar BLOCKS={json.dumps(blocks)};\nvar DUR={dur};\nvar VEND={vend};\n"
            f"var CHUNKS={json.dumps(captions(words))};\nvar IMG={json.dumps((P / 'assets' / 'img').as_posix())};\n"
            f"var SPEC={json.dumps(spec)};\n")
    (B / "video.jsx").write_text(head + (LIB / "ec_lib.jsx").read_text(encoding="utf-8") + "\nbuildVideo();\n", encoding="utf-8")

    if "--mix" not in a:
        out = cli("script", "video.jsx", "--empty", "--save-as", "video.ecproj", cwd=B)
        ev = next(l for l in out.splitlines() if l.startswith("EVENTS="))[7:]
        (B / "events.json").write_text(ev, encoding="utf-8")
        print(out.splitlines()[-1], f"| dur {dur}s")
    events = json.loads((B / "events.json").read_text(encoding="utf-8"))

    if "--frames" in a:
        i = a.index("--frames")
        ts = a[i + 1].split(",") if i + 1 < len(a) and not a[i + 1].startswith("-") else [f"{t:.2f}" for t in np.arange(0.5, dur, 1.5)]
        F = B / "frames"; F.mkdir(exist_ok=True)
        pngs = []
        for t in ts:
            p = F / f"f_{float(t):06.2f}.png"
            cli("render-frame", "--project", "video.ecproj", "--comp", comp, "--time", t, "--max-side", "480", "--out", str(p), cwd=B)
            pngs.append(p)
        sheet(pngs, [f"{float(t):.2f}" for t in ts], B / "sheet.png")
    if "--render" in a:
        print(cli("render", "--project", "video.ecproj", "--comp", comp, "--out", "visual.mp4", "--format", "h264", "--audio", "off", cwd=B).splitlines()[-1])
    if "--render" in a or "--mix" in a:
        mix(P, B, spec, events, dur)


if __name__ == "__main__":
    main()
