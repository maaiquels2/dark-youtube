import json, sys, time
from pathlib import Path
sys.path.insert(0, "."); import app
pid = "zz-ftx-thumb-bg"
V = ["A dark glass skyscraper of a crypto exchange collapsing into glowing teal digital fragments over a stormy night city, dramatic low angle, strong rim light, all action on the left two-thirds, right third dark smoky empty space, no people, no faces, no text, no logos.",
     "A huge open steel vault with glowing gold coins pouring out and dissolving into red smoke and digital dust, deep black background, intense red and teal lighting, left-weighted composition with empty dark right third, no people, no faces, no text, no logos.",
     "A shattered red stock-crash chart line made of neon glass plunging downward across a dark trading floor, sparks and smoke, cinematic red and black, empty dark right third for overlay, no people, no faces, no numbers, no text, no logos."]
d = {"id": pid, "title": "FTX thumbnail backgrounds (temp)", "language": "en", "minutes": 1,
     "scenes": [{"narration": "Background.", "visual_prompt": v, "mode": "image", "source": "site"} for v in V]}
d = app.with_prompts(d)
(Path("projects") / f"{pid}.json").write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
(Path("projects") / pid).mkdir(exist_ok=True); print("ok")
