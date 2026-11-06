# Rodada 4: mais 5 conceitos de capa para Binance e 5 para Weil (sem repetir a rodada 3).
# Fatos usados (narração e descrição dos vídeos): Binance ~$6.3B em ~20 min; Tether e Circle congelaram ~$2.36B; BTC/ETH não
# podem ser congelados; TRM Labs: maior roubo cripto registrado. Weil: fundada em 1931; "o advogado que Wall Street chamava";
# lucro por sócio ~metade do de Kirkland e Wachtell (Reuters/American Lawyer); fusão com Willkie desfeita (Bloomberg Law).
# Rodar da raiz do repo: python research/capas_ab_2026-11-03/teste_photocraft/montar4.py
import sys, math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageOps
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent)); sys.path.insert(0, str(HERE))
import make_capas as M
import montar2 as M2
import montar3 as R3

W, H = M.W, M.H
OUT = HERE / 'r4'; OUT.mkdir(exist_ok=True)
INK, PAPER = R3.INK, R3.PAPER
BIN_LOGO = M.BIN / 'entities/binance-logo.png'
WEIL_LOGO = M.WEI / 'entities/weil-logo.png'
YEL = (240, 185, 11)


def bin_symbol(size):
    s = Image.open(BIN_LOGO).convert('RGBA').crop((0, 0, 378, 380))
    return s.resize((size, size), Image.LANCZOS)


