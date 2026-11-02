"""Gerador de Shorts nativos verticais (1080x1920) a partir das falas ja gravadas do video longo.
Uso: python scratch/short_native.py <nome>   (nome em SHORTS abaixo) -> projects/<id>/output/shorts/<nome>.mp4
Cada segmento: fala gravada ("src": comeco da narracao, "start"/"end_before": palavras de corte) ou fala nova ("tts"),
e um visual: kinetic | counter | rows | person | cta. "at" = palavra falada (ou segundos, numero) em que o elemento entra."""
import json, re, shutil, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT))
import os
PID = os.environ.get("SHORT_PID", "tricolor-car-loan-20261027-210000"); PD = ROOT / "projects" / PID; HF = ROOT / "tools/hyperframes"
pj = json.loads((ROOT / "projects" / f"{PID}.json").read_text(encoding="utf-8")); WJ = json.loads((PD / "audio/words.json").read_text(encoding="utf-8"))
norm = lambda s: re.sub(r"[^a-z0-9.$]", "", s.lower())
SRC_DOJ = "U.S. Department of Justice (SDNY)"
HW = "one-man-cost-banks-10-billion-nobody-saw-his-name-20261024-005905"

SHORTS = {
 "hwang-1": {"music": "darkest-child.mp3", "source": "U.S. v. Hwang (S.D.N.Y.) · Photo: Archegos project credits", "segs": [
   {"tts": "Bill Hwang asked for no prison. The judge gave him eighteen years.",
    "vis": {"type": "kinetic", "lines": [["Asked for", 0.0, "mid"], ["NO PRISON", 1.0, "amber"], ["Got 18 years", 3.2, "mid"]]}},
   {"src": "After an eight-week trial", "vis": {"type": "rows", "label": "THE VERDICT · JULY 2024", "rows": [["10 of 11", "counts: guilty", "10"], ["21 years", "what prosecutors asked", "21"], ["18 years", "what the judge gave", "18"]]}},
   {"src": "Two of his own senior staffers", "vis": {"type": "rows", "label": "TESTIMONY", "rows": [["2 insiders", "pleaded guilty and testified", "pleaded"], ["Lied to banks", "to win more credit", "lying"]]}},
   {"src": "Halligan, found guilty", "vis": {"type": "counter", "label": "PATRICK HALLIGAN · GUILTY ON ALL 3", "prefix": "", "value": 8, "dec": 0, "suffix": " years", "at": "eight", "sub": "both expected to stay free on bail during appeals", "sub_at": "bail"}},
   {"tts": "The full story is on The Cracked Ledger.", "vis": {"type": "cta"}}]},
 "hwang-2": {"music": "darkest-child.mp3", "source": "U.S. v. Hwang (S.D.N.Y.) · SEC · Company filings", "segs": [
   {"tts": "Banned from trading, Bill Hwang had Wall Street's banks lining up to lend to him.",
    "vis": {"type": "kinetic", "lines": [["Banned.", 0.0, "mid"], ["Wall Street", 2.5, "mid"], ["LINED UP", 3.3, "amber"], ["to lend to him.", 4.6, "mid"]]}},
   {"src": "In 2012", "vis": {"type": "rows", "label": "TIGER ASIA · HIS OLD FUND", "rows": [["2012", "pleaded guilty to insider trading", "2012"], ["$44M", "paid in the case", "44"]]}},
   {"src": "Two years later", "vis": {"type": "rows", "label": "HONG KONG · 2014", "rows": [["4 years", "banned from trading", "four"]]}},
   {"src": "Most careers end", "vis": {"type": "rows", "label": "2013", "rows": [["Archegos", "his new family office", "Archegos"], ["Big banks", "lined up to lend to it", "banks"]]}},
   {"src": "A fund with", "vis": {"type": "kinetic", "lines": [["A fraud record", 0.0, "mid"], ["one of their", 1.4, "mid"], ["BEST", 2.5, "amber"], ["customers.", 3.2, "mid"]]}},
   {"tts": "The full story is on The Cracked Ledger.", "vis": {"type": "cta"}}]},
 "hwang-3": {"music": "stay-the-course.mp3", "source": "Yahoo Finance daily closes · Company filings", "segs": [
   {"tts": "In four trading days, ViacomCBS lost more than half of its value.",
    "vis": {"type": "kinetic", "lines": [["4 trading days", 0.0, "mid"], ["MORE THAN", 1.4, "mid"], ["HALF", 2.2, "amber"], ["of its value gone.", 3.3, "mid"]]}},
   {"src": "On Monday", "vis": {"type": "counter", "label": "VIACOMCBS · MON. MARCH 22, 2021", "prefix": "$", "value": 100.34, "dec": 2, "suffix": "", "at": "100", "sub": "the highest close in its history", "sub_at": "highest"}},
   {"src": "Two days later", "vis": {"type": "rows", "label": "WEDNESDAY", "rows": [["-23%", "in a single session", "23"], ["$70.10", "closing price", "70"]]}},
   {"src": "On Thursday", "vis": {"type": "rows", "label": "THURSDAY–FRIDAY", "rows": [["Thursday", "Morgan Stanley starts selling Archegos-related shares", "Morgan"], ["$48.23", "Friday's close", "48"]]}},
   {"tts": "The full story is on The Cracked Ledger.", "vis": {"type": "cta"}}]},
 "native-2": {"music": "darkest-child.mp3", "source": SRC_DOJ + " · Photo: Bing Guan/Bloomberg (via Insurance Journal)", "segs": [
   {"tts": "Three weeks before his company collapsed, prosecutors say the CEO was paid six point two five million dollars.",
    "vis": {"type": "kinetic", "tag": "ALLEGED", "lines": [["3 weeks before", 0.0, "mid"], ["the collapse", 0.9, "mid"], ["$6.25M", 3.2, "amber"], ["to the CEO", 4.6, "mid"]]}},
   {"src": "Then the money", "vis": {"type": "counter", "label": "BONUS · ALLEGED", "prefix": "$", "value": 15, "dec": 0, "suffix": "M", "at": "15", "sub": "while calling the company insolvent", "sub_at": "insolvent"}},
   {"src": "On August 19", "vis": {"type": "counter", "label": "PAID · AUG. 19–20, 2025", "prefix": "$", "value": 6.25, "dec": 2, "suffix": "M", "at": "6.25", "sub": "two payments", "sub_at": "two", "pills": [["Aug. 19", "19"], ["Aug. 20", "20"]]}},
   {"src": "On August 27", "vis": {"type": "rows", "label": "AUG. 27, 2025 · ALLEGED", "rows": [["Beverly Hills", "a multimillion-dollar property", "Beverly"]]}},
   {"src": "Roughly three", "vis": {"type": "rows", "label": "THEN", "rows": [["1,000+", "employees on unpaid leave", "employees"], ["Sept. 10", "Chapter 7 bankruptcy", "September"], ["$900M+", "owed to its largest lenders", "900"]]}},
   {"src": "All of this is alleged", "vis": {"type": "person", "photo": "daniel-chu.jpg", "label": "DANIEL CHU · FOUNDER", "name": "Pleaded not guilty", "lines": [["Presumed innocent", "Chu"], ["Trial: Jan. 25, 2027", "guilty"]]}},
   {"tts": "The full story is on The Cracked Ledger.", "vis": {"type": "cta"}}]},
 "native-3": {"music": "stay-the-course.mp3", "source": "Fitch Ratings · Edmunds · J.D. Power · Cox Automotive", "segs": [
   {"tts": "When a car lender collapses, your loan does not disappear.",
    "vis": {"type": "kinetic", "lines": [["When the lender", 0.0, "mid"], ["collapses,", 0.8, "mid"], ["your loan", 1.7, "amber"], ["doesn't disappear.", 2.4, "mid"]]}},
   {"src": "Tricolor's collapse", "vis": {"type": "rows", "label": "WHAT STAYS", "rows": [["The contract", "a loan is a contract", "contract"], ["A new owner", "someone owns it", "owns"], ["The payment", "still due every month", "due"]]}},
   {"src": "What we can measure", "vis": {"type": "rows", "label": "THE MARKET THEY WERE IN", "rows": [["6.9%", "subprime borrowers 60+ days late · record (Fitch)", "6.9"],
                                                                                                        ["3 in 10", "trade-ins underwater · ~$6,900 (Edmunds)", "3"], ["13%", "new-car loans at 84+ months (J.D. Power)", "84"]]}},
   {"src": "And repossessions", "vis": {"type": "counter", "label": "CARS REPOSSESSED IN 2024", "prefix": "", "value": 1.73, "dec": 2, "suffix": "M", "at": "1.73", "sub": "most since 2009 · up 43% from 2022 (Cox Automotive)", "sub_at": "2009"}},
   {"tts": "The full story is on The Cracked Ledger.", "vis": {"type": "cta"}}]},
}


