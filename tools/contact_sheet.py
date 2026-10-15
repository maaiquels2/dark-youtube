import json, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
P = Path("projects/ftx-how-8-billion-vanished-overnight-20261015-155014")
d = json.loads((P.parent / (P.name + ".json")).read_text(encoding="utf-8"))
T = P / "work" / "sheet"; T.mkdir(parents=True, exist_ok=True)
tw, th, cols = 384, 216, 6
ims = []
for i, s in enumerate(d["scenes"]):
    f = P / s["file"]; o = T / f"{i+1:02d}.jpg"
    if f.suffix.lower() in (".mp4", ".webm", ".mov"):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "2", "-i", str(f), "-frames:v", "1", str(o)])
        src = o
    else:
        src = f
    im = Image.open(src).convert("RGB"); w, h = im.size
    im.thumbnail((tw, th)); c = Image.new("RGB", (tw, th), (255, 0, 255)); c.paste(im, ((tw - im.width)//2, (th - im.height)//2))
    ImageDraw.Draw(c).text((6, 4), f"{i+1} {'V' if f.suffix.lower()=='.mp4' else 'I'} {w}x{h}", fill=(255, 255, 0), font=ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 18), stroke_width=2, stroke_fill=(0,0,0))
    ims.append(c)
for part in range(0, len(ims), 36):
    ch = ims[part:part+36]; rows = (len(ch)+cols-1)//cols
    S = Image.new("RGB", (cols*tw, rows*th))
    for k, c in enumerate(ch): S.paste(c, ((k % cols)*tw, (k//cols)*th))
    S.save(P / "output" / f"contact-sheet-{part//36+1}.jpg", quality=85)
print("ok", len(ims))
