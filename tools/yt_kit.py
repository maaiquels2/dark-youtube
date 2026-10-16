import json, re
from pathlib import Path
import sys; pid = sys.argv[1] if len(sys.argv) > 1 else open("fb_id.txt").read().strip(); P = Path("projects"); d = json.loads((P / f"{pid}.json").read_text(encoding="utf-8")); pdir = P / pid
srt = (pdir / "output/final.srt").read_text(encoding="utf-8").strip().split("\n\n")
cues = []
for b in srt:
    l = b.split("\n"); m = re.match(r"(\d+):(\d+):(\d+),(\d+)", l[1]); t = int(m[1]) * 3600 + int(m[2]) * 60 + int(m[3]); cues.append((t, " ".join(l[2:]).lower()))
norm = lambda s: re.sub(r"[^a-z0-9 ]", "", s.lower())
chap = []
for i, s in enumerate(d["scenes"]):
    ch = s.get("chapter") or next((g.get("title") for g in s.get("gfx") or [] if g.get("type") == "chapter"), "")
    if not ch: continue
    w = norm(s["narration"]).split()[:4]; key = " ".join(w)
    t = next((c[0] for c in cues if key and key in norm(c[1])), None)
    if t is None: t = next((c[0] for c in cues if w and norm(c[1]).startswith(w[0])), None)
    chap.append((t, ch, i + 1))
chap = [c for c in chap if c[0] is not None]; chap.sort()
if not chap or chap[0][0] != 0: chap.insert(0, (0, "The $12 million question", 1))
fmt = lambda t: f"{t//60}:{t%60:02d}"
srcs = []
for ch in d["dossier"]["chapters"]:
    for f in ch.get("facts") or []:
        u = f.get("url")
        if u and u not in srcs: srcs.append(u)
for s in d["scenes"]:
    for g in s.get("gfx") or []:
        if g.get("url") and g["url"] not in srcs: srcs.append(g["url"])
photos = []
for e in d.get("entities") or []:
    for k, v in (e.get("credits") or {}).items():
        if k.endswith("_source") or k == "logo": continue
        line = f"{e.get('full_name') or e['name']} ({k.replace('_', ' ').replace('hq photo', 'building photo')}): {v}"
        if line not in photos: photos.append(line)
title = "First Brands: The $11.6 Billion Collapse and the Alleged Fraud Behind It"
desc = f"""In September 2025, auto-parts giant First Brands Group filed for bankruptcy. Prosecutors say it declared just $12 million in cash against more than $9 billion in liabilities. Court documents show $11.6 billion in total liabilities. How did an Ohio maker of brakes, filters and wipers become one of the biggest credit shocks in years, and what do prosecutors allege happened inside?

This documentary covers the Chapter 11 filing, the exposure of lenders and funds (Jefferies' Point Bonita fund, UBS funds, Raistone), the impact on workers and automakers' supply chains, the January 2026 indictment of founder Patrick James and his brother Edward James, the guilty pleas of two former finance executives, and where the case stands as of October 15, 2026.

IMPORTANT: Patrick James and Edward James have pleaded not guilty and deny wrongdoing. The charges in the indictment are accusations. The defendants are presumed innocent unless and until proven guilty in a court of law. Everything described about the alleged schemes is an allegation by prosecutors. The trial is scheduled for February 2027.

CHAPTERS
""" + "\n".join(f"{fmt(t)} {c}" for t, c, _ in chap) + """

SOURCES
""" + "\n".join(f"- {u}" for u in srcs) + """

MUSIC
"Floating Cities", "Investigations", "Darkest Child", "Heartbreaking" by Kevin MacLeod (incompetech.com)
Licensed under Creative Commons: By Attribution 4.0 License
https://creativecommons.org/licenses/by/4.0/

PHOTO CREDITS (Wikimedia Commons)
""" + "\n".join(f"- {p}" for p in photos) + """
Agency seals are U.S. government works (public domain). Company logos are trademarks of their owners, shown for identification.

Visuals: illustrative scenes are AI-generated (no real people depicted) and motion graphics are built from the cited sources. Headlines are recreated for illustration.

This video is for educational and journalistic purposes and is not financial or legal advice.

#FirstBrands #Finance #Documentary"""
tags = ["First Brands", "First Brands Group", "First Brands bankruptcy", "Patrick James", "Edward James", "First Brands indictment", "auto parts bankruptcy", "Chapter 11", "Jefferies Point Bonita", "UBS First Brands", "Raistone", "supply chain finance", "private credit", "double pledged collateral", "corporate fraud allegations", "SDNY", "business documentary", "finance documentary", "The Cracked Ledger", "FRAM"]
kit = {"title": title, "description": desc, "tags": tags, "chapters": [[fmt(t), c, n] for t, c, n in chap]}
(pdir / "output/youtube_kit.json").write_text(json.dumps(kit, ensure_ascii=False, indent=2), encoding="utf-8")
(pdir / "output/youtube_kit.md").write_text(f"# {title}\n\n{desc}\n\nTAGS: {', '.join(tags)}\n", encoding="utf-8")
print(len(title), len(desc), sum(len(t) for t in tags) + len(tags)); print("\n".join(f"{fmt(t)} {c} (scene {n})" for t, c, n in chap))

