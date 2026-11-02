"""Snapshot SOMENTE LEITURA do YouTube Studio e do TikTok Studio de um canal, no formato dos arquivos de OpenBot\Shared\*_analytics.
Uso: python puzzles/snapshot.py syw|ledger|walt   (o Chrome do canal ja deve estar com a porta de depuracao aberta)"""
import sys, time
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright

SHARED = Path(r"C:\Users\Admin\OpenBot\Shared")
CH = {
 "syw": dict(port=9335, uc="UCrgIwaM5dsNRgrKqZkOepRg", nome="Show Your Work Puzzles", pasta="show_your_work_analytics", suf="syw"),
 "ledger": dict(port=9336, uc="UCvmyoFV8fg5fMtoejd82CRA", nome="The Cracked Ledger", pasta="cracked_ledger_analytics", suf="ledger"),
 "walt": dict(port=9334, uc="UCh9ek7ZsZO3DptaNSPdqRTA", nome="Grandpa Walt Tales", pasta="walt_analytics", suf="walt"),
}
k = sys.argv[1]; c = CH[k]
YT = f"https://studio.youtube.com/channel/{c['uc']}"
PAGES = [("conteudo_videos", f"{YT}/videos/upload"), ("conteudo_shorts", f"{YT}/videos/short"),
         ("analises_visao_geral", f"{YT}/analytics/tab-overview/period-default"),
         ("analises_alcance", f"{YT}/analytics/tab-reach_viewers/period-default"),
         ("tiktok_posts", "https://www.tiktok.com/tiktokstudio/content"),
         ("tiktok_analises", "https://www.tiktok.com/tiktokstudio/analytics")]
now = datetime.now(); out = [f"# Snapshot {c['nome']} - {now:%d/%m/%Y %H:%M}", ""]
with sync_playwright() as p:
    b = p.chromium.connect_over_cdp(f"http://127.0.0.1:{c['port']}", timeout=30000); ctx = b.contexts[0]
    for name, url in PAGES:
        pg = ctx.new_page()
        try:
            pg.goto(url, wait_until="domcontentloaded", timeout=45000); time.sleep(10 if "analytics" in url else 8)
            t = pg.inner_text("body", timeout=20000)
            if "studio.youtube" in url and c["nome"] not in t: t = "[canal errado ou deslogado: " + pg.url[:80] + "]\n" + t[:300]
            if "tiktok" in url and ("Log in to TikTok" in t or "login" in pg.url.lower()): t = "[tiktok_deslogado]"
        except Exception as e:
            t = f"[erro: {type(e).__name__}]"
        finally:
            pg.close()
        out += [f"## {name}", t.strip(), ""]; time.sleep(3)
dst = SHARED / c["pasta"] / f"{now:%Y-%m-%d_%H%M}_{c['suf']}.md"
dst.write_text("\n".join(out), encoding="utf-8"); print(dst)
