"""Logo/brand artifact check for Grok media (Validacao stage).
Samples frames from every Grok-generated scene, sends labeled grids to the OpenAI vision model
(analysis only, no generation) and flags scenes with visible logos, emblems, brand marks or seals.
Results are cached per file (path + mtime) in project["logo_check"]."""
import base64, io, json, shutil, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import app

TILE = (640, 360)
def _ff(): return shutil.which("ffmpeg") or "ffmpeg"
def _fp(): return shutil.which("ffprobe") or "ffprobe"

def _frames(src):
    if src.suffix.lower() not in (".mp4", ".mov", ".webm"):
        return [Image.open(src).convert("RGB")]
    try: dur = float(subprocess.run([_fp(), "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(src)], capture_output=True, text=True).stdout or 6)
    except Exception: dur = 6
    out = []
    with tempfile.TemporaryDirectory() as td:
        for k, fr in enumerate((0.08, 0.35, 0.65, 0.93)):
            o = Path(td) / f"{k}.jpg"
            subprocess.run([_ff(), "-y", "-v", "error", "-ss", f"{dur*fr:.2f}", "-i", str(src), "-frames:v", "1", "-vf", "scale=640:-2", str(o)])
            if o.is_file(): out.append(Image.open(o).convert("RGB"))
    return out

def _grid(tiles):
    cols = 3; rows = (len(tiles) + cols - 1) // cols
    g = Image.new("RGB", (cols * TILE[0], rows * TILE[1]), "black"); d = ImageDraw.Draw(g)
    try: fn = ImageFont.truetype("arial.ttf", 30)
    except Exception: fn = ImageFont.load_default()
    for j, (lab, im) in enumerate(tiles):
        x, y = (j % cols) * TILE[0], (j // cols) * TILE[1]; g.paste(im.resize(TILE), (x, y))
        d.rectangle([x, y, x + 130, y + 40], fill="black"); d.text((x + 6, y + 4), lab, fill="yellow", font=fn)
    b = io.BytesIO(); g.save(b, "JPEG", quality=82); return base64.b64encode(b.getvalue()).decode()

PROMPT = ("You are a broadcast compliance checker. Each tile is labeled (e.g. S50-2). Flag ONLY tiles that show a recognizable "
          "brand logo, corporate emblem, trademark symbol, official seal/crest, national flag, religious symbol (cross etc.), or a readable brand name (e.g. a red 'N', swoosh, "
          "apple logo, bank logo, flag-like emblem on a wall). Ignore generic picture frames, blank papers and unreadable blur. "
          "Reply in JSON: {\"flagged\":[{\"tile\":\"S50-2\",\"what\":\"short description\"}]}")

def _ask(b64):
    key = app.api_key()
    d = app._post("https://api.openai.com/v1/responses", {"model": app.MODEL, "max_output_tokens": 1500,
        "text": {"format": {"type": "json_object"}},
        "input": [{"role": "user", "content": [{"type": "input_text", "text": PROMPT},
                                               {"type": "input_image", "image_url": f"data:image/jpeg;base64,{b64}"}]}]}, key)
    return app._parse_json(app._responses_text(d)).get("flagged") or []

def check(d, pdir, force=False):
    pdir = Path(pdir); cache = d.get("logo_check") or {}; files = cache.get("files") or {}
    todo = []
    for i, s in enumerate(d.get("scenes") or []):
        f = s.get("file") or ""
        if not f.startswith("media/") or not (pdir / f).is_file(): continue
        sig = f"{f}:{int((pdir / f).stat().st_mtime)}"
        if not force and files.get(str(i + 1), {}).get("sig") == sig: continue
        todo.append((i + 1, f, sig))
    tiles, owners = [], {}
    for n, f, sig in todo:
        for k, im in enumerate(_frames(pdir / f)):
            lab = f"S{n}-{k}"; tiles.append((lab, im)); owners[lab] = n
        files[str(n)] = {"sig": sig, "flags": []}
    for c in range(0, len(tiles), 9):
        for fl in _ask(_grid(tiles[c:c + 9])):
            n = owners.get(str(fl.get("tile", "")).strip())
            if n: files[str(n)]["flags"].append(fl.get("what") or "logo")
    overrides = set(cache.get("ok_override") or [])
    flagged = [{"scene": int(n), "what": v["flags"]} for n, v in files.items() if v["flags"] and int(n) not in overrides]
    d["logo_check"] = {"files": files, "ok_override": sorted(overrides), "flagged": sorted(flagged, key=lambda x: x["scene"]), "checked": len(files)}
    return d["logo_check"]
