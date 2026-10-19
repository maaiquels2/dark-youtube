"""Dark Studio - etapas do fluxo: Pesquisa (dossie) -> Roteiro do dossie -> Imagens reais -> Prompts Grok -> Validacao.
Usa app.chat_json (OpenAI, so texto). Imagens reais vem de fontes licenciadas (Wikimedia Commons) com credito."""
import json, re, time, urllib.request, urllib.parse, urllib.error
from pathlib import Path
import entities as E

def _app():
    import app; return app

def _load(pid):
    a = _app(); return a.load_project(pid)

def _save(d):
    a = _app()
    with a.LOCK:
        a.proj_path(d["id"]).write_text(json.dumps({k: v for k, v in d.items() if not k.startswith("_")}, ensure_ascii=False, indent=2), encoding="utf-8")
    return d

def url_ok(u):
    try:
        r = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 Chrome/130"}), timeout=20)
        return r.status < 400
    except urllib.error.HTTPError as e:
        return e.code in (401, 403, 429)  # existe, mas bloqueia robos
    except Exception:
        return False

# ---------------- 1) Pesquisa ----------------
def research(pid):
    d = _load(pid); a = _app()
    if not (d.get("facts") or d.get("research_notes")):
        raise a.ApiError("Cole as notas de pesquisa (fatos com fontes) no campo de pesquisa antes de gerar o dossie.")
    sys = ("You are a meticulous research editor for a documentary channel. Build a research dossier ONLY from the notes given. "
           "Never add facts, names, numbers or URLs that are not in the notes. Reply only in json.")
    u = ("Organize these research notes into a dossier grouped by story chapter (chronological, 6-10 chapters). "
         "For every fact keep date, amount (if any), the exact source URL from the notes, and whether it is an allegation. "
         "List ALL people (including judges, prosecutors, defendants, cooperators, executives), companies/funds/banks, government agencies and courts mentioned, "
         "with role and legal status where relevant. json: {\"chapters\":[{\"title\":\"...\",\"summary\":\"...\",\"facts\":[{\"date\":\"...\",\"text\":\"...\","
         "\"amount\":\"\",\"allegation\":false,\"url\":\"...\"}]}],\"people\":[{\"name\":\"...\",\"role\":\"...\",\"status\":\"...\"}],"
         "\"companies\":[{\"name\":\"...\",\"role\":\"...\"}],\"agencies\":[{\"name\":\"...\",\"full_name\":\"...\"}],\"courts\":[{\"name\":\"...\",\"full_name\":\"...\"}]}\n\nNOTES:\n"
         + (d.get("research_notes") or d.get("facts")))
    dos = a.chat_json(sys, u, 16000)
    cache = {}
    for ch in dos.get("chapters") or []:
        for f in ch.get("facts") or []:
            uu = f.get("url") or ""
            if uu.startswith("http"):
                if uu not in cache: cache[uu] = url_ok(uu)
                f["url_ok"] = cache[uu]
    dos["sources_checked"] = len(cache); dos["sources_ok"] = sum(cache.values())
    d["dossier"] = dos; _save(d)
    return dos

def dossier_text(dos):
    out = []
    for i, ch in enumerate(dos.get("chapters") or [], 1):
        out.append(f"CHAPTER {i}: {ch.get('title')} - {ch.get('summary','')}")
        for f in ch.get("facts") or []:
            out.append(f"- {f.get('date','')}: {'[ALLEGATION] ' if f.get('allegation') else ''}{f.get('text')} {f.get('amount') or ''} {f.get('url','')}".strip())
    for k in ("people", "companies", "agencies", "courts"):
        if dos.get(k): out.append(k.upper() + ": " + "; ".join(f"{x.get('name')} ({x.get('full_name') or x.get('role','')}{', ' + x['status'] if x.get('status') else ''})" for x in dos[k]))
    return "\n".join(out)

