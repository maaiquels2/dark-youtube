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

def _scene_visual_names(s):
    out = []
    for g in s.get("gfx") or []:
        t = g.get("type")
        for k in ("name", "company", "entity", "speaker", "center", "outlet"):
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
    for i, s in enumerate(pj.get("scenes") or []):
        ms = mentions(s.get("narration", ""), ents)
        unknown = [n for n in extra.get(str(i), []) if not mentions(n, ents)]
        vis = _scene_visual_names(s); missing = []
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

def extract_mentions(pj, chat_json):
    """IA (texto) lista empresas/orgaos/tribunais/pessoas citados por cena, para achar quem falta no registro."""
    lines = "\n".join(f"{i}: {s.get('narration','')}" for i, s in enumerate(pj["scenes"]))
    r = chat_json("You extract named entities. Return json only.",
                  "For each numbered scene list every company, fund, bank, government agency, court and named person "
                  "mentioned (proper names only, as written). Return json {\"scenes\": {\"<idx>\": [names]}}.\n\n" + lines)
    pj["entity_mentions"] = {k: v for k, v in (r.get("scenes") or {}).items() if v}
    return pj["entity_mentions"]
