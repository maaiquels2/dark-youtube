"""Reusable YouTube Studio upload via the dedicated Chrome (CDP port 9333, already logged in).

Usage: python tools/yt_upload.py <project_id> --thumb output/thumb.jpg --date "18 de out. de 2026" --time 18:00
Reads output/final.mp4, output/final.srt and output/youtube_kit.json (see tools/yt_kit.py).
Sets title/description/thumbnail/tags, not-for-kids, altered content = yes, language/category,
uploads the SRT, schedules (São Paulo tz) and verifies after reload. Screenshots go to output_yt/.
Studio UI is Portuguese; labels below match that locale. No credentials are read or stored.
"""
import argparse, json, time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
CHANNEL = "UCvmyoFV8fg5fMtoejd82CRA"
SHOTS = ROOT / "output_yt"

def studio_page(p):
    b = p.chromium.connect_over_cdp("http://127.0.0.1:9333"); ctx = b.contexts[0]
    pg = next((x for x in ctx.pages if "studio.youtube.com" in x.url), None) or ctx.new_page()
    return ctx, pg

def shot(pg, name):
    SHOTS.mkdir(exist_ok=True); pg.screenshot(path=str(SHOTS / f"{name}.png"))

def fill(pg, sel, text):
    pg.locator(sel).first.click(); pg.keyboard.press("Control+A"); pg.keyboard.press("Delete"); pg.keyboard.insert_text(text); time.sleep(1)

def pick(pg, trigger, label):
    pg.locator(trigger).first.click(); time.sleep(1)
    pg.locator(f"tp-yt-paper-item:has-text('{label}')").filter(visible=True).first.click(); time.sleep(1)

def upload(pid, thumb, date, hhmm, lang="Inglês", category="Educação"):
    pdir = ROOT / "projects" / pid; out = pdir / "output"
    kit = json.loads((out / "youtube_kit.json").read_text(encoding="utf-8"))
    with sync_playwright() as p:
        ctx, pg = studio_page(p); pg.bring_to_front()
        pg.goto(f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload?d=ud", wait_until="domcontentloaded"); time.sleep(6)
        # >50MB files can't go through Playwright over CDP; set them directly in the browser
        cdp = ctx.new_cdp_session(pg); doc = cdp.send("DOM.getDocument", {"depth": -1, "pierce": True})
        nid = cdp.send("DOM.querySelector", {"nodeId": doc["root"]["nodeId"], "selector": "input[type=file]"})["nodeId"]
        cdp.send("DOM.setFileInputFiles", {"nodeId": nid, "files": [str(out / "final.mp4")]}); time.sleep(12)
        fill(pg, "#title-textarea #textbox", kit["title"]); fill(pg, "#description-textarea #textbox", kit["description"])
        pg.locator("input#file-loader").first.set_input_files(str(pdir / thumb)); time.sleep(5)
        pg.locator("tp-yt-paper-radio-button[name=VIDEO_MADE_FOR_KIDS_NOT_MFK]").first.click()
        pg.locator("#toggle-button").first.click(); time.sleep(2)
        pg.locator("tp-yt-paper-radio-button[name=VIDEO_HAS_ALTERED_CONTENT_YES]").first.click()
        t = pg.locator("#tags-container input#text-input").first; t.click(); t.fill(",".join(kit["tags"]) + ",")
        langs = pg.evaluate("() => [...document.querySelectorAll('ytcp-dropdown-trigger')].map(e=>e.innerText)").__str__()
        if f"Idioma do vídeo {lang}" not in langs.replace("\\n", " "): pick(pg, "#language-input ytcp-dropdown-trigger", lang)
        if category not in langs: pick(pg, "#category ytcp-dropdown-trigger", category)
        vid = pg.locator("ytcp-video-info a").first.get_attribute("href").rsplit("/", 1)[-1]; shot(pg, "01-details")
        pg.locator("#next-button").click(); time.sleep(3)
        pg.locator("#subtitles-button, ytcp-button:has-text('Adicionar')").first.click(); time.sleep(4)
        pg.get_by_text("Enviar arquivo", exact=True).filter(visible=True).first.click(); time.sleep(2)
        with pg.expect_file_chooser() as fc:
            pg.locator("ytcp-button:has-text('Continuar')").filter(visible=True).first.click()
        fc.value.set_files(str(out / "final.srt")); time.sleep(6)
        pg.locator("ytcp-button:has-text('Pronto')").filter(visible=True).first.click(); time.sleep(4)
        pg.locator("#next-button").click(); time.sleep(3); pg.locator("#next-button").click(); time.sleep(3)
        pg.locator("#second-container-expand-button").click(); time.sleep(2)
        pg.locator("#datepicker-trigger").click(); time.sleep(2)
        di = pg.locator("ytcp-date-picker input").filter(visible=True).first; di.fill(date); pg.keyboard.press("Enter"); time.sleep(2)
        ti = pg.locator("#time-of-day-container input").first; ti.click(); ti.fill(hhmm); pg.keyboard.press("Enter"); time.sleep(2)
        pg.locator("#timezone-select-button").click(); time.sleep(2)
        pg.evaluate("""() => { const it=[...document.querySelectorAll('tp-yt-paper-item')].find(e=>/S.o Paulo/.test(e.innerText)); it.scrollIntoView(); it.click(); }"""); time.sleep(2)
        shot(pg, "02-schedule"); pg.locator("#done-button").click(); time.sleep(6)
        return vid

def verify(vid):
    with sync_playwright() as p:
        _, pg = studio_page(p)
        pg.goto(f"https://studio.youtube.com/video/{vid}/edit", wait_until="domcontentloaded"); time.sleep(10)
        r = {"title": pg.locator("#title-textarea #textbox").first.inner_text(),
             "not_for_kids": pg.locator("tp-yt-paper-radio-button[name=VIDEO_MADE_FOR_KIDS_NOT_MFK]").first.get_attribute("aria-checked"),
             "visibility": pg.locator("ytcp-video-metadata-visibility").first.inner_text().replace("\n", " ")}
        pg.locator("ytcp-video-metadata-visibility").first.click(); time.sleep(3)
        r["date"] = pg.locator("#datepicker-trigger").filter(visible=True).first.inner_text().strip()
        r["time"] = pg.locator("#time-of-day-container input").filter(visible=True).first.input_value()
        shot(pg, "03-verify"); pg.keyboard.press("Escape")
        return r

if __name__ == "__main__":
    a = argparse.ArgumentParser(); a.add_argument("pid"); a.add_argument("--thumb", required=True)
    a.add_argument("--date", required=True); a.add_argument("--time", default="18:00"); a.add_argument("--verify-only")
    o = a.parse_args()
    vid = o.verify_only or upload(o.pid, o.thumb, o.date, o.time)
    print("https://www.youtube.com/watch?v=" + vid); print(verify(vid))