# ---------------- 2) Roteiro a partir do dossie ----------------
def script_from_dossier(pid, gfx=True):
    """gfx=False: so a narracao; os graficos vem em plan_gfx (duas etapas: o roteiro inteiro estourou o tempo da API)."""
    d = _load(pid); a = _app()
    if not d.get("dossier"): raise a.ApiError("Gere o dossie de pesquisa primeiro (etapa Pesquisa).")
    p = dict(d, facts=dossier_text(d["dossier"]))
    r = a.write_script(p, gfx=gfx)
    keep = {k: d[k] for k in d if k not in ("scenes", "hook", "retention_beats", "description", "validation", "prompts_enriched")}
    keep.update({k: r[k] for k in ("hook", "retention_beats", "description", "scenes") if k in r})
    keep["script_from_dossier"] = True
    return a.save_project(keep)

def plan_gfx(pid, batch=20):
    """Segunda etapa do roteiro: com a narracao pronta, o modelo escolhe os graficos de cada cena (app.GFX_SPEC), em lotes,
    levando os tipos das 3 cenas anteriores para respeitar as regras de sequencia. Testado no WeWork em 18/10: ~3 min, 51% sem IA."""
    d = _load(pid); a = _app(); sc = d["scenes"]
    facts = dossier_text(d["dossier"]) if d.get("dossier") else "\n".join(
        dict.fromkeys(f"- {f} (source: {(s.get('sources') or [{}])[0].get('title', '')})" for s in sc for f in s.get("key_facts") or []))
    full = set(FULL_GFX) | {"real_photo"}; full.discard("chapter"); kinds = []
    chapters = ", ".join(str(i + 1) for i, s in enumerate(sc) if s.get("chapter"))
    sys_ = ("You are the graphics director of a faceless business documentary channel. Use only the verified facts given, with their source. "
            "Never invent numbers, quotes or sources. Reply only in JSON (a single json object).")
    for st in range(0, len(sc), batch):
        prev = " ".join(f"#{k + 1}:{t}" for k, t in enumerate(kinds[-3:], len(kinds) - len(kinds[-3:])))
        lines = "\n".join(f"{i + 1}: {s['narration']}" for i, s in enumerate(sc[st:st + batch], st))
        u = ("Verified facts you may use (with sources):\n" + facts + "\n\n" + a.GFX_SPEC + "\n"
             + (f"Full-screen types of the previous scenes (keep the sequence rules across batches): {prev}\n" if prev else "")
             + (f"Chapters start at scenes {chapters}: put a chapter item on each of them.\n" if chapters else "")
             + 'For each scene below choose its gfx list following the VISUAL DECISION.\njson: {"scenes":[{"i":<scene number>,"gfx":[...]}]}\n\n' + lines)
        got = {int(x["i"]): x.get("gfx") or [] for x in a.chat_json(sys_, u, 12000).get("scenes") or [] if str(x.get("i", "")).isdigit()}
        for i in range(st, min(st + batch, len(sc))):
            g = [x for x in got.get(i + 1, []) if isinstance(x, dict) and x.get("type")]
            if sc[i].get("chapter") and not any(x["type"] == "chapter" for x in g):  # capitulo do roteiro nunca se perde
                g.insert(0, {"type": "chapter", "number": 1 + sum(1 for s in sc[:i] if s.get("chapter")), "title": sc[i]["chapter"]})
            sc[i]["gfx"] = g; kinds.append(next((x["type"] for x in g if x["type"] in full), "IA"))
    d["gfx_planned"] = True
    return a.save_project(d)

# ---------------- 3) Imagens reais ----------------
def _commons_search(q, n=6):
    u = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({"action": "query", "list": "search", "srsearch": q, "srnamespace": 6, "srlimit": n, "format": "json"})
    r = json.load(urllib.request.urlopen(urllib.request.Request(u, headers=E.UA), timeout=20))
    return [x["title"] for x in r["query"]["search"]]

def _pick(titles, must, phrase=None):
    for t in titles:
        low = t.lower()
        if phrase and phrase.lower() not in low: continue
        if all(m.lower() in low for m in must) and not low.endswith((".pdf", ".djvu", ".tif", ".tiff")): return t
    return None

