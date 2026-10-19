import json, sys
sys.path.insert(0, "."); import app, pipeline
pid = open("fb_id.txt").read().strip(); d = app.load_project(pid)
FULL = {"timeline","chart","document","quote","relmap","scale","chapter","headline","photo","entity_full"}
VER = [("Transport Topics","Mar 6, 2026","Ex-First Brands CFO Pleads Guilty in Fraud Case","https://www.ttnews.com/articles/first-brands-cfo-pleads-guilty",("graham",)),
       ("Transport Topics","Oct 8, 2026","James brothers trade blame in First Brands case","https://www.ttnews.com/articles/james-brothers-blame-first-brands",("separate trial",))]
for o, dt, h, u, kw in VER:
    for i, s in enumerate(d["scenes"]):
        n = s.get("narration","").lower()
        if all(k in n for k in kw) and not any(g.get("type") in FULL for g in s.get("gfx") or []):
            s.setdefault("gfx", []).insert(0, {"type":"headline","outlet":o,"date":dt,"headline":h,"url":u,"verified":True}); print("headline ->", i+1, h); break
pipeline._save(d)
