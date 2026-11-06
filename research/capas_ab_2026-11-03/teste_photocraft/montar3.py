# Rodada 3: 5 versões de capa para Weil e 5 para Binance (estilo claro do Bagholder, objeto fundido com a marca,
# antes/depois, êxodo, versão escura). Objetos: ComfyUI (JuggernautXL) ou foto real; recorte e brilho: PhotoCraft 0.19.
# Rodar da raiz do repo: python research/capas_ab_2026-11-03/teste_photocraft/montar3.py
import sys, math, subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import make_capas as M
import montar2 as M2

W, H = M.W, M.H
OUT = HERE / 'r3'; OUT.mkdir(exist_ok=True)
INK = (27, 27, 30); GREEN = (40, 170, 70); PAPER = (236, 234, 228); GRIDC = (206, 210, 212)
PC = Path(__file__).resolve().parents[3] / 'tools/craft_apps/photocraft/photocraft-cli.exe'


# ---------- fundos ----------
def paper_bg():
    im = Image.new('RGB', (W, H), PAPER); d = ImageDraw.Draw(im)
    for x in range(0, W, 40):
        d.line([(x, 0), (x, H)], fill=GRIDC, width=1 if x % 200 else 2)
    for y in range(0, H, 40):
        d.line([(0, y), (W, y)], fill=GRIDC, width=1 if y % 200 else 2)
    rng = np.random.default_rng(7)  # leve sujeira de papel
    n = rng.normal(0, 6, (H, W, 1)).astype('int16')
    v = 1 - 0.18 * ((np.linspace(-1, 1, W)[None, :] ** 2 + np.linspace(-1, 1, H)[:, None] ** 2) / 2)[..., None]
    a = np.clip(np.asarray(im, dtype='int16') * v + n, 0, 255).astype('uint8')
    return Image.fromarray(a)


