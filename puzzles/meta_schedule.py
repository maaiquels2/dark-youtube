"""Show Your Work Puzzles: agenda Reels no Facebook + Instagram pelo Meta Business Suite (Chrome Profile 6, CDP 9335, login do usuario).
Uso: python puzzles/meta_schedule.py <n>   (n = 2..6; um por dia, 19:00 America/Sao_Paulo, 26/10 a 30/10)
Adaptado de tools/walt_meta_reels.py. Para no primeiro problema; confere o destino antes de enviar."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
ASSET = "https://business.facebook.com/latest/reels_composer/?asset_id=1402222739645815&business_id=1096751559873404"
EPS = {
 2: ("ep02_monty_hall", "26", "100 doors, one car. You pick one, the host opens 98 empty ones. Stay or switch? 🚪\n\n#math #montyhall #probability #puzzle"),
 3: ("ep03_birthday_paradox", "27", "Why do just 23 people give you a 50% chance of a shared birthday? Count the pairs. 🎂\n\n#math #probability #birthdayparadox #puzzle"),
 4: ("ep04_josephus", "28", "41 people in a circle, every second one is out. Who survives? A binary shortcut knows. ⭕\n\n#math #puzzle #binary #josephus"),
 5: ("ep05_tower_of_hanoi", "29", "Move 64 disks one at a time and it takes about 585 billion years. ⏳\n\n#math #towerofhanoi #exponential #puzzle"),
 6: ("ep06_hh_vs_ht", "30", "Same coin, same odds, but waiting for HH takes 6 flips and HT only 4. 🪙\n\n#math #probability #coinflip #puzzle"),
}
HH, MM = "19", "00"


def main():
    n = int(sys.argv[1]); folder, day, cap = EPS[n]
    vid = str((ROOT / "puzzles" / folder / "renders" / f"{folder}_loud.mp4").resolve())
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9335", timeout=30000); ctx = b.contexts[0]
        pg = ctx.new_page(); pg.bring_to_front()
        pg.goto(ASSET, wait_until="domcontentloaded"); pg.wait_for_timeout(9000)
        body = pg.evaluate("document.body.innerText")
        assert "Show Your Work Puzzles" in body and "syw.puzzles" in body, "destino nao e Show Your Work + syw.puzzles"
        with pg.expect_file_chooser(timeout=20000) as fc:
            pg.get_by_text("Adicionar vídeo", exact=True).first.click()
        fc.value.set_files(vid)
        for _ in range(60):
            if "100%" in pg.evaluate("document.body.innerText"): break
            pg.wait_for_timeout(2000)
        else: raise RuntimeError("upload nao chegou a 100%")
        pg.wait_for_timeout(3000)
        box = pg.locator('[contenteditable="true"]').first; box.click(); pg.keyboard.insert_text(cap); pg.wait_for_timeout(2000)
        pg.get_by_text("Detalhes do reel", exact=True).first.click(); pg.wait_for_timeout(800)
        for _ in range(2):
            pg.get_by_role("button", name="Avançar").last.click(); pg.wait_for_timeout(6000)
        assert "Opções de programação" in pg.evaluate("document.body.innerText"), "nao chegou ao passo Compartilhar"
        pg.get_by_text("Programar", exact=True).first.click(); pg.wait_for_timeout(2500)
        dates = pg.locator('input[placeholder="dd/mm/aaaa"]'); hs = pg.locator('input[aria-label="horas"]'); ms = pg.locator('input[aria-label="minutos"]')
        for i in (0, 1):                                    # 0 = Facebook, 1 = Instagram
            dates.nth(i).click(); pg.wait_for_timeout(1200)
            cell = pg.locator(f"text=/^{day}$/").filter(visible=True)
            assert cell.count() == 1, f"calendario: {cell.count()} celulas para o dia {day}"
            cell.first.click(); pg.wait_for_timeout(700)
            for loc, v in ((hs.nth(i), HH), (ms.nth(i), MM)):
                loc.click(); pg.keyboard.press("Control+A"); pg.keyboard.type(v); pg.wait_for_timeout(300)
            pg.get_by_text("Opções de programação", exact=True).first.click(); pg.wait_for_timeout(500)
        vals = pg.evaluate(r"[...document.querySelectorAll('input')].filter(e=>e.offsetParent&&e.placeholder==='dd/mm/aaaa').map(e=>e.value)")
        assert all(v.startswith(f"{day} de outubro") for v in vals), f"datas erradas: {vals}"
        txt = pg.evaluate("document.body.innerText"); want = f"{HH}\n:\n{MM}\nAmerica/Sao_Paulo"
        assert txt.count(want) == 2, f"horas erradas na tela (esperado {HH}:{MM} em Facebook e Instagram)"
        pg.screenshot(path=str(ROOT / "scratch" / f"meta_{n}_before.png"), timeout=60000)
        pg.get_by_role("button", name="Programar").last.click()
        for _ in range(30):
            t = pg.evaluate("document.body.innerText")
            if "Reel programado" in t: break
            pg.wait_for_timeout(1000)
        else: raise RuntimeError("sem confirmacao 'Reel programado'")
        msg = pg.evaluate(r"(document.body.innerText.match(/Seu reel está programado[^\n]*/)||['?'])[0]")
        pg.get_by_role("button", name="Concluir").first.click(); pg.wait_for_timeout(2000)
        print("agendado:", n, folder, msg); pg.close()


main()
