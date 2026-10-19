import subprocess, re, sys, shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
pid = open(sys.argv[1]+"_id.txt").read().strip(); o = Path("projects") / pid / "output"; out = Path("output_progress")/sys.argv[1]/"final"; out.mkdir(parents=True, exist_ok=True)
FF = shutil.which("ffmpeg") or r"C:\Users\Admin\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.1-full_build\bin\ffmpeg.EXE"
dur = float(subprocess.run([shutil.which("ffprobe"),"-v","error","-show_entries","format=duration","-of","csv=p=0",str(o/"final.mp4")],capture_output=True,text=True).stdout); N = 48; ims = []
for k in range(N):
    t = 4 + k * (dur - 8) / (N - 1); f = out / f"f{k:02d}.jpg"
    subprocess.run([FF, "-y", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", str(o / "final.mp4"), "-frames:v", "1", "-q:v", "3", str(f)]); ims.append((t, f))
fnt = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 18)
S = Image.new("RGB", (6 * 320, 8 * 200), (10, 10, 12)); d = ImageDraw.Draw(S)
for k, (t, f) in enumerate(ims):
    x, y = (k % 6) * 320, (k // 6) * 200; S.paste(Image.open(f).resize((320, 180)), (x, y)); d.text((x + 4, y + 181), f"{int(t//60)}:{int(t%60):02d}", font=fnt, fill=(230, 230, 230))
S.save(out / "final-contact-sheet.jpg", quality=85)
srt = (o / "final.srt").read_text(encoding="utf-8").strip().split("\n\n")
short = [b for b in srt if len(b.split("\n")) >= 3 and len(" ".join(b.split("\n")[2:]).split()) <= 2]
print("cues", len(srt), "<=2-word cues:", len(short)); [print(" ", b.replace("\n", " | ")) for b in short[:10]]
