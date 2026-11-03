"""Reusable YouTube Studio upload via the dedicated Chrome (CDP port 9333, already logged in).

Inclui MELHORIA 7:
  - Sincronizacao automatica de status="agendado", scheduled_at e published_url em projects/<id>.json e output/shorts/shorts.json
    para que o painel do Dark Studio mostre o selo dourado "Agendado" imediatamente apos cada envio.
  - Fila persistente (output_yt/upload_queue.json) caso o limite diario de 10 envios/24h do YouTube seja atingido,
    com suporte a `python tools/yt_upload.py --flush-queue` para retomar envios pendentes.
"""
import argparse, json, os, time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
CHANNEL = "UCvmyoFV8fg5fMtoejd82CRA"
SHOTS = ROOT / "output_yt"
QUEUE_FILE = SHOTS / "upload_queue.json"


def studio_page(p, fresh=False):
    """fresh=True: aba nova. Reaproveitar a aba de um envio/conferencia anterior travava o envio seguinte no '#next-button'."""
    b = p.chromium.connect_over_cdp(f"http://127.0.0.1:{os.environ.get('YT_CDP_PORT', '9333')}"); ctx = b.contexts[0]   # Ledger: YT_CDP_PORT=9336 (browser_profile_ledger)
    pg = (None if fresh else next((x for x in ctx.pages if "studio.youtube.com" in x.url), None)) or ctx.new_page()
    return ctx, pg


def shot(pg, name):
    SHOTS.mkdir(exist_ok=True); pg.screenshot(path=str(SHOTS / f"{name}.png"))


def fill(pg, sel, text):
    pg.locator(sel).first.click(); pg.keyboard.press("Control+A"); pg.keyboard.press("Delete"); pg.keyboard.insert_text(text); time.sleep(1)
    pg.evaluate("() => document.activeElement && document.activeElement.blur()"); time.sleep(0.7)


def pick(pg, trigger, label):
    pg.locator(trigger).first.click(); time.sleep(1)
    pg.locator(f"tp-yt-paper-item:has-text('{label}')").filter(visible=True).first.click(); time.sleep(1)


