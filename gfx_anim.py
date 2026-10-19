"""Dark Studio - graficos animados (MP4) para dados com fonte:
  moneyflow: mapa escuro estilizado (Natural Earth, dominio publico) com rota brilhante e particulas de dinheiro
             {"type":"moneyflow","title","flows":[{"from":{"name","lon","lat"},"to":{...},"amount":"$715M","date":"Oct 2025"}],"bbox":[lon0,lat0,lon1,lat1],"source"}
  collapse:  queda de valor (linha ou barras), acento vermelho, marcadores de evento, contador final
             {"type":"collapse","title","unit":"$B","mode":"line|bars","points":[{"label","value","event":""}],"final":{"label","value","from"},"source"}
             linha: "axis_min" (piso do eixo, p/ quedas pequenas) e "ref":{"value","label"} (linha de referencia, ex.: $1.00)
"""
import json, math, subprocess, shutil
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import gfx  # noqa: carrega gfx antes de gfx2 (evita import circular)
import gfx2 as V
W, H = 1920, 1080
ANIM = {"moneyflow", "collapse"}
AS = Path(__file__).resolve().parent / "assets"

def _ease(t): return 1 - (1 - max(0, min(1, t))) ** 3

def _ffmpeg():
    try:
        import montage
        if montage.FFMPEG: return montage.FFMPEG
    except Exception: pass
    return shutil.which("ffmpeg") or "ffmpeg"

def encode(frames_iter, out, fps=30):
    out = Path(out); p = subprocess.Popen([_ffmpeg(), "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", str(out)], stdin=subprocess.PIPE)
    for f in frames_iter: p.stdin.write(f.convert("RGB").tobytes())
    p.stdin.close(); p.wait(); return out

def _money(n):  # "$715M" -> (prefix, valor, sufixo)
    import re
    m = re.match(r"([^\d]*)([\d,.]+)(.*)", str(n))
    return (m.group(1), float(m.group(2).replace(",", "")), m.group(3)) if m else ("", 0.0, str(n))

def _dec(ref):  # casas decimais do valor final (ex.: $0.97 -> 2), usadas tambem durante a contagem
    return 2 if ref < 10 and round(ref, 1) != ref else 1 if (ref < 100 and ref != int(ref)) else 0

def _fmtc(pre, v, suf, ref):
    dec = _dec(ref)
    return f"{pre}{v:,.{dec}f}{suf}"

# ---------- mapa ----------
_LAND = None
def _polys():
    global _LAND
    if _LAND is None:
        _LAND = []
        for fn in ("ne_110m_land.geojson",):
            g = json.load(open(AS / fn, encoding="utf-8"))
            for f in g["features"]:
                geo = f["geometry"]; cs = geo["coordinates"] if geo["type"] == "MultiPolygon" else [geo["coordinates"]]
                for poly in cs: _LAND.append(poly[0])
    return _LAND

def _states():
    g = json.load(open(AS / "ne_110m_admin1.geojson", encoding="utf-8")); out = []
    for f in g["features"]:
        geo = f["geometry"]; cs = geo["coordinates"] if geo["type"] == "MultiPolygon" else [geo["coordinates"]]
        for poly in cs: out.append(poly[0])
    return out

def _proj(bbox):
    lon0, lat0, lon1, lat1 = bbox; my = lambda la: math.log(math.tan(math.pi / 4 + math.radians(max(-80, min(80, la))) / 2))
    y0, y1 = my(lat0), my(lat1); rx = lambda lo: math.radians(lo); lon0r, lon1r = rx(lon0), rx(lon1); sx = W / (lon1r - lon0r); sy = H / (y1 - y0); s = min(sx, sy)
    ox = (W - (lon1r - lon0r) * s) / 2; oy = (H - (y1 - y0) * s) / 2
    return lambda lo, la: (ox + (rx(lo) - lon0r) * s, H - (oy + (my(la) - y0) * s))

def map_base(bbox, seed=51):
    im = V.backdrop(seed, tint=(12, 16, 22), leak=V.TEAL).convert("RGBA"); P = _proj(bbox)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for ring in _polys():
        pts = [P(lo, la) for lo, la in ring]
        if len(pts) > 2: d.polygon(pts, fill=(34, 44, 54, 255), outline=(70, 110, 120, 255))
    if (bbox[2] - bbox[0]) < 90:
        for ring in _states():
            pts = [P(lo, la) for lo, la in ring]
            if len(pts) > 2: d.line(pts + [pts[0]], fill=(58, 80, 90, 255), width=1)
    gl = lay.filter(ImageFilter.GaussianBlur(10)); im.alpha_composite(Image.blend(Image.new("RGBA", (W, H), (0, 0, 0, 0)), gl, 0.5)); im.alpha_composite(lay)
    # retícula de pontos
    dd = ImageDraw.Draw(im)
    for x in range(0, W, 48):
        for y in range(0, H, 48): dd.point((x, y), fill=(60, 72, 80))
    return V.grain(im.convert("RGB"), 8).convert("RGBA"), P

