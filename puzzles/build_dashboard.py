"""Monta o painel HTML (autocontido, interativo) a partir dos JSON de puzzles/dashboard/data.
Uso: python puzzles/build_dashboard.py     -> puzzles/dashboard/index.html (+ copia em OpenBot/Shared/dashboard_canais/)"""
import base64, glob, json, re, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "dashboard"
SHARED = Path(r"C:\Users\Admin\OpenBot\Shared\dashboard_canais")
ORDER = ["syw", "ledger", "walt"]
NAV = {"Skip navigation", "Ask Studio", "Create", "Your channel", "Dashboard", "Content", "Analytics", "Community", "Languages",
       "Subtitles", "Content detection", "Earn", "Customization", "Audio library", "Settings", "Send feedback"}
NUMTOK = re.compile(r"^(?:[<>~+\-]?[\d.,]+[KMB%]?|—|--|\([+\-\d.,%]+\))$")
DUR = re.compile(r"^\d+:\d\d(?::\d\d)?$")
DATE_EN = re.compile(r"^[A-Z][a-z]{2} \d{1,2}, \d{4}$")


def L(t): return [l.strip() for l in t.split("\n") if l.strip()]
def isnum(s): return bool(NUMTOK.match(s))


def yt_table(txt):
    ls = L(txt); i = next((j for j, l in enumerate(ls) if l == "Total"), None)
    if i is None: return {"total": [], "rows": []}
    total, rows, cur, dur = [], [], None, ""
    for l in ls[i + 1:]:
        if l == "Save report" or l.startswith("Rows per page"): break
        if DUR.match(l): dur = l; continue
        if isnum(l):
            (cur["n"] if cur else total).append(l)
        else:
            cur = {"label": l, "dur": dur, "n": []}; rows.append(cur); dur = ""
    return {"total": total, "rows": rows}


def yt_list(txt):
    ls = L(txt); idx = [j for j, l in enumerate(ls) if DUR.match(l)]; out = []
    for a, b in zip(idx, idx[1:] + [len(ls)]):
        seg = ls[a + 1:b]
        if not seg: continue
        vis = next((s for s in seg if s in ("Public", "Scheduled", "Private", "Unlisted", "Draft")), "")
        date = next((s for s in seg if DATE_EN.match(s)), "")
        nums = [s for s in seg if re.fullmatch(r"[\d,]+", s)]
        out.append({"dur": ls[a], "titulo": seg[0], "vis": vis, "data": date, "views": nums[-2] if len(nums) >= 2 else "", "coment": nums[-1] if nums else ""})
    return out


def tt_list(txt):
    ls = L(txt); idx = [j for j, l in enumerate(ls) if re.fullmatch(r"\d\d:\d\d", l)]; out = []
    for a, b in zip(idx, idx[1:] + [len(ls)]):
        seg = ls[a + 1:b]
        if len(seg) < 4: continue
        nums = [s for s in seg if re.fullmatch(r"[\d.,KM]+", s)]
        out.append({"dur": ls[a], "titulo": seg[0], "data": seg[1], "vis": seg[2], "views": nums[-3] if len(nums) >= 3 else "", "curtidas": nums[-2] if len(nums) >= 2 else "", "coment": nums[-1] if nums else ""})
    return out


HEAD = {"Origem de tráfego", "Traffic source", "Termos pesquisados", "Search queries", "Gênero", "Gender", "Idade", "Age", "Localizações", "Locations",
        "Horários mais ativos", "Most active times", "Baixar dados", "Download data", "Publicações que seus espectadores também visualizaram"}


def pairs_after(ls, names, stops):
    i = next((j for j, l in enumerate(ls) if l in names), None)
    if i is None: return []
    out = []; j = i + 1
    while j + 1 < len(ls) and ls[j] not in stops and ls[j] not in HEAD:
        if re.fullmatch(r"[<>]?[\d.,]+%", ls[j + 1]): out.append([ls[j], ls[j + 1]]); j += 2
        else: j += 1
    return out


