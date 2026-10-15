import sys, time
from playwright.sync_api import sync_playwright
pid = open("fb_id.txt").read().strip(); out = sys.argv[1] if len(sys.argv) > 1 else "output_ui"
import os; os.makedirs(out, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True); pg = b.new_page(viewport={"width": 1600, "height": 1000})
    pg.goto("http://127.0.0.1:8765/"); time.sleep(1.5)
    pg.evaluate(f"openProj('{pid}')"); time.sleep(2)
    for k in ["pesquisa", "imagens", "prompts", "validacao"]:
        pg.evaluate(f"go('{k}')"); time.sleep(2.5)
        pg.screenshot(path=f"{out}/ui-{k}.png", full_page=False)
    b.close()
print("ok")
