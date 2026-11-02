"""Show Your Work Puzzles: agenda um video no TikTok Studio (Chrome Profile 6, CDP 9335, login do usuario).
Uso: python puzzles/tiktok_schedule.py <n> [--dry] [--warm SEGUNDOS]   (n = 2..6; 18:00 America/Sao_Paulo, 26/10 a 30/10)
Cuidados pedidos pelo usuario: rola o feed antes de postar (sem curtir/seguir/comentar), um video por vez, 90-120 s entre videos
(o intervalo e feito por quem chama este script). Para se aparecer CAPTCHA ou verificacao."""
import random, sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
SHOTS = ROOT / "scratch" / "tt"
EPS = {
 2: ("ep02_monty_hall", 26, "100 doors, one car. You pick one, the host opens 98 empty ones. Stay or switch? #math #montyhall #probability #puzzle"),
 3: ("ep03_birthday_paradox", 27, "Why do just 23 people give you a 50% chance of a shared birthday? Count the pairs. #math #probability #birthdayparadox #puzzle"),
 4: ("ep04_josephus", 28, "41 people in a circle, every second one is out. Who survives? A binary shortcut knows. #math #puzzle #binary #josephus"),
 5: ("ep05_tower_of_hanoi", 29, "Move 64 disks one at a time and it takes about 585 billion years. #math #towerofhanoi #exponential #puzzle"),
 6: ("ep06_hh_vs_ht", 30, "Same coin, same odds, but waiting for HH takes 6 flips and HT only 4. #math #probability #coinflip #puzzle"),
 13: ("ep13_two_envelopes", 31, "Two envelopes, one holds twice the other. You open yours: $100. Switch? The math says yes, then says switch back. #math #probability #paradox #puzzle"),
}


EPS2 = {
 1: ("ep07_moser_circle", 2, "The pattern 1, 2, 4, 8, 16 breaks at 6. Count the regions of a circle and see why. #math #puzzle #pattern #regions"),
 2: ("ep08_party_of_six", 3, "Among any 6 people, 3 always know each other or are all strangers. Here is why. #math #ramsey #graphtheory #puzzle"),
 3: ("ep09_medical_test", 4, "A 99% accurate test says positive. Your chance of being sick? About 50%. #math #probability #bayes #puzzle"),
 4: ("ep10_simpson", 5, "A beats B in each group, but B wins overall. Simpson's paradox with real data. #math #statistics #simpsonsparadox #puzzle"),
 5: ("ep11_hat_prisoners", 6, "100 prisoners, red or blue hats: one bit of parity saves 99. #math #puzzle #logic #hats"),
 14: ("ep14_prisoner_boxes", 1, "100 prisoners, 100 boxes, 50 tries each. Random guessing: about 0%. With the right plan: about 31%. #math #puzzle #probability #logic"),
 6: ("ep12_ant_rope", 7, "An ant on a rope that stretches 1 km per second: does it ever arrive? Yes. #math #infinity #harmonicseries #puzzle"),
}


def shot(pg, name):
    SHOTS.mkdir(parents=True, exist_ok=True); pg.screenshot(path=str(SHOTS / f"{name}.png"), timeout=60000)


def warm(pg, seconds):
    """So olha o feed: rola devagar com pausas irregulares. Nada de curtir, seguir ou comentar."""
    pg.goto("https://www.tiktok.com/foryou", wait_until="domcontentloaded"); time.sleep(6)
    end = time.time() + seconds
    while time.time() < end:
        time.sleep(random.uniform(5, 11)); pg.mouse.wheel(0, random.choice([700, 800, 900]))
    if pg.locator("text=/captcha|verify|Drag the slider/i").count(): raise SystemExit("verificacao/CAPTCHA no TikTok: parei")


