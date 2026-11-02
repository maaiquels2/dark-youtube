# Capa do ep02 no padrão do ep01: foto à esquerda com degradê, texto Anton à direita. Rodar da raiz do projeto.
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1280, 720
bg = Image.new('RGB', (W, H))
px = bg.load()
for y in range(H):
    for x in range(W):
        c = max(0.0, 1 - math.hypot((x - 820) / 700, (y - 360) / 500))
        px[x, y] = tuple(int(a + (b - a) * c) for a, b in zip((17, 18, 20), (27, 29, 32)))

im = Image.open('scamlaw/ep02_zelle/assets/img/thumb_send.jpg').convert('RGB')
im = im.resize((620, int(620 * im.height / im.width)))
top = (im.height - H) // 2 + 120
im = im.crop((0, top, 620, top + H)).filter(ImageFilter.GaussianBlur(6))  # app gerado tem texto/numero falso: desfocar
mask = Image.new('L', (620, H), 255)
md = ImageDraw.Draw(mask)
for x in range(380, 620):
    md.line([(x, 0), (x, H)], fill=int(255 * (1 - (x - 380) / 240)))
bg.paste(im, (0, 0), mask)

d = ImageDraw.Draw(bg)
anton = ImageFont.truetype('fonts/Anton-Regular.ttf', 118)
label = ImageFont.truetype('fonts/Inter-VF.ttf', 17)
try:
    label.set_variation_by_axes([600])
except Exception:
    pass
d.text((40, 36), 'I L L U S T R A T I O N', font=label, fill=(168, 162, 154))
d.text((470, 150), 'YOU PRESSED', font=anton, fill=(236, 232, 225))
d.text((470, 290), 'SEND.', font=anton, fill=(236, 232, 225))
d.text((470, 450), 'NO REFUND.', font=anton, fill=(208, 64, 47))
bg.save('scamlaw/ep02_zelle/kit/thumb_ep02.jpg', quality=92)
