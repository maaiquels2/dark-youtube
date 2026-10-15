import json, sys, time, traceback
sys.path.insert(0, "."); import app, pipeline
pid = open("fb_id.txt").read().strip()
cur = json.load(open("tools/curated/first-brands-entities.json", encoding="utf-8"))
steps = sys.argv[1:] or ["research", "script", "images", "prompts", "validate"]
def log(*a): print(time.strftime("%H:%M:%S"), *a, flush=True)
for st in steps:
    log("START", st)
    try:
        if st == "research":
            d = app.load_project(pid); d["research_notes"] = d.get("research_notes") or d.get("facts"); pipeline._save(d)
            r = pipeline.research(pid); log("dossier", len(r["chapters"]), "chapters", r["sources_ok"], "/", r["sources_checked"], "sources ok")
        elif st == "script":
            r = pipeline.script_from_dossier(pid); log("scenes", len(r["scenes"]), "words", sum(len(s["narration"].split()) for s in r["scenes"]))
        elif st == "images":
            r = pipeline.collect_images(pid, cur); log(r["entities"], "entities,", r["with_real_visual"], "real"); [log(" ", x) for x in r["log"]]
        elif st == "prompts":
            r = pipeline.enrich_prompts(pid); log("beats", sum(1 for s in r["scenes"] if s.get("beat")))
        elif st == "validate":
            r = pipeline.validate(pid); log("ok", r["ok"], "cards+", r["entity_cards_added"], "callouts+", r["amount_callouts_added"], "gaps", json.dumps(r["gaps"])[:3000])
            if r["ok"]: log("gfx", app.gfx_render(pid))
    except Exception:
        log(traceback.format_exc()); break
log("DONE")
