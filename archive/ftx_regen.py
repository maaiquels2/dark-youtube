import json, sys, shutil
from pathlib import Path
sys.path.insert(0, "."); import app
f = Path("projects/ftx-how-8-billion-vanished-overnight-20261015-155014.json"); P = f.with_suffix("")
d = json.loads(f.read_text(encoding="utf-8"))
new = {5: "Split composition of an abstract glowing order-book grid and a separate empty desk with volatile abstract chart lines on a monitor. Eye-level camera, neutral lighting, no people, no faces, no eyes, no readable labels or brand identifiers.",
 20: "Close-up of gloved hands opening a plain unmarked folder beside a simple diagram of two connected glass money reservoirs. Warm desk lighting, shallow focus, completely blank paper, no letters, no words, no labels anywhere.",
 25: "Two streams of differently colored light particles merge inside a transparent glass chamber until their origins become indistinguishable. Macro tracking shot, cold laboratory lighting, purely abstract, no faces, no sculptures, no figures, no text.",
 65: "A plain blank folder waits in an otherwise empty metal processing tray beneath a desk lamp. Tight static shot, muted office palette, completely blank surfaces, no letters, no words, no labels, no stamps.",
 69: "A closed plain folder rests beside a blank calendar page and a still hourglass on a dark wooden desk. Close overhead framing, cool afternoon light, completely blank paper, no letters, no numbers, no words."}
rej = P / "media" / "rejected"; rej.mkdir(parents=True, exist_ok=True)
for n, vp in new.items():
    s = d["scenes"][n - 1]; s["visual_prompt"] = vp
    if s.get("file") and (P / s["file"]).is_file(): shutil.move(str(P / s["file"]), rej / Path(s["file"]).name)
    s["file"] = None; s["status"] = "pendente"; s["grok_prompt"] = None
d = app.with_prompts(d)
f.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
print([d["scenes"][n-1]["grok_prompt"][:60] for n in new])
