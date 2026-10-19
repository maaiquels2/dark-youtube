import json, sys, time, re
sys.path.insert(0, "."); import app, pipeline, entities as E
pid = open("fb_id.txt").read().strip(); pdir = app.PROJECTS / pid
d = app.load_project(pid)
cur = {e["name"]: e for e in json.load(open("tools/curated/first-brands-entities.json", encoding="utf-8"))}
ok_photos = {n for n, e in cur.items() if e.get("photo")}
keep = []
for e in d.get("entities") or []:
    n = e["name"]
    if pipeline.JUNK.match(n) or n in ("Court presiding over United States v. Patrick James and Edward James",): print("drop", n); continue
    if n == "DOJ SDNY": print("merge DOJ SDNY -> SDNY alias"); continue
    if n == "First Brands / First Brands Group": print("drop dup", n); continue
    if e.get("kind") == "person" and e.get("photo") and n not in ok_photos:
        f = pdir / e["photo"]; f.unlink(missing_ok=True); e.pop("photo"); (e.get("credits") or {}).pop("photo", None); (e.get("credits") or {}).pop("photo_source", None); print("removed wrong photo", n)
    keep.append(e)
for e in keep:
    if e["name"] == "SDNY": e["aliases"] = list(set((e.get("aliases") or []) + ["DOJ SDNY"]))
d["entities"] = keep
narr = " ".join(s.get("narration", "") for s in d["scenes"])
print("SEC mentioned:", bool(re.search(r"\bSEC\b|Securities and Exchange Commission", narr)))
VER = [{"outlet": "Transport Topics", "date": "Mar 6, 2026", "headline": "Ex-First Brands CFO Pleads Guilty in Fraud Case", "url": "https://www.ttnews.com/articles/first-brands-cfo-pleads-guilty", "kw": ("cfo", "graham", "guilty", "cooperat")},
       {"outlet": "Transport Topics", "date": "Oct 8, 2026", "headline": "James brothers trade blame in First Brands case", "url": "https://www.ttnews.com/articles/james-brothers-blame-first-brands", "kw": ("separate", "blame", "trial")}]
for i, s in enumerate(d["scenes"]):
    for g in s.get("gfx") or []:
        if g.get("type") == "headline":
            t = (s.get("narration", "") + " " + g.get("headline", "")).lower()
            best = max(VER, key=lambda v: sum(k in t for k in v["kw"]))
            print(f"scene {i+1}: headline '{g.get('outlet')}: {g.get('headline')}' -> '{best['outlet']}: {best['headline']}'")
            g.update(outlet=best["outlet"], date=best["date"], headline=best["headline"], url=best["url"], verified=True)
pipeline._save(d)
