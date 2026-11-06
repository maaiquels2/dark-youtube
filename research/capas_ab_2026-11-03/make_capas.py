# 5 capas de teste por video (Rule Changed ep01/ep02, Ledger Tricolor/Weil/Binance).
# Padroes de research/youtube_ab_2026-11-03/canais_vencedores.md + REGRAS_UNIVERSAIS §12.
# Rodar da raiz: python research/capas_ab_2026-11-03/make_capas.py
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageEnhance

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
W, H = 1280, 720
ANTON = str(ROOT / 'fonts/Anton-Regular.ttf')
INTER = str(ROOT / 'fonts/Inter-VF.ttf')

# paletas
L_BG = (11, 14, 20); L_RED = (214, 52, 44); L_TXT = (240, 236, 228); L_YEL = (240, 180, 60)
R_BG = (17, 18, 20); R_RED = (208, 64, 47); R_TXT = (236, 232, 225); R_PAPER = (236, 228, 208); R_SUB = (168, 162, 154)

TRI = ROOT / 'projects/tricolor-car-loan-20261027-210000'
WEI = ROOT / 'projects/weil-gotshal-wind-down-20261030-190000'
BIN = ROOT / 'projects/binance-hack-north-korea-20261102-150000'
EP1 = ROOT / 'scamlaw/ep01_robocalls'
EP2 = ROOT / 'scamlaw/ep02_zelle'


def font(path, size, weight=None):
    f = ImageFont.truetype(path, size)
    if weight:
        try:
            f.set_variation_by_axes([weight])
        except Exception:
            pass
    return f


def cover(path, w=W, h=H, cx=0.5, cy=0.5):
    im = Image.open(path).convert('RGB')
    s = max(w / im.width, h / im.height)
    im = im.resize((math.ceil(im.width * s), math.ceil(im.height * s)), Image.LANCZOS)
    x = int((im.width - w) * cx); y = int((im.height - h) * cy)
    return im.crop((x, y, x + w, y + h))


def darken(im, f):
    return ImageEnhance.Brightness(im).enhance(f)


def fade(im, side='left', start=0.35, end=0.75, color=(0, 0, 0)):
    """escurece um lado para o texto (side = lado do texto)"""
    ov = Image.new('RGB', im.size, color)
    m = Image.new('L', im.size, 0); d = ImageDraw.Draw(m)
    for x in range(im.width):
        t = x / im.width if side == 'right' else 1 - x / im.width
        a = 0 if t < start else (255 if t > end else int(255 * (t - start) / (end - start)))
        d.line([(x, 0), (x, im.height)], fill=a)
    return Image.composite(ov, im, m)


def fit(text, path, size, maxw):
    f = font(path, size)
    while f.getlength(text) > maxw and size > 20:
        size -= 4; f = font(path, size)
    return f


def txt(d, xy, text, size, fill, maxw=1200, path=ANTON, anchor='la', stroke=0):
    f = fit(text, path, size, maxw)
    d.text(xy, text, font=f, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=(0, 0, 0))
    return f


def boxed(d, xy, text, size, fg, bg, pad=(18, 6), maxw=1200):
    f = fit(text, ANTON, size, maxw)
    x, y = xy
    l, t, r, b = d.textbbox((x, y), text, font=f)
    d.rectangle([l - pad[0], t - pad[1], r + pad[0], b + pad[1]], fill=bg)
    d.text((x, y), text, font=f, fill=fg)
    return b + pad[1]


def label(d, xy, text, fill=R_SUB, size=17):
    d.text(xy, ' '.join(text), font=font(INTER, size, 600), fill=fill)


def ledger_brand(im):
    d = ImageDraw.Draw(im)
    f = font(ANTON, 22); t = 'THE CRACKED LEDGER'
    w = f.getlength(t)
    d.rectangle([W - w - 44, H - 52, W - 14, H - 14], fill=L_BG)
    d.text((W - w - 29, H - 49), t, font=f, fill=L_TXT)


