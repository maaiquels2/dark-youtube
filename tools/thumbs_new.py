# thumbnails: fundo = cena Grok (sem rostos) + foto real do CEO (Commons, licenca livre) + logo com placa + valor verificado
import sys, json, subprocess, shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
sys.path.insert(0, "."); import montage, pipeline
key = sys.argv[1]; pid = open(f"{key}_id.txt").read().strip(); P = Path("projects") / pid
d = json.load(open(f"projects/{pid}.json", encoding="utf-8")); ents = {e["name"]: e for e in d["entities"]}
CFG = {"svb": ("Greg Becker", "Silicon Valley Bank", [36, 40, 44],
         [("thumb-a-42b-one-day", [("$42 BILLION", 140, "Y", None), ("IN ONE DAY", 120, "W", "R")]),
          ("thumb-b-48-hours", [("48 HOURS", 150, "W", None), ("$209B BANK", 110, "Y", None), ("GONE", 110, "W", "R")]),
          ("thumb-c-bank-run", [("THE $42B", 130, "Y", None), ("BANK RUN", 130, "W", "R")])]),
       "lehman": ("Richard S. Fuld Jr.", "Lehman Brothers Holdings Inc.", [44, 48, 52],
         [("thumb-a-639b-bankrupt", [("$639 BILLION", 130, "Y", None), ("BANKRUPT", 130, "W", "R")]),
          ("thumb-b-158-years", [("158 YEARS", 140, "W", None), ("GONE IN", 100, "Y", None), ("ONE WEEKEND", 100, "W", "R")]),
          ("thumb-c-weekend", [("THE WEEKEND", 110, "W", None), ("WALL ST BROKE", 110, "Y", "R")])])}
person_n, comp_n, bgsc, V = CFG[key]
OUT = P / "output"; work = P / "work" / "thumb_bg"; work.mkdir(parents=True, exist_ok=True)
FF = shutil.which("ffmpeg"); W, H = 1280, 720
# Anton (OFL, fonts/) no lugar do Impact do Windows; Impact so de reserva
_ANTON = Path("fonts/Anton-Regular.ttf")
F = lambda n, s: ImageFont.truetype(str(_ANTON), s) if n == "impact.ttf" and _ANTON.is_file() else ImageFont.truetype(f"C:/Windows/Fonts/{n}", s)
COL = {"Y": (255, 214, 10), "W": (255, 255, 255), "R": (214, 32, 39), None: None}
def cover(im, w, h):
    r = max(w / im.width, h / im.height); im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2; return im.crop((x, y, x + w, y + h))
bgs = []
n = len(d["scenes"]); cands = [i for i, s in enumerate(d["scenes"]) if (s.get("file") or "").startswith("media/") and pipeline.act_of(i, n) in ("act2", "act3")]
for k, i in enumerate([cands[int(len(cands) * f)] for f in (0.3, 0.6, 0.9)] if cands else []):
    src = P / d["scenes"][i]["file"]; o = work / f"bg{k}.jpg"
    if src.suffix == ".mp4": subprocess.run([FF, "-y", "-v", "error", "-ss", "2", "-i", str(src), "-frames:v", "1", str(o)])
    else: Image.open(src).convert("RGB").save(o)
    bgs.append(o)
def person(h):
    im = Image.open(P / ents[person_n]["photo"]).convert("RGB")
    im = ImageEnhance.Contrast(ImageEnhance.Color(im).enhance(0.85)).enhance(1.12)
    if im.width > im.height * 0.9: c = im.width // 2; im = im.crop((max(0, c - int(im.height * 0.45)), 0, min(im.width, c + int(im.height * 0.45)), im.height))
    r = h / im.height; im = im.resize((round(im.width * r), h), Image.LANCZOS)
    m = Image.new("L", im.size, 255); dr = ImageDraw.Draw(m); fw = round(im.width * 0.38)
    for x in range(fw): dr.line([(x, 0), (x, im.height)], fill=round(255 * (x / fw) ** 1.6))
    return im, m
def make(bg, lines, name):
    im = ImageEnhance.Brightness(cover(Image.open(bg).convert("RGB"), W, H)).enhance(0.62)
    ph, pm = person(H); im.paste(ph, (W - ph.width + 40, 0), pm)
    ov = Image.new("RGBA", (W, H)); od = ImageDraw.Draw(ov)
    for x in range(800): od.line([(x, 0), (x, H)], fill=(0, 0, 0, round(185 * (1 - x / 800))))
    im = Image.alpha_composite(im.convert("RGBA"), ov); dr = ImageDraw.Draw(im); y = 190 if len(lines) == 2 else 160
    for s, size, col, box in lines:
        f = F("impact.ttf", size); bb = dr.textbbox((0, 0), s, font=f)
        if box: dr.rectangle([44, y + bb[1] - 12, 44 + bb[2] + 36, y + bb[3] + 12], fill=COL[box]); dr.text((62, y), s, font=f, fill=COL[col])
        else: dr.text((56, y), s, font=f, fill=COL[col], stroke_width=8, stroke_fill=(0, 0, 0))
        y += bb[3] + 30
    pl = Image.open(montage.make_plate(P / ents[comp_n]["logo"], P / "work" / "logo_plate_thumb.png")).convert("RGBA")
    pw = 260; pl = pl.resize((pw, round(pl.height * pw / pl.width)), Image.LANCZOS); im.alpha_composite(pl, (48, 48))
    o = OUT / f"{name}.jpg"; im.convert("RGB").save(o, quality=92); return o
outs = [make(bgs[k % len(bgs)], l, nm) for k, (nm, l) in enumerate(V)]
sheet = Image.new("RGB", (W, H), (20, 20, 20))
for k, o in enumerate(outs): sheet.paste(Image.open(o).resize((W // 2, H // 2)), ((k % 2) * W // 2, (k // 2) * H // 2))
sheet.save(OUT / "thumbs-sheet.jpg", quality=88); print([str(o) for o in outs])