def arrow_line(im, pts, color, width=30, head=70, alpha=255):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.line(pts, fill=color + (alpha,), width=width, joint='curve')
    (x0, y0), (x1, y1) = pts[-2], pts[-1]; a = math.atan2(y1 - y0, x1 - x0)
    d.polygon([(x1 + head * .6 * math.cos(a), y1 + head * .6 * math.sin(a)), (x1 + head * math.cos(a + 2.5), y1 + head * math.sin(a + 2.5)),
               (x1 + head * math.cos(a - 2.5), y1 + head * math.sin(a - 2.5))], fill=color + (alpha,))
    sh = lay.filter(ImageFilter.GaussianBlur(6)); sh = Image.merge('RGBA', (*Image.new('RGB', (W, H), (0, 0, 0)).split(), sh.split()[3].point(lambda v: v // 3)))
    base = im.convert('RGBA'); base.alpha_composite(sh, (6, 8)); base.alpha_composite(lay); return base.convert('RGB')


def rise_fall(im, x0, x1, ytop, ybot, peak=0.45):
    """seta verde subindo e vermelha despencando (estilo Bagholder)"""
    x1 = min(x1, 1170); ybot = min(ybot, 630)  # seta não encosta na marca do canal
    xp = x0 + (x1 - x0) * peak
    up = [(x0, ybot - 60), (x0 + (xp - x0) * .35, ytop + 170), (x0 + (xp - x0) * .55, ytop + 220), (xp, ytop)]
    down = [(xp, ytop), (xp + (x1 - xp) * .3, ytop + 160), (xp + (x1 - xp) * .45, ytop + 110), (xp + (x1 - xp) * .75, ybot - 120),
            (xp + (x1 - xp) * .85, ybot - 160), (x1, ybot)]
    im = arrow_line(im, up, GREEN, head=0); return arrow_line(im, down, M.L_RED)


def drop_shadow(obj, off=(14, 18), blur=18, op=110):
    a = obj.split()[3]
    sh = Image.new('RGBA', (obj.width + 80, obj.height + 80), (0, 0, 0, 0))
    sh.paste(Image.new('RGBA', obj.size, (0, 0, 0, op)), (40 + off[0], 40 + off[1]), a)
    sh = sh.filter(ImageFilter.GaussianBlur(blur)); sh.alpha_composite(obj, (40, 40)); return sh


def cutout(name, h=None, w=None, angle=0, crop_bottom=0):
    im = Image.open(HERE / f'cut_{name}.png').convert('RGBA')
    if crop_bottom: im = im.crop((0, 0, im.width, im.height - crop_bottom))
    a = im.split()[3].point(lambda v: 0 if v < 40 else v); im.putalpha(a)
    if angle: im = im.rotate(angle, expand=True, resample=Image.BICUBIC)
    im = im.crop(im.getbbox())
    if h: im = im.resize((int(im.width * h / im.height), h), Image.LANCZOS)
    if w: im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
    return im


def headline(d, xy, text, size, fill=INK, maxw=1200, anchor='la'):
    return M.txt(d, xy, text, size, fill, maxw=maxw, anchor=anchor)


def brand_light(im):  # marca do canal em fundo claro
    M.ledger_brand(im)


# ---------- objetos de marca ----------
def binance_coin(size=560):
    """moeda de ouro rachada (ComfyUI) com o símbolo real da Binance cunhado"""
    coin = cutout('c4_coin_0', w=size)
    sym = Image.open(M.BIN / 'entities/binance-logo.png').convert('RGBA').crop((0, 0, 378, 380))
    s = int(size * .52); sym = sym.resize((s, s), Image.LANCZOS)
    mask = Image.new('L', coin.size, 0); mask.paste(sym.split()[3], ((coin.width - s) // 2, (coin.height - s) // 2))
    mask = mask.filter(ImageFilter.GaussianBlur(1.2))
    arr = np.asarray(coin).astype('float32'); m = np.asarray(mask, dtype='float32')[..., None] / 255
    # cunhagem: baixo-relevo escurecido + borda de luz em cima/esquerda
    emb = np.asarray(mask.filter(ImageFilter.EMBOSS).convert('L'), dtype='float32')[..., None] - 128
    rgb = arr[..., :3] * (1 - .62 * m) + np.clip(emb, -70, 70) * 1.3 * (m > 0.02)
    rgb = np.clip(rgb, 0, 255)
    return Image.fromarray(np.concatenate([rgb, arr[..., 3:]], axis=2).astype('uint8'), 'RGBA')


def logo_card_l(path, w, bg=(250, 248, 244)):
    return M.logo_card(path, w, bg=bg, pad=22, radius=14)


def split_card(card, gap=26, drop=40, rot=(5, -8)):
    """cartão de logo partido em dois pedaços (corte em zigue-zague)"""
    w, h = card.size; cx = w // 2
    poly = [(0, 0), (cx + 20, 0), (cx - 15, h * .3), (cx + 25, h * .55), (cx - 10, h * .8), (cx + 10, h), (0, h)]
    m = Image.new('L', card.size, 0); ImageDraw.Draw(m).polygon(poly, fill=255)
    a = card.copy(); a.putalpha(ImageChops.multiply(card.split()[3], m))
    b = card.copy(); b.putalpha(ImageChops.multiply(card.split()[3], ImageOps.invert(m)))
    a = a.crop(a.getbbox()).rotate(rot[0], expand=True, resample=Image.BICUBIC)
    b = b.crop(b.getbbox()).rotate(rot[1], expand=True, resample=Image.BICUBIC)
    return a, b


# ---------------- BINANCE ----------------
def bin1():  # Bagholder claro com moeda da marca
    im = paper_bg(); im = rise_fall(im, 40, 1240, 300, 690, peak=.3)
    c = drop_shadow(binance_coin(450)); im = M.paste_rot(im, c, (W // 2 - c.width // 2 + 60, 215))
    d = ImageDraw.Draw(im); headline(d, (W // 2, 22), '20 MINUTES.', 190, anchor='ma', maxw=1180)
    brand_light(im); return im


def bin2():  # escura, moeda com brilho amarelo
    im = M2.background(900, 380, (150, 110, 10))
    c = binance_coin(520)
    tmp = HERE / '_coin_tmp.png'; c.save(tmp)
    subprocess.run([str(PC), 'run', str(tmp), '--cmd', 'layer.layerStyle.outerGlow', '--params',
                    '{"color":"#f0b90b","opacity":40,"size":120,"spread":0,"technique":"softer"}', '--out', str(HERE / '_coin_glow.png')],
                   capture_output=True)
    g = Image.open(HERE / '_coin_glow.png').convert('RGBA'); g = g.crop(g.getbbox())
    im = M.paste_rot(im, g, (1240 - g.width, H // 2 - g.height // 2))
    d = ImageDraw.Draw(im)
    M.txt(d, (56, 150), '$6.3B', 300, M.L_TXT, maxw=600)
    M.boxed(d, (66, 545), 'GONE IN 20 MINUTES', 78, M.L_TXT, M.L_RED, maxw=560)
    M.ledger_brand(im); return im


def bin3():  # antes / depois
    im = paper_bg(); d = ImageDraw.Draw(im)
    full = drop_shadow(cutout('b2_safe_3', h=400)); empty = drop_shadow(cutout('b3_safe_1', h=400))
    im = M.paste_rot(im, full, (330 - full.width // 2, 230)); im = M.paste_rot(im, empty, (950 - empty.width // 2, 230))
    im = arrow_line(im, [(560, 450), (720, 450)], M.L_RED, width=26, head=60)
    d = ImageDraw.Draw(im)
    M.boxed(d, (200, 660), 'BEFORE', 40, (250, 250, 250), INK)
    M.boxed(d, (790, 660), '20 MIN LATER', 40, (250, 250, 250), M.L_RED)
    headline(d, (W // 2, 20), '$6.3B GONE', 180, anchor='ma')
    im = M.paste_rot(im, logo_card_l(M.BIN / 'entities/binance-logo.png', 240, bg=(20, 20, 22)), (W - 290, 34))
    brand_light(im); return im


def bin4():  # FBI
    im = M2.background(330, 360, (25, 40, 110))
    seal = Image.open(M.BIN / 'entities/fbi-seal.png').convert('RGBA'); seal = seal.crop(seal.getbbox()); seal.thumbnail((400, 400))
    im = M.paste_rot(im, drop_shadow(seal, op=160), (50, 90))
    c = binance_coin(220); im = M.paste_rot(im, drop_shadow(c, op=160), (430, 450))
    d = ImageDraw.Draw(im)
    M.txt(d, (640, 150), 'THE FBI', 130, M.L_TXT, maxw=600)
    M.txt(d, (640, 290), 'NAMED', 130, M.L_TXT, maxw=600)
    M.txt(d, (640, 430), 'NORTH KOREA', 140, M.L_RED, maxw=600)
    M.ledger_brand(im); return im


def bin5():  # cofre vazio no papel claro, com a marca
    im = paper_bg(); im = rise_fall(im, 660, 1180, 110, 560, peak=.3)
    s = drop_shadow(cutout('b3_safe_1', h=470)); im = M.paste_rot(im, s, (1240 - s.width, 200))
    im = M.paste_rot(im, logo_card_l(M.BIN / 'entities/binance-logo.png', 330, bg=(20, 20, 22)), (56, 50))
    d = ImageDraw.Draw(im)
    headline(d, (56, 190), '$6.3B', 260, maxw=600)
    M.boxed(d, (66, 560), 'EMPTIED IN 20 MIN', 74, (250, 250, 250), M.L_RED, maxw=560)
    brand_light(im); return im


# ---------------- WEIL ----------------
def weil1():  # Bagholder claro com o prédio real (GM Building, sede da Weil)
    im = paper_bg(); im = rise_fall(im, 720, 1250, 120, 660, peak=.35)
    b = drop_shadow(cutout('gm_building', h=600)); im = M.paste_rot(im, b, (1000 - b.width // 2, 110))
    im = M.paste_rot(im, logo_card_l(M.WEI / 'entities/weil-logo.png', 230), (56, 50))
    d = ImageDraw.Draw(im)
    headline(d, (56, 190), '95 YEARS.', 170, maxw=640)
    M.boxed(d, (66, 430), 'GONE IN 4 WEEKS', 84, (250, 250, 250), M.L_RED, maxw=600)
    brand_light(im); return im


def weil2():  # logo partido no papel claro
    im = paper_bg(); im = rise_fall(im, 40, 1240, 300, 700, peak=.3)
    card = logo_card_l(M.WEI / 'entities/weil-logo.png', 640)
    a, b = split_card(card)
    im = M.paste_rot(im, drop_shadow(a), (260, 280)); im = M.paste_rot(im, drop_shadow(b), (620, 330))
    d = ImageDraw.Draw(im)
    headline(d, (W // 2, 24), 'NO DEBT. STILL GONE.', 170, anchor='ma', maxw=1200)
    brand_light(im); return im


def weil3():  # êxodo: logo da Weil e setas para os rivais citados no vídeo
    im = M2.background(360, 380, (110, 28, 24))
    im = M.paste_rot(im, logo_card_l(M.WEI / 'entities/weil-logo.png', 300), (60, 300))
    rivals = ['paulweiss-logo.png', 'simpson-logo.png', 'sullivan-logo.png', 'cravath-logo.png']
    ys = [120, 270, 420, 570]
    d = ImageDraw.Draw(im)
    for f, y in zip(rivals, ys):
        cd = logo_card_l(M.WEI / 'entities' / f, 300)
        if cd.height > 120: cd = cd.resize((int(cd.width * 120 / cd.height), 120))
        im = M.paste_rot(im, cd, (440, y - cd.height // 2))
        im = arrow_line(im, [(370, 360), (430, y)], M.L_RED, width=10, head=26)
    d = ImageDraw.Draw(im)
    M.txt(d, (800, 160), 'THE', 130, M.L_TXT, maxw=440)
    M.txt(d, (800, 290), 'PARTNERS', 130, M.L_TXT, maxw=440)
    M.txt(d, (800, 420), 'LEFT.', 170, M.L_RED, maxw=440)
    M.ledger_brand(im); return im


def weil4():  # cadeira vazia no papel claro
    im = paper_bg(); im = rise_fall(im, 700, 1250, 110, 620, peak=.3)
    c = drop_shadow(cutout('weil_chair_a', h=540)); im = M.paste_rot(im, c, (1230 - c.width, 150))
    im = M.paste_rot(im, logo_card_l(M.WEI / 'entities/weil-logo.png', 230), (56, 50))
    d = ImageDraw.Draw(im)
    headline(d, (56, 190), '$2B FIRM.', 170, maxw=600)
    M.boxed(d, (66, 430), 'NO DEBT. GONE.', 90, (250, 250, 250), M.L_RED, maxw=560)
    brand_light(im); return im


def weil5():  # escura: clientes famosos, depois ela mesma
    im = M2.background(900, 380, (110, 28, 24))
    b = cutout('gm_building', h=640)
    b = Image.merge('RGBA', (*ImageOps.grayscale(b.convert('RGB')).convert('RGB').split(), b.split()[3]))
    im = M.paste_rot(im, b, (1060 - b.width // 2, 70))
    x = 56
    for f in ['lehman-logo.png', 'enron-logo.png', 'gm-logo.png']:
        cd = logo_card_l(M.WEI / 'entities' / f, 250)
        cd = Image.merge('RGBA', (*ImageOps.grayscale(cd.convert('RGB')).convert('RGB').split(), cd.split()[3]))
        if cd.height > 150: cd = cd.resize((int(cd.width * 150 / cd.height), 150))
        im = M.paste_rot(im, cd, (x, 60)); x += cd.width + 24
    d = ImageDraw.Draw(im)
    M.txt(d, (56, 250), 'THEN', 150, M.L_TXT, maxw=620)
    M.txt(d, (56, 410), 'ITSELF.', 190, M.L_RED, maxw=620)
    M.ledger_brand(im); return im


if __name__ == '__main__':
    sets = {'binance': [bin1, bin2, bin3, bin4, bin5], 'weil': [weil1, weil2, weil3, weil4, weil5]}
    for k, fs in sets.items():
        ims = []
        for i, f in enumerate(fs, 1):
            im = f(); im.save(OUT / f'{k}_v{i}.jpg', quality=93); ims.append(im)
        tw, th = 400, 225
        S = Image.new('RGB', (3 * (tw + 10) + 10, 2 * (th + 10) + 10), (245, 245, 245))
        for i, im in enumerate(ims):
            S.paste(im.resize((tw, th), Image.LANCZOS), (10 + (i % 3) * (tw + 10), 10 + (i // 3) * (th + 10)))
        S.save(OUT / f'feed_{k}.jpg', quality=90)
    print('ok')