def scn(prefix): return next(i for i, s in enumerate(pj["scenes"], 1) if s["narration"].startswith(prefix))
OUTN = lambda name: PD / "output" / "shorts" / f"{name}.mp4"


def build_audio(name, spec, WK):
    import montage
    parts, segs, words, t, GAP = [], [], [], 0.0, 0.3
    for k, sg in enumerate(spec["segs"]):
        o = WK / f"p{k}.wav"
        if "tts" in sg:
            mp = WK / f"tts{k}.mp3"
            if not mp.is_file(): montage.Job(PID).tts_eleven(len(pj["scenes"]) - 1, sg["tts"], mp)
            subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(mp), "-ar", "48000", "-ac", "2", str(o)], check=True); ws = []
        else:
            n = scn(sg["src"]); allw = WJ[str(n)]["words"]; a, b = 0, len(allw)
            if sg.get("start"): a = next(i for i, x in enumerate(allw) if norm(x["w"]) == norm(sg["start"]) and i > 2)
            if sg.get("end_before"): b = max(i for i, x in enumerate(allw) if norm(x["w"]) == norm(sg["end_before"]))
            t0 = max(0, allw[a]["s"] - 0.05); t1 = allw[b - 1]["e"] + 0.15; ws = [dict(w=x["w"], s=x["s"] - t0, e=x["e"] - t0) for x in allw[a:b]]
            subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(PD / "audio" / f"scene-{n:02d}.mp3"), "-ss", f"{t0:.3f}", "-to", f"{t1:.3f}", "-ar", "48000", "-ac", "2", str(o)], check=True)
        d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(o)], capture_output=True, text=True).stdout)
        segs.append((t, d)); words += [dict(x, s=x["s"] + t, e=x["e"] + t, seg=k) for x in ws]; parts.append(o); t += d + GAP
    sil = WK / "sil.wav"; subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", str(GAP), str(sil)], check=True)
    (WK / "list.txt").write_text("\n".join(f"file '{p.as_posix()}'\nfile '{sil.as_posix()}'" for p in parts), encoding="utf-8")
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(WK / "list.txt"), str(WK / "voice.wav")], check=True)
    return segs, words, round(t + 1.0, 2)


