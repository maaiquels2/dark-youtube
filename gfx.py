"""Dark Studio - motion graphics (Pillow). Gera PNGs 1920x1080 a partir de specs por cena.
Tipos de tela cheia (substituem a midia da cena; o Ken Burns da montagem da o movimento):
  timeline, chart, document, quote, relmap, scale, chapter, headline, photo (foto real licenciada), entity_full
Tipos de sobreposicao (PNG transparente por cima do clipe):
  lower_third, logo, callout, parties, citation, entity (card grande logo/selo/foto + nome)
"""
import math, textwrap, os as _os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1920, 1080
FULL = {"timeline", "chart", "document", "quote", "relmap", "scale", "chapter", "headline", "photo", "entity_full"}
OVER = {"lower_third", "logo", "callout", "parties", "citation", "entity"}
BG, PANEL, LINE = (11, 14, 20), (22, 27, 37), (52, 60, 76)
WHITE, MUTED, RED, GOLD, TEAL = (245, 246, 248), (160, 168, 182), (229, 72, 77), (255, 214, 10), (56, 189, 199)
_FONTS = {
    "bold": ["C:/Windows/Fonts/arialbd.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"],
    "reg": ["C:/Windows/Fonts/arial.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"],
    "impact": ["C:/Windows/Fonts/impact.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"],
    "serif": ["C:/Windows/Fonts/georgia.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"],
    "serifb": ["C:/Windows/Fonts/georgiab.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"],
}
def F(kind, size):
    for p in _FONTS[kind]:
        if Path(p).is_file():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def tw(d, s, f):
    b = d.textbbox((0, 0), s, font=f); return b[2] - b[0]
def wrap(d, s, f, maxw):
    out, cur = [], ""
    for w in str(s).split():
        t = (cur + " " + w).strip()
        if tw(d, t, f) <= maxw: cur = t
        else:
            if cur: out.append(cur)
            cur = w
    if cur: out.append(cur)
    return out

def background(accent=RED):
    im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
    for x in range(0, W, 80): d.line([(x, 0), (x, H)], fill=(16, 20, 28))
    for y in range(0, H, 80): d.line([(0, y), (W, y)], fill=(16, 20, 28))
    g = Image.new("L", (W, H), 0); gd = ImageDraw.Draw(g)
    gd.ellipse([-400, -500, W + 400, H + 300], fill=60); g = g.filter(ImageFilter.GaussianBlur(220))
    im = Image.composite(Image.new("RGB", (W, H), (26, 32, 46)), im, g)
    ImageDraw.Draw(im).rectangle([0, 0, W, 10], fill=accent)
    return im

def kicker(d, text, y=90, color=RED):
    f = F("bold", 34); d.rectangle([120, y + 8, 132, y + 44], fill=color)
    d.text((150, y), str(text).upper(), font=f, fill=color)

def source_tag(d, src, y=H - 70):
    if src: d.text((120, y), f"Source: {src}", font=F("reg", 28), fill=MUTED)

