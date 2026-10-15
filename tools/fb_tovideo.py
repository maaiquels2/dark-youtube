import json, sys, shutil
sys.path.insert(0, "."); import app, pipeline
pid = open("fb_id.txt").read().strip(); pdir = app.PROJECTS / pid; d = app.load_project(pid); sc = d["scenes"]; n = len(sc)
img = [i for i, s in enumerate(sc) if s.get("source") != "gfx" and s.get("mode") != "video"]
pr = lambda i: (0 if i < 4 else 1 if pipeline.act_of(i, n) == "act3" else 2 if pipeline.act_of(i, n) == "act2" else 3, i)
pick = sorted(sorted(img, key=pr)[:20])
if 19 not in pick and 19 in img: pick[-1] = 19; pick.sort()   # cena 20 tinha texto legivel
fb = pdir / "media" / "fallback"; fb.mkdir(parents=True, exist_ok=True)
for i in pick:
    s = sc[i]; f = pdir / s["file"]
    if f.is_file(): shutil.move(str(f), fb / f.name); s["fallback_file"] = f"media/fallback/{f.name}"
    s.update(mode="video", status="pendente", file=None, error=None)
    if i == 19: s["visual_prompt"] = s["visual_prompt"] + " The building facade has NO lettering, no signs, no inscriptions."
pipeline._save(d); print("video:", [i + 1 for i in pick]); open("fb_video_pick.txt", "w").write(json.dumps(pick))
