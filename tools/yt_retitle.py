"""Change the title of an existing YouTube video via the dedicated Chrome (CDP port 9333, already logged in).

Usage: python tools/yt_retitle.py <video_id> "<new title>"
Opens the Studio edit page, replaces the title, saves, reloads and prints the saved title.
Only touches the title field. Screenshots go to output_yt/. No credentials are read or stored.
"""
import sys, time
from yt_upload import studio_page, shot, fill
from playwright.sync_api import sync_playwright

def retitle(vid, title):
    if len(title) > 100:
        raise SystemExit("Title over 100 characters")
    with sync_playwright() as p:
        _, pg = studio_page(p)
        url = f"https://studio.youtube.com/video/{vid}/edit"
        pg.goto(url, wait_until="domcontentloaded"); time.sleep(10)
        old = pg.locator("#title-textarea #textbox").first.inner_text().strip()
        print("OLD:", old)
        if old == title:
            print("Already set."); return
        fill(pg, "#title-textarea #textbox", title)
        pg.locator("ytcp-button#save, #save").filter(visible=True).first.click(); time.sleep(6)
        shot(pg, f"retitle-{vid}-saved")
        pg.goto(url, wait_until="domcontentloaded"); time.sleep(10)
        new = pg.locator("#title-textarea #textbox").first.inner_text().strip()
        print("NEW:", new)
        print("OK" if new == title else "MISMATCH")

if __name__ == "__main__":
    retitle(sys.argv[1], sys.argv[2])
