# -*- coding: utf-8 -*-
"""Dark Studio - gera cenas no grok.com/imagine automaticamente.

Abordagem (igual a Fabrica TikTok): Chrome NATIVO do sistema com um perfil
DEDICADO (browser_profile/) - nunca o Chrome/perfis do usuario. Para automatizar,
o Chrome dedicado e aberto com --remote-debugging-port e o worker se conecta via
CDP (Playwright connect_over_cdp). So mata processos Chrome cujo command line
contem o caminho do perfil dedicado.

Uso: python grok_worker.py <project_id> [--scenes 0,3,5] [--concurrency 2] [--login]
Controle: logs/grok_control.txt com run|pause|stop. Status: logs/grok_auto.json
"""
import argparse, asyncio, base64, hashlib, json, os, re, socket, subprocess, sys, time, traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECTS = ROOT / "projects"
PROFILE = ROOT / "browser_profile"
PORT = int(os.environ.get("DS_CDP_PORT", "9333"))
URL = "https://grok.com/imagine"
CHROME_PATHS = [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe")]
RES_RE = os.environ.get("DS_GROK_RES", r"1080p")  # plano atual suporta 1080p; cai para 720p se o Grok recusar
VIDEO_GAP = 20.0          # ~3 videos/min
IMAGE_GAP = 4.0
MAX_RETRIES = 2
GEN_TIMEOUT = {"image": 180, "video": 600}

LOGIN_RE = re.compile(r"accounts\.x\.ai|/sign-?in|/login", re.I)
CAPTCHA_RE = re.compile(r"verify you are human|verifique que voc[eê] [eé] humano|are you a robot|captcha|cloudflare", re.I)
LIMIT_RE = re.compile(r"reached (your|the) (daily |usage )?limit|limit reached|rate limit|too many requests|"
                      r"atingiu (o|seu) limite|limite (di[aá]rio|atingido)|try again later|tente novamente mais tarde|"
                      r"upgrade to (supergrok|premium)", re.I)


SLUG_SKIP = set("""a an the of in on at to for from with and or by as into onto over under before after between beside behind
above below toward towards through across around while its their his her this that these those one two three is are was were be
wide close closeup medium tight shot view interior exterior frame framed begin track glide smooth slow slowly ascending descending
aerial move moves reveals revealing documentary reconstruction conceptual composition cinematic anonymous contemporary modern
realistic scene image video camera subject inside outside seen viewed level dramatic soft warm cold golden light lighting
reconstructed reconstruct during late early smoothly showing shows""".split())


def slug(text, n=3):
    """Resumo curto do prompt para o nome do arquivo: '03_warehouse_cash_tray'."""
    out = []
    for w in re.findall(r"[a-z]+", re.sub(r"^\s*subject:\s*", "", (text or "").lower())):
        if len(w) > 2 and w not in SLUG_SKIP and w not in out:
            out.append(w)
            if len(out) == n:
                break
    return "_".join(out) or "scene"


class NeedsUser(Exception):
    pass


def chrome_exe():
    for p in CHROME_PATHS:
        if os.path.isfile(p):
            return p
    raise RuntimeError("Chrome nao encontrado.")


def port_open():
    s = socket.socket(); s.settimeout(0.5)
    try:
        s.connect(("127.0.0.1", PORT)); return True
    except OSError:
        return False
    finally:
        s.close()


def profile_chrome_pids():
    """PIDs de chrome.exe que usam SOMENTE o perfil dedicado do Dark Studio."""
    needle = str(PROFILE).lower()
    ps = ("Get-CimInstance Win32_Process -Filter \"Name='chrome.exe'\" | "
          "ForEach-Object { \"$($_.ProcessId)`t$($_.CommandLine)\" }")
    out = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True, timeout=30).stdout
    pids = []
    for line in out.splitlines():
        pid, _, cmd = line.partition("\t")
        if needle in cmd.lower() and pid.strip().isdigit():
            pids.append(int(pid))
    return pids


