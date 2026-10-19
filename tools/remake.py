# -*- coding: utf-8 -*-
"""Dark Studio - remake de um video ja pronto com o acabamento novo (o original nao e alterado).
Etapas (todas por padrao, ou --steps copy,convert,...):
  copy      copia o projeto para <id-curto>-ec-<data> (midia, narracao, entidades, graficos, musica)
  convert   graficos do gfx.py -> scenes[i]["ec"] (EffectCraft); o que nao tem equivalente fica como PNG/animacao do gfx.py
  cues      deixas musicais automaticas (abertura, capitulos, impacto, desfecho)
  sheet     folha de contato de logos/selos/fotos usados (conferir antes de renderizar: o Commons tem logos errados)
  cards     cartao de capitulo antigo (gfx/full-NN.png com texto) -> card-NN.png sem texto: senao o capitulo sai duplicado
  words     tempo de cada palavra (tools/words.py)        clean    apaga texto escrito pelo Grok (tools/media_ai.py)
  local     cenas ainda sem midia: imagem gerada na placa (tools/local_img.py, FLUX.2 Klein), depois o parallax anima
  parallax  fotos reais em tela cheia viram plano 2.5D    gfx      renderiza no EffectCraft (tools/ec_gfx.py)
  validate  Validacao do pipeline (sem correcao automatica)          montage  tools/montar.py (caminho EffectCraft)
Uso: python tools/remake.py <projeto_original> [--steps convert,cues] [--new <id>]
Video novo (roteiro com flow/relmap/stack/list/takeaway/real_photo), no proprio projeto, depois da narracao e ANTES do Grok/Flow:
  python tools/remake.py <id> --new <id> --steps convert,cues,sheet,words,gfx
  -> as cenas convertidas ganham arquivo (grafico ou foto real) e o worker as pula; so o resto vai para o Grok/Flow.
  Sem Grok/Flow (cenas de clima e lugar): depois do passo acima, --steps local,clean,parallax,validate,montage
  -> o resto vira imagem local animada; cena que precisa de acao de pessoas: gerar antes no Grok/Flow (ja tera arquivo e e pulada).
"""
import argparse, collections, json, re, shutil, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]; P = ROOT / "projects"; PY = sys.executable
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tools"))
import scenes  # noqa: E402
import projfile  # noqa: E402
MUSIC = {"E": "echoes-of-time-v2.mp3", "S": "stay-the-course.mp3", "I": "interloper.mp3", "K": "darkest-child.mp3"}
TITLES = {"E": "Echoes of Time v2", "S": "Stay the Course", "I": "Interloper", "K": "Darkest Child"}
CREDIT = "Kevin MacLeod (incompetech.com), licensed under Creative Commons: By Attribution 4.0, https://creativecommons.org/licenses/by/4.0/"
IMPACT = re.compile(r"bankrupt|chapter 11|collaps|indict|guilty|sentenc|fraud|seiz|fail|run on|withdr", re.I)


