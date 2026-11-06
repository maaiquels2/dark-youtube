# Capas v2 (Weil, Binance): objeto no momento do desastre, luz de recorte na cor da marca (PhotoCraft),
# gráfico caindo atrás do objeto, sombra de chão, texto à esquerda. Rodar da raiz do repo.
import sys, math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import make_capas as M

W, H = M.W, M.H


def background(cx, cy, tint):
    im = Image.new('RGB', (W, H), M.L_BG)
    glow = Image.new('RGB', (W, H), (0, 0, 0)); g = ImageDraw.Draw(glow)
    g.ellipse([cx - 430, cy - 360, cx + 430, cy + 360], fill=tint)
    glow = glow.filter(ImageFilter.GaussianBlur(160))
    im = Image.blend(im, Image.eval(glow, lambda v: v), 0.0)  # base
    im = Image.fromarray(__import__('numpy').clip(__import__('numpy').asarray(im, dtype='int16') + __import__('numpy').asarray(glow, dtype='int16') // 3, 0, 255).astype('uint8'))
    d = ImageDraw.Draw(im)
    for x in range(0, W, 64):
        d.line([(x, 0), (x, H)], fill=(20, 24, 32), width=1)
    for y in range(0, H, 64):
        d.line([(0, y), (W, y)], fill=(20, 24, 32), width=1)
    return im


def chart(im, pts, color, alpha=170, width=16):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.line(pts, fill=color + (alpha,), width=width, joint='curve')
    (x0, y0), (x1, y1) = pts[-2], pts[-1]; a = math.atan2(y1 - y0, x1 - x0); h = 46
    d.polygon([(x1 + h * .6 * math.cos(a), y1 + h * .6 * math.sin(a)), (x1 + h * math.cos(a + 2.5), y1 + h * math.sin(a + 2.5)),
               (x1 + h * math.cos(a - 2.5), y1 + h * math.sin(a - 2.5))], fill=color + (alpha,))
    base = im.convert('RGBA'); base.alpha_composite(lay); return base.convert('RGB')


def floor_shadow(im, cx, y, w, h=46, strength=200):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.ellipse([cx - w // 2, y - h // 2, cx + w // 2, y + h // 2], fill=(0, 0, 0, strength))
    lay = lay.filter(ImageFilter.GaussianBlur(22))
    base = im.convert('RGBA'); base.alpha_composite(lay); return base.convert('RGB')


def obj(name, h, angle=0):
    """devolve (imagem com brilho, caixa da parte solida) com a parte solida medindo h de altura"""
    im = Image.open(HERE / f'glow_{name}.png').convert('RGBA')
    solid = Image.open(HERE / f'cut_{name}.png').convert('RGBA').split()[3].point(lambda v: 255 if v > 200 else 0)
    sb = solid.getbbox(); s = h / (sb[3] - sb[1])
    im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    return im, tuple(int(v * s) for v in sb)


def place(im, o, right, floor):
    """cola o objeto com a parte solida terminando em x=right e encostando no chao y=floor"""
    img, sb = o
    x = right - sb[2]; y = floor - sb[3]
    im = floor_shadow(im, x + (sb[0] + sb[2]) // 2, floor - 4, int((sb[2] - sb[0]) * 1.05))
    return M.paste_rot(im, img, (x, y))


def brand_logo(im, path, w, xy, bg):
    return M.paste_rot(im, M.logo_card(path, w, bg=bg, pad=18, radius=14), xy)


def weil(angle, tag):
    im = background(900, 420, (120, 30, 26))
    im = chart(im, [(660, 120), (730, 200), (775, 165), (830, 380), (865, 350), (905, 600)], M.L_RED, 150, 14)
    im = place(im, obj('weil_chair_a', 560), 1225, 650)
    im = brand_logo(im, M.WEI / 'entities/weil-logo.png', 220, (60, 54), (250, 248, 244))
    d = ImageDraw.Draw(im)
    M.txt(d, (56, 190), 'NO DEBT.', 178, M.L_TXT, maxw=600)
    M.txt(d, (56, 400), 'STILL GONE.', 178, M.L_RED, maxw=600)
    M.ledger_brand(im); im.save(HERE / f'capa2_weil_{tag}.jpg', quality=93); return im


def binance():
    im = background(930, 400, (150, 110, 10))
    im = place(im, obj('b3_safe_1', 520), 1225, 650)
    im = brand_logo(im, M.BIN / 'entities/binance-logo.png', 300, (60, 54), (18, 18, 20))
    d = ImageDraw.Draw(im)
    M.txt(d, (56, 160), '$6.3B', 300, M.L_TXT, maxw=600)
    M.boxed(d, (66, 545), 'GONE IN 20 MINUTES', 78, M.L_TXT, M.L_RED, maxw=560)
    M.ledger_brand(im); im.save(HERE / 'capa2_binance.jpg', quality=93); return im


if __name__ == '__main__':
    outs = [weil(0, 'empe'), binance()]
    tw, th = 400, 225
    S = Image.new('RGB', (2 * tw + 30, th + 20), (245, 245, 245))
    for i, im in enumerate(outs):
        S.paste(im.resize((tw, th), Image.LANCZOS), (10 + i * (tw + 10), 10))
    S.save(HERE / 'feed_v2.jpg', quality=90)
    print('ok')
