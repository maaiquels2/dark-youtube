import sys, json, subprocess, shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, "."); import pipeline
FF = shutil.which("ffmpeg"); fn = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 18)
TITLES = {"svb": "Silicon Valley Bank: How a $209 Billion Bank Died in 48 Hours", "lehman": "Lehman Brothers: The Weekend Wall Street Broke ($639 Billion Bankruptcy)"}
for k in ("svb", "lehman"):
    pid = open(f"{k}_id.txt").read().strip(); P = Path("projects") / pid; d = pipeline._load(pid); dos = d["dossier"]
    out = Path("output_progress") / k; out.mkdir(parents=True, exist_ok=True)
    L = [f"# {d['title']} - dossier summary", "", f"**Proposed YouTube title:** {TITLES[k]}", "", f"Hook: {d.get('hook')}", "", f"Scenes: {len(d['scenes'])} (video {sum(1 for s in d['scenes'] if s.get('mode')=='video')})", ""]
    for c in dos["chapters"]:
        L.append(f"## {c.get('title') or c.get('name')}")
        for f in c.get("facts") or []: L.append(f"- {f.get('fact') or f.get('text')} ([source]({f.get('url')}))")
        L.append("")
    for grp in ("people", "companies", "agencies"):
        L.append(f"## {grp.title()}"); L += [f"- {x.get('name')}: {x.get('role') or x.get('status') or ''}" for x in dos.get(grp) or []]; L.append("")
    L.append("## Visual assets (real, licensed)")
    for e in d.get("entities") or []:
        a = [kk for kk in ("photo", "logo", "seal", "hq_photo") if e.get(kk)]
        L.append(f"- {e['name']}: {', '.join(a) if a else 'name card'}" + (f" — {'; '.join(v for kk, v in (e.get('credits') or {}).items() if not kk.endswith('_source'))}" if a else ""))
    (out / "dossier-summary.md").write_text("\n".join(L), encoding="utf-8")
    tiles = []
    for e in d.get("entities") or []:
        for kk in ("photo", "logo", "seal", "hq_photo"):
            if e.get(kk) and (P / e[kk]).is_file(): tiles.append((f"{e['name'][:26]} ({kk})", P / e[kk]))
    for i, s in enumerate(d["scenes"]):
        f = s.get("file") or ""
        if f.startswith("media/") and (P / f).is_file():
            if f.endswith(".mp4"):
                o = out / f"s{i+1}.jpg"; subprocess.run([FF, "-y", "-v", "error", "-ss", "2", "-i", str(P / f), "-frames:v", "1", "-vf", "scale=480:-2", str(o)]); tiles.append((f"S{i+1} video", o))
            else: tiles.append((f"S{i+1} image", P / f))
    tiles = tiles[:48]; cols = 6; rows = (len(tiles) + cols - 1) // cols
    S = Image.new("RGB", (cols * 320, rows * 205), (12, 12, 14)); dr = ImageDraw.Draw(S)
    for j, (lab, f) in enumerate(tiles):
        try:
            im = Image.open(f).convert("RGBA"); bg = Image.new("RGBA", im.size, (235, 235, 235, 255) if "logo" in lab or "seal" in lab else (0, 0, 0, 255)); im = Image.alpha_composite(bg, im).convert("RGB")
            im.thumbnail((320, 180)); x, y = (j % cols) * 320, (j // cols) * 205; S.paste(im, (x + (320 - im.width) // 2, y)); dr.text((x + 4, y + 182), lab, font=fn, fill=(230, 230, 230))
        except Exception as ex: print(ex)
    S.save(out / "sketch-sheet.jpg", quality=85); print(k, len(tiles), "tiles")
