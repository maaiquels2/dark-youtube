"""10 projetos curtos (bloco do pancreas do Mounjaro v2), um por estilo de imagem."""
import json, subprocess, shutil
from pathlib import Path
R = Path(__file__).resolve().parent; SRC = R.parent / "mounjaro_v2"
A, B = 25.6, 33.85
T = json.load(open(SRC / "assets/timing_raw.json"))
words = [dict(w, s=round(w["s"] - A, 3), e=round(w["e"] - A, 3)) for w in T["words"] if A <= w["s"] < B]
text = json.load(open(SRC / "narration.json", encoding="utf-8"))["blocks"][3]
for img in sorted((R / "img").glob("*_s11.png")):
    name = img.stem[:-4]; P = R / name; (P / "assets/img").mkdir(parents=True, exist_ok=True)
    from PIL import Image
    im = Image.open(img).convert("RGB")
    if name in ("07_anatomy_book", "10_graph_notebook"):   # fundo claro: faixas escuras para titulo e legenda brancos
        from PIL import ImageDraw
        h = im.height; m = Image.new("L", im.size, 0); d = ImageDraw.Draw(m)
        for y in range(h):
            a = min(1, 1.6 - y / (0.2 * h)) if y < 0.32 * h else max(0, (y - 0.5 * h) / (0.15 * h))
            d.line([(0, y), (im.width, y)], fill=int(215 * min(1, a)))
        im = Image.composite(Image.new("RGB", im.size, (12, 14, 20)), im, m)
    im.save(P / "assets/img/pancreas.jpg", quality=92)
    (P / "narration.json").write_text(json.dumps({"blocks": [text]}), encoding="utf-8")
    (P / "assets/timing_raw.json").write_text(json.dumps({"words": words, "blocks": [0.0], "end": round(B - A, 3)}), encoding="utf-8")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(A), "-to", str(B), "-i", str(SRC / "assets/voice.wav"), str(P / "assets/voice.wav")], check=True)
    holo = name == "06_hologram"
    of = {"t": "organ_focus", "image": "pancreas.jpg", "scale": 1.1, "zoom": [100, 110], "label": {"text": "PANCREAS"},
          "emit": {"at": "unlocks", "from": [560, 735], "dir": [-0.2, -1]},
          "hold": {"at": "holds", "x": 420, "y": 640, "text": "GLUCAGON", "color": [0.3, 0.9, 1]}}
    if not holo: of["photo"] = True
    S = {"comp": f"st_{name}", "out": name, "music": "library/music/incompetech/echoes-of-time-v2.mp3", "music_gain": 0.16,
         "tail": 0.8, "finish": {"glow": 1.1 if holo else 0.5},
         "blocks": [{"scenes": [of, {"t": "meter", "bg": False, "dir": "h", "y": 1300, "label": "BLOOD SUGAR", "from": 180, "to": 90,
                                      "max": 250, "value": False, "show": "blood", "at": "sugar+0.3", "reach": "down+0.6"}]}]}
    (P / "scenes.json").write_text(json.dumps(S, ensure_ascii=False, indent=1), encoding="utf-8")
    print("ok", name)
