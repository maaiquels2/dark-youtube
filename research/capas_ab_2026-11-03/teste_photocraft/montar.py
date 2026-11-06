# Capas de teste: objeto gerado no ComfyUI (JuggernautXL), recortado e estilizado no PhotoCraft 0.19, texto pelo make_capas.
import sys
from pathlib import Path
from PIL import Image, ImageDraw
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import make_capas as M

def obj(name, h):
    im = Image.open(HERE / f'styled_{name}.png').convert('RGBA'); im = im.crop(im.getbbox())
    return im.resize((int(im.width * h / im.height), h), Image.LANCZOS)

def bg():
    im = Image.new('RGB', (M.W, M.H), M.L_BG); d = ImageDraw.Draw(im)
    for r in range(520, 0, -8):  # luz suave atrás do objeto
        c = int(14 + 22 * (1 - r / 520)); d.ellipse([930 - r, 380 - r, 930 + r, 380 + r], fill=(c, c + 2, c + 8))
    return im

# Weil
im = bg(); ch = obj('weil_chair_a', 600); im = M.paste_rot(im, ch, (1240 - ch.width - 60, 70))
d = ImageDraw.Draw(im)
M.zigzag(d, [(560, 140), (650, 250), (720, 200), (820, 420)], width=22, head=50)
M.txt(d, (60, 170), 'NO DEBT.', 170, M.L_TXT, maxw=620); M.txt(d, (60, 370), 'STILL GONE.', 170, M.L_RED, maxw=620)
M.ledger_brand(im); im.save(HERE / 'capa_weil_photocraft.jpg', quality=92)

# Binance
im = bg(); v = obj('bin_vault_a', 560); im = M.paste_rot(im, v, (1240 - v.width - 50, 100))
im = M.paste_rot(im, M.logo_card(M.BIN / 'entities/binance-logo.png', 300, bg=(20, 20, 22), pad=20), (60, 50))
d = ImageDraw.Draw(im)
M.txt(d, (60, 190), '$6.3B', 280, M.L_TXT, maxw=620)
M.boxed(d, (70, 540), 'GONE IN 20 MINUTES', 74, M.L_TXT, M.L_RED, maxw=580)
M.ledger_brand(im); im.save(HERE / 'capa_binance_photocraft.jpg', quality=92)

# comparação: atual | script | photocraft, no tamanho do feed
rows = [(M.WEI / 'output/capa-1.jpg', HERE.parent / 'ledger_weil/v1_predio_queda.jpg', HERE / 'capa_weil_photocraft.jpg'),
        (M.BIN / 'output/capa-1.jpg', HERE.parent / 'ledger_binance/v3_numero.jpg', HERE / 'capa_binance_photocraft.jpg')]
tw, th = 400, 225; S = Image.new('RGB', (3 * tw + 40, 2 * (th + 34) + 10), (245, 245, 245)); d = ImageDraw.Draw(S)
for r, fs in enumerate(rows):
    for c, f in enumerate(fs):
        x, y = 10 + c * (tw + 10), 10 + r * (th + 34)
        S.paste(Image.open(f).convert('RGB').resize((tw, th), Image.LANCZOS), (x, y))
        d.text((x, y + th + 5), ['ATUAL', 'SÓ SCRIPT', 'COMFYUI + PHOTOCRAFT'][c], font=M.font(M.INTER, 17, 600), fill=(20, 20, 20))
S.save(HERE / 'comparacao.jpg', quality=90)
print('ok')