def _bez(a, b, t, lift=0.22):
    (x0, y0), (x1, y1) = a, b; mx, my = (x0 + x1) / 2, (y0 + y1) / 2; dist = math.hypot(x1 - x0, y1 - y0)
    cx, cy = mx, my - dist * lift
    return ((1 - t) ** 2 * x0 + 2 * (1 - t) * t * cx + t * t * x1, (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t * t * y1)

def moneyflow_frames(s, dur=7.0, fps=30):
    flows = s.get("flows") or []; pts_all = [(f[k]["lon"], f[k]["lat"]) for f in flows for k in ("from", "to")]
    bbox = s.get("bbox") or [min(p[0] for p in pts_all) - 12, min(p[1] for p in pts_all) - 8, max(p[0] for p in pts_all) + 12, max(p[1] for p in pts_all) + 8]
    base, P = map_base(bbox); n = int(dur * fps)
    d0 = ImageDraw.Draw(base); V.kicker(d0, s.get("title", "Follow the money")); V.source(d0, s.get("source"))
    for i in range(n):
        t = i / (n - 1); im = base.copy(); glow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow); d = ImageDraw.Draw(im)
        for k, f in enumerate(flows):
            st = max(0, min(1, (t - 0.08 - k * 0.12) / 0.45)); a, b = P(f["from"]["lon"], f["from"]["lat"]), P(f["to"]["lon"], f["to"]["lat"])
            col = tuple(f.get("color") or V.AMBER)
            path = [_bez(a, b, u / 60) for u in range(int(60 * _ease(st)) + 1)]
            if len(path) > 1:
                gd.line(path, fill=col + (255,), width=14); d.line(path, fill=(255, 236, 190), width=4)
            for q in range(14):  # particulas
                u = ((t * 1.6 + q / 14) % 1.0)
                if u <= _ease(st):
                    x, y = _bez(a, b, u); r = 6 if q % 3 else 9
                    gd.ellipse([x - r * 2, y - r * 2, x + r * 2, y + r * 2], fill=col + (200,)); d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 246, 210))
            for p, lab, al in ((a, f["from"]["name"], 1), (b, f["to"]["name"], st)):
                if al <= 0: continue
                pul = 18 + 10 * math.sin(t * 12 + k); gd.ellipse([p[0] - pul, p[1] - pul, p[0] + pul, p[1] + pul], fill=V.TEAL + (160,))
                d.ellipse([p[0] - 9, p[1] - 9, p[0] + 9, p[1] + 9], fill=(240, 250, 250)); fl = V.F("sansb", 32); lw = V.tw(d, lab, fl)
                lx = p[0] + 22 if p[0] + 22 + lw < W - 40 else p[0] - 22 - lw; d.text((lx, p[1] + 14), lab, font=fl, fill=(236, 240, 240))
            if st > 0.6:  # rotulo de valor + data no meio do arco
                al = min(1, (st - 0.6) / 0.3); mx, my = _bez(a, b, 0.5)
                pre, v, suf = _money(f.get("amount", "")); txt = _fmtc(pre, v * _ease(al), suf, v)
                fa = V.F("num", 72); wv = V.text_w(_fmtc(pre, v, suf, v), fa, True)  # largura do valor final: o contador nao balanca
                V.glow_text(im, (mx - wv / 2, my - 170), txt, fa, (255, 222, 140), V.AMBER, 18, tabular=True)
                if f.get("date"): d.text((mx - V.tw(d, f["date"], V.F("sansm", 28)) / 2, my - 80), f["date"], font=V.F("sansm", 28), fill=(220, 214, 200))
        im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(10)))
        yield im

