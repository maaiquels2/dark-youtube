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

def studio_page(p, fresh=False):
    """fresh=True: aba nova. Reaproveitar a aba de um envio/conferencia anterior travava o envio seguinte no '#next-button'."""
    b = p.chromium.connect_over_cdp("http://127.0.0.1:9333"); ctx = b.contexts[0]
    pg = (None if fresh else next((x for x in ctx.pages if "studio.youtube.com" in x.url), None)) or ctx.new_page()
    return ctx, pg

def shot(pg, name):
    SHOTS.mkdir(exist_ok=True); pg.screenshot(path=str(SHOTS / f"{name}.png"))

def fill(pg, sel, text):
    pg.locator(sel).first.click(); pg.keyboard.press("Control+A"); pg.keyboard.press("Delete"); pg.keyboard.insert_text(text); time.sleep(1)
    pg.evaluate("() => document.activeElement && document.activeElement.blur()"); time.sleep(0.7)  # fecha as sugestoes de #hashtag (cobrem o campo seguinte); Escape fecharia o dialogo

def pick(pg, trigger, label):
    pg.locator(trigger).first.click(); time.sleep(1)
    pg.locator(f"tp-yt-paper-item:has-text('{label}')").filter(visible=True).first.click(); time.sleep(1)

def upload(pid, thumb, date, hhmm, lang="Inglês", category="Educação", video=None, kit=None, srt="output/final.srt"):
    """Video longo: padrao (final.mp4 + youtube_kit.json + SRT + thumbnail). Short: video=<arquivo>, kit={title,description,tags},
    thumb=None e srt=None (a legenda ja esta gravada na imagem; o fluxo de Short nao aceita thumbnail propria)."""
    pdir = ROOT / "projects" / pid; out = pdir / "output"
    kit = kit or json.loads((out / "youtube_kit.json").read_text(encoding="utf-8"))
    video = Path(video) if video else out / "final.mp4"
    with sync_playwright() as p:
        ctx, pg = studio_page(p, fresh=True); pg.bring_to_front()  # a aba fica aberta: um video longo continua subindo por ela
        pg.goto(f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload?d=ud", wait_until="domcontentloaded"); time.sleep(6)
        # >50MB files can't go through Playwright over CDP; set them directly in the browser
        cdp = ctx.new_cdp_session(pg); doc = cdp.send("DOM.getDocument", {"depth": -1, "pierce": True})
        nid = cdp.send("DOM.querySelector", {"nodeId": doc["root"]["nodeId"], "selector": "input[type=file]"})["nodeId"]
        cdp.send("DOM.setFileInputFiles", {"nodeId": nid, "files": [str(video)]}); time.sleep(12)
        if pg.get_by_text("limite diário de envios", exact=False).count():  # o Studio bloqueia por 24 h ou ate a verificacao do canal
            shot(pg, "00-limite-diario"); raise SystemExit("YouTube: limite diario de envios alcancado (verificar o canal ou esperar 24 h)")
        fill(pg, "#title-textarea #textbox", kit["title"]); fill(pg, "#description-textarea #textbox", kit["description"])
        if thumb: pg.locator("input#file-loader").first.set_input_files(str(pdir / thumb)); time.sleep(5)
        pg.locator("tp-yt-paper-radio-button[name=VIDEO_MADE_FOR_KIDS_NOT_MFK]").first.click()
        pg.locator("#toggle-button").first.click(); time.sleep(2)
        pg.locator("tp-yt-paper-radio-button[name=VIDEO_HAS_ALTERED_CONTENT_YES]").first.click()
        t = pg.locator("#tags-container input#text-input").first; t.click(); t.fill(",".join(kit["tags"]) + ",")
        langs = pg.evaluate("() => [...document.querySelectorAll('ytcp-dropdown-trigger')].map(e=>e.innerText)").__str__()
        if f"Idioma do vídeo {lang}" not in langs.replace("\\n", " "): pick(pg, "#language-input ytcp-dropdown-trigger", lang)
        if category not in langs: pick(pg, "#category ytcp-dropdown-trigger", category)
        vid = pg.locator("ytcp-video-info a").first.get_attribute("href").rsplit("/", 1)[-1]; shot(pg, "01-details")
        pg.locator("#next-button").click(); time.sleep(3)
        if srt:
            pg.locator("#subtitles-button, ytcp-button:has-text('Adicionar')").first.click(); time.sleep(4)
            pg.get_by_text("Enviar arquivo", exact=True).filter(visible=True).first.click(); time.sleep(2)
            with pg.expect_file_chooser() as fc:
                pg.locator("ytcp-button:has-text('Continuar')").filter(visible=True).first.click()
            fc.value.set_files(str(pdir / srt)); time.sleep(6)
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
        _, pg = studio_page(p, fresh=True)
        pg.goto(f"https://studio.youtube.com/video/{vid}/edit", wait_until="domcontentloaded")
        pg.locator("#title-textarea #textbox").first.wait_for(timeout=90000); time.sleep(3)  # o editor demora a carregar logo apos um envio
        r = {"title": pg.locator("#title-textarea #textbox").first.inner_text(),
             "not_for_kids": pg.locator("tp-yt-paper-radio-button[name=VIDEO_MADE_FOR_KIDS_NOT_MFK]").first.get_attribute("aria-checked"),
             "visibility": pg.locator("ytcp-video-metadata-visibility").first.inner_text().replace("\n", " ")}
        pg.locator("ytcp-video-metadata-visibility").first.click(); time.sleep(3)
        r["date"] = pg.locator("#datepicker-trigger").filter(visible=True).first.inner_text().strip()
        r["time"] = pg.locator("#time-of-day-container input").filter(visible=True).first.input_value()
        shot(pg, "03-verify"); pg.keyboard.press("Escape"); time.sleep(1); pg.close()  # conferencia so le: a aba pode fechar
        return r

def reschedule(vid, date, hhmm):
    """Muda a data/hora de estreia de um video ja agendado (fuso de Sao Paulo) e salva. Confira depois com verify()."""
    with sync_playwright() as p:
        _, pg = studio_page(p, fresh=True)
        pg.goto(f"https://studio.youtube.com/video/{vid}/edit", wait_until="domcontentloaded")
        pg.locator("ytcp-video-metadata-visibility").first.wait_for(timeout=90000); time.sleep(3)
        pg.locator("ytcp-video-metadata-visibility").first.click(); time.sleep(3)
        pg.locator("#datepicker-trigger").filter(visible=True).first.click(); time.sleep(2)
        di = pg.locator("ytcp-date-picker input").filter(visible=True).first; di.fill(date); pg.keyboard.press("Enter"); time.sleep(2)
        ti = pg.locator("#time-of-day-container input").filter(visible=True).first; ti.click(); ti.fill(hhmm); pg.keyboard.press("Enter"); time.sleep(2)
        shot(pg, f"resched-{vid}-1")
        pg.locator("ytcp-video-visibility-select ~ * #save-button, #save-button").filter(visible=True).first.click(); time.sleep(3)  # "Concluído" do dialogo
        pg.locator("ytcp-button#save").filter(visible=True).first.click(); time.sleep(6)  # "Salvar" da pagina
        shot(pg, f"resched-{vid}-2"); pg.close()


if __name__ == "__main__":
    a = argparse.ArgumentParser(); a.add_argument("pid"); a.add_argument("--thumb", required=True)
    a.add_argument("--date", required=True); a.add_argument("--time", default="18:00"); a.add_argument("--verify-only")
    o = a.parse_args()
    vid = o.verify_only or upload(o.pid, o.thumb, o.date, o.time)
    print("https://www.youtube.com/watch?v=" + vid); print(verify(vid))