# ---------------- BINANCE ----------------
def bin6():  # ampulheta de moedas, escura
    im = M2.background(960, 380, (150, 110, 10))
    hg = R3.cutout('r4_hg_2', h=620); im = M.paste_rot(im, R3.drop_shadow(hg, op=170), (960 - hg.width // 2 - 40, 40))
    im = M.paste_rot(im, R3.logo_card_l(BIN_LOGO, 300, bg=(18, 18, 20)), (56, 54))
    d = ImageDraw.Draw(im)
    M.txt(d, (56, 190), '$6.3B', 250, M.L_TXT, maxw=620)
    M.boxed(d, (66, 545), 'IN 20 MINUTES', 84, M.L_TXT, M.L_RED, maxw=560)
    M.ledger_brand(im); return im


def bin7():  # gelo com Tether e USDC dentro
    im = R3.paper_bg()
    ice = R3.cutout('r4_ice_0', h=470).copy()
    for f, y in [('tether-logo.png', .30), ('circle-logo.png', .58)]:
        c = R3.logo_card_l(M.BIN / 'entities' / f, int(ice.width * .62), bg=(235, 242, 248))
        c.putalpha(c.split()[3].point(lambda v: int(v * .78)))
        c = c.filter(ImageFilter.GaussianBlur(1.2))
        ice.alpha_composite(c, ((ice.width - c.width) // 2, int(ice.height * y) - c.height // 2))
    im = M.paste_rot(im, R3.drop_shadow(ice), (60, 140))
    d = ImageDraw.Draw(im)
    R3.headline(d, (660, 170), 'FROZEN.', 200, maxw=580)
    M.boxed(d, (670, 440), 'NOT ALL OF IT.', 92, (250, 250, 250), M.L_RED, maxw=560)
    M.ledger_brand(im); return im


def bin8():  # cronômetro desenhado: 20 de 60 minutos
    im = M2.background(900, 360, (120, 20, 16)); d = ImageDraw.Draw(im)
    cx, cy, r = 920, 370, 270
    d.ellipse([cx - r - 18, cy - r - 18, cx + r + 18, cy + r + 18], fill=(40, 42, 48))
    d.rectangle([cx - 34, cy - r - 70, cx + 34, cy - r - 10], fill=(40, 42, 48)); d.rectangle([cx - 60, cy - r - 92, cx + 60, cy - r - 62], fill=(40, 42, 48))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(236, 232, 225))
    d.pieslice([cx - r + 10, cy - r + 10, cx + r - 10, cy + r - 10], -90, 30, fill=M.L_RED)
    for i in range(60):
        a = math.radians(i * 6 - 90); l = 34 if i % 5 == 0 else 16; w = 6 if i % 5 == 0 else 3
        d.line([(cx + (r - 8) * math.cos(a), cy + (r - 8) * math.sin(a)), (cx + (r - 8 - l) * math.cos(a), cy + (r - 8 - l) * math.sin(a))], fill=INK, width=w)
    a = math.radians(30); d.line([(cx, cy), (cx + (r - 50) * math.cos(a), cy + (r - 50) * math.sin(a))], fill=INK, width=14)
    d.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], fill=INK)
    sym = bin_symbol(120); im = M.paste_rot(im, sym, (cx - 150, cy + 40))
    d = ImageDraw.Draw(im)
    M.txt(d, (56, 150), '$6.3B', 260, M.L_TXT, maxw=560)
    M.txt(d, (56, 470), '20 MIN.', 150, M.L_RED, maxw=560)
    M.ledger_brand(im); return im


def bin9():  # recibo desenhado
    im = R3.paper_bg()
    rc = Image.new('RGBA', (430, 600), (0, 0, 0, 0)); d = ImageDraw.Draw(rc)
    pts = [(0, 0), (430, 0), (430, 570)] + [(430 - i * 21.5, 570 + (12 if i % 2 else -0)) for i in range(21)] + [(0, 570)]
    d.polygon(pts, fill=(252, 251, 247, 255))
    mono = M.font(str(Path(M.ROOT) / 'fonts/CourierPrime-Bold.ttf'), 30)
    d.text((215, 40), 'BINANCE HACK', font=M.font(str(Path(M.ROOT) / 'fonts/CourierPrime-Bold.ttf'), 40), fill=INK, anchor='ma')
    d.text((215, 92), 'OCT 29, 2026', font=mono, fill=(110, 110, 110), anchor='ma')
    d.line([(30, 140), (400, 140)], fill=(150, 150, 150), width=3)
    rows = [('STOLEN', '$6.3B'), ('FROZEN', '$2.36B'), ('TIME', '~20 MIN')]
    y = 170
    for k, v in rows:
        d.text((34, y), k, font=mono, fill=INK); d.text((396, y), v, font=mono, fill=INK, anchor='ra'); y += 58
    d.line([(30, y + 6), (400, y + 6)], fill=(150, 150, 150), width=3)
    d.text((34, y + 30), 'PAID BY', font=M.font(str(Path(M.ROOT) / 'fonts/CourierPrime-Bold.ttf'), 40), fill=M.L_RED)
    d.text((396, y + 30), '???', font=M.font(str(Path(M.ROOT) / 'fonts/CourierPrime-Bold.ttf'), 40), fill=M.L_RED, anchor='ra')
    rc = rc.rotate(-5, expand=True, resample=Image.BICUBIC)
    im = M.paste_rot(im, R3.drop_shadow(rc), (90, 40))
    im = M.paste_rot(im, R3.logo_card_l(BIN_LOGO, 300, bg=(18, 18, 20)), (900, 60))
    d = ImageDraw.Draw(im)
    R3.headline(d, (640, 220), 'WHO PAYS', 170, maxw=600)
    R3.headline(d, (640, 410), 'THE BILL?', 170, fill=M.L_RED, maxw=600)
    M.ledger_brand(im); return im


def bin10():  # símbolo estilhaçado
    im = M2.background(900, 360, (150, 110, 10))
    sym = bin_symbol(520)
    cx, cy = 260, 260; pieces = [(-90, -20), (-20, 60), (60, 140), (140, 230), (230, 270)]
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    for i, (a0, a1) in enumerate(pieces):
        m = Image.new('L', sym.size, 0)
        ImageDraw.Draw(m).pieslice([cx - 600, cy - 600, cx + 600, cy + 600], a0, a1, fill=255)
        p = sym.copy(); p.putalpha(Image.composite(sym.split()[3], Image.new('L', sym.size, 0), m))
        mid = math.radians((a0 + a1) / 2); off = 26 + 10 * i
        p = p.rotate((i - 2) * 4, resample=Image.BICUBIC)
        lay.alpha_composite(p, (int(700 + off * math.cos(mid)), int(100 + off * math.sin(mid))))
    base = im.convert('RGBA'); base.alpha_composite(lay); im = base.convert('RGB')
    d = ImageDraw.Draw(im)
    M.txt(d, (56, 170), 'RECORD', 190, M.L_TXT, maxw=600)
    M.txt(d, (56, 370), 'HEIST.', 190, M.L_RED, maxw=600)
    d.text((62, 590), 'LARGEST CRYPTO THEFT ON RECORD, PER TRM LABS', font=M.font(M.INTER, 22, 600), fill=(170, 170, 170))
    M.ledger_brand(im); return im


# ---------------- WEIL ----------------
def weil6():  # caixa de mudança com o logo da Weil colado
    im = R3.paper_bg()
    box = R3.cutout('r4_box_0', h=520).copy()
    lg = R3.logo_card_l(WEIL_LOGO, int(box.width * .40)).rotate(-3, expand=True, resample=Image.BICUBIC)
    bb = box.getbbox(); box.alpha_composite(lg, (int(box.width * .22), int(box.height * .62)))
    im = M.paste_rot(im, R3.drop_shadow(box), (1250 - box.width, 160))
    d = ImageDraw.Draw(im)
    R3.headline(d, (56, 140), 'THE', 150, maxw=600)
    R3.headline(d, (56, 290), 'PARTNERS', 150, maxw=600)
    M.boxed(d, (66, 480), 'PACKED UP.', 110, (250, 250, 250), M.L_RED, maxw=560)
    M.ledger_brand(im); return im


def weil7():  # linha do tempo: 95 anos x 4 semanas
    im = M2.background(640, 400, (110, 28, 24)); d = ImageDraw.Draw(im)
    x0, x1, y = 70, 1130, 470
    d.rounded_rectangle([x0, y - 34, x1, y + 34], 34, fill=(40, 150, 70))
    d.rounded_rectangle([x1 - 8, y - 34, x1 + 70, y + 34], 20, fill=M.L_RED)
    f = M.font(M.ANTON, 46)
    d.text((x0, y + 52), '1931', font=f, fill=M.L_TXT); d.text((x1 + 70, y + 52), '2026', font=f, fill=M.L_TXT, anchor='ra')
    d.line([(x1 + 30, y - 40), (x1 + 30, y - 120)], fill=M.L_RED, width=6)
    d.text((x1 + 30, y - 130), '4 WEEKS', font=M.font(M.ANTON, 54), fill=M.L_RED, anchor='ms')
    im = M.paste_rot(im, R3.logo_card_l(WEIL_LOGO, 230), (56, 54))
    d = ImageDraw.Draw(im)
    M.txt(d, (56, 170), '95 YEARS.', 190, M.L_TXT, maxw=820)
    M.ledger_brand(im); return im


def weil8():  # lucro por sócio: Weil ~metade
    im = R3.paper_bg(); d = ImageDraw.Draw(im)
    base = 560; bw = 160
    bars = [('KIRKLAND', 1.0, (70, 74, 82)), ('WACHTELL', 1.0, (70, 74, 82)), ('WEIL', 0.5, M.L_RED)]
    for i, (name, v, c) in enumerate(bars):
        x = 640 + i * 190; h = int(420 * v)
        d.rectangle([x, base - h, x + bw, base], fill=c)
        M.txt(d, (x + bw // 2, base + 14), name, 46, INK, anchor='ma', maxw=bw + 20)
    M.txt(d, (640 + 2 * 190 + bw // 2, base - 210 - 16), '≈ HALF', 44, M.L_RED, anchor='ms')
    R3.headline(d, (56, 100), 'PAID', 200, maxw=560)
    R3.headline(d, (56, 300), 'HALF.', 200, fill=M.L_RED, maxw=560)
    d.text((62, 590), 'AVERAGE PROFIT PER PARTNER', font=M.font(M.INTER, 20, 600), fill=(90, 90, 90)); d.text((62, 618), 'PER REUTERS / THE AMERICAN LAWYER', font=M.font(M.INTER, 20, 600), fill=(90, 90, 90))
    M.ledger_brand(im); return im


def weil9():  # martelo: "o advogado de Wall Street"
    im = M2.background(900, 400, (110, 28, 24))
    g = R3.cutout('r4_gav_0', h=430); im = M.paste_rot(im, R3.drop_shadow(g, op=180), (1240 - g.width, 190))
    im = M.paste_rot(im, R3.logo_card_l(WEIL_LOGO, 230), (56, 54))
    d = ImageDraw.Draw(im)
    M.txt(d, (56, 180), "WALL STREET'S", 130, M.L_TXT, maxw=640)
    M.txt(d, (56, 320), 'LAWYER.', 160, M.L_TXT, maxw=640)
    M.boxed(d, (66, 520), 'GONE.', 100, M.L_TXT, M.L_RED)
    M.ledger_brand(im); return im


def weil10():  # fusão desfeita com a Willkie
    im = R3.paper_bg()
    a = R3.logo_card_l(WEIL_LOGO, 360); b = R3.logo_card_l(M.WEI / 'entities/willkie-logo.png', 360, bg=(250, 248, 244))
    if b.height > a.height: b = b.resize((int(b.width * a.height / b.height), a.height))
    im = M.paste_rot(im, R3.drop_shadow(a), (90, 380)); im = M.paste_rot(im, R3.drop_shadow(b), (830, 380 + (a.height - b.height) // 2))
    d = ImageDraw.Draw(im)
    y = 380 + a.height // 2 + 40
    for x in range(500, 830, 34): d.line([(x, y), (x + 18, y)], fill=INK, width=8)
    d.line([(615, y - 60), (715, y + 60)], fill=M.L_RED, width=22); d.line([(615, y + 60), (715, y - 60)], fill=M.L_RED, width=22)
    R3.headline(d, (W // 2, 30), 'THE MERGER', 160, anchor='ma', maxw=1100)
    R3.headline(d, (W // 2, 200), 'FAILED.', 160, fill=M.L_RED, anchor='ma', maxw=1100)
    M.ledger_brand(im); return im


if __name__ == '__main__':
    sets = {'binance': [bin6, bin7, bin8, bin9, bin10], 'weil': [weil6, weil7, weil8, weil9, weil10]}
    for k, fs in sets.items():
        ims = []
        for i, f in enumerate(fs, 6):
            im = f(); im.save(OUT / f'{k}_v{i}.jpg', quality=93); ims.append(im)
        tw, th = 400, 225
        S = Image.new('RGB', (3 * (tw + 10) + 10, 2 * (th + 10) + 10), (245, 245, 245))
        for i, im in enumerate(ims):
            S.paste(im.resize((tw, th), Image.LANCZOS), (10 + (i % 3) * (tw + 10), 10 + (i // 3) * (th + 10)))
        S.save(OUT / f'feed_{k}.jpg', quality=90)
    print('ok')
