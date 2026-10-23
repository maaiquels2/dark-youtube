"""Grandpa Walt - local period scenes via ComfyUI (no Grok).
Usage (from Dark YouTube root):
  python tools/walt_local.py projects/_characters/grandpa-walt/pilot_ep04_teaser.md [--seeds 3] [--scenes 03,08,09] [--episode NAME]
Reads the scene table (| # | Time | Shot | Visual | Narration | ...), generates only rows whose Shot is "Period".
Output: projects/grandpa-walt/<episode>/scenes/sceneNN_seedK.png + sceneNN_sheet.jpg. Skips existing files.
Pick a seed per scene in <episode>/scenes/picks.json ({"03": 2}); default is seed 1."""
import argparse, json, os, re, subprocess, sys, time, urllib.request
from pathlib import Path
from PIL import Image, ImageDraw
ROOT = Path(__file__).resolve().parent.parent
COMFY = ROOT / "tools" / "ComfyUI"
API = "http://127.0.0.1:8188"
CKPT = "juggernautXL_v9.safetensors"
STYLE = "authentic 1944 World War II documentary photograph, black and white, film grain, slight blur, period-accurate, realistic, archival press photo, "
NEG = "color, modern, plastic, text, watermark, logo, cartoon, illustration, painting, 3d render, cgi, close-up face, portrait, deformed, extra limbs, glossy, smooth skin"
# keyword -> (positive boost, negative add)
BOOST = [
 (r"\bnight\b|\bdark\b|before dawn", "(night:1.4), (dark low-key lighting:1.3)", "daylight, sunny, bright sky"),
 (r"\brain\b", "(heavy rain:1.4), (wet reflective surfaces:1.2), rain streaks", "dry, clear weather"),
 (r"silhouette|seen from behind|face not visible|turned away", "(silhouette:1.5), (backlit:1.3), (seen from behind:1.4), (face hidden:1.3)", "face, frontal view, looking at camera, eyes"),
 (r"weather map|isobar", "(meteorological weather chart:1.5), (hand-drawn curved isobar lines:1.4), pressure fronts drawn in pencil", "atlas, geographic map, colored countries, coastline map"),
 (r"dusk|first light|dawn", "(dim dawn light:1.2)", ""),
]
def up():
    try: urllib.request.urlopen(API + "/system_stats", timeout=3); return True
    except Exception: return False
def ensure_comfy():
    if up(): return
    print("starting ComfyUI...", flush=True)
    subprocess.Popen([str(COMFY / "python_embeded" / "python.exe"), "-s", "ComfyUI\\main.py", "--windows-standalone-build", "--listen", "127.0.0.1", "--port", "8188"],
        cwd=str(COMFY), stdout=open(COMFY / "comfy_out.log", "ab"), stderr=open(COMFY / "comfy_err.log", "ab"), creationflags=0x08000000)
    for _ in range(180):
        time.sleep(2)
        if up(): return
    sys.exit("ComfyUI did not start; see tools/ComfyUI/comfy_err.log")
def parse(md):
    out = {}
    for line in Path(md).read_text(encoding="utf-8").splitlines():
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) >= 4 and re.fullmatch(r"\d+", c[0]) and c[2].lower().startswith("period"):
            out[f"{int(c[0]):02d}"] = c[3]
    return out
def build(desc):
    pos, neg = STYLE + desc, NEG
    for rx, p, n in BOOST:
        if re.search(rx, desc, re.I):
            pos += ", " + p
            if n: neg += ", " + n
    return pos, neg
def gen(pos, neg, seed, prefix):
    wf = {"1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": CKPT}},
          "2": {"class_type": "CLIPTextEncode", "inputs": {"text": pos, "clip": ["1", 1]}},
          "3": {"class_type": "CLIPTextEncode", "inputs": {"text": neg, "clip": ["1", 1]}},
          "4": {"class_type": "EmptyLatentImage", "inputs": {"width": 1344, "height": 768, "batch_size": 1}},
          "5": {"class_type": "KSampler", "inputs": {"model": ["1", 0], "positive": ["2", 0], "negative": ["3", 0], "latent_image": ["4", 0], "seed": seed, "steps": 30, "cfg": 5.0, "sampler_name": "dpmpp_2m", "scheduler": "karras", "denoise": 1.0}},
          "6": {"class_type": "VAEDecode", "inputs": {"samples": ["5", 0], "vae": ["1", 2]}},
          "7": {"class_type": "SaveImage", "inputs": {"images": ["6", 0], "filename_prefix": prefix}}}
    r = urllib.request.urlopen(urllib.request.Request(API + "/prompt", json.dumps({"prompt": wf}).encode(), {"Content-Type": "application/json"}))
    pid = json.load(r)["prompt_id"]
    while True:
        h = json.load(urllib.request.urlopen(f"{API}/history/{pid}"))
        if pid in h:
            if h[pid].get("status", {}).get("status_str") == "error": raise RuntimeError(str(h[pid]["status"])[:300])
            if h[pid].get("outputs"): break
        time.sleep(1)
    im = list(h[pid]["outputs"].values())[0]["images"][0]
    return urllib.request.urlopen(f"{API}/view?filename={im['filename']}&subfolder={im.get('subfolder','')}&type=output").read()
def sheet(files, dst):
    W, H = 640, 366
    s = Image.new("RGB", (W * len(files), H + 24), "white"); d = ImageDraw.Draw(s)
    for i, f in enumerate(files):
        s.paste(Image.open(f).convert("RGB").resize((W, H)), (i * W, 0)); d.text((i * W + 6, H + 6), f.name, fill="black")
    s.save(dst, quality=85)
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("md"); ap.add_argument("--seeds", type=int, default=3)
    ap.add_argument("--scenes", default=""); ap.add_argument("--episode", default="")
    a = ap.parse_args()
    ep = a.episode or Path(a.md).stem
    out = ROOT / "projects" / "grandpa-walt" / ep / "scenes"; out.mkdir(parents=True, exist_ok=True)
    sc = parse(a.md); want = {f"{int(x):02d}" for x in a.scenes.split(",") if x.strip()}
    if want: sc = {k: v for k, v in sc.items() if k in want}
    if not sc: sys.exit("no Period scenes found")
    ensure_comfy(); prompts = {}
    for k, desc in sc.items():
        pos, neg = build(desc); prompts[k] = {"pos": pos, "neg": neg}; files = []
        for s in range(1, a.seeds + 1):
            f = out / f"scene{k}_seed{s}.png"; files.append(f)
            if f.exists(): continue
            t = time.time(); f.write_bytes(gen(pos, neg, int(k) * 1000 + s, f"walt_{ep}_{k}_{s}"))
            print(f.name, f"{time.time()-t:.1f}s", flush=True)
        sheet(files, out / f"scene{k}_sheet.jpg")
    pj = out / "prompts.json"; old = json.loads(pj.read_text(encoding="utf-8")) if pj.exists() else {}
    old.update(prompts); pj.write_text(json.dumps(old, indent=1), encoding="utf-8")
    print("done:", out)
if __name__ == "__main__": main()
