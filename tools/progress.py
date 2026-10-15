import json, sys, subprocess, time
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, ".")
pid = open("fb_id.txt").read().strip(); pdir = Path("projects") / pid
d = json.loads((Path("projects") / f"{pid}.json").read_text(encoding="utf-8"))
tag = sys.argv[1]; out = Path("output_progress"); out.mkdir(exist_ok=True)
import shutil; FF = shutil.which("ffmpeg") or r"C:\Users\Admin\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.1-full_build\bin\ffmpeg.EXE"
fr = []
for i, s in enumerate(d["scenes"]):
    f = s.get("file")
    if not f or not (pdir / f).is_file(): continue
    p = pdir / f
    if p.suffix.lower() in (".mp4", ".mov", ".webm"):
        tmp = out / "_f.jpg"; subprocess.run([FF, "-y", "-loglevel", "error", "-ss", "1.5", "-i", str(p), "-frames:v", "1", str(tmp)])
        im = Image.open(tmp).convert("RGB")
    else: im = Image.open(p).convert("RGB")
    ov = pdir / "gfx" / f"ov-{i+1:02d}.png"
    if ov.is_file(): im = im.resize((1920, 1080)); im.paste(Image.open(ov), (0, 0), Image.open(ov))
    fr.append((i + 1, s.get("source", ""), s.get("mode", ""), im.resize((384, 216))))
cols = 6; rows = (len(fr) + cols - 1) // cols or 1
S = Image.new("RGB", (cols * 384, rows * 240), (10, 10, 12)); dr = ImageDraw.Draw(S)
try: fnt = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 16)
except Exception: fnt = None
for k, (n, src, mode, im) in enumerate(fr):
    x, y = (k % cols) * 384, (k // cols) * 240; S.paste(im, (x, y)); dr.text((x + 6, y + 218), f"#{n} {'GFX' if src=='gfx' else mode}", font=fnt, fill=(230, 230, 230))
S.save(out / f"progress-{tag}-sheet.jpg", quality=82)
grok = [s for s in d["scenes"] if s.get("source") != "gfx"]; ok = sum(1 for s in grok if s.get("status") == "pronto" and s.get("file"))
line = f"{time.strftime('%Y-%m-%d %H:%M')} BRT | stage: {sys.argv[2] if len(sys.argv)>2 else 'Grok media'} | Grok scenes {ok}/{len(grok)} ready | gfx scenes {len(d['scenes'])-len(grok)} | sheet progress-{tag}-sheet.jpg"
with open(out / "status.txt", "a", encoding="utf-8") as f: f.write(line + "\n")
print(line)

