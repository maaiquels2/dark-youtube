"""Replace the thumbnail of an existing YouTube video via the dedicated Chrome (CDP port 9333, already logged in).

Usage: python tools/yt_rethumb.py <video_id> <thumb.jpg>
Opens the Studio edit page, uploads the custom thumbnail, saves, reloads and screenshots output_yt/thumb-<id>-saved.png.
Only touches the thumbnail. No credentials are read or stored.
"""
import sys, time
from pathlib import Path
from yt_upload import studio_page, shot
from playwright.sync_api import sync_playwright

THUMB_SRC = """() => [...document.querySelectorAll('ytcp-thumbnails-compact-editor-uploader img, #still-picker img, ytcp-video-custom-still-editor img')]
    .filter(i => i.offsetWidth > 0).map(i => i.src.slice(0, 120))"""

def rethumb(vid, thumb):
    thumb = Path(thumb).resolve()
    if not thumb.exists() or thumb.stat().st_size > 2_000_000:
        raise SystemExit("Thumbnail missing or over 2 MB")
    with sync_playwright() as p:
        _, pg = studio_page(p)
        url = f"https://studio.youtube.com/video/{vid}/edit"
        pg.goto(url, wait_until="domcontentloaded"); time.sleep(10)
        print("TITLE:", pg.locator("#title-textarea #textbox").first.inner_text().strip())
        print("BEFORE:", pg.evaluate(THUMB_SRC))
        pg.locator("input#file-loader").first.set_input_files(str(thumb)); time.sleep(8)
        shot(pg, f"thumb-{vid}-before-save")
        pg.locator("ytcp-button#save, #save").filter(visible=True).first.click(); time.sleep(8)
        pg.goto(url, wait_until="domcontentloaded"); time.sleep(12)
        print("AFTER:", pg.evaluate(THUMB_SRC))
        shot(pg, f"thumb-{vid}-saved")

if __name__ == "__main__":
    rethumb(sys.argv[1], sys.argv[2])