JUNK = re.compile(r"^(unnamed|other|various|unknown|several)\b", re.I)

def collect_images(pid, curated=None):
    """Mescla registro curado + entidades do dossie; busca automatica estrita no Commons (selo/logo/foto) com credito."""
    d = _load(pid); pdir = _app().PROJECTS / Path(pid).name
    reg = {e["name"]: e for e in d.get("entities") or []}
    for e in curated or []: reg[e["name"]] = {**reg.get(e["name"], {}), **e}
    dos = d.get("dossier") or {}
    for k, kind in (("people", "person"), ("companies", "company"), ("agencies", "agency"), ("courts", "court")):
        for x in dos.get(k) or []:
            n = x.get("name")
            if n and JUNK.match(n): continue
            if n and not any(n.lower() in [m.lower() for m in E._names(e)] for e in reg.values()):
                reg[n] = {"name": n, "kind": kind, "full_name": x.get("full_name"), "role": x.get("role") or x.get("status") or "", "aliases": []}
    log = []
    idx = E._lib_index()  # 1o: biblioteca local (nao gasta busca nem download)
    for e in reg.values():
        got = E.library_apply(e, pdir, idx)
        if got: log.append(f"{e['name']}: biblioteca <- {', '.join(got)}")
    for e in reg.values():
        if E.has_real_asset(e) or e.get("no_auto") or e.get("kind") == "person": continue  # pessoas: so foto curada (evita homonimos)
        time.sleep(5)
        n = e.get("full_name") or e["name"]; t = None; key = None
        try:
            if e["kind"] == "agency": t = _pick(_commons_search("Seal of the " + n), ["seal"], phrase=n.replace("U.S. ", "United States ")); key = "seal"
            elif e["kind"] in ("company", "fund"): t = _pick(_commons_search(n + " logo"), ["logo"], phrase=e["name"]); key = "logo"
            if t:
                ext = ".png" if t.lower().endswith((".svg", ".png")) else ".jpg"
                rel = f"entities/{re.sub('[^a-z0-9]+','-',e['name'].lower())}-{key}{ext}"
                info = E.fetch_commons(t, pdir / rel); e[key] = rel
                e.setdefault("credits", {})[key] = info["credit"]; e["credits"][key + "_source"] = info["source"]
                log.append(f"{e['name']}: {key} <- {t}")
        except Exception as ex:
            log.append(f"{e['name']}: erro {ex}")
    for e in reg.values():  # guarda o que foi achado para os proximos videos
        try:
            sv = E.library_save(e, pdir)
            if sv: log.append(f"{e['name']}: salvo na biblioteca ({', '.join(sv)})")
        except Exception as ex:
            log.append(f"{e['name']}: biblioteca erro {ex}")
    d["entities"] = list(reg.values()); d["images_done"] = True; _save(d)
    return {"entities": len(reg), "with_real_visual": sum(1 for e in reg.values() if E.has_real_asset(e)), "log": log}

# ---------------- 4) Prompts Grok ricos ----------------
ARC = {
 "act1": "ACT 1 euphoria, money flowing: warm golden light, bustling energy, busy workplaces of THIS story (offices, trading floors, factories or shops as the narration says), deals and celebrations, smooth confident camera moves",
 "act2": "ACT 2 tension and suspicion: cold blue-grey light, tight framing, slow push-ins, shadows creeping in, papers and screens examined late at night",
 "act3": "ACT 3 collapse and human impact: anonymous workers leaving with boxes, idle workplaces, creditors waiting, empty offices, rain, harsh shadows, handheld unease",
 "after": "AFTERMATH: quiet, desaturated, reflective; empty courthouse steps at dawn, still warehouses, slow pull-backs, lingering silence",
}
def act_of(i, n):
    r = i / max(1, n - 1)
    return "act1" if r < 0.3 else "act2" if r < 0.62 else "act3" if r < 0.9 else "after"

