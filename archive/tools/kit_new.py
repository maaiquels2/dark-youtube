M = {"svb": {"first": "Forty-eight hours",
  "title": "Silicon Valley Bank: How a $209 Billion Bank Died in 48 Hours",
  "intro": """On March 9, 2023, depositors pulled about $42 billion out of Silicon Valley Bank in a single day. By the next morning the bank expected about $100 billion more in withdrawal requests, and regulators shut it down before the day was over. How did the startup world's favorite bank, with about $209 billion in assets, collapse so fast?

This documentary covers SVB's boom during the tech funding frenzy, the bond losses hidden by rising interest rates, the uninsured-deposit run, the weekend decision by the FDIC, Federal Reserve and Treasury to protect all depositors, the sale to First Citizens, the Federal Reserve's own review, and the FDIC's civil lawsuit against former executives and directors.

NOTE: The FDIC's lawsuit against former SVB officers and directors contains civil allegations that have not been proven; the defendants deny wrongdoing. No criminal charges have been filed against them.""",
  "hashtags": "#SVB #SiliconValleyBank #Finance #Documentary",
  "tags": ["Silicon Valley Bank", "SVB collapse", "SVB bank run", "bank run 2023", "Greg Becker", "SVB Financial Group", "FDIC", "Federal Reserve", "First Citizens", "Signature Bank", "uninsured deposits", "interest rates", "bank failure", "2023 banking crisis", "Janet Yellen", "Jerome Powell", "business documentary", "finance documentary", "The Cracked Ledger", "startup bank"]},
 "lehman": {"first": "A name built to last",
  "title": "Lehman Brothers: The Weekend Wall Street Broke ($639 Billion Bankruptcy)",
  "intro": """On September 15, 2008, Lehman Brothers, a 158-year-old investment bank, filed the largest bankruptcy in U.S. history, listing about $639 billion in assets. How did a firm that survived the Civil War and the Great Depression run out of options in a single weekend?

This documentary covers Lehman's rise from an Alabama dry-goods store, the leveraged real-estate bet, the losses of 2008, the failed rescue weekend at the Federal Reserve Bank of New York, the shock that spread to AIG and money-market funds, the congressional hearing, and the bankruptcy examiner's report on Repo 105.

NOTE: The bankruptcy examiner's findings and lawsuits described in this video are allegations and conclusions of that report; no criminal charges were filed against Lehman executives, who have denied wrongdoing.""",
  "hashtags": "#LehmanBrothers #FinancialCrisis #Finance #Documentary",
  "tags": ["Lehman Brothers", "Lehman Brothers collapse", "Lehman bankruptcy", "2008 financial crisis", "Richard Fuld", "Repo 105", "Henry Paulson", "Timothy Geithner", "Ben Bernanke", "Barclays", "Bank of America Merrill Lynch", "AIG bailout", "Reserve Primary Fund", "Wall Street", "largest bankruptcy", "business documentary", "finance documentary", "The Cracked Ledger", "subprime crisis", "investment bank"]}}
import json, re
from pathlib import Path
import sys; key = sys.argv[1]; pid = open(f"{key}_id.txt").read().strip(); P = Path("projects"); d = json.loads((P / f"{pid}.json").read_text(encoding="utf-8")); pdir = P / pid
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
if not chap or chap[0][0] != 0: chap.insert(0, (0, M[sys.argv[1]]["first"], 1))
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
        if k.endswith("_source") or k in ("logo", "photo_short", "photo_image_url"): continue
        if e.get("photo_license") == "fair_use" and k == "photo": continue
        line = f"{e.get('full_name') or e['name']} ({k.replace('_', ' ').replace('hq photo', 'building photo')}): {v}".replace(", via Wikimedia Commons", "")
        if line not in photos: photos.append(line)
title = M[sys.argv[1]]["title"]
music = sorted({t["title"] for t in d.get("music_tracks") or []}, key=lambda x: [t["title"] for t in d["music_tracks"]].index(x))
desc = M[sys.argv[1]]["intro"] + """

CHAPTERS
""" + "\n".join(f"{fmt(t)} {c}" for t, c, _ in chap) + """

SOURCES
""" + "\n".join(f"- {u}" for u in srcs) + """

MUSIC
""" + ", ".join(f'"{m}"' for m in music) + """ by Kevin MacLeod (incompetech.com)
Licensed under Creative Commons: By Attribution 4.0 License
https://creativecommons.org/licenses/by/4.0/

PHOTO CREDITS (Wikimedia Commons)
""" + "\n".join(f"- {p}" for p in photos) + """
""" + "".join(f"\nFAIR USE NOTE: The photo of {e['name']} (Photo: {e['credits'].get('photo_short')}, {e['credits'].get('photo_source')}) is a news photograph used briefly, cropped and stylized, for commentary and news reporting under fair use (17 U.S.C. 107). No endorsement implied." for e in d.get("entities") or [] if e.get("photo_license") == "fair_use") + """
Agency seals are U.S. government works (public domain). Company logos are trademarks of their owners, shown for identification.

Visuals: illustrative scenes are AI-generated (no real people depicted) and motion graphics are built from the cited sources. Headlines are recreated for illustration.

This video is for educational and journalistic purposes and is not financial or legal advice.

""" + M[sys.argv[1]]["hashtags"]
tags = M[sys.argv[1]]["tags"]
kit = {"title": title, "description": desc, "tags": tags, "chapters": [[fmt(t), c, n] for t, c, n in chap]}
(pdir / "output/youtube_kit.json").write_text(json.dumps(kit, ensure_ascii=False, indent=2), encoding="utf-8")
(pdir / "output/youtube_kit.md").write_text(f"# {title}\n\n{desc}\n\nTAGS: {', '.join(tags)}\n", encoding="utf-8")
print(len(title), len(desc), sum(len(t) for t in tags) + len(tags)); print("\n".join(f"{fmt(t)} {c} (scene {n})" for t, c, n in chap))



