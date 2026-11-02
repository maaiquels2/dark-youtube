"""Coleta COMPLETA e SOMENTE LEITURA do YouTube Studio e do TikTok Studio de um canal (texto + capturas de tela).
Uso: python puzzles/collect.py syw|ledger|walt     (o Chrome do canal ja deve estar aberto com a porta de depuracao)
Grava puzzles/dashboard/data/<canal>_<data>.json e puzzles/dashboard/shots/<canal>_<data>/*.jpg."""
import json, sys, time
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
CH = {
 "syw": dict(port=9335, uc="UCrgIwaM5dsNRgrKqZkOepRg", nome="Show Your Work Puzzles", tt="@syw.puzzles"),
 "ledger": dict(port=9336, uc="UCvmyoFV8fg5fMtoejd82CRA", nome="The Cracked Ledger", tt="@thecrackedledger"),
 "walt": dict(port=9334, uc="UCh9ek7ZsZO3DptaNSPdqRTA", nome="Grandpa Walt Tales", tt="@grandpawalttales"),
}
k = sys.argv[1]; c = CH[k]; uc = c["uc"]
B = f"https://studio.youtube.com/channel/{uc}"
EXP = (f"{B}/analytics/tab-content/period-default/explore?entity_type=CHANNEL&entity_id={uc}&time_period={{per}}"
       "&explore_type=TABLE_AND_CHART&metric=EXTERNAL_VIEWS&granularity=DAY&t_metrics=EXTERNAL_VIEWS&t_metrics=EXTERNAL_WATCH_TIME"
       "&t_metrics=SUBSCRIBERS_NET_CHANGE&t_metrics=VIDEO_THUMBNAIL_IMPRESSIONS&t_metrics=VIDEO_THUMBNAIL_IMPRESSIONS_VTR"
       "&dimension={dim}&o_column=EXTERNAL_VIEWS&o_direction=ANALYTICS_ORDER_DIRECTION_DESC")