# ---------- colapso ----------
def collapse_frames(s, dur=7.0, fps=30):
    pts = s.get("points") or []; unit = s.get("unit", ""); mode = s.get("mode", "line"); n = int(dur * fps)
    base = V.backdrop(57, leak=V.RED).convert("RGBA"); d0 = ImageDraw.Draw(base); V.kicker(d0, s.get("title", ""), color=(240, 96, 86)); V.source(d0, s.get("source"))  # kicker vermelho claro: contraste 5.4:1 (o RED puro da 3.7:1 em texto)
    x0, x1, yb, yt = 200, W - 520, 900, 260; mx = max([float(p["value"]) for p in pts] + [1e-9])
    mn = float(s.get("axis_min") or 0) if mode != "bars" else 0.0  # barras sempre do zero
    ref = s.get("ref") if mode != "bars" else None
    if ref: mx = max(mx, float(ref["value"]))
    d0.line([(x0, yb), (x1 + 80, yb)], fill=(110, 104, 96), width=2)
    if ref:  # linha de referencia tracejada (ex.: o "buck" de $1.00)
        ry = yb - (yb - yt) * (float(ref["value"]) - mn) / (mx - mn)
        for xx in range(x0, x1 + 80, 28): d0.line([(xx, ry), (min(xx + 16, x1 + 80), ry)], fill=V.AMBER, width=3)
        d0.text((x0, ry - 42), ref.get("label", ""), font=V.F("sansm", 28), fill=(250, 206, 110))
    for g in range(1, 4):
        yy = yb - (yb - yt) * g / 4; d0.line([(x0, yy), (x1 + 80, yy)], fill=(48, 46, 44), width=1)
    def fmt(v):
        if unit == "$B" and v < 1: return f"${v * 1000:,.0f}M"
        dec = max([_dec(float(p["value"])) for p in pts] + [0])
        return f"{unit[:1] if unit.startswith('$') else ''}{v:,.{dec}f}{unit[1:] if unit.startswith('$') else unit}"
    for i in range(n):
        t = i / (n - 1); im = base.copy(); d = ImageDraw.Draw(im); glow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
        k = len(pts); prog = _ease(t / 0.8) * (k - 1) if k > 1 else 1
        if mode == "bars":
            bw = min(260, (x1 - x0) // max(1, k) - 60)
            for j, p in enumerate(pts):
                al = max(0, min(1, (t - j * 0.18) / 0.35)); v = float(p["value"]); h = (yb - yt) * (v / mx) * _ease(al)
                col = tuple(p.get("color") or (V.RED if p.get("tone") == "loss" else V.TEAL)); bx = x0 + 40 + j * (bw + 70)
                gd.rectangle([bx, yb - h, bx + bw, yb], fill=col + (140,)); d.rectangle([bx, yb - h, bx + bw, yb], fill=col)
                if al > 0: 
                    tx = p["display"] if p.get("display") and al >= 1 else fmt(v * _ease(al)); fv = V.fit(p.get("display") or fmt(v), "num", 60, bw + 60, True); V.draw_text(d, (bx + bw / 2 - V.text_w(tx, fv, True) / 2, yb - h - 78), tx, fv, V.WHITE, tabular=True)
                    for q, l in enumerate(V.wrap(d, p.get("label", ""), V.F("sansm", 26), bw + 40)[:2]): d.text((bx + bw / 2 - V.tw(d, l, V.F("sansm", 26)) / 2, yb + 16 + q * 32), l, font=V.F("sansm", 26), fill=V.MUTED)
        else:
            xs = [x0 + (x1 - x0) * j / max(1, k - 1) for j in range(k)]; ys = [yb - (yb - yt) * (float(p["value"]) - mn) / (mx - mn) for p in pts]
            line = []
            for j in range(k):
                if j <= prog: line.append((xs[j], ys[j]))
                elif j - 1 < prog: f = prog - (j - 1); line.append((xs[j - 1] + (xs[j] - xs[j - 1]) * f, ys[j - 1] + (ys[j] - ys[j - 1]) * f))
            if len(line) > 1:
                poly = line + [(line[-1][0], yb), (line[0][0], yb)]; fl = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(fl).polygon(poly, fill=V.RED + (60,)); im.alpha_composite(fl)
                gd.line(line, fill=V.RED + (255,), width=16); d.line(line, fill=(255, 120, 108), width=6)
            for j, p in enumerate(pts):
                if j <= prog:
                    d.ellipse([xs[j] - 9, ys[j] - 9, xs[j] + 9, ys[j] + 9], fill=V.WHITE); d.text((xs[j] - 40, yb + 16), p.get("label", ""), font=V.F("sansm", 24), fill=V.MUTED)
                    if p.get("event"):
                        d.line([(xs[j], ys[j] - 16), (xs[j], ys[j] - 90)], fill=V.AMBER, width=2)
                        d.text((xs[j] - 10, ys[j] - 130), p["event"], font=V.F("hand", 38), fill=(250, 206, 110))
        fin = s.get("final")
        if fin:  # contador final
            al = max(0, min(1, (t - 0.45) / 0.45)); pre, v, suf = _money(fin.get("value", "")); st = _money(fin["from"])[1] if fin.get("from") else 0.0  # "from": conta de cima p/ baixo (ex.: $1.00 -> $0.97)
            txt = _fmtc(pre, st + (v - st) * _ease(al) if v > 0 else v, suf, v)
            fv = V.fit(_fmtc(pre, v, suf, v), "num", 120, 420, True); V.glow_text(im, (W - 470, 420), txt, fv, (255, 120, 108), V.RED, 24, tabular=True)
            for q, l in enumerate(V.wrap(d, fin.get("label", ""), V.F("sansm", 30), 400)[:3]): d.text((W - 470, 570 + q * 40), l, font=V.F("sansm", 30), fill=V.WHITE)
        im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(12)))
        yield im

def render(spec, out, dur=7.0):
    fr = moneyflow_frames if spec["type"] == "moneyflow" else collapse_frames
    return encode(fr(spec, dur), out)

def still(spec, t=1.0):
    fr = moneyflow_frames if spec["type"] == "moneyflow" else collapse_frames
    fs = list(fr(spec, 0.6, 5)); return fs[min(len(fs) - 1, int(t * (len(fs) - 1)))]
