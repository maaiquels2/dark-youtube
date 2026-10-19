import sys, json, time; sys.path.insert(0, ".")
import pipeline, app, entities as E
key = sys.argv[1]; pid = open(f"{key}_id.txt").read().strip(); pdir = app.PROJECTS / pid
orig = pipeline._save
def merged(d):
    f = pipeline._load(pid); f["entities"] = d["entities"]; f["images_done"] = True; orig(f)
pipeline._save = merged
src = json.load(open("tools/curated/new-entities-src.json", encoding="utf-8"))[key]
cur = []
d0 = pipeline._load(pid); have = {e["name"]: e for e in d0.get("entities") or []}
for e in src:
    t = e.pop("_t"); old = have.get(e["name"], {}); e["credits"] = dict(old.get("credits") or {})
    for k, title in t.items():
        if old.get(k) and (pdir / old[k]).is_file(): e[k] = old[k]; continue
        ext = ".png" if title.lower().endswith((".png", ".svg")) else ".jpg"
        rel = f"entities/{''.join(c if c.isalnum() else '-' for c in e['name'].lower())}-{k}{ext}"
        time.sleep(5); info = E.fetch_commons(title, pdir / rel); e[k] = rel; e["credits"][k] = info["credit"]; e["credits"][k + "_source"] = info["source"]
    cur.append(e)
r = pipeline.collect_images(pid, cur)
print(r["entities"], "entities", r["with_real_visual"], "real"); [print(" ", x) for x in r["log"]]
d = pipeline._load(pid); print("NO VISUAL:", [e["name"] for e in d["entities"] if not E.has_real_asset(e)])