def ensure_chrome(url=URL):
    if port_open():
        return False
    if profile_chrome_pids():
        # Chrome dedicado aberto SEM depuracao (ex.: aberto a mao) - reinicia so ele.
        for pid in profile_chrome_pids():
            subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"], capture_output=True)
        time.sleep(1.5)
    PROFILE.mkdir(parents=True, exist_ok=True)
    subprocess.Popen([chrome_exe(), f"--user-data-dir={PROFILE}", "--profile-directory=Default",
                      f"--remote-debugging-port={PORT}", "--no-first-run", "--no-default-browser-check",
                      "--disable-session-crashed-bubble", "--new-window", url],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(60):
        if port_open():
            return True
        time.sleep(0.5)
    raise RuntimeError("Chrome dedicado nao abriu a porta de depuracao.")


FLOW_HOME = "https://flow.google.com/"
FLOW_MODEL = os.environ.get("DS_FLOW_MODEL", "Omni 1.1 Flash")
FLOW_CREDIT_RE = re.compile(r"cr[eé]ditos? insuficientes|sem cr[eé]ditos|not enough credits|out of credits|insufficient credits", re.I)
FLOW_FAIL_RE = re.compile(r"falha na gera|n[aã]o foi poss[ií]vel gerar|generation failed|couldn.t generate|viol(a|ou) (a|as|nossas)|policy", re.I)
FLOW_VIDS_JS = "() => [...document.querySelectorAll('video')].map(v => ({src: v.currentSrc || v.src, w: v.videoWidth, rs: v.readyState}))"


class Worker:
    def __init__(self, pid, scenes=None, concurrency=2, video_engine="grok", flow_model=FLOW_MODEL, only=None):
        self.video_engine, self.flow_model, self.only_mode = video_engine, flow_model, only
        self.pid = Path(pid).name
        self.pfile = PROJECTS / f"{self.pid}.json"
        self.pdir = PROJECTS / self.pid
        self.media = self.pdir / "media"; self.media.mkdir(parents=True, exist_ok=True)
        self.logs = self.pdir / "logs"; self.logs.mkdir(parents=True, exist_ok=True)
        self.status_f = self.logs / "grok_auto.json"
        self.ctrl_f = self.logs / "grok_control.txt"
        self.log_f = self.logs / "grok_auto.log"
        self.only = scenes
        self.conc = max(1, min(3, int(concurrency)))
        self.state = {"state": "starting", "message": "", "scenes": {}, "started_at": time.strftime("%H:%M:%S"),
                      "pid": os.getpid(), "concurrency": self.conc}
        self.last_submit = {"video": 0.0, "image": 0.0}
        self.submit_lock = asyncio.Lock()
        self.flock = asyncio.Lock()

    # ---------- infra ----------
    def log(self, msg):
        line = f"{time.strftime('%Y-%m-%d %H:%M:%S')} {msg}"
        print(line, flush=True)
        with open(self.log_f, "a", encoding="utf-8") as f:
            f.write(line + "\n")

    def save_status(self, **kw):
        self.state.update(kw); self.state["updated_at"] = time.strftime("%H:%M:%S")
        tmp = self.status_f.with_suffix(".tmp")
        tmp.write_text(json.dumps(self.state, ensure_ascii=False, indent=1), encoding="utf-8")
        os.replace(tmp, self.status_f)

    def scene_status(self, i, st, err=None):
        self.state["scenes"][str(i)] = {"status": st, "error": err, "at": time.strftime("%H:%M:%S")}
        self.save_status()

    def control(self):
        try:
            return self.ctrl_f.read_text(encoding="utf-8").strip() or "run"
        except OSError:
            return "run"

    async def gate(self):
        while True:
            c = self.control()
            if c == "stop":
                raise asyncio.CancelledError()
            if c == "pause":
                if self.state["state"] not in ("paused", "needs_user"):  # nao apaga o motivo do needs_user
                    self.save_status(state="paused", message="Pausado.")
                await asyncio.sleep(2); continue
            if self.state["state"] == "paused":
                self.save_status(state="running", message="Retomado.")
            return

    def load(self):
        return json.loads(self.pfile.read_text(encoding="utf-8"))

    async def mark_done(self, i, rel, mode, via="grok.com/imagine"):
        async with self.flock:
            for _ in range(5):
                try:
                    d = self.load()
                    d["scenes"][i].update(status="pronto", file=rel, error=None, cost_usd=0,
                                          generated_with=f"{via} ({mode}, auto)")
                    tmp = self.pfile.with_suffix(".tmp")
                    tmp.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
                    os.replace(tmp, self.pfile); return
                except (OSError, json.JSONDecodeError):
                    await asyncio.sleep(0.5)

    def file_hashes(self):
        """md5 -> numero da cena, dos arquivos que o projeto ja usa (trava contra salvar o video de outra cena)."""
        out = {}
        for i, sc in enumerate(self.load().get("scenes") or []):
            f = sc.get("file")
            if f and (self.pdir / f).is_file():
                out.setdefault(hashlib.md5((self.pdir / f).read_bytes()).hexdigest(), i + 1)
        return out

    @staticmethod
    def is_gfx(sc):
        return any((x or {}).get("type") in ("timeline", "chart", "document", "quote", "relmap", "scale", "chapter", "headline", "photo", "entity_full", "moneyflow", "collapse") for x in (sc.get("gfx") or []))

    def handoff(self):
        """Entrega para a edicao/narracao: media/manifest.json, folha de quadros e media/PRONTO."""
        d = self.load(); scenes, missing = [], []
        for i, sc in enumerate(d.get("scenes") or []):
            f = sc.get("file"); has = bool(f and (self.pdir / f).is_file())
            src = "gfx" if self.is_gfx(sc) else "grok"
            if src == "grok" and not has:
                missing.append(i + 1)
            scenes.append({"scene": i + 1, "source": src, "mode": sc.get("mode") or "image", "file": f if has else None,
                           "narration": sc.get("narration") or "",
                           "seconds": round(len((sc.get("narration") or "").split()) / 150 * 60, 1)})
        man = {"project": self.pid, "title": d.get("title"), "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
               "files_relative_to": f"projects/{self.pid}", "grok_missing": missing, "scenes": scenes}
        tmp = self.media / "manifest.tmp"
        tmp.write_text(json.dumps(man, ensure_ascii=False, indent=1), encoding="utf-8"); os.replace(tmp, self.media / "manifest.json")
        if missing:
            return f"Faltam cenas do Grok {missing}: manifest.json gravado, PRONTO nao."
        r = subprocess.run([sys.executable, str(ROOT / "tools" / "contact_sheet.py"), self.pid, str(self.media)],
                           capture_output=True, text=True, timeout=900)
        sheet = "folha de quadros" if r.returncode == 0 else "SEM folha de quadros (ver log)"
        if r.returncode:
            self.log("folha de quadros falhou: " + (r.stderr or r.stdout)[-1500:])
        (self.media / "PRONTO").write_text(time.strftime("%Y-%m-%d %H:%M:%S"), encoding="utf-8")
        name = (d.get("title") or self.pid).split(":")[0].strip()
        msg = f"{name} pronto: manifest.json, {sheet} e PRONTO em projects/{self.pid}/media/."
        self.log(msg)
        return msg

    def queue(self):
        d = self.load(); q = []
        for i, sc in enumerate(d.get("scenes") or []):
            if self.only is not None and i not in self.only:
                continue
            f = sc.get("file")
            if f and (self.pdir / f).is_file():
                continue
            if self.is_gfx(sc):
                continue  # cena de grafico (inclui mapa do dinheiro e queda animada): gerada pelo gfx.py, nao pelo Grok
            prompt = sc.get("grok_prompt") or sc.get("visual_prompt")
            if self.only_mode and ("video" if sc.get("mode") == "video" else "image") != self.only_mode:
                continue
            if prompt:
                w = len((sc.get("narration") or "").split())
                q.append((i, "video" if sc.get("mode") == "video" else "image", prompt, max(1, round(w / 150 * 60)),
                          f"{i+1:02d}_{slug(sc.get('visual_prompt') or prompt)}"))
        return q

    async def shot(self, page, name):
        try:
            p = self.logs / f"{time.strftime('%H%M%S')}-{name}.png"
            await page.screenshot(path=str(p)); return p.name
        except Exception:
            return None

    # ---------- page checks ----------
    async def check_blockers(self, page):
        url = page.url
        if LOGIN_RE.search(url):
            raise NeedsUser("login")
        try:
            txt = await page.evaluate("() => document.body ? document.body.innerText.slice(0, 20000) : ''")
        except Exception:
            txt = ""
        if await self.logged_out(page):
            raise NeedsUser("login")
        for fr in page.frames:
            if re.search(r"challenges\.cloudflare|hcaptcha|recaptcha|arkoselabs", fr.url or "", re.I):
                raise NeedsUser("captcha")
        if CAPTCHA_RE.search(txt) and re.search(r"verify|verifique|robot|human", txt, re.I):
            raise NeedsUser("captcha")
        m = LIMIT_RE.search(txt)
        if m:
            raise NeedsUser(f"limite do Grok: '{m.group(0)}'")

    async def logged_out(self, page):
        for name in ("Entrar", "Sign in", "Log in", "Criar conta", "Sign up"):
            loc = page.get_by_role("link", name=name, exact=True)
            try:
                if await loc.count() and await loc.first.is_visible():
                    return True
            except Exception:
                pass
        return False

    async def dismiss_cookies(self, page):
        for name in ("Rejeitar todos", "Reject all", "Aceitar todos os cookies", "Accept all cookies"):
            b = page.get_by_role("button", name=name)
            try:
                if await b.count() and await b.first.is_visible():
                    await b.first.click(timeout=2000); return
            except Exception:
                pass

    async def click_named(self, page, names, required=True):
        for n in names:
            loc = page.get_by_role("button", name=re.compile(rf"^\s*{n}\s*$", re.I))
            try:
                if await loc.count():
                    await loc.first.click(timeout=4000); return True
            except Exception:
                continue
        if required:
            raise RuntimeError(f"Botao nao encontrado: {names}")
        return False

    async def dismiss_popups(self, page):
        for n in ("Fechar", "Close"):
            b = page.get_by_role("button", name=n, exact=True)
            try:
                if await b.count() and await b.first.is_visible():
                    await b.first.click(timeout=2000)
            except Exception:
                pass

    async def set_mode(self, page, mode):
        names = ["Vídeo", "Video"] if mode == "video" else ["Imagem", "Image"]
        for n in names:
            r = page.get_by_role("radio", name=n, exact=True)
            if await r.count():
                await r.first.click(timeout=5000); await page.wait_for_timeout(700); return
        await self.click_named(page, names)

    async def pick_menu(self, page, labels, option_re):
        """Abre o botao com aria-label (um de labels) e escolhe o menuitemradio cujo texto casa option_re."""
        for lab in labels:
            btn = page.locator(f'button[aria-label="{lab}"]')
            if not await btn.count():
                continue
            if re.match(option_re, (await btn.first.inner_text()).strip()):
                return True
            await btn.first.click(timeout=5000); await page.wait_for_timeout(500)
            items = page.locator('[role="menuitemradio"], [role="menuitem"], [role="option"]')
            for k in range(await items.count()):
                it = items.nth(k)
                if re.match(option_re, (await it.inner_text()).strip()):
                    await it.click(timeout=4000); await page.wait_for_timeout(400); return True
            await page.keyboard.press("Escape")
        self.log(f"aviso: menu {labels} sem opcao {option_re}")
        return False

    async def set_aspect(self, page):
        await self.pick_menu(page, ["Aspecto de proporção", "Aspect ratio"], r"16:9")

    async def set_video_opts(self, page, dur):
        res = getattr(self, "res", RES_RE)
        if not await self.pick_menu(page, ["Resolução do vídeo", "Video resolution"], res) and res != "720p":
            self.log(f"aviso: opcao {res} indisponivel; usando 720p"); self.res = "720p"
            await self.pick_menu(page, ["Resolução do vídeo", "Video resolution"], "720p")
        opt = "6s" if dur <= 7 else ("10s" if dur <= 11 else "15s")
        await self.pick_menu(page, ["Duração do vídeo", "Video duration"], re.escape(opt))

    async def set_image_count(self, page):
        await self.pick_menu(page, ["Contagem de Imagens", "Image count"], r"^1\b")

    async def fill_prompt(self, page, prompt):
        box = page.locator("textarea:visible, [contenteditable='true']:visible").first
        await box.wait_for(timeout=15000)
        await box.click()
        await page.keyboard.press("Control+A"); await page.keyboard.press("Delete")
        tag = await box.evaluate("e => e.tagName")
        if tag == "TEXTAREA":
            await box.fill(prompt)
        else:
            await page.keyboard.insert_text(prompt)
        await page.wait_for_timeout(300)

    async def submit(self, page):
        await page.wait_for_timeout(400)
        for n in ("submeter", "Submit", "Enviar", "Send", "Gerar", "Generate"):
            loc = page.get_by_role("button", name=re.compile(rf"^\s*{n}\s*$", re.I))
            try:
                if await loc.count() and await loc.first.is_enabled():
                    await loc.first.click(timeout=4000); return
            except Exception:
                continue
        await page.keyboard.press("Enter")

    MEDIA_JS = """(mode) => {
      const out = [];
      const els = mode === 'video' ? document.querySelectorAll('video') : document.querySelectorAll('img');
      for (const e of els) {
        const src = mode === 'video' ? (e.currentSrc || e.src || (e.querySelector('source')||{}).src) : (e.currentSrc || e.src);
        if (!src || src.startsWith('data:image/svg')) continue;
        const r = e.getBoundingClientRect();
        const w = mode === 'video' ? (e.videoWidth || r.width) : (e.naturalWidth || 0);
        const h = mode === 'video' ? (e.videoHeight || r.height) : (e.naturalHeight || 0);
        if (w < 400 || h < 200) continue;
        out.push({src, w, h, ready: mode === 'video' ? e.readyState : (e.complete ? 4 : 0)});
      }
      return out;
    }"""

    async def wait_result(self, page, mode, before):
        deadline = time.time() + GEN_TIMEOUT[mode]
        stable_src, stable_n = None, 0
        while time.time() < deadline:
            await self.gate()
            await self.check_blockers(page)
            if getattr(page, "_ds_err", None):
                e = page._ds_err
                if LIMIT_RE.search(e) or "limit" in e.lower() or "quota" in e.lower():
                    raise NeedsUser(f"limite do Grok: {e}")
                if mode == "video" and getattr(self, "res", RES_RE) != "720p":
                    self.res = "720p"; self.log(f"Grok recusou {RES_RE} ({e}); fallback para 720p nas proximas tentativas")
                raise RuntimeError(f"Grok recusou: {e}")
            items = [x for x in await page.evaluate(self.MEDIA_JS, mode) if x["src"] not in before]
            if mode == "video":
                items = [x for x in items if x["ready"] >= 2]
            if items:
                src = items[0]["src"]
                stable_n = stable_n + 1 if src == stable_src else 1
                stable_src = src
                # imagens do Grok passam por previews progressivos: espera estabilizar
                if stable_n >= (2 if mode == "video" else 3):
                    return src
            await page.wait_for_timeout(3000)
        raise TimeoutError(f"Grok nao entregou o {mode} em {GEN_TIMEOUT[mode]}s")

    async def fetch_bytes(self, page, src):
        if src.startswith("data:"):
            return base64.b64decode(src.split(",", 1)[1])
        try:
            b64 = await page.evaluate("""async (u) => { const r = await fetch(u, {credentials:'include'});
                if (!r.ok) throw new Error('HTTP '+r.status); const b = await r.blob();
                return await new Promise(res => { const f = new FileReader(); f.onload = () => res(f.result.split(',')[1]); f.readAsDataURL(b); }); }""", src)
            return base64.b64decode(b64)
        except Exception as e:
            if src.startswith("blob:"):
                raise
            self.log(f"fetch na pagina falhou ({e}); tentando request do contexto")
            r = await page.context.request.get(src)
            if not r.ok:
                raise RuntimeError(f"download HTTP {r.status}")
            return await r.body()

    @staticmethod
    def ext_for(data, mode):
        if data[4:8] == b"ftyp": return ".mp4"
        if data[:4] == b"\x1aE\xdf\xa3": return ".webm"
        if data[:3] == b"\xff\xd8\xff": return ".jpg"
        if data[:8] == b"\x89PNG\r\n\x1a\n": return ".png"
        if data[:4] == b"RIFF" and data[8:12] == b"WEBP": return ".webp"
        return ".mp4" if mode == "video" else ".jpg"

    # ---------- Google Flow (videos enquanto o Grok esta sem credito) ----------
    async def flow_radio(self, page, label, required=True):
        loc = page.get_by_role("radio", name=re.compile(rf"(^|\s){re.escape(label)}$"))
        if not await loc.count():
            if required:
                raise RuntimeError(f"Flow: opcao '{label}' nao encontrada")
            return False
        if await loc.first.get_attribute("aria-checked") != "true":
            await loc.first.click(timeout=4000); await page.wait_for_timeout(400)
        return True

    async def flow_open(self, page):
        """Abre um projeto NOVO do Flow para esta cena: num projeto com videos antigos, um video antigo que
        carregava depois do envio era salvo como se fosse o novo (cena 53 do Lehman)."""
        await page.goto(FLOW_HOME, wait_until="domcontentloaded", timeout=60000)
        await page.wait_for_timeout(4000)
        if "accounts.google.com" in page.url:
            raise NeedsUser("login no Google Flow")
        await page.get_by_role("button", name=re.compile(r"Novo projeto|New project")).click(timeout=10000)
        await page.wait_for_url(re.compile(r"/project/"), timeout=30000)
        await page.wait_for_timeout(3000)
        if await page.locator("video").count():
            raise RuntimeError("Flow: projeto novo ja tem videos")
        await page.get_by_role("textbox").first.wait_for(timeout=20000)

    async def flow_settings(self, page, dur):
        await page.get_by_role("button", name=re.compile(r"Gatilho de configura|Settings")).click(timeout=8000)
        await page.wait_for_timeout(800)
        await self.flow_radio(page, "Vídeo"); await self.flow_radio(page, "Frames", False); await self.flow_radio(page, "16:9")
        dd = page.locator('[aria-label="Selecionar família de modelos"]')
        if self.flow_model not in await dd.inner_text():
            await dd.click(timeout=4000); await page.wait_for_timeout(600)
            await page.get_by_role("menuitem", name=re.compile(re.escape(self.flow_model))).click(timeout=4000)
            await page.wait_for_timeout(800)
        if self.flow_model not in await dd.inner_text():
            raise RuntimeError(f"Flow: modelo {self.flow_model} nao selecionado")
        await self.flow_radio(page, "720p", False)  # 1080p nao existe na geracao do Flow
        secs = [s for s in (4, 6, 8, 10) if await page.get_by_role("radio", name=re.compile(rf"(^|\s){s}s$")).count()]
        if secs:  # Omni escolhe a duracao; o Veo Fast e sempre 8s
            await self.flow_radio(page, f"{min([s for s in secs if s >= dur] or [max(secs)])}s")
        await self.flow_radio(page, "x1")
        await page.keyboard.press("Escape"); await page.wait_for_timeout(500)

    async def flow_generate(self, page, prompt, dur):
        await self.flow_open(page)
        await self.flow_settings(page, dur)
        box = page.get_by_role("textbox", name=re.compile(r"O que voc|What do you want"))
        await box.click(); await page.keyboard.press("Control+A"); await page.keyboard.press("Delete")
        await page.keyboard.insert_text(prompt); await page.wait_for_timeout(500)
        before = {v["src"] for v in await page.evaluate(FLOW_VIDS_JS) if v["src"]}
        fails0 = len(FLOW_FAIL_RE.findall(await page.evaluate("() => document.body.innerText")))
        await page.get_by_role("button", name=re.compile(r"Iniciar gera|Start generat|Generate")).click(timeout=8000)
        deadline = time.time() + GEN_TIMEOUT["video"]
        while time.time() < deadline:
            await page.wait_for_timeout(5000)
            await self.gate()
            txt = await page.evaluate("() => document.body.innerText")
            m = FLOW_CREDIT_RE.search(txt)
            if m:
                raise NeedsUser(f"creditos do Flow: '{m.group(0)}'")
            if len(FLOW_FAIL_RE.findall(txt)) > fails0:
                raise RuntimeError("Flow recusou o prompt: " + FLOW_FAIL_RE.findall(txt)[-1])
            new = [v for v in await page.evaluate(FLOW_VIDS_JS) if v["src"] and v["src"] not in before and v["w"] and v["rs"] >= 2]
            if new:
                return await self.fetch_bytes(page, new[0]["src"])
        raise TimeoutError(f"Flow nao entregou o video em {GEN_TIMEOUT['video']}s")

    # ---------- per scene ----------
    async def run_scene(self, ctx, i, mode, prompt, dur=8, name=None):
        err = None
        for attempt in range(1, MAX_RETRIES + 2):
            await self.gate()
            page = await ctx.new_page()
            page._ds_err = None
            async def _on_resp(r, page=page):
                try:
                    if r.request.method == "POST" and r.status >= 400 and "/rest/app-chat/conversations" in r.url:
                        try:
                            page._ds_err = (json.loads(await r.text()).get("error") or {}).get("message") or f"HTTP {r.status}"
                        except Exception:
                            page._ds_err = f"HTTP {r.status}"
                except Exception:
                    pass
            page.on("response", lambda r: asyncio.ensure_future(_on_resp(r)))
            try:
                self.scene_status(i, "gerando", None if attempt == 1 else f"tentativa {attempt}")
                flow = mode == "video" and self.video_engine == "flow"
                self.log(f"cena {i+1:02d} [{mode}{', flow ' + self.flow_model if flow else ''}] tentativa {attempt}")
                if flow:
                    data = await self.flow_generate(page, prompt, dur)
                    via = f"flow.google.com {self.flow_model}"
                else:
                    await page.goto(URL, wait_until="domcontentloaded", timeout=60000)
                    await page.wait_for_timeout(2500)
                    await self.dismiss_cookies(page)
                    await self.check_blockers(page)
                    await self.dismiss_popups(page)
                    await self.set_mode(page, mode)
                    await self.set_aspect(page)
                    if mode == "video":
                        await self.set_video_opts(page, dur)
                    else:
                        await self.set_image_count(page)
                    await self.fill_prompt(page, prompt)
                    before = {x["src"] for x in await page.evaluate(self.MEDIA_JS, mode)}
                    async with self.submit_lock:
                        gap = VIDEO_GAP if mode == "video" else IMAGE_GAP
                        wait = self.last_submit[mode] + gap - time.time()
                        if wait > 0:
                            await asyncio.sleep(wait)
                        await self.submit(page)
                        self.last_submit[mode] = time.time()
                    src = await self.wait_result(page, mode, before)
                    data = await self.fetch_bytes(page, src)
                    via = "grok.com/imagine"
                if len(data) < (50_000 if mode == "video" else 15_000):
                    raise RuntimeError(f"arquivo pequeno demais ({len(data)} bytes)")
                h = hashlib.md5(data).hexdigest()
                if self.hashes.get(h, i + 1) != i + 1:
                    raise RuntimeError(f"arquivo identico ao da cena {self.hashes[h]}: o resultado era de outra cena")
                self.hashes[h] = i + 1
                ext = self.ext_for(data, mode)
                for old in [*self.media.glob(f"scene-{i+1:02d}.*"), *self.media.glob(f"{i+1:02d}_*.*")]:
                    if old.is_file():
                        old.unlink()
                out = self.media / f"{name or f'scene-{i+1:02d}'}{ext}"
                out.write_bytes(data)
                await self.mark_done(i, f"media/{out.name}", mode, via)
                self.scene_status(i, "pronto")
                self.log(f"cena {i+1:02d} OK -> {out.name} ({len(data)//1024} KB)")
                return True
            except NeedsUser:
                await self.shot(page, f"cena{i+1:02d}-needs_user")
                raise
            except asyncio.CancelledError:
                raise
            except Exception as e:
                err = f"{type(e).__name__}: {str(e)[:300]}"
                s = await self.shot(page, f"cena{i+1:02d}-erro{attempt}")
                self.log(f"cena {i+1:02d} falhou: {err} (screenshot {s})")
            finally:
                try:
                    await page.close()
                except Exception:
                    pass
        self.scene_status(i, "erro", err)
        return False

    async def main(self):
        from playwright.async_api import async_playwright
        self.ctrl_f.write_text("run", encoding="utf-8")
        (self.media / "PRONTO").unlink(missing_ok=True)  # PRONTO antigo nao vale enquanto gera de novo
        q = self.queue()
        for i, *_ in q:
            self.state["scenes"][str(i)] = {"status": "na fila", "error": None}
        self.save_status(state="running", message=f"{len(q)} cenas na fila", total=len(q))
        if not q:
            self.save_status(state="done", message="Nenhuma cena pendente. " + self.handoff()); return
        ensure_chrome()
        async with async_playwright() as p:
            browser = await p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
            ctx = browser.contexts[0]
            is_flow = lambda item: item[1] == "video" and self.video_engine == "flow"
            # checagem de login no Grok antes de comecar (o Flow checa o proprio login ao abrir)
            if not all(is_flow(x) for x in q):
                page = await ctx.new_page()
                try:
                    await page.goto(URL, wait_until="domcontentloaded", timeout=60000)
                    await page.wait_for_timeout(3000)
                    await self.dismiss_cookies(page)
                    await self.check_blockers(page)
                except NeedsUser as e:
                    await self.shot(page, "needs_user")
                    self.ctrl_f.write_text("pause", encoding="utf-8")
                    self.save_status(state="needs_user", message=self.user_msg(str(e)))
                    await page.close(); return
                await page.close()

            # Grok uma cena por vez: com 2+ abas, o video de uma cena aparecia na aba da outra e era salvo
            # duas vezes (cenas repetidas no First Brands, SVB e Lehman). shortcut: volta ao paralelo quando o
            # resultado for ligado ao post da propria aba.
            sem = asyncio.Semaphore(1)
            flow_slot = asyncio.Semaphore(1)  # videos do Flow numa fila propria: rodam junto com as imagens do Grok
            self.hashes = self.file_hashes()
            stop = asyncio.Event()

            async def one(item):
                if stop.is_set():
                    return
                async with (flow_slot if is_flow(item) else sem):
                    if stop.is_set():
                        return
                    try:
                        await self.run_scene(ctx, *item)
                    except NeedsUser as e:
                        self.log(f"cena {item[0]+1:02d} pausou: {e}")
                        stop.set()
                        self.ctrl_f.write_text("pause", encoding="utf-8")
                        self.scene_status(item[0], "na fila", str(e))
                        self.save_status(state="needs_user", message=self.user_msg(str(e)))

            try:
                await asyncio.gather(*(one(x) for x in q))
            except asyncio.CancelledError:
                self.save_status(state="stopped", message="Parado pelo usuario."); return
            if self.state["state"] == "needs_user":
                return
            ok = sum(1 for v in self.state["scenes"].values() if v["status"] == "pronto")
            msg = f"Concluido: {ok}/{len(q)} cenas prontas."
            if ok == len(q):
                msg += " " + self.handoff()
            self.save_status(state="done", message=msg)
            # nao fecha o Chrome dedicado: o usuario pode continuar usando/logado

    @staticmethod
    def user_msg(reason):
        if reason == "login":
            return "Faça login no Grok na janela do Chrome do Dark Studio (botão 'Abrir Chrome do Grok') e clique em Retomar."
        if reason == "captcha":
            return "O Grok pediu verificação (captcha). Resolva na janela do Chrome do Dark Studio e clique em Retomar."
        return f"Pausado: {reason}. Aguarde o limite liberar e clique em Retomar."


def run(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--scenes", default="")
    ap.add_argument("--concurrency", type=int, default=2)
    ap.add_argument("--login", action="store_true", help="so abre o Chrome dedicado no Grok")
    ap.add_argument("--video-engine", choices=["grok", "flow"], default="grok", help="flow: videos no Google Flow, imagens seguem no Grok")
    ap.add_argument("--flow-model", default=FLOW_MODEL, help="ex.: 'Omni 1.1 Flash' (4-10s) ou 'Veo 3.1 - Fast' (8s)")
    ap.add_argument("--only", choices=["video", "image"], help="so as cenas deste tipo")
    a = ap.parse_args(argv)
    if a.login:
        ensure_chrome(); return
    scenes = [int(x) for x in a.scenes.split(",") if x.strip()] or None
    w = Worker(a.project, scenes, a.concurrency, a.video_engine, a.flow_model, a.only)
    # loop de retomada: em needs_user, espera o usuario clicar Retomar e recomeca
    while True:
        try:
            asyncio.run(w.main())
        except Exception as e:
            w.log("ERRO FATAL: " + traceback.format_exc())
            w.save_status(state="error", message=f"{type(e).__name__}: {str(e)[:300]}")
            return
        if w.state["state"] != "needs_user":
            return
        w.log("aguardando usuario (needs_user)...")
        while w.control() == "pause":
            time.sleep(2)
        if w.control() == "stop":
            w.save_status(state="stopped", message="Parado pelo usuario."); return
        w.state["scenes"] = {}


if __name__ == "__main__":
    run()
