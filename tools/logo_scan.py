import json, subprocess, shutil, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
FF = shutil.which("ffmpeg"); FP = shutil.which("ffprobe")
pid = sys.argv[1] if len(sys.argv) > 1 else open("fb_id.txt").read().strip()
pdir = Path("projects")/pid; d = json.load(open(f"projects/{pid}.json", encoding="utf-8"))
out = Path("output_yt/logo_scan"); shutil.rmtree(out, ignore_errors=True); out.mkdir(parents=True)
tiles = []
for i, s in enumerate(d["scenes"], 1):
    f = s.get("file") or ""
    if not f.startswith("media/"): continue
    src = pdir/f; ims = []
    if f.endswith(".mp4"):
        dur = float(subprocess.run([FP,"-v","error","-show_entries","format=duration","-of","csv=p=0",str(src)],capture_output=True,text=True).stdout or 6)
        for k, fr in enumerate((0.1, 0.5, 0.9)):
            o = out/f"{i:02d}-{k}.jpg"; subprocess.run([FF,"-y","-v","error","-ss",str(dur*fr),"-i",str(src),"-frames:v","1","-vf","scale=480:-2",str(o)]); ims.append(o)
    else:
        o = out/f"{i:02d}-0.jpg"; Image.open(src).convert("RGB").resize((480,270)).save(o); ims.append(o)
    for o in ims:
        if o.exists(): tiles.append((f"S{i} {o.stem[-1]}", o))
fn = ImageFont.truetype("arial.ttf", 22)
per = 20
for n in range(0, len(tiles), per):
    sheet = Image.new("RGB", (4*480, 5*270), "black"); dr = ImageDraw.Draw(sheet)
    for j, (lab, o) in enumerate(tiles[n:n+per]):
        im = Image.open(o).resize((480,270)); x, y = (j%4)*480, (j//4)*270; sheet.paste(im, (x,y)); dr.rectangle([x,y,x+90,y+28], fill="black"); dr.text((x+4,y+2), lab, fill="yellow", font=fn)
    sheet.save(out/f"sheet-{n//per:02d}.jpg", quality=85)
print(len(tiles))
