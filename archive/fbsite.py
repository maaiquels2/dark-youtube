from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(channel="chrome",headless=True); pg=b.new_page()
    try:
        pg.goto("https://firstbrandsgroup.com/",timeout=45000)
        print(pg.title()); print(pg.eval_on_selector_all("img,link[rel*=icon]","els=>els.map(e=>(e.src||e.href)+' '+(e.alt||'')).slice(0,15)"))
        pg.screenshot(path="fbsite.png")
    except Exception as e: print("ERR",e)
    b.close()
