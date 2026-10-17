"""Dark Studio - estilo v2 (documentario premium): texturas, papel envelhecido, polaroids inclinadas,
quadro de evidencias com fios vermelhos, timeline em filme, sombras suaves e brilho.
Sobrescreve os renderizadores de gfx.py (mesmos nomes). Fontes OFL em fonts/."""
import math, random
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import gfx as G

W, H = G.W, G.H
FD = Path(__file__).resolve().parent / "fonts"
INK, CREAM, PAPER = (24, 22, 20), (240, 232, 214), (232, 222, 198)
TEAL, AMBER, RED, WHITE, MUTED = (64, 196, 200), (244, 176, 66), (214, 58, 52), (246, 242, 234), (176, 170, 160)
_FC = {}
def F(kind, size):
    k = (kind, size)
    if k in _FC: return _FC[k]
    spec = {"serif": ("Playfair-VF.ttf", "Bold"), "serifx": ("Playfair-VF.ttf", "Black"), "serifr": ("Playfair-VF.ttf", "Regular"),
            "sans": ("Inter-VF.ttf", "Regular"), "sansb": ("Inter-VF.ttf", "Bold"), "sansm": ("Inter-VF.ttf", "SemiBold"),
            "type": ("CourierPrime-Regular.ttf", None), "typeb": ("CourierPrime-Bold.ttf", None),
            "hand": ("Caveat-VF.ttf", "Bold"), "cond": ("BebasNeue-Regular.ttf", None),
            "num": ("Inter-VF.ttf", "ExtraBold"), "numm": ("Inter-VF.ttf", "SemiBold")}[kind]
    try:
        f = ImageFont.truetype(str(FD / spec[0]), size)
        if spec[1]: f.set_variation_by_name(spec[1])
    except Exception:
        f = G.F("bold", size)
    _FC[k] = f; return f
tw = G.tw
def wrap(d, s, f, mw): return G.wrap(d, s, f, mw)

# ---------- tipografia (ver PADRAO_VIDEOS.md > Fontes e tipografia) ----------
# Sistema: Inter (texto, rotulos, numeros) + Playfair Display (titulos). Courier Prime, Caveat e Bebas Neue so dentro de
# objetos de cena (documento datilografado, anotacao a mao, carimbo). Hierarquia em 1080p: titulo 132/96/76, subtitulo 48-60,
# texto 30-38, rotulo 24-30, credito >= 16. Sem libraqm o PIL nao liga recursos OpenType (tnum/lnum): os numeros sao
# desenhados em celulas de largura fixa (algarismos tabulares, nao "dancam" nos contadores) e com a Inter, que tem algarismos
# alinhados (a Playfair usa algarismos de estilo antigo, que sobem e descem: bonitos em texto, ruins em valores grandes).
DIGITS = "0123456789"
def _cell(font): return max(font.getlength(c) for c in DIGITS)

def text_w(text, font, tabular=False, tracking=0.0):
    text = str(text)
    if not tabular and not tracking: return font.getlength(text)
    cw = _cell(font) if tabular else 0; tr = tracking * font.size
    return sum((cw if tabular and c in DIGITS else font.getlength(c)) + tr for c in text) - (tr if text else 0)

def draw_text(d, xy, text, font, fill, tabular=False, tracking=0.0):
    """Texto com algarismos tabulares e/ou espacamento entre letras (tracking em em, ex.: 0.08 para rotulos em caixa alta)."""
    text = str(text); x, y = xy
    if not tabular and not tracking: d.text((x, y), text, font=font, fill=fill); return
    cw = _cell(font) if tabular else 0; tr = tracking * font.size
    for c in text:
        if tabular and c in DIGITS:
            d.text((x + (cw - font.getlength(c)) / 2, y), c, font=font, fill=fill); x += cw + tr
        else:
            d.text((x, y), c, font=font, fill=fill); x += font.getlength(c) + tr

def wrap_balanced(d, s, f, mw):
    """Mesmo numero de linhas do wrap normal, mas com linhas de tamanho parecido (evita palavra sozinha na ultima linha)."""
    lines = wrap(d, s, f, mw)
    if len(lines) < 2: return lines
    lo, hi = mw * 0.4, mw
    while hi - lo > 4:
        mid = (lo + hi) / 2
        if len(wrap(d, s, f, mid)) <= len(lines): hi = mid
        else: lo = mid
    return wrap(d, s, f, hi)