def tt_metrics(txt):
    ls = L(txt); names = {"Visualizações de vídeo": "Visualizações de vídeo", "Video views": "Visualizações de vídeo", "Visualizações de perfil": "Visualizações de perfil",
                          "Profile views": "Visualizações de perfil", "Curtidas": "Curtidas", "Likes": "Curtidas", "Comentários": "Comentários", "Comments": "Comentários",
                          "Compartilhamentos": "Compartilhamentos", "Shares": "Compartilhamentos", "Total de seguidores": "Total de seguidores",
                          "Total followers": "Total de seguidores", "Seguidores líquidos": "Seguidores líquidos", "Net followers": "Seguidores líquidos",
                          "Total de espectadores": "Total de espectadores", "Total viewers": "Total de espectadores", "Novos espectadores": "Novos espectadores",
                          "New viewers": "Novos espectadores"}
    out = []
    for j, l in enumerate(ls):
        if l in names and j + 1 < len(ls) and isnum(ls[j + 1]) and names[l] not in [o["nome"] for o in out]:
            d = ls[j + 2] if j + 2 < len(ls) and isnum(ls[j + 2]) else ""
            out.append({"nome": names[l], "valor": ls[j + 1], "delta": d})
    return out


def parse(res):
    P = {p["id"]: p for p in res["paginas"]}; D = {"erros": [p["id"] + ": " + p["erro"] for p in res["paginas"] if p["erro"]]}
    g = lambda i: P.get(i, {}).get("texto", "")
    D["yt_por_video"] = yt_table(g("yt_por_video")); D["yt_origens"] = yt_table(g("yt_origens")); D["yt_paises"] = yt_table(g("yt_paises"))
    D["yt_busca"] = yt_table(g("yt_busca")); D["yt_dispositivos"] = yt_table(g("yt_dispositivos")); D["yt_tudo_origens"] = yt_table(g("yt_tudo_origens"))
    D["yt_videos"] = yt_list(g("yt_videos")); D["yt_shorts"] = yt_list(g("yt_shorts"))
    pub = L(g("yt_publico")); D["yt_publico"] = {"audiencia_mensal": next((pub[j + 1] for j, l in enumerate(pub) if l == "Monthly audience" and j + 1 < len(pub) and isnum(pub[j + 1])), "")}
    D["tt_posts"] = tt_list(g("tt_posts"))
    ov = L(g("tt_visao_geral")); D["tt_metricas"] = tt_metrics(g("tt_visao_geral"))
    D["tt_trafego"] = pairs_after(ov, {"Origem de tráfego", "Traffic source"}, {"Termos pesquisados", "Search queries"})
    D["tt_termos"] = pairs_after(ov, {"Termos pesquisados", "Search queries"}, set())
    fo = L(g("tt_seguidores")); D["tt_seguidores_m"] = tt_metrics(g("tt_seguidores"))
    D["tt_genero"] = pairs_after(fo, {"Gênero", "Gender"}, {"Idade", "Age"}); D["tt_idade"] = pairs_after(fo, {"Idade", "Age"}, {"Localizações", "Locations"})
    D["tt_local"] = pairs_after(fo, {"Localizações", "Locations"}, {"Horários mais ativos", "Most active times"})
    D["tt_espectadores_m"] = tt_metrics(g("tt_espectadores"))
    vw = L(g("tt_espectadores")); k = next((j for j, l in enumerate(vw) if "também visualizaram" in l or "also watched" in l), None)
    D["tt_tambem_viram"] = vw[k + 1:k + 16] if k is not None else []
    return D


def img_b64(folder, name):
    p = ROOT / "shots" / folder / name
    return "data:image/jpeg;base64," + base64.b64encode(p.read_bytes()).decode() if p.is_file() else ""


def main():
    ins = json.loads((ROOT / "insights.json").read_text(encoding="utf-8")) if (ROOT / "insights.json").is_file() else {}
    canais = []
    for k in ORDER:
        fs = sorted(glob.glob(str(ROOT / "data" / f"{k}_*.json")))
        if not fs: continue
        res = json.loads(Path(fs[-1]).read_text(encoding="utf-8")); folder = Path(fs[-1]).stem
        D = parse(res)
        pags = [{"id": p["id"], "plat": p["plataforma"], "titulo": p["titulo"], "erro": p["erro"], "texto": p["texto"],
                 "imgs": [img_b64(folder, n) for n in p["imagens"]]} for p in res["paginas"]]
        canais.append({"k": k, "nome": res["nome"], "tiktok": res["tiktok"], "quando": res["quando"], "dados": D, "pags": pags, "insights": ins.get(k, [])})
    html = (ROOT / "template.html").read_text(encoding="utf-8").replace("/*__DATA__*/", "const DATA = " + json.dumps(canais, ensure_ascii=False).replace("</", "<\\/") + ";")
    (ROOT / "index.html").write_text(html, encoding="utf-8")
    SHARED.mkdir(parents=True, exist_ok=True); shutil.copy(ROOT / "index.html", SHARED / "index.html")
    print("ok:", ROOT / "index.html", f"({len(html)//1024} KB)", "canais:", [c["k"] for c in canais])


main()