def cue(at, k, segs, words):
    if isinstance(at, (int, float)): return round(segs[k][0] + at, 2)
    for x in words:
        if x["seg"] == k and norm(x["w"]).startswith(norm(at)): return round(x["s"], 2)
    raise KeyError(f"palavra '{at}' nao achada no segmento {k}")


UNITS = ("billion", "million", "trillion", "thousand", "percent")


def join_decimals(words):
    """Legenda: a transcricao separa decimais ("6 36 billion", "2 point 4 billion"); junta em "6.36" / "2.4"."""
    out, i = [], 0
    while i < len(words):
        x = words[i]; nx = words[i + 1:i + 4]
        if re.fullmatch(r"\$?\d+", x["w"]) and len(nx) >= 2:
            if re.fullmatch(r"\d{1,2}", nx[0]["w"]) and nx[1]["w"].lower().strip(".,") in UNITS and nx[0]["seg"] == x["seg"]:
                out.append(dict(x, w=f'{x["w"]}.{nx[0]["w"]}', e=nx[0]["e"])); i += 2; continue
            if nx[0]["w"].lower() == "point" and len(nx) >= 2 and re.fullmatch(r"\d+[.,]?", nx[1]["w"]):
                out.append(dict(x, w=f'{x["w"]}.{nx[1]["w"]}', e=nx[1]["e"])); i += 3; continue
        out.append(x); i += 1
    return out