FULL_GFX = ("timeline", "chart", "document", "quote", "relmap", "scale", "chapter", "headline", "photo", "entity_full", "moneyflow", "collapse",
            "flow", "stack", "list", "takeaway")  # os 4 ultimos so existem no EffectCraft (tools/remake.py convert + tools/ec_gfx.py)
GFX_HINTS = ("timeline", "chart", "scale", "moneyflow", "collapse", "relmap", "document", "flow", "stack", "list")
PROMPT_RULES = (
    "RULES FOR EVERY visual_prompt (40-70 words):\n"
    "1. EXPLAIN, don't decorate: a viewer with the sound off should understand the narration line from the picture. "
    "Choose a device: 'reconstruction' (the real event in its real place and era), 'human' (the people affected), or 'establishing' (place/time). "
    "Abstract ideas (leverage, debt, deposits, liquidity, funds moving, who owed whom, who gets paid first, ratios) are NOT pictured: set gfx_hint (rule 8) "
    "and still write a plain establishing or human visual_prompt as a fallback. Never a symbolic object standing for an idea (crates for leverage, keys for leases, "
    "glass boxes, chess pieces, water tanks) and never 'an analyst looking at screens/charts/documents'.\n"
    "2. ONE clear subject doing ONE visible action that fits a ~6-second clip; say how the frame changes from start to end. No lists of three simultaneous actions.\n"
    "3. Never let the meaning depend on readable text, numbers, charts on screens, calendars, nameplates or signed papers: the generator garbles text. "
    "Papers and screens may appear only blank, out of focus or turned away.\n"
    "4. Camera: give lens + ONE move that matches the emotion (static locked-off, slow push-in, lateral dolly, pull-back reveal, handheld drift). "
    "Vary shot size: never the same shot type, and never the same setting, in more than 2 consecutive scenes (e.g. not three courtroom corridors in a row; "
    "legal beats can use details: file boxes on a cart, an empty witness chair, a pen above a signature line, courthouse steps at dawn).\n"
    "5. Era accuracy: phones, cars, monitors, clothing and architecture match the date in the narration.\n"
    "6. CONTINUITY: when a scene involves an element of the VISUAL BIBLE (protagonist silhouette, headquarters, recurring places), describe it with the same words.\n"
    "7. Do not write 'no logos / no text / no faces' inside visual_prompt (added automatically); describe what IS in frame.\n"
    "8. If a data graphic would explain the line better than any picture (amounts compared, dates in sequence, money moving between named parties, "
    "a value collapsing, who owes whom), set gfx_hint to one of " + "|".join(GFX_HINTS) + " and say in gfx_why which sourced numbers/dates it needs; still write the visual_prompt.\n")