SRCH = "&filters=%5B%7B%22name%22%3A%22TRAFFIC_SOURCE_TYPE%22%2C%22value%22%3A%5B%22YT_SEARCH%22%5D%7D%5D"
PAGES = [  # (id, plataforma, titulo, url, analise?, clicar_aba)
 ("yt_videos", "youtube", "Conteúdo: vídeos", f"{B}/videos/upload", False, None),
 ("yt_shorts", "youtube", "Conteúdo: Shorts", f"{B}/videos/short", False, None),
 ("yt_visao_geral", "youtube", "Análise: visão geral", f"{B}/analytics/tab-overview/period-default", True, None),
 ("yt_conteudo", "youtube", "Análise: conteúdo (como os espectadores encontram você)", f"{B}/analytics/tab-content/period-default", True, None),
 ("yt_publico", "youtube", "Análise: público", f"{B}/analytics/tab-overview/period-default", True, "Audience"),
 ("yt_tendencias", "youtube", "Análise: tendências", f"{B}/analytics/tab-overview/period-default", True, "Trends"),
 ("yt_por_video", "youtube", "Por vídeo, 28 dias (modo avançado)", EXP.format(per="4_weeks", dim="VIDEO"), True, None),
 ("yt_origens", "youtube", "Origens de tráfego, 28 dias (modo avançado)", EXP.format(per="4_weeks", dim="TRAFFIC_SOURCE_TYPE"), True, None),
 ("yt_busca", "youtube", "Termos de pesquisa do YouTube, 28 dias (modo avançado)", EXP.format(per="4_weeks", dim="TRAFFIC_SOURCE_DETAIL") + SRCH, True, None),
 ("yt_paises", "youtube", "Países, 28 dias (modo avançado)", EXP.format(per="4_weeks", dim="COUNTRY"), True, None),
 ("yt_dispositivos", "youtube", "Dispositivos, 28 dias (modo avançado)", EXP.format(per="4_weeks", dim="DEVICE_TYPE"), True, None),
 ("yt_tudo_origens", "youtube", "Origens de tráfego, desde o início (modo avançado)", EXP.format(per="lifetime", dim="TRAFFIC_SOURCE_TYPE"), True, None),
 ("tt_posts", "tiktok", "Publicações", "https://www.tiktok.com/tiktokstudio/content", False, None),
 ("tt_visao_geral", "tiktok", "Análise: visão geral", "https://www.tiktok.com/tiktokstudio/analytics/overview", True, None),
 ("tt_conteudo", "tiktok", "Análise: conteúdo", "https://www.tiktok.com/tiktokstudio/analytics/content", True, None),
 ("tt_espectadores", "tiktok", "Análise: espectadores", "https://www.tiktok.com/tiktokstudio/analytics/viewers", True, None),
 ("tt_seguidores", "tiktok", "Análise: seguidores", "https://www.tiktok.com/tiktokstudio/analytics/followers", True, None),
]
now = datetime.now(); stamp = f"{now:%Y-%m-%d_%H%M}"
OUT = ROOT / "dashboard"; (OUT / "data").mkdir(parents=True, exist_ok=True)
SH = OUT / "shots" / f"{k}_{stamp}"; SH.mkdir(parents=True, exist_ok=True)
res = {"canal": k, "nome": c["nome"], "tiktok": c["tt"], "quando": now.isoformat(timespec="minutes"), "paginas": []}
with sync_playwright() as p:
    b = p.chromium.connect_over_cdp(f"http://127.0.0.1:{c['port']}", timeout=30000); ctx = b.contexts[0]
    for pid, plat, titulo, url, deep, aba in PAGES:
        pg = ctx.new_page(); item = dict(id=pid, plataforma=plat, titulo=titulo, url=url, texto="", imagens=[], erro="")
        try:
            pg.set_viewport_size({"width": 1440, "height": 1500 if deep else 1100})
            pg.goto(url, wait_until="domcontentloaded", timeout=45000); time.sleep(14 if deep else 9)
            if aba: pg.get_by_text(aba, exact=True).first.click(); time.sleep(12)
            t = pg.inner_text("body", timeout=20000)
            if plat == "youtube" and c["nome"] not in t:
                item["erro"] = "canal errado ou deslogado: " + pg.url[:90]
            elif plat == "tiktok" and ("Log in to TikTok" in t or "login" in pg.url.lower() or "Entrar no TikTok" in t):
                item["erro"] = "tiktok deslogado"
            else:
                for step in range(3 if deep else 1):
                    f = SH / f"{pid}_{step}.jpg"; pg.screenshot(path=str(f), type="jpeg", quality=72, timeout=60000)
                    item["imagens"].append(f.name)
                    if step < (2 if deep else 0):
                        pg.mouse.move(900, 700); pg.mouse.wheel(0, 1100); time.sleep(4)
                        t2 = pg.inner_text("body", timeout=20000)
                        if len(t2) > len(t): t = t2
            if pid == "tt_posts" and not item["erro"]:  # lista carrega aos poucos e os agendados vem antes dos publicados
                for _ in range(25):
                    pg.mouse.move(900, 600); pg.mouse.wheel(0, 2500); time.sleep(2.5)
                    t2 = pg.inner_text("body", timeout=20000)
                    if len(t2) <= len(t): break
                    t = t2
            item["texto"] = t
            if "Oops" in t[:400] or "Ops," in t[:400]: item["erro"] = (item["erro"] + " página com erro (Oops)").strip()
        except Exception as e:
            item["erro"] = f"{type(e).__name__}: {str(e)[:120]}"
        finally:
            pg.close()
        res["paginas"].append(item); print(pid, "ERRO " + item["erro"] if item["erro"] else f"ok ({len(item['texto'])} car., {len(item['imagens'])} imagens)", flush=True)
        time.sleep(3)
dst = OUT / "data" / f"{k}_{stamp}.json"
dst.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8"); print(dst)