def roman(n):
    out = ""
    for v, s in ((10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")):
        while n >= v: out += s; n -= v
    return out


def unit(u):
    u = (u or "").strip(); pre = "$" if u.startswith("$") else ""; rest = u.lstrip("$").strip()
    suf = {"B": " BILLION", "BN": " BILLION", "M": " MILLION", "K": " THOUSAND", "%": "%", "": ""}.get(rest.upper(), " " + rest)
    return pre, suf


def cut(t, n):
    """Corta no ultimo espaco, nunca no meio da palavra ('...POINT BONIT')."""
    return t if len(t) <= n else t[:n].rsplit(" ", 1)[0].rstrip(" ,;:-·")


def src_title(src, scene):
    """Fonte legivel: link -> titulo da fonte verificada da cena com esse link (ou a primeira); nunca 'Fdic.Gov'."""
    src = (src or "").strip(); srcs = scene.get("sources") or []
    if src.startswith("http") or not src:
        hit = next((x for x in srcs if x.get("url") and (x["url"] in src or src in x["url"])), None) or (srcs[0] if srcs else None)
        if hit and hit.get("title"): return hit["title"][:70]
        return re.sub(r"^https?://(www\.)?", "", src).split("/")[0]
    return src[:70]


def convert(pj):
    """gfx (gfx.py) -> ec (tools/ec_gfx.py). Retorna contagem por tipo convertido/mantido."""
    ents = {e["name"]: e for e in pj.get("entities") or []}
    alias = {a.lower(): e for e in ents.values() for a in [e["name"]] + list(e.get("aliases") or [])}
    def asset(n):
        e = ents.get(n) or {}
        return e.get("logo") or e.get("seal")
    def node(n, credits):  # parte de um flow/relmap: logo da entidade, foto se for pessoa, senao cartao de texto
        name = n.get("name") or ""; e = alias.get(name.lower()) or {}
        out = {"label": name.upper()[:28], "sub": n.get("note") or n.get("relation") or "", "say": n.get("say") or name}
        if e.get("logo") or e.get("seal"): out["file"] = e.get("logo") or e.get("seal")
        elif e.get("kind") == "person" and e.get("photo"):
            out.update(file=e["photo"], h=300); credits.append((e.get("credits") or {}).get("photo", ""))
        for k in ("alert_say", "alert_label"):
            if n.get(k): out[k] = n[k] if k == "alert_say" else n[k].upper()
        if n.get("bar") is not None:
            out.update(bar=float(n["bar"]), bar_label=(n.get("bar_label") or "").upper(), bar_color="red" if n.get("bar_alert") else "amber")
        return out
    stat = collections.Counter(); used_photos = set(); diagrams = collections.Counter()
    def sig(g):  # mesmas partes = mesmo diagrama, seja flow ou relmap
        return frozenset(str(x).lower() for x in [n.get("name", "") for n in g.get("nodes") or []] + ([g["center"]] if g.get("center") else []))
    for s in pj["scenes"]:
        gfx = s.get("gfx_legacy") or s.get("gfx") or []; ov, full, keep, rec = [], None, [], []  # gfx_legacy: pode rodar de novo
        def recusa(g, motivo):  # a cena vira IA (scenes.kind): o item fica guardado com o motivo, nao volta para gfx
            rec.append(dict(g, motivo=motivo)); stat["recusado: " + motivo] += 1
        chips, people, others, callouts = [], [], [], []
        explicit = {g.get("name") for g in gfx if g.get("type") == "lower_third"}
        for g in gfx:
            t = g.get("type")
            if t == "chapter":
                ov.append({"type": "chapter", "num": roman(int(g.get("number") or 1)), "title": g.get("title", "")}); stat[t] += 1
            elif t == "lower_third":
                ov.append({"type": "lower_third", "name": g["name"], "role": (g.get("role") or "").upper()[:60]}); stat[t] += 1
            elif t == "entity":
                n = g.get("name"); e = ents.get(n) or {}
                if asset(n): chips.append(asset(n))
                elif n not in explicit: (people if e.get("kind") == "person" else others).append((n, e.get("role") or (e.get("kind") or "").upper()))
                stat[t] += 1
            elif t == "parties":
                for n in g.get("items") or []:
                    if asset(n): chips.append(asset(n))
                    else: others.append((n, "ALSO INVOLVED"))
                stat[t] += 1
            elif t == "logo":  # logo da empresa citada: o mesmo selo do canto (antes ficava como PNG antigo que a montagem EC nao desenha)
                n = g.get("company") or g.get("name") or ""; e = alias.get(n.lower()) or {}
                if e.get("logo") or e.get("seal"): chips.append(e.get("logo") or e.get("seal"))
                elif n: others.append((n, "ALSO INVOLVED"))
                stat[t] += 1
            elif t in ("callout", "citation"):
                callouts.append({"type": "callout", "label": cut(src_title(g.get("source"), s).upper(), 46) or ("SOURCE" if t == "citation" else "KEY FACT"),
                                 "text": g.get("text", ""), "_citation": t == "citation"}); stat[t] += 1
            elif t == "timeline" and len(g.get("events") or []) <= 6:
                full = {"type": "timeline", "title": g.get("title", ""), "highlight": g.get("highlight", len(g["events"]) - 1),
                        "events": [{"date": str(e.get("date", "")).upper(), "label": e.get("label", "")} for e in g["events"]],
                        "source": src_title(g.get("source"), s)}; stat[t] += 1
            elif t == "chart" and 1 <= len(g.get("series") or []) <= 2:
                pre, suf = unit(g.get("unit")); ser = g["series"]; src = g.get("source", "")
                src = src_title(src, s)
                if len(ser) == 1:
                    v = float(ser[0]["value"])  # prejuizo vem negativo: o contador anima o valor absoluto com "-" na frente
                    full = {"type": "counter", "prefix": ("-" if v < 0 else "") + pre, "value": abs(v), "dec": 0 if v == int(v) else 1, "suffix": suf,
                            "label": cut(ser[0]["label"].upper(), 40), "sub": g.get("title", ""), "source": src}
                else:
                    cols = ["teal", "red"] if g.get("highlight", 1) == 1 else ["red", "teal"]
                    full = {"type": "versus", "title": g.get("title", ""), "source": src, "items": [  # barra pelo tamanho; negativo fica vermelho
                        {"label": cut(x["label"].upper(), 30), "prefix": pre, "value": abs(float(x["value"])), "dec": 0 if float(x["value"]) == int(float(x["value"])) else 1,
                         "suffix": suf.replace(" BILLION", "B").replace(" MILLION", "M"), "color": "red" if float(x["value"]) < 0 else c} for x, c in zip(ser, cols)]}
                stat["chart"] += 1
            elif t == "quote":
                full = {"type": "statement", "label": (g.get("speaker") or "").upper()[:50], "text": g.get("text", ""),
                        "sub": g.get("role", ""), "source": g.get("source", "")}; stat[t] += 1
            elif t in ("flow", "relmap") and diagrams[sig(g)] >= 2:
                recusa(g, "mesmo diagrama pela 3a vez")
            elif t == "flow" and 2 <= len(g.get("nodes") or []) <= 3:  # tempos: tools/ec_gfx.py timing() pelo "say"
                cr = []
                full = {"type": "flow", "label": (g.get("label") or g.get("title") or "").upper()[:44],
                        "nodes": [node(n, cr) for n in g["nodes"]], "source": src_title(g.get("source"), s),
                        "edges": [{k: (e[k].upper() if k.endswith("label") else e[k]) for k in
                                   ("from", "to", "label", "say", "stop_say", "stop_label", "alert_say", "alert_label") if e.get(k) is not None}
                                  for e in g.get("edges") or [] if 0 <= int(e.get("from", -1)) < len(g["nodes"]) and 0 <= int(e.get("to", -1)) < len(g["nodes"])]}
                if g.get("note"): full.update(note=g["note"], note_say=g.get("note_say"), note_color="red" if g.get("note_alert") else "cream")
                if any(cr): full["credit"] = "Photo: " + next(c for c in cr if c)
                stat[t] += 1; diagrams[sig(g)] += 1
            elif t == "relmap" and 2 <= len(g.get("nodes") or []) <= 4:
                cr = []; sats = [node(n, cr) for n in g["nodes"]]
                for x, n in zip(sats, g["nodes"]):
                    if not x.get("file"): x["label"] = (n.get("name") or "")[:28]  # cartao de texto: grafia original ("JPMorgan Chase")
                full = {"type": "relmap", "title": g.get("title", ""), "sats": sats,
                        "center": node({"name": g.get("center", ""), "note": g.get("center_role", ""), "say": g.get("center_say")}, cr),
                        "source": src_title(g.get("source"), s)}
                if any(cr): full["credit"] = "Photo: " + next(c for c in cr if c)
                stat[t] += 1; diagrams[sig(g)] += 1
            elif t == "stack" and len({float(x.get("fill") or 0) for x in g.get("tiers") or []}) == 1 and g.get("tiers"):
                full = {"type": "list", "label": (g.get("label") or g.get("title") or "").upper()[:40],  # barras iguais nao dizem nada: vira lista
                        "items": [{"text": x.get("label", ""), "say": x.get("say") or x.get("label", "")} for x in g["tiers"]]}
                stat["stack -> list"] += 1
            elif t == "stack" and 2 <= len(g.get("tiers") or []) <= 4:
                full = {"type": "stack", "label": (g.get("label") or "").upper()[:40], "title": g.get("title", ""), "source": src_title(g.get("source"), s),
                        "tiers": [{"label": x.get("label", ""), "sub": x.get("note", ""), "fill": max(0.0, min(1.0, float(x.get("fill") or 0))),
                                   "say": x.get("say")} for x in g["tiers"]]}
                if g.get("highlight") is not None:
                    full.update(highlight=int(g["highlight"]), highlight_label=(g.get("highlight_label") or "").upper(), highlight_say=g.get("highlight_say"))
                if g.get("illustrative", True): full["note"] = "ILLUSTRATIVE ORDER"  # sem numero com fonte, a barra e so a ordem
                stat[t] += 1
            elif t == "list" and 2 <= len(g.get("items") or []) <= 4:
                full = {"type": "list", "label": (g.get("label") or "").upper()[:40], "items": [{"text": str(x), "say": str(x)} for x in g["items"]]}
                stat[t] += 1
            elif t == "takeaway" and g.get("text") and len(g["text"].split()) <= 12:  # frase longa = narracao escrita na tela: fica a IA
                full = {"type": "statement", "label": (g.get("label") or "").upper()[:40], "text": g["text"], "sub": g.get("sub", "")}; stat[t] += 1
            elif t == "real_photo":  # foto real do Commons na cena inteira (tools/parallax.py anima depois)
                e = alias.get(str(g.get("entity") or "").lower()) or {}
                k = g.get("which") or ("photo" if e.get("kind") == "person" else "hq_photo")
                f = e.get(k) or e.get("hq_photo") or e.get("photo")
                if f and f not in used_photos:  # a mesma foto uma vez por video
                    used_photos.add(f)
                    k = k if e.get(k) else ("hq_photo" if e.get("hq_photo") else "photo")
                    s.setdefault("orig_file", s.get("file")); credit = (e.get("credits") or {}).get(k, "")
                    s.update(file=f, source="real_photo", mode="image", status="pronto", photo_credit="Photo: " + credit if credit else "")
                    ov.append({"type": "tag", "text": "  ·  ".join(x for x in (e["name"].upper(), str(g.get("place") or "").upper()) if x), "start": 0.6})
                    if credit: ov.append({"type": "credit", "text": "Photo: " + credit})
                    stat[t] += 1
                else:
                    recusa(g, "foto real sem foto ou ja usada")
            elif t in scenes.FULL and t not in scenes.PIL_FULL:  # so o EffectCraft desenharia e ele nao aceitou (tamanho, frase longa)
                recusa(g, f"{t} fora do limite do EffectCraft")
            else:
                keep.append(g); stat["mantido:" + str(t)] += 1  # o gfx.py desenha (tools/produce.py chama na etapa render_graficos)
        if full:  # logo que ja esta num cartao do grafico nao se repete no canto
            shown = {x.get("file") for k in ("nodes", "sats") for x in full.get(k) or []} | {(full.get("center") or {}).get("file")}
            chips = [c for c in chips if c not in shown]
        if chips: ov.append({"type": "chip", "files": list(dict.fromkeys(chips))[:4]})
        for n, role in people[:2]:  # um lower third por pessoa: a Validacao exige o nome exato (nada de "A · B")
            ov.append({"type": "lower_third", "name": n, "role": (role or "").upper()[:50]})
        others += people[2:]
        if others:  # empresas sem logo: um destaque com todos os nomes
            callouts.append({"type": "callout", "label": "ALSO INVOLVED", "text": ", ".join(dict.fromkeys(n for n, _ in others[:4]))})
        if any(c.get("label") != "SOURCE" and c["text"] and any(ch.isdigit() for ch in c["text"]) for c in callouts):
            callouts = [c for c in callouts if not c.pop("_citation", False)]  # a fonte ja esta no rotulo dos valores
        for c in callouts: c.pop("_citation", None)
        stagger([o for o in ov if o["type"] == "lower_third"]); stagger(callouts)
        ov += callouts[:3]
        s["gfx_legacy"] = gfx; s["gfx"] = keep  # s["gfx"] so com o que continua vindo do gfx.py (Validacao le gfx + ec)
        if rec: s["gfx_recusado"] = rec
        else: s.pop("gfx_recusado", None)
        s["ec"] = {k: v for k, v in (("full", full), ("overlay", ov)) if v}
        if not s["ec"]: s.pop("ec")
    return stat


def stagger(items, t0=0.6, slot=4.3):
    """Itens no mesmo canto aparecem um depois do outro (o ultimo fica ate o fim da cena)."""
    for k, e in enumerate(items):
        e["start"] = round(t0 + k * slot, 2)
        if k < len(items) - 1: e["end"] = round(e["start"] + slot - 0.4, 2)


def cues(pj):
    sc = pj["scenes"]; n = len(sc); out = []; off = collections.Counter()
    def add(a, b, k, why, **kw):
        out.append({"from_scene": a, "to_scene": b, "file": "music/" + MUSIC[k], "offset": off[k] * 60, "volume": 0.17, "why": why, **kw}); off[k] += 1
    add(1, 3, "E", "abertura")
    imp = set()
    for i, s in enumerate(sc, 1):
        ec = s.get("ec") or {}; txt = json.dumps(ec, ensure_ascii=False) + " ".join(g.get("type", "") for g in s.get("gfx") or [])
        if (ec.get("full") or {}).get("type") == "stamp" or "collapse" in txt or "moneyflow" in txt or \
                any(e.get("type") == "callout" and IMPACT.search(e.get("text", "")) for e in ec.get("overlay") or []):
            imp.add(i)
    for i, s in enumerate(sc, 1):
        if i <= 3 or i > n - 3: continue
        if i in imp and (i - 1) not in imp:
            j = i
            while j + 1 in imp or j + 2 in imp: j += 1
            add(max(4, i - 1), min(n - 3, j), "I", "momento de impacto")
        elif any(e.get("type") == "chapter" for e in (s.get("ec") or {}).get("overlay") or []) and not any(c["from_scene"] <= i <= c["to_scene"] for c in out):
            add(i, i, "S" if len(out) % 2 else "E", "capitulo")
    add(n - 2, n, "K", "desfecho", tail=0, fade_out=4)
    pj["music_cues"] = sorted(out, key=lambda c: c["from_scene"])
    pj["music_tracks"] = [{"file": "music/" + MUSIC[k], "title": TITLES[k], "credit": CREDIT} for k in "ESIK"]
    return len(out)


def sheet(pdir, pj, out):
    from PIL import Image, ImageDraw
    files = []
    for s in pj["scenes"]:
        ec = s.get("ec") or {}
        for e in ([ec.get("full")] if ec.get("full") else []) + list(ec.get("overlay") or []):
            files += [e.get("file"), e.get("photo")] + list(e.get("files") or []) + [x.get("file") for x in e.get("items") or [] if isinstance(x, dict)]
    files = [f for f in dict.fromkeys(files) if f and (pdir / f).is_file()]
    W, H = 300, 170; cols = 5; rows = max(1, (len(files) + cols - 1) // cols)
    sh = Image.new("RGB", (W * cols, (H + 20) * rows), (60, 60, 60)); d = ImageDraw.Draw(sh)
    for k, f in enumerate(files):
        im = Image.open(pdir / f).convert("RGBA"); bg = Image.new("RGBA", im.size, (236, 228, 208, 255)); im = Image.alpha_composite(bg, im).convert("RGB")
        im.thumbnail((W - 10, H - 10)); x, y = (k % cols) * W, (k // cols) * (H + 20)
        sh.paste(im, (x + (W - im.width) // 2, y + 5)); d.text((x + 4, y + H + 3), Path(f).name[:40], fill=(255, 255, 255))
    sh.save(out, quality=88); return len(files)


def kit(pdir, pj, orig_pj):
    """output/youtube_kit.json a partir da descricao ORIGINAL (output/original_kit.json, lida do Studio): capitulos com os
    tempos do remake, musicas novas; titulo, tags, fontes e creditos iguais. Thumbnail = a publicada no original."""
    import shorts
    src = json.loads((pdir / "output" / "original_kit.json").read_text(encoding="utf-8")); desc = src["description"]
    D, st = shorts.timeline(pdir, pj["scenes"])
    chap = [(int(st[i]), e["title"]) for i, s in enumerate(pj["scenes"]) for e in (s.get("ec") or {}).get("overlay", []) if e["type"] == "chapter"]
    old = re.search(r"CHAPTERS\n((?:\d+:\d\d .*\n?)+)", desc)
    if not chap or chap[0][0] > 0:  # o YouTube exige um capitulo em 0:00: usa o nome da abertura do original
        chap.insert(0, (0, old.group(1).splitlines()[0].split(" ", 1)[1] if old else "Introduction"))
    lines = "\n".join(f"{t // 60}:{t % 60:02d} {c}" for t, c in chap)
    if old: desc = desc.replace(old.group(1).rstrip("\n"), lines)
    desc = re.sub(r'(MUSIC\n)"[^\n]*by Kevin MacLeod', r'\1' + ", ".join(f'"{t}"' for t in TITLES.values()) + " by Kevin MacLeod", desc)
    assert len(desc) <= 5000, len(desc)
    cover = orig_pj.get("thumbnail") or orig_pj.get("cover")
    if cover: shutil.copyfile(P / orig_pj["id"] / cover, pdir / "output" / "thumb.jpg")
    k = {"title": src["title"], "description": desc, "tags": src.get("tags") or []}
    (pdir / "output" / "youtube_kit.json").write_text(json.dumps(k, ensure_ascii=False, indent=2), encoding="utf-8")
    return lines


def cards(pn, pj):
    """Apaga 'CHAPTER N' + titulo + sublinhado do cartao antigo com LaMa; o capitulo do EffectCraft entra sozinho por cima."""
    import media_ai as M
    from PIL import Image, ImageDraw
    out = []
    for i, s in enumerate(pj["scenes"]):
        if (s.get("gfx_legacy") or [{}])[0].get("type") != "chapter" or not s["file"].startswith("gfx/full-"): continue
        img = Image.open(pn / s["file"]).convert("RGB"); boxes = M.ocr(img, min_score=0.3, min_len=1)
        assert boxes, f"cena {i+1}: nenhum texto no cartao"
        xs = [p[0] for b, _, _ in boxes for p in b]; ys = [p[1] for b, _, _ in boxes for p in b]; h = max(ys) - min(ys)
        m = Image.new("L", img.size, 0)
        ImageDraw.Draw(m).rectangle([min(xs) - h * .3, min(ys) - h * .25, max(xs) + h * .3, max(ys) + h * .6], fill=255)  # .6: sublinhado
        s["file"] = f"gfx/card-{i+1:02d}.png"; M.inpaint(img, m).save(pn / s["file"]); out.append(i + 1)
        for e in (s.get("ec") or {}).get("overlay", []):
            if e["type"] == "chapter": e["end"] = 999  # titulo ate o fim da cena (o ec_gfx limita a duracao); sem ele o cartao fica vazio
    return out


def run(*args):
    r = subprocess.run([PY] + list(args), cwd=ROOT, env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8"})
    if r.returncode: raise RuntimeError(f"falhou: {' '.join(map(str, args))}")  # RuntimeError: o produce.py registra e retoma


def copy(old, new):
    """Copia o projeto antigo para <new> (midia, narracao, entidades, graficos, musica) sem alterar o original."""
    po, pn = P / old, P / new; fn = P / f"{new}.json"
    assert not pn.exists(), f"{new} ja existe"
    pn.mkdir()
    for d in ("media", "audio", "entities", "gfx", "music", "assets"):
        if (po / d).is_dir(): shutil.copytree(po / d, pn / d)
    copy_music(pn)
    pj = json.loads((P / f"{old}.json").read_text(encoding="utf-8"))
    pj.update(id=new, remake_of=old, status="draft")
    for k in ("published_url", "scheduled_at", "published_at", "legacy_complete", "validation"): pj.pop(k, None)
    projfile.create(fn, pj); print("copia:", new)


def copy_music(pn):
    """Trilhas de suspense (aprovadas no remake do WeWork) em <projeto>/music/, onde as deixas apontam."""
    (pn / "music").mkdir(exist_ok=True)
    for f in MUSIC.values():
        if not (pn / "music" / f).is_file(): shutil.copyfile(ROOT / "library" / "music" / "incompetech" / f, pn / "music" / f)


def run_steps(new, steps, old=None):
    """Etapas sobre um projeto que ja existe. O produce.py chama esta funcao direto, sem abrir outro processo.
    As do proprio modulo rodam aqui; as ferramentas com dependencias proprias (FLUX, EffectCraft, OCR) em processo separado."""
    pn, fn = P / new, P / f"{new}.json"
    if "convert" in steps:
        with projfile.edit(fn) as pj: print("convertido:", dict(convert(pj)))
    if "cues" in steps:
        with projfile.edit(fn) as pj: print("deixas musicais:", cues(pj))
        copy_music(pn)  # projeto novo (produce) nao passa pelo copy: as deixas apontam para music/
    pj = projfile.read(fn)
    if "sheet" in steps:
        out = pn / "logs" / "logos-sheet.jpg"; out.parent.mkdir(exist_ok=True); print("folha de logos/fotos:", sheet(pn, pj, out), "->", out)
    if "cards" in steps:
        with projfile.edit(fn) as pj: print("cartoes limpos:", cards(pn, pj))
    if "words" in steps: run("tools/words.py", new)
    if "local" in steps: run("tools/local_img.py", new)  # cenas sem midia: FLUX na placa (antes do clean, que apaga texto escrito)
    if "clean" in steps: run("tools/media_ai.py", "clean", new)
    if "parallax" in steps: run("tools/parallax.py", new)
    if "gfx" in steps: run("tools/ec_gfx.py", new)
    if "validate" in steps:
        import pipeline
        v = pipeline.validate(new, autofix=False); print("validacao ok:", v["ok"])
        for g in v["gaps"]: print("  cena", g["scene"], g["missing"])
    if "montage" in steps: run("tools/montar.py", new, "--step", "render", "--sem-graficos")
    if "kit" in steps:
        print("capitulos:\n" + kit(pn, projfile.read(fn), json.loads((P / f"{old or new}.json").read_text(encoding="utf-8"))))


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("project"); ap.add_argument("--steps", default="copy,convert,cues,sheet,cards")
    ap.add_argument("--new", help="id do remake (padrao: <prefixo>-ec-<data>)")
    a = ap.parse_args(); steps = a.steps.split(",")
    old = a.project; new = a.new or "-".join(old.split("-")[:4]) + "-ec-" + time.strftime("%Y%m%d")
    if "copy" in steps: copy(old, new)
    run_steps(new, steps, old)


if __name__ == "__main__":
    main()
