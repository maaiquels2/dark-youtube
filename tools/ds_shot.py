import json
from pathlib import Path
pid = open("fb_id.txt").read().strip(); f = Path(f"projects/{pid}.json"); d = json.loads(f.read_text(encoding="utf-8")); d["scheduled_at"] = "2026-10-18 18:00"; f.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
from playwright.sync_api import sync_playwright
import time
with sync_playwright() as p:
    br = p.chromium.launch(channel="chrome"); pg = br.new_page(viewport={"width": 1600, "height": 1000})
    pg.goto("http://127.0.0.1:8765/", wait_until="networkidle"); time.sleep(2); pg.screenshot(path="output_yt/18-ds-list.png")
    pg.evaluate(f"openProj('{pid}','publicacao')"); time.sleep(3); pg.screenshot(path="output_yt/19-ds-publicacao.png")
    print(pg.locator("body").inner_text()[:400].replace("\n", " | "))

