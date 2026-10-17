import json, sys, time, traceback, shutil
sys.path.insert(0, "."); import app, pipeline, entities as E
key = sys.argv[1]; steps = sys.argv[2:]
pid = open(f"{key}_id.txt").read().strip(); pdir = app.PROJECTS / pid
def log(*a): print(time.strftime("%H:%M:%S"), *a, flush=True)
for st in steps:
    log("START", st)
    try:
        if st == "images":
            src = json.load(open("tools/curated/new-entities-src.json", encoding="utf-8"))[key]; cur = []
            for e in src:
                t = e.pop("_t"); e.setdefault("credits", {})
                for k, title in t.items():
                    ext = ".png" if title.lower().endswith((".png", ".svg")) else ".jpg"
                    rel = f"entities/{''.join(c if c.isalnum() else '-' for c in e['name'].lower())}-{k}{ext}"
                    try:
                        info = E.fetch_commons(title, pdir / rel); e[k] = rel; e["credits"][k] = info["credit"]; e["credits"][k + "_source"] = info["source"]
                    except Exception as ex: log("fetch fail", e["name"], ex)
                cur.append(e)
            r = pipeline.collect_images(pid, cur); log(r["entities"], "entities,", r["with_real_visual"], "real"); [log(" ", x) for x in r["log"]]
        elif st == "prompts":
            r = pipeline.enrich_prompts(pid); log("beats", sum(1 for s in r["scenes"] if s.get("beat")))
        elif st == "tovideo":
            d = app.load_project(pid); sc = d["scenes"]; n = len(sc)
            ai = [i for i, s in enumerate(sc) if s.get("source") != "gfx"]
            vid = [i for i in ai if sc[i].get("mode") == "video"]
            rest = sorted([i for i in ai if i not in vid], key=lambda i: (0 if i < 4 else 1 if pipeline.act_of(i, n) in ("act3","act2") else 2, i))
            for i in rest[:max(0, 32 - len(vid))]: sc[i]["mode"] = "video"
            for s in sc:
                if s.get("source") != "gfx": s.update(status="pendente", file=None, error=None)
            pipeline._save(d); log("ai", len(ai), "video", sum(1 for i in ai if sc[i].get("mode") == "video"))
        elif st == "validate":
            r = pipeline.validate(pid); log("ok", r["ok"], "gaps", json.dumps(r.get("gaps"))[:3000], json.dumps({k: v for k, v in r.items() if k not in ("gaps",)}, default=str)[:3000])
            if r["ok"]: log("gfx", app.gfx_render(pid))
    except Exception:
        log(traceback.format_exc()); break
log("DONE")
