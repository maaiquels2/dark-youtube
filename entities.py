"""Dark Studio - entidades (empresas, orgaos, tribunais, pessoas) e o gate de cobertura pre-render.

pj["entities"] = [{name, kind: company|agency|court|person, aliases[], full_name, role,
                   logo, seal, photo, hq_photo, credits{logo,seal,photo,hq_photo}}]  (arquivos relativos ao projeto)
Gate: toda entidade citada na narracao de uma cena precisa de um visual real na cena
(entity card / logo / seal / photo / name card / relmap / parties / quote speaker / lower_third)."""
import json, re, urllib.parse, urllib.request
from pathlib import Path

UA = {"User-Agent": "DarkStudio/1.0 (documentary tooling; contact via channel)"}

def fetch_commons(title, dest, width=1600):
    """Baixa um arquivo do Wikimedia Commons (SVG vira PNG) e devolve o credito."""
    if not title.startswith("File:"): title = "File:" + title
    u = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({
        "action": "query", "titles": title, "prop": "imageinfo", "iiprop": "url|extmetadata",
        "iiurlwidth": width, "format": "json"})
    r = json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30))
    ii = next(iter(r["query"]["pages"].values()))["imageinfo"][0]; md = ii.get("extmetadata", {})
    url = ii.get("thumburl") or ii["url"]
    dest = Path(dest); dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read())
    strip = lambda s: re.sub(r"<[^>]+>", "", s or "").strip()
    artist = strip(md.get("Artist", {}).get("value"))[:80]; lic = strip(md.get("LicenseShortName", {}).get("value"))
    return {"credit": ", ".join(x for x in [artist, lic, "via Wikimedia Commons"] if x),
            "source": ii.get("descriptionurl"), "license": lic}

def _names(e):
    return [n for n in [e["name"], e.get("full_name")] + list(e.get("aliases") or []) if n]

def _pat(n):
    return re.compile(r"(?<![A-Za-z])" + re.escape(n) + r"(?![A-Za-z])", re.I if not n.isupper() else 0)

def mentions(text, ents):
    found = []
    for e in ents:
        if any(_pat(n).search(text or "") for n in _names(e)): found.append(e["name"])
    return found

def ec_visuals(s):
    """Graficos do EffectCraft (scenes[i]["ec"], tools/ec_gfx.py) no formato que a Validacao le em s["gfx"]:
    tudo o que aparece escrito vai para "entity" (nomes visiveis) e os valores para "headline" (checagem de valores)."""
    ec = s.get("ec") or {}; out = []
    for e in ([ec["full"]] if ec.get("full") else []) + list(ec.get("overlay") or []):
        subs = [x for k in ("items", "events", "nodes", "sats", "tiers", "edges") for x in (e.get(k) or []) if isinstance(x, dict)]
        if isinstance(e.get("center"), dict): subs.append(e["center"])
        vis = [str(x[k]) for x in [e] + subs for k in ("title", "text", "label", "name", "sub", "role", "date", "note", "link",
                                                        "stop_label", "alert_label", "highlight_label") if x.get(k)]
        vis += [str(p) for p in e.get("points") or []]
        for f in [e.get("file"), e.get("photo")] + list(e.get("files") or []) + [x.get("file") for x in subs]:  # entities/<slug>-logo.png
            if f: vis.append(re.sub(r"-(logo|seal|photo)$", "", Path(f).stem).replace("-", " ").upper())
        amts = [f"{x.get('prefix', '')}{x['value']}{x.get('suffix', '')}" for x in [e] + subs if "value" in x]
        g = dict(e, entity=" | ".join(vis))
        if amts: g["headline"] = " ".join(amts)
        out.append(g)
    return out

def visuals(s):
    return list(s.get("gfx") or []) + ec_visuals(s)

def _scene_visual_names(s):
    out = []
    for g in visuals(s):
        t = g.get("type")
        for k in ("name", "company", "entity", "speaker", "center", "outlet", "source"):  # a fonte aparece escrita no rodape do grafico
            if g.get(k): out.append(str(g[k]))
        for nd in g.get("nodes") or []: out.append(str(nd.get("name", "")))
        out += [str(x) for x in g.get("items") or []]
    return " | ".join(out)

def has_real_asset(e):
    return any(e.get(k) for k in ("logo", "seal", "photo", "hq_photo"))