def enqueue_upload(job):
    SHOTS.mkdir(exist_ok=True)
    q = json.loads(QUEUE_FILE.read_text(encoding="utf-8")) if QUEUE_FILE.is_file() else []
    if not any(x.get("pid") == job.get("pid") and x.get("video") == job.get("video") for x in q):
        q.append(job)
        QUEUE_FILE.write_text(json.dumps(q, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Adicionado a fila pendente ({QUEUE_FILE}): {job.get('video')}", flush=True)


def sync_project_status(pid, vid, date, hhmm, video_path):
    """Sincroniza status='agendado' e URL publicada no JSON do projeto ou no shorts.json."""
    pfile = ROOT / "projects" / f"{pid}.json"
    pdir = ROOT / "projects" / pid
    vname = Path(video_path).name
    # Short = qualquer arquivo dentro de output/shorts (short-N, native-N, weil-N, binance-N...).
    # Antes so "short-*" contava, e os Shorts nativos sobrescreviam o youtube_id do video longo no JSON do projeto.
    if Path(video_path).parent.name == "shorts" or vname.startswith("short-"):
        sf = pdir / "output" / "shorts" / "shorts.json"
        if sf.is_file():
            shorts = json.loads(sf.read_text(encoding="utf-8"))
            for s in shorts:
                if s.get("file") == vname:
                    s["youtube_id"] = vid
                    s["published_url"] = f"https://youtube.com/shorts/{vid}"
                    s["scheduled_at"] = f"{date} {hhmm}"
                    s["status"] = "agendado"
            sf.write_text(json.dumps(shorts, ensure_ascii=False, indent=2), encoding="utf-8")
    else:
        if pfile.is_file():
            pj = json.loads(pfile.read_text(encoding="utf-8"))
            pj["status"] = "agendado"
            pj["youtube_id"] = vid
            pj["published_url"] = f"https://youtu.be/{vid}"
            pj["scheduled_at"] = f"{date} {hhmm} BRT"
            pfile.write_text(json.dumps(pj, ensure_ascii=False, indent=2), encoding="utf-8")


def upload(pid, thumb, date, hhmm, lang="Inglês", category="Educação", video=None, kit=None, srt="output/final.srt", resume=False, resume_vid=None):
    """Video longo: padrao (final.mp4 + youtube_kit.json + SRT + thumbnail). Short: video=<arquivo>, kit={title,description,tags},
    thumb=None e srt=None."""
    pdir = ROOT / "projects" / pid; out = pdir / "output"
    kit = kit or json.loads((out / "youtube_kit.json").read_text(encoding="utf-8"))
    video = Path(video) if video else out / "final.mp4"
    with sync_playwright() as p:
        ctx, pg = studio_page(p, fresh=True); pg.bring_to_front()
        if resume_vid:   # rascunho conhecido: abre pela lista (a pagina /edit tem um 2o campo de titulo atras da janela e o fill errava)
            pg.goto(f"https://studio.youtube.com/channel/{CHANNEL}/videos/{os.environ.get('YT_RESUME_TAB', 'short')}", wait_until="domcontentloaded"); time.sleep(8)
            row = pg.locator(f"ytcp-video-row:has(a[href*='{resume_vid}'])").first
            row.hover(); time.sleep(1)
            row.locator("ytcp-button:has-text('Editar rascunho'), a:has-text('Editar rascunho')").first.click(); time.sleep(6)
        elif resume:   # um envio anterior parou no meio e deixou um rascunho com o arquivo ja enviado: reabre o primeiro rascunho
            pg.goto(f"https://studio.youtube.com/channel/{CHANNEL}/videos/{os.environ.get('YT_RESUME_TAB', 'upload')}", wait_until="domcontentloaded"); time.sleep(7)  # Short em rascunho fica na aba "short"
            pg.locator("ytcp-video-row:has-text('Rascunho') ytcp-button:has-text('Editar rascunho'), ytcp-video-row:has-text('Rascunho') a:has-text('Editar rascunho')").first.click(); time.sleep(6)
        else:
            pg.goto(f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload?d=ud", wait_until="domcontentloaded"); time.sleep(6)
            cdp = ctx.new_cdp_session(pg); doc = cdp.send("DOM.getDocument", {"depth": -1, "pierce": True})
            nid = cdp.send("DOM.querySelector", {"nodeId": doc["root"]["nodeId"], "selector": "input[type=file]"})["nodeId"]
            cdp.send("DOM.setFileInputFiles", {"nodeId": nid, "files": [str(video)]}); time.sleep(12)
        if not (resume or resume_vid) and pg.get_by_text("limite diário de envios", exact=False).count():
            shot(pg, "00-limite-diario")
            enqueue_upload({
                "pid": pid, "thumb": thumb, "date": date, "hhmm": hhmm,
                "lang": lang, "category": category, "video": str(video), "kit": kit, "srt": srt,
            })
            pg.close()
            raise SystemExit("YouTube: limite diario de envios alcancado (salvo em output_yt/upload_queue.json para retomar com --flush-queue)")
        fill(pg, "#title-textarea #textbox", kit["title"]); fill(pg, "#description-textarea #textbox", kit["description"])
        if thumb: pg.locator("input#file-loader").first.set_input_files(str(pdir / thumb)); time.sleep(5)
        pg.locator("tp-yt-paper-radio-button[name=VIDEO_MADE_FOR_KIDS_NOT_MFK]").first.click()
        pg.locator("#toggle-button").first.click(); time.sleep(2)
        pg.locator("tp-yt-paper-radio-button[name=VIDEO_HAS_ALTERED_CONTENT_YES]").first.click()
        if kit.get("tags"):
            t = pg.locator("#tags-container input#text-input").first; t.click(); t.fill(",".join(kit["tags"]) + ",")
        langs = pg.evaluate("() => [...document.querySelectorAll('ytcp-dropdown-trigger')].map(e=>e.innerText)").__str__()
        if f"Idioma do vídeo {lang}" not in langs.replace("\\n", " "): pick(pg, "#language-input ytcp-dropdown-trigger", lang)
        if category not in langs: pick(pg, "#category ytcp-dropdown-trigger", category)
        vid = pg.locator("ytcp-video-info a").first.get_attribute("href").rsplit("/", 1)[-1]; shot(pg, "01-details")
        pg.locator("#next-button").click(); time.sleep(3)
        if srt:
            shot(pg, "wizard-pre-legendas")   # diagnostico: em que tela do assistente estamos antes de procurar o botao de legendas
            pg.locator("#subtitles-button, ytcp-button:has-text('Adicionar')").filter(visible=True).first.click(); time.sleep(4)
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
        # o menu de fuso deixa um fundo (iron-overlay-backdrop) por cima e o clique normal em Programar e barrado: clique direto no botao
        shot(pg, "02-schedule"); pg.locator("#done-button").first.evaluate("e => e.click()"); time.sleep(6)
        # 02/11/2026: com a verificacao de direitos ainda rodando, o YouTube mostra "Ainda estamos verificando seu conteudo"
        # com um botao Ok; sem clicar, o agendamento nao fecha e o envio seguinte travou a aba.
        for _ in range(3):
            ok = pg.locator("ytcp-button:has-text('Ok'), tp-yt-paper-dialog button:has-text('Ok')").filter(visible=True)
            if not ok.count(): break
            shot(pg, "02b-aviso-verificacao"); ok.first.click(); time.sleep(4)
            done = pg.locator("#done-button").filter(visible=True)
            if done.count(): done.first.evaluate("e => e.click()"); time.sleep(6)
        shot(pg, "03-depois-programar")
        sync_project_status(pid, vid, date, hhmm, video)
        pg.close(run_before_unload=False)   # nao deixar aba de envio aberta para o proximo envio
        return vid


def flush_queue():
    if not QUEUE_FILE.is_file():
        print("Fila vazia."); return
    q = json.loads(QUEUE_FILE.read_text(encoding="utf-8"))
    if not q:
        print("Fila vazia."); return
    rem = []
    for i, job in enumerate(q):
        try:
            vid = upload(job["pid"], job.get("thumb"), job["date"], job["hhmm"],
                         lang=job.get("lang", "Inglês"), category=job.get("category", "Educação"),
                         video=job.get("video"), kit=job.get("kit"), srt=job.get("srt"))
            print(f"Enviado da fila: {job.get('video')} -> https://youtu.be/{vid}", flush=True)
        except SystemExit as e:
            print(f"Pausa na fila ({e}); restam {len(q) - i} itens.", flush=True)
            rem.extend(q[i:])
            break
    QUEUE_FILE.write_text(json.dumps(rem, ensure_ascii=False, indent=2), encoding="utf-8")


def verify(vid):
    with sync_playwright() as p:
        _, pg = studio_page(p, fresh=True)
        pg.goto(f"https://studio.youtube.com/video/{vid}/edit", wait_until="domcontentloaded")
        pg.locator("#title-textarea #textbox").first.wait_for(timeout=90000); time.sleep(3)
        r = {"title": pg.locator("#title-textarea #textbox").first.inner_text(),
             "not_for_kids": pg.locator("tp-yt-paper-radio-button[name=VIDEO_MADE_FOR_KIDS_NOT_MFK]").first.get_attribute("aria-checked"),
             "visibility": pg.locator("ytcp-video-metadata-visibility").first.inner_text().replace("\n", " ")}
        pg.locator("ytcp-video-metadata-visibility").first.click(); time.sleep(3)
        r["date"] = pg.locator("#datepicker-trigger").filter(visible=True).first.inner_text().strip()
        r["time"] = pg.locator("#time-of-day-container input").filter(visible=True).first.input_value()
        shot(pg, "03-verify"); pg.keyboard.press("Escape"); time.sleep(1); pg.close()
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
        pg.locator("ytcp-video-visibility-select ~ * #save-button, #save-button").filter(visible=True).first.click(); time.sleep(3)
        pg.locator("ytcp-button#save").filter(visible=True).first.click(); time.sleep(6)
        shot(pg, f"resched-{vid}-2"); pg.close()


if __name__ == "__main__":
    a = argparse.ArgumentParser(); a.add_argument("pid", nargs="?"); a.add_argument("--thumb")
    a.add_argument("--date"); a.add_argument("--time", default="18:00"); a.add_argument("--verify-only")
    a.add_argument("--flush-queue", action="store_true"); a.add_argument("--resume", action="store_true", help="termina o rascunho que um envio anterior deixou")
    o = a.parse_args()
    if o.flush_queue:
        flush_queue(); raise SystemExit(0)
    vid = o.verify_only or upload(o.pid, o.thumb, o.date, o.time, resume=o.resume)
    print("https://www.youtube.com/watch?v=" + vid); print(verify(vid))