def enrich_prompts(pid):
    d = _load(pid); a = _app(); sc = d["scenes"]
    sys = ("You are a documentary director of photography writing image/video generation prompts for Grok Imagine. Reply only in json. "
           "Never depict a real person's likeness (people only as silhouettes, hands, backs, out-of-focus), no logos, no brand names, no readable text.")
    bible = d.get("visual_bible") or ""
    prev = []  # ultimas cenas do lote anterior: variedade tambem na emenda entre lotes
    for st in range(0, len(sc), 20):
        part = [(i, s) for i, s in enumerate(sc[st:st + 20], st)]
        lines = "\n".join(f"{i} <{act_of(i, len(sc))}>: [{'GFX' if any(g.get('type') in FULL_GFX for g in s.get('gfx') or []) else 'AI'}] {s.get('narration')}" for i, s in part)
        ask_bible = "" if bible else (
            "First define a short VISUAL BIBLE for the whole video (json key visual_bible, 50-90 words): how the anonymous protagonist always looks "
            "(silhouette, build, clothing, seen from behind), the headquarters and 2-3 recurring places (architecture, era, materials, no signage), and the base palette. ")
        u = ("Story so far: " + (d.get("hook") or "") + "\n"
             + (f"VISUAL BIBLE (reuse exactly): {bible}\n" if bible else ask_bible)
             + (f"Previous scenes (do not repeat their shot type or setting): {' | '.join(prev)}\n" if prev else "")
             + "For each scene, identify its story beat and write a visual prompt that SHOWS exactly what the narration says "
             "(subject, action, setting, era, props, shot type, lens, camera move, lighting, color, mood). "
             "Follow the EMOTIONAL ARC tag of each scene, so emotion tracks the financial impact as the story unfolds: " + " | ".join(ARC.values()) + ". "
             "People are ALWAYS anonymous (seen from behind, silhouettes, hands, out of focus); never a real person's likeness. Emotion comes from lighting, camera movement and situations.\n"
             + PROMPT_RULES +
             "Skip scenes marked GFX (return them with empty visual_prompt). json: {" + ('' if bible else '"visual_bible":"...",') + "\"scenes\":[{\"i\":0,\"beat\":\"...\","
             "\"device\":\"reconstruction|human|establishing\",\"shot\":\"wide|medium|close-up|macro|aerial|overhead|tracking|over-the-shoulder|low-angle\","
             "\"setting\":\"2-5 words\",\"mood\":\"...\",\"camera\":\"lens + one move\",\"visual_prompt\":\"...\",\"gfx_hint\":\"\",\"gfx_why\":\"\"}]}\n\n" + lines)
        r = a.chat_json(sys, u, 12000)
        if not bible and r.get("visual_bible"):
            bible = d["visual_bible"] = re.sub(r"\s+", " ", str(r["visual_bible"])).strip()
        for x in r.get("scenes") or []:
            i = int(x.get("i", -1))
            if 0 <= i < len(sc) and x.get("visual_prompt"):
                ac = act_of(i, len(sc))
                if ac == "act3" and sc[i].get("source") != "gfx": sc[i]["mode"] = "video"  # mais video no colapso
                sc[i].update(act=ac, beat=x.get("beat"), shot=x.get("shot"), mood=x.get("mood"), camera=x.get("camera"), visual_prompt=x["visual_prompt"],
                             device=x.get("device"), setting=x.get("setting"))
                h = str(x.get("gfx_hint") or "").strip().lower()
                if h in GFX_HINTS: sc[i].update(gfx_hint=h, gfx_why=x.get("gfx_why") or "")
                else: sc[i].pop("gfx_hint", None); sc[i].pop("gfx_why", None)
                prev = (prev + [f"#{i} {x.get('shot')} / {x.get('setting') or ''}"])[-3:]
    d["prompts_enriched"] = True
    return a.save_project(d)

def gfx_hints(d):
    """Cenas onde o diretor de fotografia sugeriu um grafico com dados no lugar (ou alem) do clipe. Aviso, nao bloqueia."""
    out = []
    for i, s in enumerate(d.get("scenes") or []):
        if s.get("gfx_hint") and not any(g.get("type") in FULL_GFX for g in s.get("gfx") or []):
            out.append({"scene": i + 1, "gfx": s["gfx_hint"], "why": s.get("gfx_why") or ""})
    return out

def title_check(t):
    """Avisos (nao bloqueiam) quando o titulo foge das regras de clique do PADRAO_VIDEOS.md."""
    t = (t or "").strip(); w = []
    if not t: return ["sem título"]
    if len(t) > 60: w.append(f"{len(t)} caracteres (máx. 60)")
    if re.match(r"^[^:]{2,40}:\s", t) and not t.lower().startswith("the "): w.append("formato manchete 'Nome: ...' (esconder o nome da empresa)")
    if re.match(r"(?i)^(the )?rise and fall", t): w.append("'rise and fall' é título de assunto, não de história")
    return w

# ---------------- 5) Validacao ----------------
AMT = re.compile(r"\$\s?\d[\d,]*(?:\.\d+)?\s?(?:billion|million|thousand|bn|B|M|K)?\b", re.I)
ACR_SKIP = {"CEO", "CFO", "COO", "VP", "US", "U", "S", "OK", "TV", "AI", "I", "II", "III", "LLC", "INC", "CO", "A", "AM", "PM"}

