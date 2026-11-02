"""Correcoes do v2: recorte do pancreas centrado, GLUCAGON legivel, barras do cerebro acima da legenda."""
import json
from pathlib import Path
from PIL import Image

P = Path(__file__).parent
# recorte 1.7x em volta do pancreas (420, 578) -> imagem 864x1536 com o pancreas no centro
Z, cx, cy = 1.7, 430, 560
w, h = 864 / Z, 1536 / Z
x0, y0 = cx - w / 2, cy - h / 2
Image.open(P / "assets/img/01_body.jpg").crop((round(x0), round(y0), round(x0 + w), round(y0 + h))) \
    .resize((864, 1536), Image.LANCZOS).save(P / "assets/img/03_pancreas_zoom.jpg", quality=92)
m = lambda x, y: [round((x - x0) * Z), round((y - y0) * Z)]

S = json.loads((P / "scenes.json").read_text(encoding="utf-8"))
for blk in S["blocks"]:
    for sc in blk["scenes"]:
        if sc.get("t") == "organ_focus" and sc.get("label", {}).get("text") == "PANCREAS":
            sc["image"] = "03_pancreas_zoom.jpg"; sc.pop("scale", None)
            sc["emit"]["from"] = m(420, 578)
            sc["hold"].update(dict(zip(("x", "y"), m(470, 600))), color=[0.3, 0.9, 1])
        if sc.get("t") == "meter" and sc.get("meters"):
            sc["y"] = 1080
(P / "scenes.json").write_text(json.dumps(S, ensure_ascii=False, indent=1), encoding="utf-8")
print("pancreas:", m(420, 578), "| hold:", m(470, 600))
