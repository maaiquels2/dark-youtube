import json, sys, re, time
sys.path.insert(0, "."); import app, pipeline
key = sys.argv[1]; pid = open(f"{key}_id.txt").read().strip(); d = app.load_project(pid)
FED = "Federal Reserve review of SVB, Apr 28 2023"; FDIC = "FDIC press release, Mar 26 2023"
A = {"svb": [
  ({"type": "collapse", "title": "The run on Silicon Valley Bank", "unit": "$B", "mode": "bars", "points": [
     {"label": "Deposits, end-2019", "value": 62, "display": "~$62B", "color": [64, 196, 200]},
     {"label": "Deposits, end-2021", "value": 189, "display": "~$189B", "color": [64, 196, 200]},
     {"label": "Withdrawn on Mar 9, 2023", "value": 42, "display": "~$42B", "tone": "loss"},
     {"label": "Requests expected Mar 10", "value": 100, "display": "~$100B", "tone": "loss"}],
    "final": {"label": "withdrawn in a single day", "value": "$42B"}, "source": FED}, lambda n: "hundred billion" in n and ("42" in n or "forty-two" in n)),
  ({"type": "moneyflow", "title": "Where Silicon Valley Bank went", "flows": [
     {"from": {"name": "Silicon Valley Bank Â· Santa Clara, Calif.", "lon": -121.95, "lat": 37.35},
      "to": {"name": "First Citizens Â· Raleigh, N.C.", "lon": -78.64, "lat": 35.78},
      "amount": "~$72B in assets", "date": "bought at a $16.5B discount Â· Mar 26, 2023"}],
    "bbox": [-126, 30, -70, 46], "source": FDIC}, lambda n: "first citizens" in n),
 ], "lehman": [
  ({"type": "collapse", "title": "Lehman Brothers at the end", "unit": "$B", "mode": "bars", "points": [
     {"label": "Assets in the filing", "value": 639, "display": "~$639B", "color": [64, 196, 200]},
     {"label": "Debts in the filing", "value": 613, "display": "~$613B", "tone": "loss"},
     {"label": "Q3 2008 loss (pre-announced)", "value": 3.9, "display": "~$3.9B", "tone": "loss"}],
    "final": {"label": "largest bankruptcy in U.S. history", "value": "$639B"}, "source": "Federal Reserve History; FCIC Report (2011)"}, lambda n: ("639" in n or "thirty-nine billion" in n) and ("613" in n or "thirteen billion" in n)),
 ]}
FULL = {"timeline","chart","document","quote","relmap","scale","chapter","headline","photo","entity_full","moneyflow","collapse"}
for spec, test in A[key]:
    for i, s in enumerate(d["scenes"]):
        n = (s.get("narration") or "").lower()
        if test(n) and not any(g.get("type") in FULL for g in s.get("gfx") or []):
            s["gfx"] = [spec] + [g for g in s.get("gfx") or [] if g.get("type") == "citation"]; print(spec["type"], "-> scene", i + 1); break
    else:
        # fallback: first matching scene even with other full gfx (replace them)
        for i, s in enumerate(d["scenes"]):
            if test((s.get("narration") or "").lower()):
                s["gfx"] = [spec]; print(spec["type"], "-> scene (replaced)", i + 1); break
        else: print(spec["type"], "no scene")
for s in d["scenes"]:
    if s.get("chapter"): s["chapter"] = re.sub(r"^(Act [IV]+\s*[â€”-]\s*|\d+\.\s*)", "", s["chapter"])
    for g in s.get("gfx") or []:
        if g.get("type") == "chapter" and g.get("title"): g["title"] = re.sub(r"^(Act [IV]+\s*[â€”-]\s*|\d+\.\s*)", "", g["title"])
C = "Kevin MacLeod (incompetech.com), licensed under Creative Commons: By Attribution 4.0, https://creativecommons.org/licenses/by/4.0/"
# MUSIC RULE (default): one calm bed for the whole video, ~-20 dB under narration (+ sidechain ducking in montage)
d["music_tracks"] = [{"file": "music/floating-cities.mp3", "from_scene": 1, "volume": 0.07, "title": "Floating Cities", "act": "all", "credit": C}]
# no sparse charts: single-value charts become an amount callout
for s in d["scenes"]:
    new = []
    for g in s.get("gfx") or []:
        pts = g.get("points") or g.get("bars") or g.get("data") or g.get("series") or []
        if g.get("type") == "chart" and len(pts) < 2:
            p = pts[0] if pts else {}
            txt = p.get("display") or p.get("value_label") or str(p.get("value", "")) if isinstance(p, dict) else str(p)
            if txt: new.append({"type": "callout", "text": f"{txt} {p.get('label','') if isinstance(p, dict) else ''}".strip(), "source": (g.get("source") or "")[:60]})
            print("sparse chart -> callout", txt); continue
        new.append(g)
    s["gfx"] = new
pipeline._save(d); print("music single track")