# ---------------- tela cheia ----------------
def r_chapter(s):
    im = background(); d = ImageDraw.Draw(im)
    n = s.get("number"); t = s.get("title", "")
    if n: d.text((W // 2 - tw(d, f"CHAPTER {n}", F("bold", 40)) // 2, 380), f"CHAPTER {n}", font=F("bold", 40), fill=RED)
    f = F("impact", 130); lines = wrap(d, t.upper(), f, 1500); y = 450
    for l in lines: d.text((W // 2 - tw(d, l, f) // 2, y), l, font=f, fill=WHITE); y += 150
    d.rectangle([W // 2 - 120, y + 20, W // 2 + 120, y + 28], fill=GOLD)
    return im

def r_timeline(s):
    im = background(); d = ImageDraw.Draw(im); kicker(d, s.get("title", "Timeline"))
    ev = (s.get("events") or [])[:6]; n = max(1, len(ev)); y0 = 560
    x0, x1 = 200, W - 200; d.line([(x0, y0), (x1, y0)], fill=LINE, width=8)
    hl = s.get("highlight")
    for k, e in enumerate(ev):
        x = x0 + (x1 - x0) * (k / (n - 1) if n > 1 else 0.5)
        hot = (hl is not None and k == hl) or (hl is None and k == n - 1)
        c = RED if hot else TEAL
        d.ellipse([x - 22, y0 - 22, x + 22, y0 + 22], fill=c, outline=BG, width=6)
        fd, fl = F("bold", 46), F("reg", 34)
        up = k % 2 == 0; date = str(e.get("date", ""))
        lines = wrap(d, e.get("label", ""), fl, 360)
        if up:
            yy = y0 - 80 - 46 - 44 * len(lines)
            d.text((x - tw(d, date, fd) // 2, yy), date, font=fd, fill=GOLD if hot else WHITE); yy += 60
        else:
            yy = y0 + 60; d.text((x - tw(d, date, fd) // 2, yy), date, font=fd, fill=GOLD if hot else WHITE); yy += 60
        for l in lines: d.text((x - tw(d, l, fl) // 2, yy), l, font=fl, fill=WHITE if hot else MUTED); yy += 44
        d.line([(x, y0 - 30 if up else y0 + 30), (x, y0 - 70 if up else y0 + 55)], fill=LINE, width=3)
    source_tag(d, s.get("source")); return im

def _fmt(v, unit):
    if unit in ("$B", "B"): return f"${v:,.1f}B".replace(".0B", "B")
    if unit in ("$M", "M"): return f"${v:,.0f}M"
    if unit == "%": return f"{v:g}%"
    return f"{v:,g}{unit or ''}"

def r_chart(s):
    im = background(); d = ImageDraw.Draw(im); kicker(d, s.get("title", ""))
    ser = (s.get("series") or [])[:8]; unit = s.get("unit", "")
    vals = [float(x.get("value", 0)) for x in ser] or [1]; mx = max(vals) or 1
    left, right, top, bot = 200, W - 160, 230, H - 200
    n = len(ser); slot = (right - left) / max(1, n); bw = min(220, slot * 0.6)
    hl = s.get("highlight", n - 1)
    d.line([(left, bot), (right, bot)], fill=LINE, width=4)
    for k, x in enumerate(ser):
        v = float(x.get("value", 0)); h = (bot - top - 80) * v / mx
        cx = left + slot * (k + 0.5); c = RED if k == hl else TEAL
        d.rounded_rectangle([cx - bw / 2, bot - h, cx + bw / 2, bot], radius=10, fill=c)
        lab = _fmt(v, unit); f = F("impact", 64 if k == hl else 52)
        d.text((cx - tw(d, lab, f) / 2, bot - h - 80), lab, font=f, fill=GOLD if k == hl else WHITE)
        fl = F("bold", 30)
        for j, l in enumerate(wrap(d, x.get("label", ""), fl, slot - 20)[:2]):
            d.text((cx - tw(d, l, fl) / 2, bot + 20 + j * 38), l, font=fl, fill=MUTED)
    source_tag(d, s.get("source")); return im

def r_document(s):
    im = background(TEAL); d = ImageDraw.Draw(im)
    kicker(d, s.get("doc", "Court document"), color=TEAL)
    px0, py0, px1, py1 = 260, 190, W - 260, H - 150
    sh = Image.new("L", (W, H), 0); ImageDraw.Draw(sh).rectangle([px0 + 18, py0 + 24, px1 + 18, py1 + 24], fill=160)
    im.paste((0, 0, 0), mask=sh.filter(ImageFilter.GaussianBlur(18))); d = ImageDraw.Draw(im)
    d.rectangle([px0, py0, px1, py1], fill=(244, 241, 232))
    fh = F("serifb", 34); hdr = s.get("header") or s.get("doc", "")
    d.text((px0 + 70, py0 + 50), str(hdr).upper()[:70], font=fh, fill=(40, 40, 40))
    d.line([(px0 + 70, py0 + 105), (px1 - 70, py0 + 105)], fill=(150, 150, 150), width=2)
    f = F("serif", 44); text = s.get("excerpt", ""); hl = s.get("highlight") or ""
    lines = wrap(d, text, f, px1 - px0 - 140); y = py0 + 150
    # posicao do trecho destacado (por palavras)
    hw = hl.split(); words_done = 0
    allw = text.split()
    start = -1
    for i in range(len(allw) - len(hw) + 1):
        if hw and [w.strip('.,;:"“”') for w in allw[i:i + len(hw)]] == [w.strip('.,;:"“”') for w in hw]: start = i; break
    for l in lines[:12]:
        x = px0 + 70
        for w in l.split():
            idx = words_done; words_done += 1
            ww = tw(d, w + " ", f)
            if start >= 0 and start <= idx < start + len(hw):
                d.rectangle([x - 4, y + 4, x + ww - 6, y + 56], fill=(255, 222, 89))
            d.text((x, y), w, font=f, fill=(25, 25, 25)); x += ww
        y += 66
    source_tag(d, s.get("source"), H - 110); return im

def r_quote(s):
    im = background(); d = ImageDraw.Draw(im)
    d.text((170, 140), "\u201c", font=F("serifb", 300), fill=RED)
    f = F("serifb", 64); lines = wrap(d, s.get("text", ""), f, 1500); y = 330
    for l in lines[:6]: d.text((230, y), l, font=f, fill=WHITE); y += 84
    d.rectangle([230, y + 30, 330, y + 36], fill=GOLD)
    d.text((230, y + 60), str(s.get("speaker", "")), font=F("bold", 42), fill=GOLD)
    if s.get("role"): d.text((230, y + 115), s["role"], font=F("reg", 34), fill=MUTED)
    source_tag(d, s.get("source")); return im

def _card(d, cx, cy, title, sub, color, w=420, h=130):
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], radius=18, fill=PANEL, outline=color, width=5)
    ft = F("bold", 38); fs = F("reg", 28)
    tl = wrap(d, title, ft, w - 40)[:2]; yy = cy - (len(tl) * 44 + (34 if sub else 0)) / 2
    for l in tl: d.text((cx - tw(d, l, ft) / 2, yy), l, font=ft, fill=WHITE); yy += 44
    if sub: d.text((cx - tw(d, sub, fs) / 2, yy + 2), sub[:40], font=fs, fill=MUTED)

def r_relmap(s, ents=None):
    im = background(); d = ImageDraw.Draw(im); kicker(d, s.get("title", "Who is connected"))
    nodes = (s.get("nodes") or [])[:8]; cx, cy = W // 2, 600; R = 360
    pts = []
    for k, nd in enumerate(nodes):
        a = -math.pi / 2 + 2 * math.pi * k / max(1, len(nodes))
        pts.append((cx + R * 1.75 * math.cos(a), cy + R * math.sin(a)))
    for (x, y), nd in zip(pts, nodes):
        d.line([(cx, cy), (x, y)], fill=LINE, width=5)
        rel = nd.get("relation", "")
        if rel:
            mx, my = (cx + x) / 2, (cy + y) / 2; fr = F("bold", 26); w = tw(d, rel, fr)
            d.rounded_rectangle([mx - w / 2 - 14, my - 22, mx + w / 2 + 14, my + 22], radius=10, fill=BG, outline=GOLD, width=2)
            d.text((mx - w / 2, my - 16), rel, font=fr, fill=GOLD)
    for (x, y), nd in zip(pts, nodes): _card(d, x, y, nd.get("name", ""), nd.get("role", ""), TEAL, 380, 120)
    _card(d, cx, cy, s.get("center", ""), s.get("center_role", ""), RED, 460, 150)
    source_tag(d, s.get("source")); return im

def r_scale(s):
    im = background(); d = ImageDraw.Draw(im); kicker(d, s.get("title", "Putting it in perspective"))
    amt = str(s.get("amount", "")); f = F("impact", 220)
    d.text((W // 2 - tw(d, amt, f) // 2, 250), amt, font=f, fill=GOLD)
    fc = F("bold", 56); y = 560
    for l in wrap(d, s.get("comparison", ""), fc, 1500)[:3]: d.text((W // 2 - tw(d, l, fc) // 2, y), l, font=fc, fill=WHITE); y += 72
    n = int(s.get("blocks") or 0)
    if n:
        n = min(n, 60); bw = 48; cols = min(n, 30); x0 = W // 2 - cols * (bw + 10) // 2; yb = y + 40
        for k in range(n):
            x = x0 + (k % cols) * (bw + 10); yy = yb + (k // cols) * (bw + 10)
            d.rounded_rectangle([x, yy, x + bw, yy + bw], radius=6, fill=RED if k == 0 else TEAL)
    source_tag(d, s.get("source")); return im

def r_headline(s):
    im = background(); d = ImageDraw.Draw(im)
    px0, py0, px1, py1 = 220, 230, W - 220, H - 230
    d.rounded_rectangle([px0, py0, px1, py1], radius=16, fill=(250, 250, 250))
    d.rectangle([px0, py0, px1, py0 + 90], fill=(30, 30, 30))
    d.text((px0 + 50, py0 + 22), str(s.get("outlet", "")).upper(), font=F("bold", 44), fill=WHITE)
    if s.get("date"): d.text((px1 - 50 - tw(d, s["date"], F("reg", 32)), py0 + 30), s["date"], font=F("reg", 32), fill=(200, 200, 200))
    f = F("serifb", 70); y = py0 + 150
    for l in wrap(d, s.get("headline", ""), f, px1 - px0 - 120)[:4]: d.text((px0 + 60, y), l, font=f, fill=(20, 20, 20)); y += 88
    d.text((px0 + 60, py1 - 60), "Headline as reported; recreated for illustration", font=F("reg", 26), fill=(120, 120, 120))
    return im

# ---------------- sobreposicoes ----------------
def o_lower_third(im, s, photos):
    d = ImageDraw.Draw(im); name = s.get("name", ""); role = s.get("role", "")
    x0, y1 = 100, H - 120; ph = photos.get(name) if photos else None
    fn, fr = F("bold", 54), F("reg", 34)
    w = max(tw(d, name, fn), tw(d, role, fr)) + 80; h = 150; x = x0
    if ph and Path(ph["file"]).is_file():
        p = Image.open(ph["file"]).convert("RGB"); s2 = 220
        r = max(s2 / p.width, s2 / p.height); p = p.resize((round(p.width * r), round(p.height * r)))
        p = p.crop(((p.width - s2) // 2, 0, (p.width - s2) // 2 + s2, s2))
        m = Image.new("L", (s2, s2), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, s2, s2], radius=20, fill=255)
        im.paste(p, (x0, y1 - s2), m); x = x0 + s2 + 20
        if ph.get("credit"): d.text((x0, y1 + 8), ph["credit"][:60], font=F("reg", 20), fill=MUTED)
    d.rounded_rectangle([x, y1 - h, x + w, y1], radius=14, fill=(14, 17, 24, 235))
    d.rectangle([x, y1 - h, x + 12, y1], fill=RED)
    d.text((x + 40, y1 - h + 22), name, font=fn, fill=WHITE)
    d.text((x + 40, y1 - h + 90), role, font=fr, fill=GOLD)

def o_callout(im, s, k=0, top=120):
    d = ImageDraw.Draw(im); t = str(s.get("text", "")); f = F("impact", 96)
    w = tw(d, t, f) + 90; x1 = W - 70; y0 = top + k * 170
    if y0 + 140 > H - 110: x1 = 70 + w; y0 = 180 + (k % 3) * 170
    d.rounded_rectangle([x1 - w, y0, x1, y0 + 140], radius=16, fill=(14, 17, 24, 235))
    d.rectangle([x1 - w, y0, x1 - w + 12, y0 + 140], fill=GOLD)
    d.text((x1 - w + 50, y0 + 14), t, font=f, fill=GOLD)
    if s.get("source"): o_citation(im, {"text": s["source"]})

def o_parties(im, s):
    d = ImageDraw.Draw(im); items = (s.get("items") or [])[:5]; f = F("bold", 36)
    title = s.get("title"); y = 140
    if title: d.text((100, y), title.upper(), font=F("bold", 30), fill=MUTED); y += 50
    for it in items:
        w = tw(d, it, f) + 70
        d.rounded_rectangle([100, y, 100 + w, y + 70], radius=12, fill=(14, 17, 24, 235), outline=TEAL, width=3)
        d.text((135, y + 14), it, font=f, fill=WHITE); y += 88

def o_citation(im, s):
    d = ImageDraw.Draw(im); t = "Source: " + str(s.get("text", "")); f = F("reg", 26)
    w = tw(d, t, f) + 40
    d.rounded_rectangle([W - 60 - w, H - 80, W - 60, H - 34], radius=10, fill=(14, 17, 24, 210))
    d.text((W - 40 - w, H - 74), t, font=f, fill=(225, 228, 235))

def o_logo(im, s, logos):
    lg = (logos or {}).get(s.get("company", "")) or (logos or {}).get("_default")
    if not lg or not Path(lg).is_file(): 
        d = ImageDraw.Draw(im); t = s.get("company", ""); f = F("bold", 40); w = tw(d, t, f) + 50
        d.rounded_rectangle([60, 60, 60 + w, 130], radius=14, fill=(248, 248, 246, 230)); d.text((85, 72), t, font=f, fill=(20, 20, 20)); return
    from montage import make_plate
    p = Image.open(make_plate(lg, Path(lg).with_name(Path(lg).stem + "_plate.png"))).convert("RGBA")
    w = int(W * 0.10); p = p.resize((w, round(p.height * w / p.width)), Image.LANCZOS); im.alpha_composite(p, (60, 60))


# ---------------- entidades ----------------
KIND_LABEL = {"company": "COMPANY", "agency": "U.S. GOVERNMENT AGENCY", "court": "COURT", "person": "PERSON", "fund": "FUND"}

def _fit(path, mw, mh):
    p = Image.open(path).convert("RGBA"); r = min(mw / p.width, mh / p.height)
    return p.resize((max(1, round(p.width * r)), max(1, round(p.height * r))), Image.LANCZOS)

def _cover(path, w, h):
    p = Image.open(path).convert("RGB"); r = max(w / p.width, h / p.height)
    p = p.resize((round(p.width * r), round(p.height * r)), Image.LANCZOS)
    return p.crop(((p.width - w) // 2, (p.height - h) // 2, (p.width - w) // 2 + w, (p.height - h) // 2 + h))

def _ent_mark(e):
    for k in ("logo", "seal"):
        if e.get(k) and Path(e[k]).is_file(): return e[k], k
    return None, None

def _ent_title(e, first):
    if e.get("kind") in ("agency", "court") and e.get("full_name"): return e["full_name"]
    return (e.get("full_name") if first and e.get("full_name") else None) or e.get("name", "")

def o_entity(im, s, ents, y0=70):
    e = (ents or {}).get(s.get("name", ""), {"name": s.get("name", ""), "kind": "company"})
    d = ImageDraw.Draw(im)
    cw = 620; x1 = W - 70; x0 = x1 - cw
    title = _ent_title(e, s.get("first")); ft = F("bold", 44 if len(title) < 26 else 34)
    tl = wrap(d, title, ft, cw - 60)[:3]
    mark, mk = _ent_mark(e); ph = e.get("photo") if e.get("kind") == "person" and e.get("photo") and Path(e["photo"]).is_file() else None
    top = (230 if mk == "seal" else 190) if (mark or ph) else 0
    if y0 + top + 200 > H - 120: top = 0; mark = ph = None  # sem espaco: cartao compacto so com nome
    sub = e.get("role") or KIND_LABEL.get(e.get("kind"), ""); fs = F("bold", 26); sl = wrap(d, sub, fs, cw - 70)[:2]
    h = top + 40 + len(tl) * 52 + len(sl) * 34 + 16
    d.rounded_rectangle([x0 + 8, y0 + 10, x1 + 8, y0 + h + 10], radius=22, fill=(0, 0, 0, 120))
    d.rounded_rectangle([x0, y0, x1, y0 + h], radius=22, fill=(14, 17, 24, 245))
    if mark:
        d.rounded_rectangle([x0, y0, x1, y0 + top], radius=22, fill=(250, 250, 248, 240))
        d.rectangle([x0, y0 + top - 22, x1, y0 + top], fill=(250, 250, 248, 240))
        lg = _fit(mark, cw - 120, top - 50); im.alpha_composite(lg, (x0 + (cw - lg.width) // 2, y0 + (top - lg.height) // 2))
    elif ph:
        p = _cover(ph, cw, top); m = Image.new("L", (cw, top), 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, cw, top + 30], radius=22, fill=255); im.paste(p, (x0, y0), m)
    d.rectangle([x0, y0 + top, x0 + 12, y0 + h - 20], fill=RED if e.get("kind") != "agency" else TEAL)
    y = y0 + top + 24
    for l in tl: d.text((x0 + 40, y), l, font=ft, fill=WHITE); y += 52
    for l in sl: d.text((x0 + 40, y + 2), l, font=fs, fill=GOLD); y += 34
    cr = (e.get("credits") or {}).get("photo") if ph else None
    if cr: d.text((x0 + 10, y0 + h + 14), cr[:70], font=F("reg", 18), fill=(200, 204, 212)); h += 26
    return y0 + h + 30

def r_photo(s):
    im = _cover(s["file"], W, H).convert("RGBA")
    g = Image.new("L", (1, H)); [g.putpixel((0, y), int(max(0, (y - H * 0.45) / (H * 0.55)) * 235)) for y in range(H)]
    shade = Image.new("RGBA", (W, H), (8, 10, 14, 0)); shade.putalpha(g.resize((W, H)))
    im = Image.alpha_composite(im, shade); d = ImageDraw.Draw(im)
    if s.get("kicker"): kicker(d, s["kicker"], y=H - 330)
    f = F("bold", 64); y = H - 260
    for l in wrap(d, s.get("caption", ""), f, W - 240)[:2]: d.text((120, y), l, font=f, fill=WHITE); y += 76
    if s.get("credit"): d.text((120, H - 60), "Photo: " + s["credit"][:120], font=F("reg", 24), fill=(205, 208, 215))
    return im.convert("RGB")

def r_entity_full(s, ents=None):
    e = (ents or {}).get(s.get("name", ""), {"name": s.get("name", "")})
    hq = e.get("hq_photo") if e.get("hq_photo") and Path(e["hq_photo"]).is_file() else None
    if hq:
        im = _cover(hq, W, H).filter(ImageFilter.GaussianBlur(6)); im = Image.blend(im, Image.new("RGB", (W, H), BG), 0.62)
    else: im = background()
    im = im.convert("RGBA"); d = ImageDraw.Draw(im); mark, _ = _ent_mark(e)
    y = 200
    if mark:
        lg = _fit(mark, 900, 330); pw, ph_ = lg.width + 120, lg.height + 100
        d.rounded_rectangle([W // 2 - pw // 2, y, W // 2 + pw // 2, y + ph_], radius=30, fill=(250, 250, 248, 235))
        im.alpha_composite(lg, (W // 2 - lg.width // 2, y + 50)); y += ph_ + 50
    else: y = 380
    t = _ent_title(e, True).upper(); ft = F("impact", 96 if len(t) < 30 else 76)
    for l in wrap(d, t, ft, 1680)[:3]: d.text((W // 2 - tw(d, l, ft) // 2, y), l, font=ft, fill=WHITE); y += ft.size + 14
    sub = s.get("role") or e.get("role") or KIND_LABEL.get(e.get("kind"), "")
    d.text((W // 2 - tw(d, sub, F("bold", 40)) // 2, y + 10), sub, font=F("bold", 40), fill=GOLD)
    cr = (e.get("credits") or {}).get("hq_photo") if hq else None
    if cr: d.text((60, H - 50), "Photo: " + cr[:120], font=F("reg", 22), fill=(200, 204, 212))
    return im.convert("RGB")

def _typewriter(full, out, dur, ents=None):
    """Documento/citacao com efeito maquina de escrever (MP4): texto revelado em etapas, depois segura."""
    import gfx_anim
    key = "excerpt" if full["type"] == "document" else "text"; txt = str(full.get(key, "")); words = txt.split()
    steps = min(18, max(6, len(words) // 3)); fps = 30; total = int(dur * fps); reveal = int(min(dur * 0.55, 4.5) * fps)
    frames = []
    for k in range(1, steps + 1):
        sp = dict(full); sp[key] = " ".join(words[:max(1, round(len(words) * k / steps))])
        if full["type"] == "document" and k < steps: sp["highlight"] = ""
        frames.append(globals()["r_" + full["type"]](sp))
    def gen():
        for f in range(total):
            yield frames[min(steps - 1, int(f / max(1, reveal) * steps))]
    return gfx_anim.encode(gen(), out, fps)

def _draw_ov(g, photos, logos, ents, st):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); t = g["type"]
    if t == "lower_third": o_lower_third(im, g, photos)
    elif t == "callout": o_callout(im, g, st["kc"], st["ey"] if st["ey"] > 70 else 120); st["kc"] += 1
    elif t == "parties": o_parties(im, g)
    elif t == "citation": o_citation(im, g)
    elif t == "logo": o_logo(im, g, logos)
    elif t == "entity": st["ey"] = o_entity(im, g, ents, st["ey"])
    return im

# entrada animada por tipo (aplicada na montagem): slide da direita/esquerda/baixo + fade
ENTER = {"entity": "right", "callout": "up", "parties": "left", "citation": "fade", "logo": "fade", "lower_third": "left"}

def render_scene(spec_list, out_dir, idx, photos=None, logos=None, ents=None, dur=7.0):
    """Retorna (full_png/mp4 or None, overlay_png or None). Grava tambem camadas ov-NN-k.png + ov-NN.json p/ entradas animadas."""
    import json as _j
    out_dir = Path(out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    for f in out_dir.glob(f"ov-{idx+1:02d}-*.png"): f.unlink()
    an = next((g for g in spec_list or [] if g.get("type") in ("moneyflow", "collapse")), None)
    fp = op = None
    if an:  # grafico animado vira o clipe da cena (MP4)
        import gfx_anim
        fp = gfx_anim.render(an, out_dir / f"anim-{idx+1:02d}.mp4", float(an.get("seconds") or max(5.0, dur)))
    full = None if an else next((g for g in spec_list or [] if g.get("type") in FULL), None)
    if full:
        if full["type"] in ("document", "quote") and _os.environ.get("DS_TYPEWRITER", "1") == "1":
            fp = _typewriter(full, out_dir / f"tw-{idx+1:02d}.mp4", max(4.0, dur), ents)
        else:
            fp = out_dir / f"full-{idx+1:02d}.png"
            fn = globals()["r_" + full["type"]]
            (fn(full, ents) if full["type"] in ("entity_full", "relmap") else fn(full)).save(fp)
    ov = [g for g in spec_list or [] if g.get("type") in OVER]
    if ov:
        ov.sort(key=lambda g: g["type"] != "entity"); st = {"kc": 0, "ey": 70}
        comp = Image.new("RGBA", (W, H), (0, 0, 0, 0)); layers = []
        for k, g in enumerate(ov):
            lay = _draw_ov(g, photos, logos, ents, st); comp.alpha_composite(lay)
            lp = out_dir / f"ov-{idx+1:02d}-{k}.png"; lay.save(lp)
            layers.append({"file": lp.name, "enter": ENTER.get(g["type"], "fade"), "delay": round(0.35 + 0.45 * k, 2)})
        op = out_dir / f"ov-{idx+1:02d}.png"; comp.save(op)
        (out_dir / f"ov-{idx+1:02d}.json").write_text(_j.dumps(layers), encoding="utf-8")
    return fp, op

def render_project(pfile, pdir):
    """Renderiza todos os graficos do projeto. Tela cheia vira a midia da cena (source=gfx)."""
    import json
    pfile, pdir = Path(pfile), Path(pdir)
    pj = json.loads(pfile.read_text(encoding="utf-8"))
    photos = {k: dict(v, file=str(pdir / v["file"])) for k, v in (pj.get("people_photos") or {}).items() if v.get("file")}
    logos = {k: str(pdir / v) for k, v in (pj.get("logos") or {}).items()}
    lg = (pj.get("logo") or {}).get("file")
    if lg and (pdir / lg).is_file(): logos.setdefault("_default", str(pdir / lg))
    ents = {}
    for e in pj.get("entities") or []:
        e2 = dict(e)
        for k in ("logo", "seal", "photo", "hq_photo"):
            if e2.get(k): e2[k] = str(pdir / e2[k])
        ents[e["name"]] = e2
    gd = pdir / "gfx"; gd.mkdir(exist_ok=True)
    for f in list(gd.glob("ov-*.png")) + list(gd.glob("ov-*.json")): f.unlink()
    nf = no = 0
    for i, s in enumerate(pj["scenes"]):
        spec = [dict(g, file=str(pdir / g["file"])) if g.get("type") == "photo" and g.get("file") else g for g in s.get("gfx") or []]
        fp, op = render_scene(spec, gd, i, photos, logos, ents, max(4.0, len((s.get('narration') or '').split()) / 2.6))
        if fp:
            s.update(file=fp.relative_to(pdir).as_posix(), status="pronto", source="gfx", error=None); nf += 1
        elif s.get("source") == "gfx":
            s.update(file=None, status="pendente", source="site")
        if op: no += 1
    pfile.write_text(json.dumps(pj, ensure_ascii=False, indent=2), encoding="utf-8")
    return nf, no


# estilo v2 (premium) por padrao; DS_GFX_STYLE=v1 volta ao estilo plano
import os as _os
if _os.environ.get("DS_GFX_STYLE", "v2") != "v1":
    try:
        import gfx2 as _g2
        globals().update({_k: getattr(_g2, _k) for _k in _g2.OVERRIDES})
    except Exception as _e:
        print("[gfx] estilo v2 indisponivel:", _e)
