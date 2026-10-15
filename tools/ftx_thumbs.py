# compoe thumbnails FTX: fundo Grok (sem rostos) + foto real Commons (CC BY 3.0) + logo com placa + valor verificado
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
sys.path.insert(0, ".")
import montage
P = Path("projects/ftx-how-8-billion-vanished-overnight-20261015-155014")
A, OUT = P / "assets", P / "output" / "thumbs"; OUT.mkdir(parents=True, exist_ok=True)
W, H = 1280, 720
F = lambda n, s: ImageFont.truetype(f"C:/Windows/Fonts/{n}", s)
def cover(im, w, h):
    r = max(w / im.width, h / im.height); im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2; return im.crop((x, y, x + w, y + h))
def person(h):
    im = Image.open(A / "sbf_commons_ccby3.png").convert("RGB")
    im = ImageEnhance.Contrast(ImageEnhance.Color(im).enhance(0.85)).enhance(1.12)
    r = h / im.height; im = im.resize((round(im.width * r), h), Image.LANCZOS)
    m = Image.new("L", im.size, 255); d = ImageDraw.Draw(m)
    fw = round(im.width * 0.38)
    for x in range(fw): d.line([(x, 0), (x, im.height)], fill=round(255 * (x / fw) ** 1.6))
    return im, m
def text(d, xy, s, font, fill, stroke=8):
    d.text(xy, s, font=font, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))
def make(bg, lines, name):
    im = cover(Image.open(bg).convert("RGB"), W, H)
    im = ImageEnhance.Brightness(im).enhance(0.7)
    ph, pm = person(H); im.paste(ph, (W - ph.width + 40, 0), pm)
    ov = Image.new("RGBA", (W, H)); od = ImageDraw.Draw(ov)
    for x in range(760): od.line([(x, 0), (x, H)], fill=(0, 0, 0, round(170 * (1 - x / 760))))
    im = Image.alpha_composite(im.convert("RGBA"), ov)
    d = ImageDraw.Draw(im); y = 170
    for s, size, col, box in lines:
        f = F("impact.ttf", size); bb = d.textbbox((0, 0), s, font=f)
        if box:
            d.rectangle([44, y + bb[1] - 14, 44 + bb[2] + 36, y + bb[3] + 14], fill=box); text(d, (62, y), s, f, col, 0)
        else:
            text(d, (56, y), s, f, col)
        y += bb[3] + 34
    pl = Image.open(montage.make_plate(A / "logo.png", P / "work" / "logo_plate.png")).convert("RGBA")
    pw = 230; pl = pl.resize((pw, round(pl.height * pw / pl.width)), Image.LANCZOS); im.alpha_composite(pl, (48, 48))
    o = OUT / f"{name}.jpg"; im.convert("RGB").save(o, quality=92); return o
bgs = sorted((P / "work" / "thumb_bg").glob("*.*"))
Y, Wt, R = (255, 214, 10), (255, 255, 255), (214, 32, 39)
V = [("thumb-a-8-billion-gone", [("$8 BILLION", 150, Y, None), ("GONE", 150, Wt, R)]),
     ("thumb-b-vanished", [("$8B", 190, Y, None), ("VANISHED", 120, Wt, R)]),
     ("thumb-c-where-did-it-go", [("WHERE DID", 100, Wt, None), ("$8 BILLION GO?", 112, Y, None)])]
outs = [make(bgs[k % len(bgs)], l, n) for k, (n, l) in enumerate(V)]
sheet = Image.new("RGB", (W, H), (20, 20, 20))
for k, o in enumerate(outs):
    t = Image.open(o).resize((W // 2, H // 2)); sheet.paste(t, ((k % 2) * W // 2, (k // 2) * H // 2))
sheet.save(OUT / "sheet.jpg", quality=88); print([o.name for o in outs])
