"""Mounjaro completo em 7 estilos, a partir do mounjaro_3d (mesma voz e cenas; muda imagem e coordenadas)."""
import json, shutil
from pathlib import Path
from PIL import Image, ImageDraw
R = Path(__file__).resolve().parent; PZ = R.parent; BASE = PZ / "mounjaro_3d"
# brain, stomach, pancreas (corpo) e emissao do hipotalamo (cerebro), px da imagem 864x1536
C = {"03_vivid_vector": ((430,165),(480,460),(420,560),(375,735)),
     "04_minimal_info": ((430,165),(460,570),(435,645),(400,750)),
     "05_clay":         ((426,165),(456,540),(441,645),(381,750)),
     "07_anatomy_book": ((429,120),(450,570),(420,645),(360,705)),
     "08_papercraft":   ((432,195),(462,480),(432,630),(312,720)),
     "09_lowpoly":      ((429,150),(444,540),(414,615),(369,750)),
     "10_graph_notebook":((420,135),(411,570),(400,620),(306,675))}
LIGHT = ("07_anatomy_book", "10_graph_notebook")
def bands(im):   # fundo claro: faixas escuras para titulo e legenda brancos
    h = im.height; m = Image.new("L", im.size, 0); d = ImageDraw.Draw(m)
    for y in range(h):
        a = min(1, 1.6 - y / (0.2 * h)) if y < 0.32 * h else max(0, (y - 0.5 * h) / (0.15 * h))
        d.line([(0, y), (im.width, y)], fill=int(215 * min(1, a)))
    return Image.composite(Image.new("RGB", im.size, (12, 14, 20)), im, m)
for st, (br, sto, pan, hyp) in C.items():
    P = PZ / f"mounjaro_{st}"; (P / "assets/img").mkdir(parents=True, exist_ok=True)
    for f in ("voice.wav", "timing_raw.json"): shutil.copy(BASE / "assets" / f, P / "assets" / f)
    shutil.copy(BASE / "narration.json", P / "narration.json"); shutil.copy(BASE / "assets/img/06_pen.jpg", P / "assets/img/06_pen.jpg")
    src = {"01_body": R / f"full/{st}__body.png", "04_stomach": R / f"full/{st}__stomach.png",
           "05_brain": R / f"full/{st}__brain.png", "03_pancreas": R / f"img/{st}_s11.png"}
    for k, f in src.items():
        im = Image.open(f).convert("RGB"); (bands(im) if st in LIGHT else im).save(P / f"assets/img/{k}.jpg", quality=92)
    S = json.load(open(BASE / "scenes.json", encoding="utf-8")); S["comp"] = S["out"] = f"mounjaro_{st}"
    for s in S["blocks"][0]["scenes"]:
        if s["t"] == "body_map":
            pos = {"BRAIN": br, "STOMACH": sto, "PANCREAS": pan}
            for sp in s["spots"]: sp["x"], sp["y"] = pos[sp["label"]]
    for s in S["blocks"][5]["scenes"]:
        if s["t"] == "organ_focus": s["emit"]["from"] = list(hyp)
    (P / "scenes.json").write_text(json.dumps(S, ensure_ascii=False, indent=1), encoding="utf-8")
    print("ok", P.name)
