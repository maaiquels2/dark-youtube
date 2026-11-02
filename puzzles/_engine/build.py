"""Generic episode builder: python build.py <episode_dir> [--voice] [--render]
Episode dir holds ep.json {title, keys, blocks[]} and scene.js (defines scene(t, b, u) -> stat text).
--voice  paid ElevenLabs call (Brian) with word timings; without it reuses assets/timing.json
--render hyperframes render to renders/<dirname>.mp4
"""
import base64, json, re, subprocess, sys, urllib.request
from pathlib import Path

ENGINE = Path(__file__).resolve().parent
ROOT = ENGINE.parents[1]
VOICE_ID, SPEED = "nPczCjzI2devNBz1zQrb", 1.08

def env_val(name):
    for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
        if line.startswith(name + "="):
            return line.split("=", 1)[1].strip().strip('"')
    sys.exit(f"{name} missing in .env")

def tts(text):
    body = {"text": text, "model_id": "eleven_multilingual_v2",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75, "style": 0.25,
                               "use_speaker_boost": True, "speed": SPEED}}
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/with-timestamps?output_format=mp3_44100_128",
        data=json.dumps(body).encode(),
        headers={"xi-api-key": env_val("ELEVEN_LABS_KEY"), "Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=180).read())

def main():
    ep = Path(sys.argv[1]).resolve()
    wide = "--wide" in sys.argv
    lead = float(sys.argv[sys.argv.index("--lead") + 1]) if "--lead" in sys.argv else 0.0
    chapter = sys.argv[sys.argv.index("--chapter") + 1] if "--chapter" in sys.argv else ""
    cfg = json.loads((ep / "ep.json").read_text(encoding="utf-8"))
    src = ep
    if wide:                                   # versao 16:9 numa pasta propria, reaproveitando voz e tempos
        ep = ROOT / "puzzles" / "_wide" / src.name; (ep / "assets").mkdir(parents=True, exist_ok=True)
        for f in ("voice.mp3", "timing.json"): (ep / "assets" / f).write_bytes((src / "assets" / f).read_bytes())
        (ep / "scene.js").write_bytes((src / "scene.js").read_bytes())
    blocks = cfg["blocks"]
    text = " ".join(blocks)
    assets = ep / "assets"; assets.mkdir(exist_ok=True)
    tj = assets / "timing.json"
    if "--voice" in sys.argv:
        r = tts(text)
        (assets / "voice.mp3").write_bytes(base64.b64decode(r["audio_base64"]))
        al = r["alignment"]
        if len(al["characters"]) != len(text):
            sys.exit(f"alignment length {len(al['characters'])} != text {len(text)}")
        words = [{"w": m.group(), "s": round(al["character_start_times_seconds"][m.start()], 3),
                  "e": round(al["character_end_times_seconds"][m.end() - 1], 3)} for m in re.finditer(r"\S+", text)]
        starts, off = [], 0
        for blk in blocks:
            starts.append(round(al["character_start_times_seconds"][off], 3)); off += len(blk) + 1
        tj.write_text(json.dumps({"words": words, "blocks": starts}), encoding="utf-8")
    t = json.loads(tj.read_text(encoding="utf-8"))
    vend = max(w["e"] for w in t["words"])
    html = (ENGINE / ("template_wide.html" if wide else "template.html")).read_text(encoding="utf-8")
    tail = 0.6 if wide and "--end" not in sys.argv else 4.5
    if wide: t["words"] = [{**w, "s": round(w["s"] + lead, 3), "e": round(w["e"] + lead, 3)} for w in t["words"]]; t["blocks"] = [round(v + lead, 3) for v in t["blocks"]]; vend += lead
    scene = (ep / "scene.js").read_text(encoding="utf-8")
    for k, v in {"__WORDS__": json.dumps(t["words"]), "__BLOCKS__": json.dumps(t["blocks"] + [round(vend + 0.3, 3)]),
                 "__VEND__": f"{vend:.3f}", "__DUR__": f"{vend + tail:.3f}", "__TITLE__": cfg["title"], "__LEAD__": f"{lead}", "__CHAPTER__": chapter,
                 "__KEYS__": json.dumps(cfg["keys"])}.items():
        html = html.replace(k, v)
    html = html.replace("/*__SCENE__*/", scene)
    (ep / "index.html").write_text(html, encoding="utf-8")
    for f in ("hyperframes.json", "package.json"):
        if not (ep / f).exists():
            src = ROOT / "puzzles" / "ep01_poisoned_bottles" / f
            (ep / f).write_text(src.read_text(encoding="utf-8").replace("ep01-poisoned-bottles", ep.name.replace("_", "-")), encoding="utf-8")
    print(f"{ep.name}: speech {vend:.1f}s, video {vend + tail:.1f}s", flush=True)
    if "--render" in sys.argv:
        (ep / "renders").mkdir(exist_ok=True)
        subprocess.run(["npx", "--yes", "hyperframes@0.8.191", "render", "-o", f"renders/{ep.name}.mp4", "--quiet"],
                       cwd=ep, check=True, shell=True)

main()