def zigzag(d, pts, color=L_RED, width=26, head=58):
    d.line(pts, fill=color, width=width, joint='curve')
    (x0, y0), (x1, y1) = pts[-2], pts[-1]
    a = math.atan2(y1 - y0, x1 - x0)
    p = [(x1 + head * 0.6 * math.cos(a), y1 + head * 0.6 * math.sin(a)),
         (x1 + head * math.cos(a + 2.5), y1 + head * math.sin(a + 2.5)),
         (x1 + head * math.cos(a - 2.5), y1 + head * math.sin(a - 2.5))]
    d.polygon(p, fill=color)


def logo_card(path, w, bg=(242, 239, 233), pad=36, radius=22):
    lg = Image.open(path).convert('RGBA')
    bb = lg.getbbox()
    if bb:
        lg = lg.crop(bb)
    s = (w - 2 * pad) / lg.width
    lg = lg.resize((int(lg.width * s), int(lg.height * s)), Image.LANCZOS)
    card = Image.new('RGBA', (w, lg.height + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(card).rounded_rectangle([0, 0, card.width - 1, card.height - 1], radius, fill=bg + (255,))
    card.alpha_composite(lg, (pad, pad))
    return card


def paste_rot(im, layer, xy, angle=0):
    if angle:
        layer = layer.rotate(angle, expand=True, resample=Image.BICUBIC)
    base = im.convert('RGBA'); base.alpha_composite(layer, (int(xy[0]), int(xy[1])))
    return base.convert('RGB')


def stamp(text, size, color, angle=-12, border=8):
    f = font(ANTON, size)
    tw = int(f.getlength(text)); th = int(size * 1.25)
    lay = Image.new('RGBA', (tw + 60, th + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rectangle([border, border, lay.width - border, lay.height - border], outline=color + (255,), width=border)
    d.text((30, 14), text, font=f, fill=color + (255,))
    return lay.rotate(angle, expand=True, resample=Image.BICUBIC)


def photo_frame(path, w, h, cx=0.5, cy=0.4, border=10):
    p = cover(path, w, h, cx, cy)
    fr = Image.new('RGB', (w + 2 * border, h + 2 * border), (242, 239, 233)); fr.paste(p, (border, border))
    return fr


def save(im, name):
    (OUT / name).parent.mkdir(parents=True, exist_ok=True)
    im.save(OUT / name, quality=92)


# ---------------- LEDGER: TRICOLOR ("Your Car Loan Is Someone Else's Bond") ----------------
def tricolor():
    # 1 objeto + queda
    im = darken(cover(TRI / 'media/local-02.jpg', cy=0.6), 0.55); im = fade(im, 'left', 0.4, 0.8)
    d = ImageDraw.Draw(im)
    zigzag(d, [(700, 180), (820, 300), (900, 240), (1040, 440), (1120, 400), (1200, 600)])
    txt(d, (60, 150), 'SOLD', 190, L_TXT); txt(d, (60, 360), 'TWICE?', 190, L_RED)
    boxed(d, (66, 600), 'ALLEGED', 40, L_BG, L_YEL)
    ledger_brand(im); save(im, 'ledger_tricolor/v1_objeto_queda.jpg')

    # 2 logo + carimbo
    im = Image.new('RGB', (W, H), L_BG)
    im = paste_rot(im, logo_card(TRI / 'entities/tricolor-logo.png', 560, bg=(250, 248, 244)), (90, 200), 0)
    im = paste_rot(im, stamp('BANKRUPT', 120, L_RED, -14), (170, 250))
    d = ImageDraw.Draw(im)
    txt(d, (770, 200), 'WHO', 170, L_TXT); txt(d, (770, 390), 'PAYS?', 170, L_YEL)
    ledger_brand(im); save(im, 'ledger_tricolor/v2_logo_carimbo.jpg')

    # 3 numeros em 2 barras (alegacao do indiciamento)
    im = Image.new('RGB', (W, H), L_BG); d = ImageDraw.Draw(im)
    base = 620
    d.rectangle([120, base - 460, 400, base], fill=(70, 74, 82)); d.rectangle([480, base - 290, 760, base], fill=L_RED)
    txt(d, (260, base - 480), '$2.2B', 110, L_TXT, anchor='ms'); txt(d, (620, base - 310), '$1.4B', 110, L_TXT, anchor='ms')
    txt(d, (260, base + 50), 'PROMISED', 46, L_TXT, anchor='ms'); txt(d, (620, base + 50), 'THERE', 46, L_TXT, anchor='ms')
    txt(d, (840, 220), 'THE', 120, L_TXT); txt(d, (840, 350), 'GAP', 190, L_YEL)
    boxed(d, (846, 600), 'ALLEGED', 36, L_BG, L_YEL)
    ledger_brand(im); save(im, 'ledger_tricolor/v3_numero_barras.jpg')

    # 4 pessoa (foto real com credito)
    im = darken(cover(TRI / 'media/local-30.jpg'), 0.35); d = ImageDraw.Draw(im)
    fr = photo_frame(TRI / 'entities/daniel-chu-photo.jpg', 420, 520, 0.45, 0.25)
    im.paste(fr, (70, 90)); d = ImageDraw.Draw(im)
    txt(d, (580, 170), 'THE CEO', 150, L_TXT); txt(d, (580, 340), 'CHARGED.', 170, L_RED)
    txt(d, (586, 560), 'HE PLEADED NOT GUILTY', 40, L_YEL, path=ANTON)
    ledger_brand(im); save(im, 'ledger_tricolor/v4_pessoa.jpg')

    # 5 cadeia: carro -> bancos
    im = Image.new('RGB', (W, H), L_BG)
    car = cover(TRI / 'media/local-35.jpg', 470, 330, 0.5, 0.6); im.paste(car, (50, 300))
    y = 250
    for lg in ['fifth-third-logo.png', 'barclays-logo.png', 'jpmorgan-logo.png']:
        c = logo_card(TRI / 'entities' / lg, 330, pad=22); im = paste_rot(im, c, (880, y)); y += c.height + 22
    d = ImageDraw.Draw(im)
    zigzag(d, [(560, 470), (840, 470)], color=L_YEL, width=20, head=46)
    txt(d, (50, 60), 'YOUR LOAN.', 120, L_TXT); txt(d, (650, 60), 'THEIR BOND.', 120, L_YEL, maxw=600)
    ledger_brand(im); save(im, 'ledger_tricolor/v5_cadeia.jpg')


# ---------------- LEDGER: WEIL ("The $2 Billion Law Firm That Fell in 4 Weeks") ----------------
def weil():
    # 1 predio + queda
    im = darken(cover(WEI / 'entities/gm-building.jpg', cy=0.3), 0.6); im = fade(im, 'left', 0.35, 0.7, L_BG)
    d = ImageDraw.Draw(im)
    zigzag(d, [(820, 120), (900, 260), (980, 200), (1080, 430), (1150, 380), (1220, 620)])
    txt(d, (60, 170), 'NO DEBT.', 170, L_TXT); txt(d, (60, 370), 'STILL GONE.', 170, L_RED, maxw=700)
    ledger_brand(im); save(im, 'ledger_weil/v1_predio_queda.jpg')

    # 2 logo partido
    im = Image.new('RGB', (W, H), L_BG)
    card = logo_card(WEI / 'entities/weil-logo.png', 620, bg=(250, 248, 244))
    a = card.crop((0, 0, card.width // 2, card.height)); b = card.crop((card.width // 2, 0, card.width, card.height))
    im = paste_rot(im, a, (80, 250), 6); im = paste_rot(im, b, (420, 270), -9)
    d = ImageDraw.Draw(im)
    txt(d, (800, 230), 'GONE.', 230, L_RED)
    ledger_brand(im); save(im, 'ledger_weil/v2_logo_partido.jpg')

    # 3 numero
    im = darken(cover(WEI / 'media/local-12.jpg'), 0.35); d = ImageDraw.Draw(im)
    txt(d, (80, 120), '95 YEARS.', 200, L_TXT); txt(d, (80, 360), '4 WEEKS.', 200, L_RED)
    ledger_brand(im); save(im, 'ledger_weil/v3_numero.jpg')

    # 4 escritorio vazio (caixa de mudanca)
    im = darken(cover(WEI / 'media/local-51.jpg', cy=0.5), 0.75); im = fade(im, 'right', 0.45, 0.85, L_BG)
    d = ImageDraw.Draw(im)
    txt(d, (700, 180), 'THE PARTNERS', 110, L_TXT, maxw=540); txt(d, (700, 330), 'LEFT.', 200, L_YEL)
    ledger_brand(im); save(im, 'ledger_weil/v4_escritorio.jpg')

    # 5 clientes famosos -> ela mesma
    im = Image.new('RGB', (W, H), L_BG)
    x = 60
    for lg in ['lehman-logo.png', 'enron-logo.png', 'gm-logo.png']:
        c = logo_card(WEI / 'entities' / lg, 200, pad=22)
        c = Image.merge('RGBA', (*ImageOps.grayscale(c.convert('RGB')).convert('RGB').split(), c.split()[3]))
        if c.height > 200: c = c.resize((int(c.width * 200 / c.height), 200))
        im = paste_rot(im, c, (x, 300 - c.height // 2)); x += 230
    im = paste_rot(im, logo_card(WEI / 'entities/weil-logo.png', 360, bg=(250, 248, 244)), (90, 470))
    d = ImageDraw.Draw(im)
    txt(d, (790, 200), 'THEN', 150, L_TXT); txt(d, (790, 370), 'ITSELF.', 190, L_RED, maxw=450)
    ledger_brand(im); save(im, 'ledger_weil/v5_clientes.jpg')


# ---------------- LEDGER: BINANCE ("The $6.3 BILLION Heist the FBI Pins on North Korea") ----------------
def binance():
    # 1 logo + queda
    im = darken(cover(BIN / 'media/local-04.jpg'), 0.45); d = ImageDraw.Draw(im)
    im = paste_rot(im, logo_card(BIN / 'entities/binance-logo.png', 520, bg=(20, 20, 22)), (60, 80))
    d = ImageDraw.Draw(im)
    zigzag(d, [(700, 160), (820, 300), (900, 240), (1040, 470), (1110, 420), (1200, 640)])
    txt(d, (60, 300), '20 MINUTES.', 210, L_TXT, maxw=640); boxed(d, (66, 560), 'THEN IT WAS GONE', 60, L_TXT, L_RED, maxw=600)
    ledger_brand(im); save(im, 'ledger_binance/v1_logo_queda.jpg')

    # 2 FBI x Binance
    im = Image.new('RGB', (W, H), L_BG)
    seal = Image.open(BIN / 'entities/fbi-seal.png').convert('RGBA'); seal.thumbnail((400, 400))
    im = paste_rot(im, seal, (70, 70))
    d = ImageDraw.Draw(im)
    txt(d, (520, 110), 'THE FBI', 130, L_TXT); txt(d, (520, 260), 'POINTS AT', 130, L_TXT)
    txt(d, (520, 410), 'NORTH KOREA', 150, L_RED, maxw=720)
    ledger_brand(im); save(im, 'ledger_binance/v2_fbi.jpg')

    # 3 numero
    im = darken(cover(BIN / 'media/local-30.jpg'), 0.4); d = ImageDraw.Draw(im)
    txt(d, (70, 90), '$6.3B', 330, L_TXT); boxed(d, (80, 480), 'GONE IN 20 MINUTES', 90, L_TXT, L_RED, maxw=900)
    ledger_brand(im); save(im, 'ledger_binance/v3_numero.jpg')

    # 4 sala de servidores + pergunta
    im = darken(cover(BIN / 'media/local-11.jpg'), 0.5); im = fade(im, 'left', 0.3, 0.7, L_BG)
    d = ImageDraw.Draw(im)
    txt(d, (60, 160), 'WHO PAYS', 190, L_TXT); txt(d, (60, 380), 'THE BILL?', 190, L_YEL)
    ledger_brand(im); save(im, 'ledger_binance/v4_quem_paga.jpg')

    # 5 congelado x perdido
    im = Image.new('RGB', (W, H), L_BG); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W // 2, H], fill=(20, 40, 58))
    im = paste_rot(im, logo_card(BIN / 'entities/tether-logo.png', 420, bg=(240, 244, 248), pad=24), (110, 130))
    im = paste_rot(im, logo_card(BIN / 'entities/circle-logo.png', 420, bg=(240, 244, 248), pad=24), (110, 290))
    d = ImageDraw.Draw(im)
    txt(d, (W // 4, 640), 'FROZEN', 140, (150, 210, 245), anchor='ms')
    f = font(ANTON, 200)
    d.text((W * 3 // 4, 330), 'BTC + ETH', font=fit('BTC + ETH', ANTON, 120, 520), fill=(120, 120, 128), anchor='mm')
    txt(d, (W * 3 // 4, 640), 'GONE', 140, L_RED, anchor='ms')
    ledger_brand(im); save(im, 'ledger_binance/v5_congelado_perdido.jpg')


# ---------------- RULE CHANGED ep01 ("The Fake Local Number That Changed the Law") — sem numeros ----------------
def caller_id(w=430, h=250, name='Incoming call', sub='Your area'):
    c = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 28, fill=(28, 30, 34, 235))
    d.text((32, 30), name, font=font(INTER, 30, 500), fill=(200, 200, 200, 255))
    d.text((32, 80), '(•••) •••-••••', font=font(INTER, 54, 700), fill=(255, 255, 255, 255))
    d.text((32, 168), sub, font=font(INTER, 30, 500), fill=(130, 200, 140, 255))
    return c


def ep01():
    # 1 identificador de chamada falso
    im = darken(cover(EP1 / 'assets/img/phone_kitchen.jpg', cy=0.55), 0.55).filter(ImageFilter.GaussianBlur(7)); im = fade(im, 'right', 0.4, 0.75, R_BG)
    im = paste_rot(im, caller_id(), (90, 230), 0)
    im = paste_rot(im, stamp('FAKE', 110, R_RED, -12), (300, 300))
    d = ImageDraw.Draw(im); label(d, (40, 36), 'ILLUSTRATION')
    txt(d, (700, 200), 'NOT YOUR', 150, R_TXT, maxw=540); txt(d, (700, 370), 'NEIGHBOR.', 150, R_RED, maxw=540)
    save(im, 'rulechanged_ep01/v1_identificador.jpg')

    # 2 so a pergunta
    im = darken(cover(EP1 / 'assets/img/phone_screen.jpg', cy=0.45), 0.7).filter(ImageFilter.GaussianBlur(9)); im = fade(im, 'right', 0.35, 0.65, R_BG)
    d = ImageDraw.Draw(im); label(d, (40, 36), 'ILLUSTRATION')
    txt(d, (640, 220), 'ANSWER', 200, R_TXT, maxw=600); txt(d, (640, 430), 'IT?', 200, R_RED)
    save(im, 'rulechanged_ep01/v2_atender.jpg')

    # 3 papel: a lei
    im = Image.new('RGB', (W, H), R_BG)
    paper = Image.new('RGBA', (560, 620), R_PAPER + (255,)); pd = ImageDraw.Draw(paper)
    pd.text((40, 50), 'PUBLIC LAW', font=font(INTER, 28, 700), fill=(60, 55, 50))
    pd.text((40, 110), 'TRACED', font=font(ANTON, 130), fill=(30, 28, 26))
    pd.text((40, 260), 'ACT', font=font(ANTON, 130), fill=(30, 28, 26))
    for i in range(6):
        pd.line([(40, 440 + i * 28), (520 - (i % 3) * 60, 440 + i * 28)], fill=(150, 142, 128), width=6)
    pd.line([(40, 410), (330, 410)], fill=R_RED + (255,), width=10)
    im = paste_rot(im, paper, (80, 60), 4)
    d = ImageDraw.Draw(im)
    txt(d, (700, 200), 'ONE TRICK.', 140, R_TXT, maxw=540); txt(d, (700, 360), 'NEW LAW.', 150, R_RED, maxw=540)
    save(im, 'rulechanged_ep01/v3_papel_lei.jpg')

    # 4 central de chamadas
    im = darken(cover(EP1 / 'assets/img/callcenter.jpg', cy=0.5), 0.6); im = fade(im, 'left', 0.3, 0.65, R_BG)
    d = ImageDraw.Draw(im); label(d, (40, 36), 'ILLUSTRATION')
    txt(d, (60, 190), 'THEY FAKED', 150, R_TXT, maxw=620); txt(d, (60, 370), 'YOUR AREA.', 150, R_RED, maxw=620)
    save(im, 'rulechanged_ep01/v4_central.jpg')

    # 5 FCC + telefone
    im = darken(cover(EP1 / 'assets/img/hangup.jpg', cy=0.6), 0.5); im = fade(im, 'right', 0.4, 0.7, R_BG)
    seal = Image.open(EP1 / 'entities/fcc_seal.png').convert('RGBA'); seal.thumbnail((300, 300))
    im = paste_rot(im, seal, (90, 330))
    d = ImageDraw.Draw(im); label(d, (40, 36), 'ILLUSTRATION')
    txt(d, (690, 200), 'CALLER ID', 150, R_TXT, maxw=560); txt(d, (690, 370), 'LIED.', 190, R_RED)
    save(im, 'rulechanged_ep01/v5_fcc.jpg')


# ---------------- RULE CHANGED ep02 ("Why Your Bank Says 'You Sent It Yourself'") — sem numeros ----------------
def ep02():
    # 1 ligacao "do banco"
    im = darken(cover(EP2 / 'assets/img/phone_ear.jpg', cy=0.4), 0.7); im = fade(im, 'right', 0.4, 0.75, R_BG)
    d = ImageDraw.Draw(im); label(d, (40, 36), 'ILLUSTRATION')
    txt(d, (690, 180), "IT WASN'T", 150, R_TXT, maxw=560); txt(d, (690, 350), 'THE BANK.', 150, R_RED, maxw=560)
    save(im, 'rulechanged_ep02/v1_ligacao.jpg')

    # 2 logo Zelle + carimbo
    im = Image.new('RGB', (W, H), R_BG)
    zl = Image.open(EP2 / 'assets/img/l_zelle.jpg').convert('RGB')
    zl = zl.crop((int(zl.width * .1), int(zl.height * .2), int(zl.width * .9), int(zl.height * .8)))  # cartão creme com o logo
    zl.thumbnail((440, 520))
    im = paste_rot(im, zl.convert('RGBA'), (110, 110))
    im = paste_rot(im, stamp('NO REFUND', 90, R_RED, -14), (90, 300))
    d = ImageDraw.Draw(im)
    txt(d, (680, 200), 'YOU WERE', 140, R_TXT, maxw=560); txt(d, (680, 360), 'TRICKED.', 170, R_RED, maxw=560)
    save(im, 'rulechanged_ep02/v2_zelle_carimbo.jpg')

    # 3 carta de contestacao negada (papel)
    im = Image.new('RGB', (W, H), R_BG)
    paper = Image.new('RGBA', (540, 640), R_PAPER + (255,)); pd = ImageDraw.Draw(paper)
    pd.text((40, 50), 'FRAUD CLAIM', font=font(INTER, 34, 700), fill=(40, 36, 32))
    for i in range(9):
        pd.line([(40, 130 + i * 34), (500 - (i % 4) * 50, 130 + i * 34)], fill=(150, 142, 128), width=6)
    paper.alpha_composite(stamp('DENIED', 120, R_RED, -10), (60, 330))
    im = paste_rot(im, paper, (90, 50), -3)
    d = ImageDraw.Draw(im)
    txt(d, (700, 190), 'YOUR BANK', 140, R_TXT, maxw=540); txt(d, (700, 350), 'SAYS NO.', 160, R_RED, maxw=540)
    save(im, 'rulechanged_ep02/v3_carta_negada.jpg')

    # 4 dedo no enviar (atual simplificada, 2 palavras)
    im = darken(cover(EP2 / 'assets/img/thumb_send.jpg', cy=0.55), 0.8).filter(ImageFilter.GaussianBlur(5))
    im = fade(im, 'right', 0.4, 0.7, R_BG)
    d = ImageDraw.Draw(im); label(d, (40, 36), 'ILLUSTRATION')
    txt(d, (700, 230), 'NOT', 200, R_TXT); txt(d, (700, 440), 'COVERED.', 160, R_RED, maxw=540)
    save(im, 'rulechanged_ep02/v4_nao_coberto.jpg')

    # 5 EUA x Reino Unido
    im = Image.new('RGB', (W, H), R_BG)
    l = cover(EP2 / 'assets/img/bank_branch.jpg', W // 2, H, 0.5, 0.5); r = cover(EP2 / 'assets/img/london_street.jpg', W // 2, H, 0.5, 0.5)
    im.paste(darken(l, 0.45), (0, 0)); im.paste(darken(r, 0.45), (W // 2, 0))
    d = ImageDraw.Draw(im); d.rectangle([W // 2 - 4, 0, W // 2 + 4, H], fill=R_TXT)
    label(d, (40, 36), 'ILLUSTRATION')
    txt(d, (W // 4, 300), 'U.S.', 150, R_TXT, anchor='ms'); txt(d, (W // 4, 520), 'YOU PAY.', 130, R_RED, anchor='ms', maxw=560)
    txt(d, (W * 3 // 4, 300), 'U.K.', 150, R_TXT, anchor='ms'); txt(d, (W * 3 // 4, 520), 'BANK PAYS.', 130, (120, 200, 140), anchor='ms', maxw=560)
    save(im, 'rulechanged_ep02/v5_eua_uk.jpg')


def sheets():
    """folha por video no tamanho do feed (~360 px de largura) + atual para comparar"""
    atuais = {'ledger_tricolor': TRI / 'output/capa-1.jpg', 'ledger_weil': WEI / 'output/capa-1.jpg',
              'ledger_binance': BIN / 'output/capa-1.jpg', 'rulechanged_ep01': EP1 / 'kit/thumb_ep01.jpg',
              'rulechanged_ep02': EP2 / 'kit/thumb_ep02.jpg'}
    for k, atual in atuais.items():
        fs = [atual] + sorted((OUT / k).glob('v*.jpg'))
        tw, th = 360, 202
        S = Image.new('RGB', (3 * (tw + 12) + 12, 2 * (th + 40) + 12), (245, 245, 245)); d = ImageDraw.Draw(S)
        for i, f in enumerate(fs):
            x = 12 + (i % 3) * (tw + 12); y = 12 + (i // 3) * (th + 40)
            S.paste(Image.open(f).convert('RGB').resize((tw, th), Image.LANCZOS), (x, y))
            d.text((x, y + th + 6), 'ATUAL' if i == 0 else f.stem, font=font(INTER, 18, 600), fill=(20, 20, 20))
        S.save(OUT / f'folha_{k}.jpg', quality=90)


if __name__ == '__main__':
    tricolor(); weil(); binance(); ep01(); ep02(); sheets()
    print('ok')