def _amt_val(s):
    m = re.search(r"(\d[\d,]*(?:\.\d+)?)\s*(billion|bn|b|million|m|thousand|k)?", s.replace("$", ""), re.I)
    if not m: return None
    v = float(m.group(1).replace(",", "")); u = (m.group(2) or "").lower()
    return round(v * (1000 if u in ("billion", "bn", "b") else 0.001 if u in ("thousand", "k") else 1 if u in ("million", "m") else 1e-6), 3)

def _gfx_amounts(s):
    vals = set()
    for g in E.visuals(s):
        unit = str(g.get("unit") or "")
        for k in ("text", "amount", "headline", "excerpt", "title"):
            for m in AMT.finditer(str(g.get(k) or "")): vals.add(_amt_val(m.group()))
        for nd in g.get("nodes") or []:
            for m in AMT.finditer(str(nd.get("relation") or "")): vals.add(_amt_val(m.group()))
        for t in [p.get("display") for p in g.get("points") or [] if isinstance(p, dict)] + [(g.get("final") or {}).get("value")]:
            for m in AMT.finditer(str(t or "")): vals.add(_amt_val(m.group()))  # rotulos das barras do grafico collapse
        for se in g.get("series") or []:
            try: vals.add(_amt_val(f"{se.get('value')}{' billion' if 'B' in unit else ' million' if 'M' in unit else ''}"))
            except Exception: pass
    return vals

def validate(pid, autofix=True):
    d = _load(pid)
    rep = E.coverage(d, autofix=autofix)
    names = {n.upper() for e in d.get("entities") or [] for n in E._names(e)}
    amt_gaps, acr_gaps, added = [], [], 0
    for i, s in enumerate(d.get("scenes") or []):
        narr = s.get("narration") or ""
        have = _gfx_amounts(s)
        for m in AMT.finditer(narr):
            v = _amt_val(m.group())
            if v in have: continue
            if autofix:
                src = ((s.get("sources") or [{}])[0] or {}).get("title") or ""
                s.setdefault("gfx", []).append({"type": "callout", "text": m.group().strip(), "source": (src if len(src) <= 60 else src[:60].rsplit(" ", 1)[0] + "…"), "auto": True}); have.add(v); added += 1
            else: amt_gaps.append({"scene": i + 1, "amount": m.group().strip()})
        for a in set(re.findall(r"\b[A-Z]{2,6}\b", narr)) - ACR_SKIP:
            if a not in names and not any(a in str(g.get("text", "")) + str(g.get("title", "")) + str(g.get("entity", "")) for g in E.visuals(s)):
                acr_gaps.append({"scene": i + 1, "acronym": a})
    gaps = rep["gaps"] + [{"scene": g["scene"], "missing": [g["amount"] + " (amount)"]} for g in amt_gaps] \
         + [{"scene": g["scene"], "missing": [g["acronym"] + " (acronym not in registry)"]} for g in acr_gaps]
    try:
        import logo_check
        import app as _app; lc = logo_check.check(d, _app.PROJECTS / Path(pid).name)
        gaps += [{"scene": f["scene"], "missing": ["logo/brand artifact: " + "; ".join(f["what"])[:120]]} for f in lc["flagged"]]
    except Exception as e:
        lc = {"error": str(e)[:200]}
    tc = text_check(d)
    gfx_rules = [{"scene": i + 1, "issue": "gráfico com uma barra só (regra: nunca); use scale/callout ou compare com outro valor"}
                 for i, s in enumerate(d.get("scenes") or []) for g in s.get("gfx") or [] if g.get("type") == "chart" and len(g.get("series") or []) < 2]
    gaps += [{"scene": t["scene"], "missing": ["overlay text: " + t["issue"]]} for t in tc]
    gaps.sort(key=lambda g: g["scene"])
    v = {"title_check": title_check(d.get("title")), "gfx_hints": gfx_hints(d), "gfx_rules": gfx_rules, "text_check": tc, "logo_check": {k: lc.get(k) for k in ("checked", "flagged", "error") if k in lc}, "ok": not gaps, "gaps": gaps, "entity_cards_added": rep["added_cards"], "amount_callouts_added": added,
         "name_card_only": rep["name_card_only"], "mentions": rep["mentions"]}
    d["validation"] = v; d.pop("coverage", None); _save(d)
    return v