def coverage(pj, autofix=True, max_cards=3):
    """Retorna relatorio; com autofix insere entity cards onde faltam. ok=False lista lacunas."""
    ents = pj.get("entities") or []; by = {e["name"]: e for e in ents}
    seen, gaps, added, rows = set(), [], 0, []
    extra = pj.get("entity_mentions") or {}  # {scene_idx: [nomes extraidos por IA]}
    lg = pj.get("logo") or {}; lg_ent = lg.get("entity") if lg.get("enabled") else None  # logo de canto da montagem (cenas com "logo")
    for i, s in enumerate(pj.get("scenes") or []):
        ms = mentions(s.get("narration", ""), ents)
        unknown = [n for n in extra.get(str(i), []) if not mentions(n, ents)]
        vis = _scene_visual_names(s) + (" | " + lg_ent if lg_ent and s.get("logo") else ""); missing = []
        for n in ms:
            ok = any(_pat(a).search(vis) for a in _names(by[n]))
            if not ok and autofix:
                cards = sum(1 for g in s.get("gfx") or [] if g.get("type") == "entity")
                if cards < max_cards:
                    s.setdefault("gfx", []).append({"type": "entity", "name": n, "first": n not in seen,
                                                    "auto": True, "slot": cards}); added += 1; ok = True
            if not ok and autofix:  # cartoes cheios: entra como chip num overlay "parties" (nome visivel na tela)
                pt = next((g for g in s.get("gfx") or [] if g.get("type") == "parties"), None)
                if not pt: pt = {"type": "parties", "title": "Also involved", "items": [], "auto": True}; s.setdefault("gfx", []).append(pt)
                pt["items"].append(by[n].get("full_name") or n); added += 1; ok = True
            if not ok: missing.append(n)
            seen.add(n)
        for n in unknown: missing.append(n + " (not in entity registry)")
        if missing: gaps.append({"scene": i + 1, "missing": missing, "narration": s.get("narration", "")[:140]})
        rows.append({"scene": i + 1, "mentions": ms})
    weak = [e["name"] for e in ents if not has_real_asset(e)]
    rep = {"ok": not gaps, "gaps": gaps, "added_cards": added, "name_card_only": weak,
           "mentions": sum(len(r["mentions"]) for r in rows)}
    pj["coverage"] = rep
    return rep

# ---------------- Biblioteca local de entidades (reaproveitada entre videos) ----------------
# library/entities/<slug>/ : logo.*, seal.*, photo.*, hq_photo.* + meta.json (nome, apelidos, tipo, creditos/licencas)
LIBRARY = Path(__file__).resolve().parent / "library" / "entities"
ASSET_KEYS = ("logo", "seal", "photo", "hq_photo")

def slug(n):
    return re.sub(r"[^a-z0-9]+", "-", (n or "").lower()).strip("-")

def _lib_index():
    idx = {}
    if not LIBRARY.is_dir(): return idx
    for m in LIBRARY.glob("*/meta.json"):
        try: meta = json.loads(m.read_text(encoding="utf-8"))
        except Exception: continue
        for n in [meta.get("name"), meta.get("full_name")] + list(meta.get("aliases") or []):
            if n: idx.setdefault(slug(n), m.parent)
    return idx

def library_apply(e, pdir, idx=None):
    """Preenche logo/selo/foto que faltam na entidade com o que ja existe na biblioteca. Copia para o projeto."""
    import shutil
    idx = _lib_index() if idx is None else idx
    folder = next((idx[slug(n)] for n in _names(e) if slug(n) in idx), None)
    if not folder: return []
    meta = json.loads((folder / "meta.json").read_text(encoding="utf-8")); got = []
    if meta.get("kind") and e.get("kind") and meta["kind"] != e["kind"]: return []  # mesmo nome, outra coisa
    for k in ASSET_KEYS:
        f = next(iter(sorted(folder.glob(k + ".*"))), None)
        if e.get(k) or not f: continue
        rel = f"entities/{slug(e['name'])}-{k}{f.suffix.lower()}"
        (Path(pdir) / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(f, Path(pdir) / rel); e[k] = rel; got.append(k)
        cr = (meta.get("credits") or {})
        for ck in (k, k + "_source"):
            if cr.get(ck): e.setdefault("credits", {})[ck] = cr[ck]
    for a in [meta.get("name")] + list(meta.get("aliases") or []):
        if a and a != e["name"] and a not in (e.get("aliases") or []): e.setdefault("aliases", []).append(a)
    return got

def library_save(e, pdir):
    """Guarda na biblioteca os arquivos reais da entidade (so acrescenta, nunca sobrescreve)."""
    import shutil
    if not has_real_asset(e) or not e.get("name"): return []
    folder = _lib_index().get(slug(e["name"])) or (LIBRARY / slug(e["name"]))
    folder.mkdir(parents=True, exist_ok=True); mf = folder / "meta.json"
    meta = json.loads(mf.read_text(encoding="utf-8")) if mf.is_file() else {"name": e["name"], "kind": e.get("kind")}
    if e.get("full_name") and not meta.get("full_name"): meta["full_name"] = e["full_name"]
    meta["aliases"] = sorted({*(meta.get("aliases") or []), *(e.get("aliases") or [])} - {meta["name"]})
    saved = []
    for k in ASSET_KEYS:
        src = Path(pdir) / e[k] if e.get(k) else None
        if not src or not src.is_file() or any(folder.glob(k + ".*")): continue
        shutil.copyfile(src, folder / (k + src.suffix.lower())); saved.append(k)
        cr = e.get("credits") or {}
        for ck in (k, k + "_source"):
            if cr.get(ck): meta.setdefault("credits", {})[ck] = cr[ck]
    mf.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    return saved

def extract_mentions(pj, chat_json):
    """IA (texto) lista empresas/orgaos/tribunais/pessoas citados por cena, para achar quem falta no registro."""
    lines = "\n".join(f"{i}: {s.get('narration','')}" for i, s in enumerate(pj["scenes"]))
    r = chat_json("You extract named entities. Return json only.",
                  "For each numbered scene list every company, fund, bank, government agency, court and named person "
                  "mentioned (proper names only, as written). Return json {\"scenes\": {\"<idx>\": [names]}}.\n\n" + lines)
    pj["entity_mentions"] = {k: v for k, v in (r.get("scenes") or {}).items() if v}
    return pj["entity_mentions"]
