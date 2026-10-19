import sys, json, time; sys.path.insert(0, ".")
import pipeline, app, entities as E
FIX = {"svb": {
  "Silicon Valley Bank": {"logo": "File:Silicon Valley Bank logo, 2022.svg"},
  "FDIC": {"seal": "File:Seal of the United States Federal Deposit Insurance Corporation.svg"},
  "Deposit Insurance Fund": {"seal": "File:Seal of the United States Federal Deposit Insurance Corporation.svg"},
  "Treasury": {"seal": "File:Seal of the United States Department of the Treasury.svg"},
  "GAO": {"seal": "File:Seal of the United States Government Accountability Office.svg"},
  "Senate Banking Committee": {"seal": "File:Seal of the United States Senate.svg"},
  "DFPI": {"logo": "File:California Department of Financial Protection and Innovation logo.png"},
  "Martin Gruenberg": {"photo": "File:Martin Gruenberg Portrait.jpg"},
 }, "lehman": {
  "Lehman Brothers Holdings Inc.": {"logo": "File:Logo of Lehman Brothers.svg"},
  "JPMorgan Chase": {"logo": "File:JPMorgan Chase.svg"},
  "AIG": {"logo": "File:AIG Logo.png"},
  "Nomura": {"logo": "File:Nomura Holdings logo.svg"},
  "Ernst & Young": {"logo": "File:Ernst & Young logo (2016).svg"},
  "Jenner & Block": {"logo": "File:Jenner & Block logo.svg"},
  "SEC": {"seal": "File:Seal of the United States Securities and Exchange Commission.svg"},
  "New York Fed": {"hq_photo": "File:2015 Federal Reserve Bank of New York from west.jpg"},
  "House Committee on Oversight and Government Reform": {"seal": "File:Seal of the United States House of Representatives.svg"},
  "New York Attorney General": {"seal": "File:Seal of the Attorney General of New York.svg"},
  "Andrew Cuomo": {"photo": "File:Andrew Cuomo (cropped).png"},
  "Henry Waxman": {"photo": "File:Henry Waxman, official photo portrait color.jpg"},
 }}
DROP = {"svb": {"First Republic": ["logo"], "Brookfield": ["logo"], "Nasdaq": ["logo"]}, "lehman": {"Merrill Lynch": ["logo"]}}
key = sys.argv[1]; pid = open(f"{key}_id.txt").read().strip(); pdir = app.PROJECTS / pid
d = pipeline._load(pid); ents = {e["name"]: e for e in d["entities"]}
for n, ks in DROP[key].items():
    for k in ks: ents[n].pop(k, None); (ents[n].get("credits") or {}).pop(k, None); (ents[n].get("credits") or {}).pop(k + "_source", None)
for n, m in FIX[key].items():
    e = ents.get(n)
    if not e: print("missing", n); continue
    for k, t in m.items():
        ext = ".png" if t.lower().endswith((".png", ".svg")) else ".jpg"
        rel = f"entities/{''.join(c if c.isalnum() else '-' for c in n.lower())}-{k}{ext}"
        for a in range(3):
            try:
                time.sleep(6); info = E.fetch_commons(t, pdir / rel); e[k] = rel; e.setdefault("credits", {})[k] = info["credit"]; e["credits"][k + "_source"] = info["source"]; print("ok", n, k); break
            except Exception as ex: print("retry", n, ex); time.sleep(30)
f = pipeline._load(pid); f["entities"] = list(ents.values()); pipeline._save(f)
print("NO VISUAL:", [e["name"] for e in ents.values() if not E.has_real_asset(e)])