def fit(text, kind, size, maxw, tabular=False, tracking=0.0, step=2, minimum=18):
    while size > minimum and text_w(text, F(kind, size), tabular, tracking) > maxw: size -= step
    return F(kind, size)

# ---------- texturas ----------
def _noise(w, h, scale=1, blur=0, seed=None):
    rng = np.random.default_rng(seed); a = rng.random((h // scale + 1, w // scale + 1)).astype(np.float32)
    im = Image.fromarray((a * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
    return im.filter(ImageFilter.GaussianBlur(blur)) if blur else im

def grain(im, amt=18, seed=None):
    n = np.asarray(_noise(im.width, im.height, 1, 0, seed), np.float32) - 128
    a = np.asarray(im.convert("RGB"), np.float32) + n[..., None] * (amt / 128)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

def vignette(im, strength=0.65):
    m = Image.new("L", im.size, 0); d = ImageDraw.Draw(m)
    d.ellipse([-im.width * 0.15, -im.height * 0.25, im.width * 1.15, im.height * 1.25], fill=255)
    m = m.filter(ImageFilter.GaussianBlur(im.width // 6))
    dark = Image.new("RGB", im.size, (0, 0, 0))
    return Image.composite(im.convert("RGB"), Image.blend(im.convert("RGB"), dark, strength), m)

def backdrop(seed=7, tint=(18, 20, 24), leak=TEAL, plate=None):
    if plate and Path(plate).is_file():
        im = G._cover(plate, W, H); im = Image.blend(im, Image.new("RGB", (W, H), tint), 0.55)
    else:
        base = np.asarray(_noise(W, H, 6, 14, seed), np.float32) / 255
        fib = np.asarray(_noise(W, H, 2, 1, seed + 1), np.float32) / 255
        v = (base * 0.6 + fib * 0.4)[..., None]
        im = Image.fromarray(np.clip(np.array(tint, np.float32) * (0.75 + 0.6 * v), 0, 255).astype(np.uint8))
    # light leaks teal/amber
    lk = Image.new("RGB", (W, H), (0, 0, 0)); d = ImageDraw.Draw(lk)
    d.ellipse([-500, -400, 700, 500], fill=leak); d.ellipse([W - 600, H - 450, W + 400, H + 400], fill=AMBER)
    lk = lk.filter(ImageFilter.GaussianBlur(260))
    im = ImageChops.screen(im, Image.blend(Image.new("RGB", (W, H)), lk, 0.32))
    return grain(vignette(im, 0.55), 14, seed)

def paper(w, h, tone=PAPER, seed=3, age=1.0):
    n1 = np.asarray(_noise(w, h, 40, 30, seed), np.float32) / 255
    n2 = np.asarray(_noise(w, h, 1, 0, seed + 2), np.float32) / 255
    v = 0.86 + 0.12 * n1 + 0.05 * n2
    yy, xx = np.mgrid[0:h, 0:w]; e = np.minimum(np.minimum(xx, w - xx), np.minimum(yy, h - yy)) / max(1, min(w, h) * 0.18)
    v = v * (0.84 + 0.16 * np.clip(e, 0, 1) ** (0.6 * age))
    a = np.array(tone, np.float32)[None, None] * v[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")

def torn(im, amp=7, seed=5, sides="tblr"):
    w, h = im.size; rng = random.Random(seed); m = Image.new("L", (w, h), 0); d = ImageDraw.Draw(m)
    def edge(n, a): return [rng.uniform(0, a) for _ in range(n)]
    pts = []
    xs = range(0, w + 1, 9)
    top = edge(len(xs), amp if "t" in sides else 0); bot = edge(len(xs), amp if "b" in sides else 0)
    ys = range(0, h + 1, 9); lef = edge(len(ys), amp if "l" in sides else 0); rig = edge(len(ys), amp if "r" in sides else 0)
    pts += [(x, top[i]) for i, x in enumerate(xs)] + [(w - rig[i], y) for i, y in enumerate(ys)]
    pts += [(x, h - bot[i]) for i, x in reversed(list(enumerate(xs)))] + [(lef[i], y) for i, y in reversed(list(enumerate(ys)))]
    d.polygon(pts, fill=255); im = im.copy(); im.putalpha(ImageChops.multiply(im.getchannel("A"), m)); return im

def place(dst, src, cx, cy, angle=0, shadow=18, glow=None):
    """Cola src (RGBA) centrado em (cx,cy), girado, com sombra suave."""
    r = src.rotate(angle, resample=Image.BICUBIC, expand=True)
    x, y = int(cx - r.width / 2), int(cy - r.height / 2)
    if glow:
        g = Image.new("RGBA", r.size, glow + (0,)); g.putalpha(r.getchannel("A").filter(ImageFilter.GaussianBlur(26)))
        dst.alpha_composite(g, (x, y)) if x >= 0 and y >= 0 else dst.paste(g, (x, y), g)
    if shadow:
        sh = Image.new("RGBA", (r.width + 80, r.height + 80), (0, 0, 0, 0))
        a = Image.new("L", sh.size, 0); a.paste(r.getchannel("A"), (40, 40))
        a = a.filter(ImageFilter.GaussianBlur(shadow)).point(lambda v: int(v * 0.65)); sh.putalpha(a)
        dst.paste(sh, (x - 40 + shadow // 2, y - 40 + shadow), sh)
    dst.paste(r, (x, y), r)
    return x, y, r.width, r.height

def tape(w=150, h=44, seed=1):
    t = Image.new("RGBA", (w, h), (236, 228, 196, 150)); t = torn(t, 4, seed, "lr"); return t

def glow_text(dst, xy, text, font, fill, glow=None, radius=18, tabular=False, tracking=0.0):
    if glow:
        lay = Image.new("RGBA", dst.size, (0, 0, 0, 0)); draw_text(ImageDraw.Draw(lay), xy, text, font, glow + (220,), tabular, tracking)
        dst.alpha_composite(lay.filter(ImageFilter.GaussianBlur(radius)))
    draw_text(ImageDraw.Draw(dst), xy, text, font, fill, tabular, tracking)

def kicker(d, text, x=120, y=96, color=AMBER):
    d.line([(x, y + 22), (x + 60, y + 22)], fill=color, width=3)
    draw_text(d, (x + 76, y), str(text).upper(), F("sansb", 30), color, tracking=0.08)

def source(d, src, x=120, y=H - 96, fill=(196, 190, 178)):
    if not src: return  # acima de 5% da borda (area segura de titulo); a barra do YouTube cobre o rodape
    f = F("sansb", 24); draw_text(d, (x, y), "SOURCE", f, fill, tracking=0.1); x += text_w("SOURCE", f, tracking=0.1) + 18
    d.text((x, y), "·  " + str(src), font=F("sansm", 24), fill=fill)

def _photo_frame(path, w, h, kind="polaroid", caption=None, seed=2):
    ph = G._cover(path, w, h)
    if kind == "polaroid":
        pad, bot = 22, (92 if caption else 60)
        fr = paper(w + pad * 2, h + pad + bot, (244, 240, 230), seed, 0.4); fr.paste(ph, (pad, pad))
        if caption:
            d = ImageDraw.Draw(fr); f = F("hand", 54); d.text((pad + 6, h + pad + 14), caption[:34], font=f, fill=(30, 34, 60))
        return fr
    ph = ph.convert("RGBA"); return torn(vignette(ph, 0.35).convert("RGBA"), 9, seed)

# ---------- tela cheia ----------
def r_chapter(s):
    im = backdrop(11, leak=AMBER).convert("RGBA"); d = ImageDraw.Draw(im)
    n = s.get("number")
    if n:
        lab = f"CHAPTER {n}"; f = F("sansm", 40); draw_text(d, (W // 2 - text_w(lab, f, True, 0.2) / 2, 340), lab, f, AMBER, True, 0.2)
    f = F("serifx", 132); y = 420
    for l in wrap_balanced(d, s.get("title", ""), f, 1560)[:3]:
        glow_text(im, (W // 2 - tw(d, l, f) // 2, y), l, f, WHITE, (0, 0, 0), 24); y += 156
    d.line([(W // 2 - 90, y + 30), (W // 2 + 90, y + 30)], fill=RED, width=4)
    return grain(im.convert("RGB"), 10)

def r_timeline(s):
    im = backdrop(13).convert("RGBA"); d = ImageDraw.Draw(im); kicker(d, s.get("title", "Timeline"))
    ev = (s.get("events") or [])[:6]; n = max(1, len(ev)); hl = s.get("highlight", -1)
    fw = min(300, (W - 200) // n - 20); sh = fw + 40; total = n * (fw + 24) + 60
    strip = Image.new("RGBA", (total, sh + 120), (16, 14, 12, 255)); sd = ImageDraw.Draw(strip)
    for x in range(14, total, 34):
        sd.rounded_rectangle([x, 16, x + 18, 40], radius=4, fill=(60, 56, 50)); sd.rounded_rectangle([x, sh + 80, x + 18, sh + 104], radius=4, fill=(60, 56, 50))
    for i, e in enumerate(ev):
        x0 = 40 + i * (fw + 24); fr = paper(fw, sh, (226, 214, 188) if i != hl else (248, 216, 150), 20 + i, 0.7)
        fd = ImageDraw.Draw(fr); dt = e.get("date", ""); fdt = fit(dt, "num", 44, fw - 44, True)
        draw_text(fd, (22, 34), dt, fdt, RED if i == hl else INK, tabular=True)
        fd.line([(22, 100), (fw - 22, 100)], fill=(120, 100, 80), width=2)
        yy = 120
        for l in wrap(fd, e.get("label", ""), F("sansm", 32), fw - 44)[:4]: fd.text((22, yy), l, font=F("sansm", 32), fill=INK); yy += 42
        strip.alpha_composite(fr, (x0, 60))
    strip = grain(strip.convert("RGB"), 10).convert("RGBA")
    place(im, strip, W // 2, 590, -1.2, 22, AMBER if hl >= 0 else None)
    source(d, s.get("source")); return grain(im.convert("RGB"), 8)

def r_chart(s):
    im = backdrop(17).convert("RGBA"); d = ImageDraw.Draw(im); kicker(d, s.get("title", ""))
    ser = (s.get("series") or [])[:7]; hl = s.get("highlight", -1); unit = s.get("unit", "")
    mx = max([float(x.get("value") or 0) for x in ser] + [1]); bw = min(200, (W - 400) // max(1, len(ser)) - 40); base = 870  # rotulos acabam antes da linha de fonte
    for i, x in enumerate(ser):
        v = float(x.get("value") or 0); h = int(560 * v / mx); x0 = 240 + i * (bw + 50)
        col = RED if i == hl else TEAL
        bar = Image.new("RGBA", (bw, max(4, h)), col + (235,)); bar = grain(bar.convert("RGB"), 12).convert("RGBA")
        place(im, bar, x0 + bw // 2, base - h // 2, 0, 14, col if i == hl else None)
        val = G._fmt(v, unit) if hasattr(G, "_fmt") else str(v); fv = fit(val, "num", 54, bw + 40, True)
        draw_text(d, (x0 + bw // 2 - text_w(val, fv, True) / 2, base - h - 74), val, fv, WHITE, tabular=True)
        for k, l in enumerate(wrap(d, x.get("label", ""), F("sansm", 26), bw + 40)[:2]):
            d.text((x0 + bw // 2 - tw(d, l, F("sansm", 26)) // 2, base + 18 + k * 32), l, font=F("sansm", 26), fill=MUTED)
    d.line([(200, base), (W - 200, base)], fill=(120, 116, 108), width=2)
    source(d, s.get("source")); return grain(im.convert("RGB"), 8)

def r_document(s):
    im = backdrop(19, tint=(20, 18, 16), leak=AMBER).convert("RGBA"); d = ImageDraw.Draw(im)
    kicker(d, s.get("doc", "Court document"))
    pw, ph = 1240, 720; pg = paper(pw, ph, (236, 226, 202), 9, 1.3); pd = ImageDraw.Draw(pg)
    pd.text((70, 56), str(s.get("header", "")).upper(), font=F("typeb", 30), fill=(60, 50, 40))
    pd.line([(70, 104), (pw - 70, 104)], fill=(90, 80, 70), width=2)
    f = F("type", 40); words = str(s.get("excerpt", "")).split(); hlw = str(s.get("highlight", "")).lower()
    lines = wrap(pd, " ".join(words), f, pw - 140); y = 140
    full = " ".join(lines); hs = full.lower().find(hlw) if hlw else -1; he = hs + len(hlw); pos = 0
    hl = Image.new("RGBA", pg.size, (0, 0, 0, 0)); hd = ImageDraw.Draw(hl); rng = random.Random(4)
    for l in lines:
        ls, le = pos, pos + len(l)
        if hs >= 0 and hs < le and he > ls:
            a, b = max(hs, ls) - ls, min(he, le) - ls
            x0 = 70 + tw(pd, l[:a], f); x1 = 70 + tw(pd, l[:b], f)
            hd.polygon([(x0 - 6, y + 4 + rng.uniform(-3, 3)), (x1 + 8, y + 2 + rng.uniform(-3, 3)), (x1 + 6, y + 50), (x0 - 8, y + 52)], fill=(255, 226, 60, 150))
        pd.text((70, y), l, font=f, fill=(34, 30, 26)); y += 58; pos = le + 1
    pg.alpha_composite(hl.filter(ImageFilter.GaussianBlur(1.2)))
    for k in range(2):  # tarjas de redacao decorativas abaixo do trecho
        yy = y + 20 + k * 58; pd.rectangle([70, yy, 70 + rng.randint(500, pw - 160), yy + 34], fill=(18, 16, 14))
    st = Image.new("RGBA", (360, 110), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
    sd.rounded_rectangle([4, 4, 356, 106], radius=10, outline=(176, 40, 36, 210), width=6)
    sd.text((30, 16), "EXHIBIT", font=F("cond", 84), fill=(176, 40, 36, 210))
    pg.alpha_composite(st.rotate(8, expand=True), (pw - 430, ph - 190))
    place(im, torn(grain(pg.convert("RGB"), 9).convert("RGBA"), 5, 8, "b"), W // 2, 575, 1.5, 26)
    clip = Image.new("RGBA", (40, 140), (0, 0, 0, 0)); ImageDraw.Draw(clip).rounded_rectangle([4, 4, 36, 136], radius=16, outline=(190, 192, 196, 255), width=6)
    im.alpha_composite(clip, (W // 2 - 520, 190))
    source(d, s.get("source")); return grain(im.convert("RGB"), 8)

def r_quote(s):
    im = backdrop(23, leak=AMBER).convert("RGBA"); d = ImageDraw.Draw(im)
    d.text((170, 150), "\u201c", font=F("serifx", 300), fill=AMBER)
    f = F("serifr", 66); y = 330
    for l in wrap(d, s.get("text", ""), f, 1500)[:6]: d.text((260, y), l, font=f, fill=WHITE); y += 88
    d.line([(260, y + 36), (360, y + 36)], fill=RED, width=4)
    d.text((260, y + 60), str(s.get("speaker", "")), font=F("sansb", 44), fill=WHITE)
    if s.get("role"): d.text((260, y + 116), s["role"], font=F("sans", 32), fill=MUTED)
    source(d, s.get("source")); return grain(im.convert("RGB"), 8)

def _note(title, sub, w=380, tone=PAPER, seed=1, mark=None):
    h = 150 if not mark else 230; n = paper(w, h, tone, seed, 0.8); nd = ImageDraw.Draw(n); y = 22
    if mark and Path(mark).is_file():
        lg = G._fit(mark, w - 60, 80); n.alpha_composite(lg, ((w - lg.width) // 2, 20)); y = 112
    ft = F("serif", 38 if len(title) < 18 else 32)
    for l in wrap(nd, title, ft, w - 40)[:2]: nd.text(((w - tw(nd, l, ft)) // 2, y), l, font=ft, fill=INK); y += 44
    if sub: nd.text(((w - tw(nd, sub, F("sansm", 24))) // 2, y + 2), sub[:34], font=F("sansm", 24), fill=(110, 90, 70))
    return grain(n.convert("RGB"), 8).convert("RGBA")

def _pin(dst, x, y, col=RED):
    d = ImageDraw.Draw(dst); d.ellipse([x - 13, y - 13, x + 13, y + 13], fill=col); d.ellipse([x - 5, y - 9, x + 2, y - 2], fill=(255, 200, 190))

def _string(dst, a, b, col=(196, 30, 30)):
    lay = Image.new("RGBA", dst.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    (x0, y0), (x1, y1) = a, b; sag = 0.08 * math.hypot(x1 - x0, y1 - y0)
    pts = [(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t + sag * 4 * t * (1 - t)) for t in [i / 24 for i in range(25)]]
    d.line(pts, fill=(0, 0, 0, 90), width=7); dst.alpha_composite(lay.filter(ImageFilter.GaussianBlur(4)), (0, 0))
    ImageDraw.Draw(dst).line(pts, fill=col, width=4)
    return pts[12]

def r_relmap(s, ents=None):
    im = backdrop(29, tint=(30, 24, 18), leak=AMBER).convert("RGBA"); d = ImageDraw.Draw(im); kicker(d, s.get("title", "Who is connected"))
    nodes = (s.get("nodes") or [])[:7]; cx, cy = W // 2, 600
    pts = [(cx + 700 * math.cos(-math.pi / 2 + 2 * math.pi * k / max(1, len(nodes))), cy + 330 * math.sin(-math.pi / 2 + 2 * math.pi * k / max(1, len(nodes)))) for k in range(len(nodes))]
    mids = [_string(im, (cx, cy - 40), (x, y - 40)) for x, y in pts]
    em = lambda n: G._ent_mark((ents or {}).get(n, {}))[0] if ents else None
    for k, ((x, y), nd) in enumerate(zip(pts, nodes)):
        place(im, _note(nd.get("name", ""), nd.get("role", ""), 360, PAPER, 30 + k, em(nd.get("name", ""))), x, y, [-4, 3, -2, 5, -3, 2, 4][k], 16)
        _pin(im, int(x), int(y - 70))
    place(im, _note(s.get("center", ""), s.get("center_role", ""), 440, (246, 226, 170), 99, em(s.get("center", ""))), cx, cy, 1.5, 20, AMBER)
    _pin(im, cx, cy - 80)
    for (mx, my), nd in zip(mids, nodes):
        rel = nd.get("relation", "")
        if rel:
            f = F("hand", 42); w = tw(d, rel, f) + 36; t = Image.new("RGBA", (w, 56), (238, 230, 200, 235)); ImageDraw.Draw(t).text((18, 2), rel, font=f, fill=(150, 20, 20))
            place(im, torn(t, 3, 7, "lr"), mx, my, -3, 8)
    source(d, s.get("source")); return grain(im.convert("RGB"), 8)

def r_scale(s):
    im = backdrop(31, leak=RED).convert("RGBA"); d = ImageDraw.Draw(im); kicker(d, s.get("title", "Putting it in perspective"))
    amt = str(s.get("amount", "")); f = fit(amt, "num", 200, W - 2 * 192, True)
    glow_text(im, (W // 2 - text_w(amt, f, True) / 2, 250), amt, f, (250, 214, 120), AMBER, 30, tabular=True)
    fc = F("sansm", 50); y = 560
    for l in wrap(d, s.get("comparison", ""), fc, 1440)[:3]: d.text((W // 2 - tw(d, l, fc) // 2, y), l, font=fc, fill=WHITE); y += 68
    source(d, s.get("source")); return grain(im.convert("RGB"), 8)

def r_headline(s):
    im = backdrop(37, tint=(22, 20, 18), leak=AMBER).convert("RGBA"); d = ImageDraw.Draw(im)
    pw, ph = 1320, 600; pg = paper(pw, ph, (234, 228, 212), 41, 1.1); pd = ImageDraw.Draw(pg)
    pd.text((60, 40), str(s.get("outlet", "")), font=F("serifx", 72), fill=INK)
    if s.get("date"): pd.text((pw - 60 - tw(pd, s["date"], F("type", 30)), 70), s["date"], font=F("type", 30), fill=(80, 70, 60))
    pd.line([(60, 140), (pw - 60, 140)], fill=INK, width=4); pd.line([(60, 150), (pw - 60, 150)], fill=INK, width=1)
    f = F("serif", 76); y = 190
    for l in wrap(pd, s.get("headline", ""), f, pw - 120)[:3]: pd.text((60, y), l, font=f, fill=(18, 16, 14)); y += 92
    for k in range(3):  # colunas de texto fingido (ilegivel)
        for r in range(4):
            yy = y + 30 + r * 22
            if yy < ph - 60: pd.line([(60 + k * 410, yy), (60 + k * 410 + 370, yy)], fill=(150, 142, 128), width=8)
    pg = torn(grain(pg.convert("RGB"), 10).convert("RGBA"), 10, 43)
    place(im, pg, W // 2, 520, -2.2, 26)
    place(im, tape(150, 44, 3), W // 2 - 690, 238, -40, 4)  # corner, clear of masthead text; place(im, tape(170, 46, 4), W // 2 + 520, 790, -24, 4)
    d.text((120, H - 66), "Headline as published · recreated for illustration", font=F("sansm", 24), fill=(190, 184, 172))
    return grain(im.convert("RGB"), 8)

def r_photo(s):
    base = backdrop(41).convert("RGBA"); fr = _photo_frame(s["file"], 1180, 700, "torn", seed=5)
    place(base, fr, W // 2 + 60, 470, -1.8, 28)
    d = ImageDraw.Draw(base)
    if s.get("kicker"): kicker(d, s["kicker"], 120, 860)
    f = F("serif", 60); y = 905
    for l in wrap(d, s.get("caption", ""), f, W - 260)[:2]: d.text((120, y), l, font=f, fill=WHITE); y += 70
    if s.get("credit"): d.text((W - 80 - tw(d, "Photo: " + s["credit"][:110], F("sans", 20)), H - 40), "Photo: " + s["credit"][:110], font=F("sans", 20), fill=(180, 176, 166))
    return grain(base.convert("RGB"), 8)

def r_entity_full(s, ents=None):
    e = (ents or {}).get(s.get("name", ""), {"name": s.get("name", "")})
    im = backdrop(43, leak=TEAL if e.get("kind") in ("agency", "court") else AMBER).convert("RGBA"); d = ImageDraw.Draw(im)
    hq = e.get("hq_photo") if e.get("hq_photo") and Path(e["hq_photo"]).is_file() else None
    mark, mk = G._ent_mark(e)
    if hq: place(im, _photo_frame(hq, 820, 560, "polaroid", None, 6), 1260, 470, 3.5, 30)
    cx = 640 if hq else W // 2
    if mark:
        cw = 560 if mk != "seal" else 380; card = paper(cw, 300 if mk != "seal" else 380, (246, 242, 232), 8, 0.5)
        lg = G._fit(mark, cw - 90, (300 if mk != "seal" else 380) - 80); card.alpha_composite(lg, ((cw - lg.width) // 2, (card.height - lg.height) // 2))
        place(im, card, cx, 400, -2.5, 24); place(im, tape(160, 44, 9), cx - 10, 400 - card.height // 2 + 6, 4, 3)
    t = G._ent_title(e, True); f = F("serifx", 84 if len(t) < 24 else 64); y = 650 if mark else 420
    for l in wrap(d, t, f, (900 if hq else 1500))[:3]:
        glow_text(im, (cx - tw(d, l, f) // 2, y), l, f, WHITE, (0, 0, 0), 20); y += f.size + 12
    sub = s.get("role") or e.get("role") or G.KIND_LABEL.get(e.get("kind"), "")
    d.text((cx - tw(d, sub.upper(), F("sansb", 30)) // 2, y + 14), sub.upper(), font=F("sansb", 30), fill=AMBER)
    cr = (e.get("credits") or {}).get("hq_photo") if hq else None
    if cr: d.text((60, H - 44), "Photo: " + cr[:120], font=F("sans", 20), fill=(180, 176, 166))
    return grain(im.convert("RGB"), 8)

# ---------- sobreposicoes (PNG transparente; entrada animada na montagem) ----------
def o_entity(im, s, ents, y0=70):
    e = (ents or {}).get(s.get("name", ""), {"name": s.get("name", ""), "kind": "company"})
    mark, mk = G._ent_mark(e); ph = e.get("photo") if e.get("kind") == "person" and e.get("photo") and Path(e["photo"]).is_file() else None
    title = G._ent_title(e, s.get("first")); sub = (e.get("role") or s.get("role") or G.KIND_LABEL.get(e.get("kind"), "")).upper()
    k = hash(e.get("name", "")) % 5; ang = [-3, 2.5, -1.5, 3.5, -2][k]
    if ph:  # polaroid inclinada
        cw = 380; fr = _photo_frame(ph, cw, 330, "polaroid", e.get("name"), k)
        d = ImageDraw.Draw(fr); fs = F("sansb", 20)
        for j, l in enumerate(wrap(d, sub, fs, cw - 10)[:2]): d.text((28, 330 + 22 + 64 + j * 24), l, font=fs, fill=(120, 60, 40))
        pc = (e.get("credits") or {}).get("photo_short") or ""
        if pc: d.text((34, 322), ("Photo: " + pc)[:44], font=F("sans", 16), fill=(245, 242, 235), stroke_width=2, stroke_fill=(20, 20, 20))
        card = fr
    else:
        cw = 600; d0 = ImageDraw.Draw(Image.new("RGB", (1, 1)))
        ft = F("serif", 50 if len(title) < 22 else 40); tl = wrap(d0, title, ft, cw - 70)[:3]
        fs = F("sansb", 22); sl = wrap(d0, sub, fs, cw - 70)[:2]
        top = (240 if mk == "seal" else 170) if mark else 0
        if y0 + top + 200 > H - 120: top = 0; mark = None
        h = top + 36 + len(tl) * (ft.size + 10) + len(sl) * 30 + 30
        card = paper(cw, h, (242, 236, 222) if e.get("kind") != "person" else (236, 230, 214), 50 + k, 0.7); cd = ImageDraw.Draw(card)
        if mark:
            lg = G._fit(mark, cw - 120, top - 50); card.alpha_composite(lg, ((cw - lg.width) // 2, 30 + (top - 40 - lg.height) // 2))
            cd.line([(40, top), (cw - 40, top)], fill=(170, 156, 130), width=2)
        y = top + 24; acc = TEAL if e.get("kind") in ("agency", "court") else RED if e.get("kind") == "person" else AMBER
        cd.rectangle([0, top + 10, 10, h - 16], fill=acc)
        for l in tl: cd.text((40, y), l, font=ft if e.get("kind") != "person" else F("typeb", ft.size - 4), fill=INK); y += ft.size + 10
        for l in sl: cd.text((40, y + 4), l, font=fs, fill=(140, 92, 40) if acc == AMBER else (30, 110, 116) if acc == TEAL else (150, 40, 34)); y += 30
        card = grain(card.convert("RGB"), 8).convert("RGBA")
    x, y, w, h = place(im, card, W - 70 - card.width // 2 - 10, y0 + card.height // 2 + 10, ang, 18)
    place(im, tape(130, 40, k + 2), x + w // 2, y + 12, ang * 3, 3)
    if ph and (e.get("credits") or {}).get("photo"):
        ImageDraw.Draw(im).text((x, y + h + 4), e["credits"]["photo"][:64], font=F("sans", 17), fill=(225, 222, 214))
        h += 22
    return y + h + 24

def o_callout(im, s, k=0, top=120):
    t = str(s.get("text", "")); loss = s.get("tone") == "loss" or any(w in t.lower() for w in ("loss", "liabilit", "debt", "owed", "exposure"))
    d = ImageDraw.Draw(im); f = fit(t, "num", 88, 1150, True, step=4, minimum=44)
    w = int(text_w(t, f, True)) + 80; x1 = W - 100; y0 = top + k * 190  # margem direita >= 5%
    if y0 + 170 > H - 110: x1 = 100 + w; y0 = 160 + (k % 3) * 190
    col = (240, 96, 86) if loss else (250, 206, 110)
    plate = Image.new("RGBA", (w, 150), (10, 10, 12, 0)); pd = ImageDraw.Draw(plate)
    pd.rounded_rectangle([0, 0, w, 150], radius=10, fill=(12, 12, 14, 170))
    im.alpha_composite(plate.filter(ImageFilter.GaussianBlur(3)), (x1 - w, y0))
    glow_text(im, (x1 - w + 40, y0 + 75 - f.size * 0.62), t, f, col, RED if loss else AMBER, 20, tabular=True)
    d.line([(x1 - w + 40, y0 + 132), (x1 - 40, y0 + 132)], fill=col, width=3)
    if s.get("source"): o_citation(im, {"text": s["source"]})

def o_parties(im, s):
    items = (s.get("items") or [])[:5]; y = 150; d = ImageDraw.Draw(im)
    if s.get("title"): d.text((96, y), s["title"].upper(), font=F("sansb", 26), fill=(236, 230, 214)); y += 46
    for i, it in enumerate(items):
        f = F("serif", 38); w = tw(d, it, f) + 70; tg = paper(w, 72, (238, 230, 210), 60 + i, 0.6)
        ImageDraw.Draw(tg).text((36, 10), it, font=f, fill=INK); tg = grain(tg.convert("RGB"), 6).convert("RGBA")
        place(im, tg, 96 + w // 2, y + 36, [-1.5, 1, -0.5, 1.5, -1][i], 12); y += 92

def o_citation(im, s):
    d = ImageDraw.Draw(im); t = "SOURCE · " + str(s.get("text", "")); f = F("sansm", 24); w = tw(d, t, f) + 36
    strip = paper(w, 44, (230, 222, 200), 77, 0.4); ImageDraw.Draw(strip).text((18, 8), t, font=f, fill=(40, 34, 28))
    im.alpha_composite(torn(strip, 3, 5, "lr"), (W - 100 - w, H - 112))

def o_lower_third(im, s, photos):
    d = ImageDraw.Draw(im); name, role = s.get("name", ""), s.get("role", "")
    fn, fr = F("serif", 58), F("sansm", 30); w = max(tw(d, name, fn), tw(d, role, fr)) + 90
    pl = Image.new("RGBA", (w, 160), (0, 0, 0, 0)); pd = ImageDraw.Draw(pl); pd.rectangle([0, 0, w, 160], fill=(10, 10, 12, 150))
    im.alpha_composite(pl.filter(ImageFilter.GaussianBlur(6)), (100, H - 290))
    d.line([(120, H - 270), (120, H - 150)], fill=AMBER, width=5)
    glow_text(im, (150, H - 280), name, fn, WHITE, (0, 0, 0), 12); d.text((152, H - 196), role, font=fr, fill=(250, 206, 110))

OVERRIDES = [n for n in dir() if n.startswith(("r_", "o_"))]

