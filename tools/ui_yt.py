import time
from playwright.sync_api import sync_playwright
pid=open("fb_id.txt").read().strip()
with sync_playwright() as p:
    br=p.chromium.launch(channel="chrome"); pg=br.new_page(viewport={"width":1920,"height":1200})
    pg.goto("http://127.0.0.1:8765/",wait_until="networkidle"); time.sleep(2); pg.screenshot(path="output_yt/ui/01-projects-yt-buttons.png")
    print(pg.locator(".yt-big").count(), pg.locator(".yt-studio").first.get_attribute("href"))
    pg.evaluate(f"openProj('{pid}','publicacao')"); time.sleep(3); pg.screenshot(path="output_yt/ui/02-publicacao-yt-buttons.png")
    pg.evaluate(f"openProj('{pid}','imagens')"); time.sleep(3); pg.screenshot(path="output_yt/ui/03-imagens-uso-justo.png",full_page=True)
    br.close()

