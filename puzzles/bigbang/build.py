import json, subprocess, sys
from pathlib import Path
D = Path(__file__).parent; ROOT = D.parents[1]
raw = json.loads((D / "assets" / "timing_raw.json").read_text(encoding="utf-8"))
words = []
for w in raw["words"]:
    t = w["w"]
    if not any(c.isalnum() for c in t):  # pontuacao gruda na palavra anterior
        if words: words[-1]["w"] += t; words[-1]["e"] = max(words[-1]["e"], w["e"])
        continue
    words.append({"w": t, "s": w["s"], "e": w["e"]})
vend = max(w["e"] for w in words); tail = 3.0
import base64
imgs = {p.stem: "data:image/jpeg;base64," + base64.b64encode(p.read_bytes()).decode() for p in sorted((D / "assets" / "img").glob("*.jpg"))}
html = (D / "template2.html").read_text(encoding="utf-8").replace("__IMGS__", json.dumps(imgs))
for k, v in {"__WORDS__": json.dumps(words), "__BLOCKS__": json.dumps(raw["blocks"] + [round(vend + 0.3, 3)]), "__VEND__": f"{vend:.3f}", "__DUR__": f"{vend + tail:.3f}"}.items():
    html = html.replace(k, v)
(D / "index.html").write_text(html, encoding="utf-8")
for f in ("hyperframes.json", "package.json"):
    if not (D / f).exists():
        s = ROOT / "puzzles" / "ep01_poisoned_bottles" / f
        (D / f).write_text(s.read_text(encoding="utf-8").replace("ep01-poisoned-bottles", "bigbang"), encoding="utf-8")
print(f"speech {vend:.1f}s video {vend+tail:.1f}s", len(words), "words")
if "--render" in sys.argv:
    (D / "renders").mkdir(exist_ok=True)
    subprocess.run(["npx", "--yes", "hyperframes@0.8.191", "render", "-o", "renders/bigbang.mp4", "--quiet"], cwd=D, check=True, shell=True)