TEXT_KEYS = ("outlet", "name", "title", "headline", "text", "label", "role", "subtitle", "source", "caption", "quote", "attribution", "highlight_text")
def _gfx_texts(g):
    for k in TEXT_KEYS:
        if isinstance(g.get(k), str): yield k, g[k]
    for k in ("events", "items", "bars", "nodes", "edges", "points", "markers"):
        for x in g.get(k) or []:
            if isinstance(x, dict):
                for kk in ("label", "name", "text", "title"):
                    if isinstance(x.get(kk), str): yield kk, x[kk]

def text_check(d):
    """Spell/name check of every overlay string: outlet and person/company names must match the dossier,
    sources or entity registry exactly; any other word must appear somewhere in narration/dossier/sources."""
    corpus = json.dumps(d.get("dossier") or {}, ensure_ascii=False) + " " + json.dumps(d.get("entities") or [], ensure_ascii=False)
    for s in d.get("scenes") or []:
        corpus += " " + (s.get("narration") or "") + " " + json.dumps(s.get("sources") or [], ensure_ascii=False) + " " + json.dumps(s.get("key_facts") or [], ensure_ascii=False)
    low = corpus.lower(); vocab = set(re.findall(r"[a-z][a-z'\-]+", low))
    common = set("the a an and or of to in on for by with from at as is was were be been are it its this that these those not no than then into over under after before about against between during without within upon per via new old says said say alleged allegedly according court case filed filing billion million thousand percent former chief officer financial executive pleaded plead pleads guilty innocent charged charges counts count trial judge prosecutors prosecutor indictment bankruptcy chapter lenders lender debt cash liabilities assets company group fund funds bank banks timeline source sources photo key date dates amount amounts total owed collapse fraud case recreated illustration headline published jan feb mar apr may jun jul aug sep sept oct nov dec january february march april june july august september october november december".split())
    out = []
    for i, s in enumerate(d.get("scenes") or []):
        for g in E.visuals(s):
            for k, t in _gfx_texts(g):
                if (k == "outlet" or (k == "name" and g.get("type") in ("entity", "lower_third", "entity_full"))) and t.strip() and t.strip().lower() not in low:
                    out.append({"scene": i + 1, "issue": f"{k} '{t}' not found in dossier/sources/registry"})
                    continue
                for w in re.findall(r"[A-Za-z][A-Za-z'\-]{3,}", t):
                    wl = w.lower().strip("'-")
                    if wl in vocab or wl in common or wl.rstrip("s") in vocab or (wl + "s") in vocab: continue
                    out.append({"scene": i + 1, "issue": f"possible typo '{w}' in {g.get('type')}.{k}", "_w": w, "_t": t})
    sus = [o for o in out if o.get("_w")]
    if sus:  # second pass: language model confirms which unknown words are really misspelled (text-only)
        try:
            import app as _app
            items = sorted({f"{o['_w']} || {o['_t']}" for o in sus})
            r = _app.chat_json("You are a meticulous copy editor. Reply in JSON.",
                "For each line 'WORD || CONTEXT', decide if WORD is misspelled or truncated (English word or proper name) in that context. "
                "Return json {\"typos\":[{\"word\":...,\"fix\":...}]} listing ONLY real errors.\n" + "\n".join(items), 1500)
            bad = {x.get("word"): x.get("fix") for x in r.get("typos") or []}
            out = [o for o in out if not o.get("_w") or o["_w"] in bad]
            for o in out:
                if o.get("_w"): o["issue"] = f"typo '{o['_w']}' -> '{bad[o['_w']]}' in {o['issue'].split(' in ', 1)[1]}"
        except Exception as e:
            print("[text_check] LLM pass failed:", e)
    for o in out: o.pop("_w", None); o.pop("_t", None)
    return out
