import json, sys
sys.path.insert(0, "."); import app, pipeline
pid = open("fb_id.txt").read().strip(); d = app.load_project(pid)
FULL = {"timeline","chart","document","quote","relmap","scale","chapter","headline","photo","entity_full","moneyflow","collapse"}
d["entities"] = [e for e in d.get("entities") or [] if e["name"] not in ("First Brands / First Brands Group", "Court presiding over United States v. Patrick James and Edward James") and not pipeline.JUNK.match(e["name"])]
for e in d["entities"]:
    if e["name"] == "Reuters" and e.get("logo"): e.pop("logo"); e.get("credits", {}).pop("logo", None); e["no_auto"] = True; print("Reuters: removed Thomson Reuters logo")
A = json.load(open("tools/curated/first-brands-anim.json", encoding="utf-8"))
def put(spec, test):
    for i, s in enumerate(d["scenes"]):
        n = s.get("narration", "").lower()
        if test(n) and not any(g.get("type") in FULL for g in s.get("gfx") or []):
            s["gfx"] = [spec] + [g for g in s.get("gfx") or [] if g.get("type") in ("citation",)]; s["mode"] = "video"; print(spec["type"], "-> scene", i + 1, n[:90]); return
    print(spec["type"], ": no free matching scene")
put(A["moneyflow"], lambda n: "715" in n)
put(A["collapse"], lambda n: "12 million" in n and "cash" in n)
pipeline._save(d)


