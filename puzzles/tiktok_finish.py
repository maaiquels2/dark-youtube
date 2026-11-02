"""Termina o agendamento de editores do TikTok Studio ja abertos (video enviado + legenda): data, 18:00, Schedule.
Uso: python puzzles/tiktok_finish.py <n>"""
import re, sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT = Path(__file__).resolve().parent.parent
DAY = {2: 26, 3: 27, 4: 28, 5: 29, 6: 30}
FILE2 = {1: "ep07_moser_circle", 2: "ep08_party_of_six", 3: "ep09_medical_test", 4: "ep10_simpson", 5: "ep11_hat_prisoners", 6: "ep12_ant_rope"}
FILE = {2: "ep02_monty_hall", 3: "ep03_birthday_paradox", 4: "ep04_josephus", 5: "ep05_tower_of_hanoi", 6: "ep06_hh_vs_ht"}
WEEK2 = "--week2" in sys.argv
n = int(sys.argv[1]); day = (n + 1) if WEEK2 else DAY[n]; MONTH = "Nov" if WEEK2 else "Oct"
if WEEK2: FILE = FILE2
def step(m): print(f"[{n}] {m}", flush=True)
with sync_playwright() as p:
    b = p.chromium.connect_over_cdp("http://127.0.0.1:9335", timeout=30000); ctx = b.contexts[0]
    pg = None
    for x in ctx.pages:
        if "tiktokstudio/upload" in x.url:
            try:
                if FILE[n] in x.inner_text("body"): pg = x
            except Exception: pass
    assert pg, "editor nao encontrado"; pg.bring_to_front(); step("editor achado")
    pg.get_by_text("Schedule", exact=True).first.scroll_into_view_if_needed(); pg.get_by_text("Schedule", exact=True).first.click(); time.sleep(2); step("schedule ligado")
    pg.get_by_text(re.compile(r"^[A-Z][a-z]{2} \d{1,2}, 20\d\d$")).filter(visible=True).first.click(); time.sleep(1.2); step("calendario aberto")
    if WEEK2:
        yr = pg.get_by_text("2026", exact=True).filter(visible=True).first
        if pg.get_by_text("October", exact=True).filter(visible=True).count():
            bb = yr.bounding_box(); pg.mouse.click(bb["x"] + bb["width"] / 2 + 83, bb["y"] + bb["height"] / 2); time.sleep(1.2)
    pg.locator('button.DatePicker__day[data-outside="false"]').get_by_text(str(day), exact=True).first.click(); time.sleep(1.2); step("dia escolhido")
    pg.get_by_text(re.compile(r"^\d{2}:\d{2}$")).filter(visible=True).first.click(); time.sleep(1.5); step("horas abertas")
    pg.get_by_text("18", exact=True).filter(visible=True).first.click(); time.sleep(1)
    m = pg.get_by_text("00", exact=True).filter(visible=True)
    bbs = [(m.nth(i).bounding_box(), i) for i in range(m.count())]
    idx = max((bb["x"], i) for bb, i in bbs if bb)[1]
    m.nth(idx).scroll_into_view_if_needed(); m.nth(idx).click(); time.sleep(1.2); pg.keyboard.press("Escape"); time.sleep(0.5)
    t = pg.inner_text("body"); i = t.find("When to post"); got = t[i:i + 110].replace(chr(10), " | "); step(got)
    assert f"{MONTH} {day}, 2026" in got and "18:00" in got, "data/hora erradas"
    pg.get_by_role("button", name="Schedule", exact=True).last.click(); time.sleep(8)
    body = pg.inner_text("body"); assert f"{MONTH} {day}, 6:00 PM" in body, "nao apareceu em Posts"
    step(f"AGENDADO {MONTH} {day}, 6:00 PM"); pg.close()