def build_html(name, spec, segs, words, TOT):
    D = HF / f"tricolor-{name}"; D.mkdir(exist_ok=True); (D / "assets").mkdir(exist_ok=True)
    for f in ("hyperframes.json", "AGENTS.md", "CLAUDE.md"): shutil.copy(HF / "tricolor-short1" / f, D / f)
    (D / "package.json").write_text((HF / "tricolor-short1/package.json").read_text().replace("tricolor-short1", f"tricolor-{name}"))
    (D / "meta.json").write_text('{"id":"tricolor-%s","name":"tricolor-%s","createdAt":"2026-10-30T00:00:00.000Z"}' % (name, name))
    for f in (HF / "tricolor-assets").iterdir(): shutil.copy(f, D / "assets")
    body, js, bgbody = "", [], ""
    def A(n):
        for d in ("entities", "media"):
            if (PD / d / n).is_file(): shutil.copy(PD / d / n, D / "assets" / n); return "assets/" + n
        raise FileNotFoundError(n)
    for k, sg in enumerate(spec["segs"]):
        if sg.get("bg"):  # fundo: foto cheia, escurecida, com zoom lento centrado (sem pulsar nem deslizar)
            bgbody += f'<div id="bg{k}" class="bgs" style="opacity:{1 if k == 0 else 0}"><img id="bgi{k}" src="{A(sg["bg"])}"></div>\n'
        v = sg["vis"]; s0 = round(segs[k][0], 2); s1 = round(segs[k + 1][0], 2) if k + 1 < len(segs) else TOT; ids = []; gb = []
        def el(i, style, html, cls=""):
            ids.append(i); gb.append(f'<div id="{i}" class="h {cls}" style="{style}">{html}</div>\n')
        for j, lf in enumerate(sg.get("logos") or []):  # logos dos citados, em cartoes claros
            n_ = len(sg["logos"]); el(f"lg{k}_{j}", f"left:{(1080 - (n_ * 440 + (n_ - 1) * 40)) / 2 + j * 480:.0f}px;top:1210px;width:440px;height:240px", f'<img src="{A(lf)}" style="width:100%;height:100%;object-fit:contain">', "logo")
            js.append(f'POP("#lg{k}_{j}",{s0 + .6 + j * .25:.2f})')
        if sg.get("faces"):  # rostos (cartoes de monograma) que entram um a um
            n_ = len(sg["faces"])
            for j, ff in enumerate(sg["faces"]):
                el(f"fc{k}_{j}", f"left:{(1080 - (n_ * 190 - 30)) / 2 + j * 190:.0f}px;top:1030px;width:160px;height:160px", f'<img src="{A(ff)}" style="width:160px;height:160px;object-fit:cover;border-radius:50%;border:5px solid #f4b042">')
                js.append(f'POP("#fc{k}_{j}",{s0 + .5 + j * .25:.2f})')
        if sg.get("dots"):  # bolinhas que aparecem uma a uma (contagem visual)
            n_ = sg["dots"]; t0 = cue(sg["dots_at"], k, segs, words) if sg.get("dots_at") is not None else s0 + .6
            for j in range(n_):
                el(f"dt{k}_{j}", f"left:{(1080 - (n_ * 120 - 36)) / 2 + j * 120:.0f}px;top:{sg.get('dots_y', 1040)}px;width:84px;height:84px", "", "dot")
                js.append(f'POP("#dt{k}_{j}",{t0 + j * .16:.2f})')
        if v.get("label"): el(f"lab{k}", "top:150px", v["label"], "lab w"); js.append(f'IN("#lab{k}",{s0})')
        if v.get("tag"): el(f"tag{k}", "left:400px;top:230px", v["tag"], "tag"); js.append(f'IN("#tag{k}",{s0 + .2})')
        if v["type"] == "kinetic":
            y = 520
            for j, (txt, at, st) in enumerate(v["lines"]):
                size = {"mid": 104, "amber": 190}[st]; col = "#f4b042" if st == "amber" else "#f6f2ea"
                glow = "text-shadow:0 0 60px rgba(244,176,66,.6);" if st == "amber" else ""
                el(f"k{k}_{j}", f"top:{y}px;font:700 {size}px/1.05 Inter;color:{col};{glow}", txt, "w"); y += size + 40
                t = cue(at, k, segs, words)
                js.append(f'tl.fromTo("#k{k}_{j}",{{opacity:0,scale:2.2}},{{opacity:1,scale:1,duration:.28,ease:"power4.in"}},{t})' if st == "amber" else f'IN("#k{k}_{j}",{t},.4)')
        elif v["type"] == "counter":
            el(f"n{k}", "top:620px;font:700 230px/1 Inter;letter-spacing:-.025em;color:#fff;text-shadow:0 0 50px rgba(255,255,255,.5)", "0", "w")
            el(f"s{k}", "top:900px;padding:0 90px;font:italic 500 54px/1.25 'Playfair Display';color:#f6f2ea", v["sub"], "w")
            t = min(cue(v["at"], k, segs, words), s0 + .3); p, sfx, dec = v["prefix"], v["suffix"], v["dec"]
            js.append(f'tl.set("#n{k}",{{opacity:1}},{t - .1});CT("#n{k}",{v["value"]},{t - .1},1.1,x=>"{p}"+x.toFixed({dec})+"{sfx}")')
            js.append(f'IN("#s{k}",{cue(v["sub_at"], k, segs, words)})')
            for j, (txt, at) in enumerate(v.get("pills") or []):  # etiquetas que pipocam no tempo da fala
                el(f"pp{k}_{j}", f"left:{540 - 170 + (j - (len(v['pills']) - 1) / 2) * 360:.0f}px;top:1080px;width:340px", txt, "pill")
                js.append(f'POP("#pp{k}_{j}",{cue(at, k, segs, words) - .05})')
        elif v["type"] == "rows":
            y = 420 if len(v["rows"]) > 1 else 640
            for j, (big, small, at) in enumerate(v["rows"]):
                el(f"r{k}_{j}", f"left:80px;top:{y}px;width:920px;height:260px", f'<div class="rb">{big}</div><div class="rs">{small}</div>', "row")
                js.append(f'POP("#r{k}_{j}",{(s0 + .3) if (len(v["rows"]) == 1 or j == 0) else cue(at, k, segs, words) - .1})'); y += 300  # 1o cartao entra logo: tela nunca fica so com rotulo
        elif v["type"] == "person":
            el(f"ph{k}", "left:240px;top:330px;width:600px;height:450px", '<img src="%s" style="width:600px;height:450px;object-fit:cover;border-radius:16px">' % (A(v["photo"]) if v["photo"] not in ("daniel-chu.jpg",) else "assets/" + v["photo"]))
            el(f"pn{k}", "top:840px;font:600 84px/1.1 'Playfair Display';color:#f6f2ea", v["name"], "w"); js += [f'POP("#ph{k}",{s0 + .1})', f'IN("#pn{k}",{s0 + .4})']
            y = 980
            for j, (txt, at) in enumerate(v["lines"]):
                el(f"pl{k}_{j}", f"top:{y}px;font:500 50px Inter;color:#f4b042;letter-spacing:.04em", txt, "w"); js.append(f'IN("#pl{k}_{j}",{cue(at, k, segs, words)})'); y += 80
        elif v["type"] == "bars":  # barras que crescem ate o valor falado
            y = 420
            for j, (lab_, vt, frac, col, at) in enumerate(v["items"]):
                el(f"b{k}_{j}", f"left:80px;top:{y}px;width:920px;height:190px", f'<div class="bl">{lab_}</div><div class="btr"><div class="bf" id="bf{k}_{j}" style="background:{col}"></div><span class="bv">{vt}</span></div>')
                t = (s0 + .4) if j == 0 else cue(at, k, segs, words) - .1
                js.append(f'IN("#b{k}_{j}",{t:.2f},.35)'); js.append(f'tl.to("#bf{k}_{j}",{{width:"{max(frac, .012) * 100:.1f}%",duration:.9,ease:"power2.out"}},{t + .15:.2f})'); y += 230
        elif v["type"] == "cta":
            el(f"e1_{k}", "top:720px;font:600 96px/1.1 'Playfair Display';color:#f6f2ea", "THE CRACKED<br>LEDGER", "w")
            el(f"e2_{k}", "top:1000px", "Full story on the channel", "lab w"); js += [f'IN("#e1_{k}",{s0},.6)', f'IN("#e2_{k}",{s0 + .5})']
        if sg.get("bg"):
            js.append(f'tl.fromTo("#bg{k}",{{opacity:0}},{{opacity:1,duration:.45}},{s0:.2f})' if k else "0")
            js.append(f'tl.fromTo("#bgi{k}",{{scale:1}},{{scale:1.12,duration:{max(s1 - s0 + .6, 1):.2f},ease:"none"}},{s0:.2f})')
        body += f'<div id="g{k}" class="grp">' + "".join(gb) + '</div>\n'
        if k + 1 < len(segs): js.append(f'OUT("{",".join("#" + i for i in ids)}",{s1 - .3})')
    caps, cur = [], []
    for i, x in enumerate(join_decimals(words)):
        if cur and (x["w"][:1].isupper() or x["seg"] != cur[-1]["seg"]): caps.append([cur[0]["s"], cur[-1]["e"] + .12, " ".join(c["w"] for c in cur)]); cur = []
        cur.append(x)
        if len(cur) == 3 or re.search(r"[.,]$", x["w"]): caps.append([cur[0]["s"], cur[-1]["e"] + .12, " ".join(c["w"] for c in cur)]); cur = []
    if cur: caps.append([cur[0]["s"], cur[-1]["e"] + .12, " ".join(c["w"] for c in cur)])
    for i in range(len(caps) - 1): caps[i][1] = min(caps[i][1], caps[i + 1][0])
    tpl = (HF / "tricolor-short1/index.html").read_text(encoding="utf-8")
    head = tpl[:tpl.index("</style>")] + ".row{background:#ece4d0;border-radius:18px;box-shadow:0 20px 50px rgba(0,0,0,.5);display:flex;flex-direction:column;justify-content:center;padding:0 50px}" \
        ".bgs{position:absolute;left:0;top:0;width:1080px;height:1920px;overflow:hidden}.bgs img{width:100%;height:100%;object-fit:cover;filter:brightness(.38) saturate(.9);transform-origin:50% 50%}.dot{border-radius:50%;background:#f4b042;box-shadow:0 0 30px rgba(244,176,66,.55)}.bl{font:600 40px Inter;color:#f6f2ea;margin-bottom:12px}.btr{position:relative;height:96px;background:rgba(255,255,255,.14);border-radius:16px;overflow:hidden}.bf{height:100%;width:0;border-radius:16px}.bv{position:absolute;left:26px;top:0;line-height:96px;font:700 58px Inter;color:#fff;text-shadow:0 2px 12px rgba(0,0,0,.7)}.logo{background:#ece4d0;border-radius:18px;padding:22px;box-sizing:border-box;box-shadow:0 20px 50px rgba(0,0,0,.5)}.grp{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:50% 40%}.grp>div{position:absolute}" \
        ".pill{background:#f4b042;color:#0b0e14;border-radius:40px;padding:18px 0;text-align:center;font:700 44px/1 Inter}" \
        ".rb{font:700 110px/1 Inter;color:#221e1a;letter-spacing:-.02em}.rs{font:500 36px/1.25 Inter;color:#5b5346;margin-top:14px}</style></head><body>"
    html = (head + f'<div id="root" data-composition-id="main" data-start="0" data-duration="{TOT}" data-width="1080" data-height="1920" data-fps="30">'
            f'<div id="all" class="clip" data-start="0" data-duration="{TOT}" data-track-index="0" style="left:0;top:0;width:1080px;height:1920px">{bgbody}{body}<div id="prog" style="position:absolute;left:0;top:0;height:10px;width:0;background:#f4b042"></div><div id="capbox"></div>'
            f'<div id="src">SOURCE · {spec["source"]}</div></div></div><script>\n'
            'const tl=gsap.timeline({paused:true});const $=s=>document.querySelector(s);\n'
            'const IN=(s,t,d=.5,y=24)=>tl.fromTo(s,{opacity:0,y:y},{opacity:1,y:0,duration:d,ease:"power3.out"},t);\n'
            'const OUT=(s,t,d=.3)=>tl.to(s,{opacity:0,duration:d},t);\n'
            'const POP=(s,t)=>tl.fromTo(s,{opacity:0,scale:.85,y:40},{opacity:1,scale:1,y:0,duration:.6,ease:"back.out(1.8)"},t);\n'
            'const SHAKE=t=>{tl.to("#root",{x:12,y:-8,duration:.05,repeat:5,yoyo:true},t);tl.to("#root",{x:0,y:0,duration:.05},t+.3)};\n'
            'const CT=(id,to,t,d,f)=>{const o={v:0};tl.to(o,{v:to,duration:d,ease:"power2.out",onUpdate:()=>{$(id).textContent=f(o.v)}},t)};\n'
            'const SW=t=>{const d=document.createElement("div");d.style.cssText="position:absolute;left:-600px;top:0;width:500px;height:1920px;background:linear-gradient(90deg,transparent,rgba(244,176,66,.16),transparent);transform:skewX(-12deg)";$("#all").appendChild(d);tl.fromTo(d,{x:0},{x:2300,duration:.8,ease:"power2.inOut"},t)};\n'
            f'for(let i=0;i<40;i++){{const d=document.createElement("div");const s=3+(i%4)*2;d.style.cssText="position:absolute;left:"+((i*137)%1080)+"px;top:"+((i*311)%1920)+"px;width:"+s+"px;height:"+s+"px;border-radius:50%;background:rgba(244,176,66,"+(.12+(i%3)*.08)+")";$("#all").prepend(d);tl.fromTo(d,{{y:0}},{{y:-300-(i%5)*140,duration:{TOT},ease:"none"}},0);}}\n'
            + ";\n".join(js) + ";\n"
            f'const CAPS={json.dumps([[round(a, 2), round(b, 2), c] for a, b, c in caps])};const box=$("#capbox");\n'
            'CAPS.forEach(c=>{const e=document.createElement("div");e.className="cap";e.style.opacity=0;e.innerHTML=c[2].replace(/(\\$?[0-9][0-9.,]*\\s*(billion|million|percent)?)/gi,"<b>$1</b>");box.appendChild(e);tl.set(e,{opacity:1},c[0]);tl.set(e,{opacity:0},c[1]);});\n'
            f'tl.to("#prog",{{width:1080,duration:{TOT},ease:"none"}},0);\n'
            'window.__timelines=window.__timelines||{};window.__timelines["main"]=tl;tl.seek(0);\n</script></body></html>')
    (D / "index.html").write_text(html, encoding="utf-8"); return D


def main(name):
    spec = SHORTS[name]; WK = PD / "work" / f"short_{name}"; WK.mkdir(parents=True, exist_ok=True)
    segs, words, TOT = build_audio(name, spec, WK); D = build_html(name, spec, segs, words, TOT)
    vid = WK / "video.mp4"
    subprocess.run(f'npx --yes hyperframes@0.8.191 render --output "{vid}"', cwd=D, shell=True, check=True, capture_output=True)
    out = PD / "output" / "shorts" / f"{name}.mp4"
    fc = ("[2:a]volume=0.045[m];[1:a]asplit=2[v][sc];[m][sc]sidechaincompress=threshold=0.02:ratio=12:attack=10:release=500[d];"
          "[v][d]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-2:LRA=11,alimiter=limit=0.7:level=disabled[a]")
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(vid), "-i", str(WK / "voice.wav"), "-stream_loop", "-1", "-i", str(PD / "music" / spec["music"]),
                    "-filter_complex", fc, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", str(out)], check=True)
    print(name, "ok", TOT, "s ->", out)


if __name__ == "__main__":
    main(sys.argv[1])