def main():
    n = int(sys.argv[1]); dry = "--dry" in sys.argv
    warm_s = int(sys.argv[sys.argv.index("--warm") + 1]) if "--warm" in sys.argv else 60
    WEEK2 = "--week2" in sys.argv; MONTH = "Nov" if WEEK2 else "Oct"
    folder, day, cap = (EPS2 if WEEK2 else EPS)[n]
    video = ROOT / "puzzles" / folder / "renders" / f"{folder}_loud.mp4"
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9335", timeout=30000); ctx = b.contexts[0]
        pg = ctx.new_page(); pg.bring_to_front()
        warm(pg, warm_s)
        pg.goto("https://www.tiktok.com/tiktokstudio/upload", wait_until="domcontentloaded"); time.sleep(8)
        if "login" in pg.url.lower(): raise SystemExit("TikTok deslogado")
        pg.locator('input[type="file"]').first.set_input_files(str(video))
        for _ in range(60):                       # espera o editor aparecer
            time.sleep(2)
            if pg.locator('div[contenteditable="true"]').filter(visible=True).count(): break
        else: shot(pg, f"{n}-no-editor"); raise SystemExit("editor nao abriu")
        time.sleep(4)
        box = pg.locator('div[contenteditable="true"]').filter(visible=True).first
        box.click(); pg.keyboard.press("Control+A"); pg.keyboard.press("Delete"); pg.keyboard.insert_text(cap); time.sleep(2)
        pg.keyboard.press("Escape"); shot(pg, f"{n}-01-editor")
        pg.mouse.wheel(0, 1400); time.sleep(2)
        pg.get_by_text("Schedule", exact=True).first.click(); time.sleep(2)
        import re
        pg.get_by_text(re.compile(r"^[A-Z][a-z]{2} \d{1,2}, 20\d\d$")).filter(visible=True).first.click(); time.sleep(1.2)
        if WEEK2:
            yr = pg.get_by_text("2026", exact=True).filter(visible=True).first
            if pg.get_by_text("October", exact=True).filter(visible=True).count():
                bb = yr.bounding_box(); pg.mouse.click(bb["x"] + bb["width"] / 2 + 83, bb["y"] + bb["height"] / 2); time.sleep(1.2)
        pg.locator('button.DatePicker__day[data-outside="false"]').get_by_text(str(day), exact=True).first.click(); time.sleep(1.2)
        pg.get_by_text(re.compile(r"^\d{2}:\d{2}$")).filter(visible=True).first.click(); time.sleep(1.5)
        pg.get_by_text("18", exact=True).filter(visible=True).first.click(); time.sleep(1)
        m = pg.get_by_text("00", exact=True).filter(visible=True)
        bbs = [(m.nth(i).bounding_box(), i) for i in range(m.count())]
        idx = max((bb["x"], i) for bb, i in bbs if bb)[1]
        m.nth(idx).scroll_into_view_if_needed(); m.nth(idx).click(); time.sleep(1.2)
        pg.keyboard.press("Escape"); time.sleep(0.5)
        t = pg.inner_text("body"); i = t.find("When to post"); got = t[i:i + 110].replace(chr(10), " | ")
        assert f"{MONTH} {day}, 2026" in got and "18:00" in got, f"data/hora erradas: {got}"
        shot(pg, f"{n}-02-before")
        if dry: print("DRY:", got); return
        for attempt in range(6):                 # nunca clicar em "Post now": espera a checagem e tenta de novo
            if pg.get_by_text("Continue to post?").count():
                pg.get_by_role("button", name="Cancel").last.click(); time.sleep(25)
            pg.get_by_role("button", name="Schedule", exact=True).last.click(); time.sleep(7)
            if not pg.get_by_text("Continue to post?").count(): break
        else: raise SystemExit("checagem do TikTok nao terminou")
        pg.goto("https://www.tiktok.com/tiktokstudio/content", wait_until="domcontentloaded"); time.sleep(8)
        body = pg.inner_text("body"); assert f"{MONTH} {day}, 6:00 PM" in body, "agendamento nao apareceu em Posts"
        shot(pg, f"{n}-03-posts"); print("agendado:", n, folder, f"{MONTH} {day}, 6:00 PM"); pg.close()


main()
