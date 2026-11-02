"""Big Bang no EffectCraft: injeta os tempos da fala no scenes.jsx, monta o .ecproj e (opcional) renderiza.
Uso: python build_ec.py [--frames 1,7.5,...] [--render]"""
import json, subprocess, sys
from pathlib import Path

D = Path(__file__).parent
CLI = Path.home() / "AppData/Local/DarkStudio/effectcraft/effectcraft-cli.exe"
raw = json.loads((D.parent / "assets" / "timing_raw.json").read_text(encoding="utf-8"))
words = []
for w in raw["words"]:
    t = w["w"]
    if not any(c.isalnum() for c in t):  # pontuacao gruda na palavra anterior
        if words: words[-1]["w"] += t; words[-1]["e"] = max(words[-1]["e"], w["e"])
        continue
    words.append({"w": t, "s": round(w["s"], 3), "e": round(w["e"], 3)})
vend = max(w["e"] for w in words)
blocks = raw["blocks"] + [round(vend + 0.3, 3)]
dur = round(vend + 3.0, 2)

# legendas: ate 3 palavras, quebra em pontuacao ou pausa
chunks, cur = [], []
for i, w in enumerate(words):
    cur.append(w)
    nxt = words[i + 1] if i + 1 < len(words) else None
    if len(cur) == 3 or w["w"][-1] in ".,:;!?" or not nxt or nxt["s"] - w["e"] > 0.35:
        chunks.append({"t": " ".join(x["w"] for x in cur).upper(), "s": cur[0]["s"], "e": nxt["s"] if nxt and nxt["s"] - cur[-1]["e"] < 0.6 else cur[-1]["e"] + 0.25})
        cur = []

img = (D.parent / "assets" / "img").as_posix()
head = (f"var WORDS={json.dumps(words)};\nvar BLOCKS={json.dumps(blocks)};\nvar DUR={dur};\nvar VEND={vend};\n"
        f"var CHUNKS={json.dumps(chunks)};\nvar IMG={json.dumps(img)};\n")
(D / "bigbang_ec.jsx").write_text(head + (D / "scenes.jsx").read_text(encoding="utf-8"), encoding="utf-8")
assert all(c["e"] > c["s"] for c in chunks), "legenda com duracao zero"


def cli(*a):
    r = subprocess.run([str(CLI), *a], cwd=D, capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = (r.stdout + r.stderr).strip()
    if r.returncode: sys.exit(out)
    return out


print(cli("script", "bigbang_ec.jsx", "--empty", "--save-as", "bigbang.ecproj").splitlines()[-1], f"| dur {dur}s, {len(chunks)} legendas")
if "--frames" in sys.argv:
    ts = sys.argv[sys.argv.index("--frames") + 1].split(",")
    (D / "frames").mkdir(exist_ok=True)
    for t in ts:
        cli("render-frame", "--project", "bigbang.ecproj", "--comp", "bigbang", "--time", t, "--max-side", "480", "--out", f"frames/f_{float(t):05.2f}.png")
    print("frames ok")
if "--render" in sys.argv:
    print(cli("render", "--project", "bigbang.ecproj", "--comp", "bigbang", "--out", "bigbang_visual.mp4", "--format", "h264", "--audio", "off").splitlines()[-1])
