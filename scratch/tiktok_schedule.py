"""Agenda Shorts no TikTok Studio pelo Chrome do Ledger (browser_profile_ledger, porta 9336), ja logado.
Uso: python scratch/tiktok_schedule.py   (lista PLANO abaixo; um envio por vez)
Fluxo testado em 02/11/2026: arquivo -> descricao -> Programar -> dia (DatePicker__day) -> hora/minuto (TimePicker__column) -> Agendar.
O TikTok Studio so aceita agendar ate ~10 dias a frente; minutos de 5 em 5."""
import json, re, sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
W = "weil-gotshal-wind-down-20261030-190000"; B = "binance-hack-north-korea-20261102-150000"
HW = "#LawFirm #BigLaw #WallStreet #Business #TheCrackedLedger"
ns = {}; exec((ROOT / "scratch/upload_weil_short.py").read_text(encoding="utf-8").split("n, date, hhmm")[0].split("import yt_upload as Y")[1], ns)
q = json.loads((ROOT / "social/queue.json").read_text(encoding="utf-8"))
tk = {Path(x["file"]).name: x["caption"] for x in q if x["project"] == B and x["platform"] == "tiktok"}
def weil(n): t, body = ns["S"][n]; return f"{t}\n\n{body}\n\n{HW}"
PLANO = [  # (arquivo, legenda, dia de novembro, hora, minuto)
    (ROOT / "projects" / W / "output/shorts/weil-1.mp4", weil(1), 3, "19", "00"),
    (ROOT / "projects" / W / "output/shorts/weil-2.mp4", weil(2), 4, "12", "00"),
    (ROOT / "projects" / W / "output/shorts/weil-3.mp4", weil(3), 4, "19", "30"),
    (ROOT / "projects" / B / "output/shorts/binance-1.mp4", tk["binance-1.mp4"], 5, "12", "00"),
    (ROOT / "projects" / B / "output/shorts/binance-2.mp4", tk["binance-2.mp4"], 5, "19", "30"),
    (ROOT / "projects" / B / "output/shorts/binance-3.mp4", tk["binance-3.mp4"], 6, "12", "00"),
]
only = set(sys.argv[1:])  # opcional: nomes de arquivo para agendar so esses


def finish(pg, tag):
    """Clica Agendar. Se o TikTok perguntar "Continuar publicando?" (verificacao do video ainda rodando), clica Cancelar,
    espera e tenta de novo: nunca clica "Publicar agora" (nao da para garantir que respeita o agendamento)."""
    for tent in range(12):
        if "tiktokstudio/content" in pg.url: return
        ag = pg.get_by_role("button", name="Agendar", exact=True)
        try: ag.click(timeout=10000)
        except Exception:   # botao sumiu: a verificacao terminou e o TikTok ja seguiu para a lista
            time.sleep(10)
            if "tiktokstudio/content" in pg.url: return
            continue
        time.sleep(5)
        for _ in range(15):
            if "tiktokstudio/content" in pg.url: return
            time.sleep(1)
        canc = pg.get_by_role("button", name="Cancelar", exact=True)
        if canc.count() and canc.first.is_visible():
            print(f"  {tag}: verificacao ainda rodando, espero (tentativa {tent + 1})", flush=True); canc.first.click(); time.sleep(30)
    pg.screenshot(path=str(ROOT / "output_yt" / f"tt-falhou-{tag}.png")); raise RuntimeError(f"{tag}: Agendar nao concluiu")


def agenda(pg, video, cap, day, hh, mm):
    pg.goto("https://www.tiktok.com/tiktokstudio/upload", wait_until="domcontentloaded"); time.sleep(8)
    small = ROOT / "scratch/tiktok_upload_copies" / video.name  # copias < 10 MB: arquivo grande estourava o tempo do set_input_files
    pg.locator("input[type=file]").first.set_input_files(str(small if small.is_file() else video), timeout=180000)
    pg.get_by_text(re.compile(r"Enviado")).first.wait_for(timeout=240000); time.sleep(3)
    ed = pg.locator("[contenteditable=true]").first; ed.click(); pg.keyboard.press("Control+A"); pg.keyboard.press("Delete")
    pg.keyboard.insert_text(cap + " "); time.sleep(2); pg.mouse.click(50, 600); time.sleep(1)
    pg.get_by_text("Programar", exact=True).first.click(); time.sleep(3)
    pg.get_by_text("de nov de", exact=False).first.click(); time.sleep(2)
    pg.locator("button.DatePicker__day").filter(has_text=re.compile(rf"^{day}$")).first.click(); time.sleep(2)
    pg.locator(r"text=/^\d{2}:\d{2}$/").first.click(); time.sleep(2)
    cols = pg.locator(".TimePicker__column")
    cols.nth(0).locator("button.TimePicker__item", has_text=re.compile(rf"^{hh}$")).first.click(); time.sleep(1)
    cols.nth(1).locator("button.TimePicker__item", has_text=re.compile(rf"^{mm}$")).first.click(); time.sleep(1)
    pg.mouse.click(50, 600); time.sleep(1)
    got = pg.evaluate(r"""() => [...document.querySelectorAll('*')].filter(e=>e.offsetParent&&e.childElementCount==0&&/(de nov de|^\d{2}:\d{2}$)/.test(e.textContent.trim())).map(e=>e.textContent.trim()).slice(0,2)""")
    if got != [f"{day} de nov de 2026", f"{hh}:{mm}"]: raise RuntimeError(f"data/hora nao bateu: {got}")
    finish(pg, video.stem)
    return got


with sync_playwright() as p:
    b = p.chromium.connect_over_cdp("http://127.0.0.1:9336"); ctx = b.contexts[0]
    pg = next((x for x in ctx.pages if "tiktokstudio" in x.url), None) or ctx.new_page()
    for video, cap, day, hh, mm in PLANO:
        if only and video.name not in only: continue
        got = agenda(pg, video, cap, day, hh, mm)
        print("AGENDADO", video.name, got, flush=True)
