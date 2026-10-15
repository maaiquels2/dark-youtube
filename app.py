"""Dark YouTube - protótipo local. Rode: python app.py  -> http://127.0.0.1:8765"""
import json, os, re, time, threading, urllib.request, urllib.error, urllib.parse, math
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STATIC = ROOT / "static"
PROJECTS = ROOT / "projects"
PROJECTS.mkdir(exist_ok=True)
PORT = int(os.environ.get("DY_PORT", "8765"))

def load_env():
    f = ROOT / ".env"
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
load_env()

def api_key():
    return os.environ.get("OPENAI_API_KEY", "").strip()

MODEL = os.environ.get("OPENAI_MODEL", "gpt-6.1-sol")

class ApiError(Exception):
    pass

def _post(url, payload, key):
    req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                                 headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise ApiError(f"Erro da API OpenAI ({e.code}): {e.read().decode(errors='ignore')[:400]}")
    except Exception as e:
        raise ApiError(f"Falha ao chamar a OpenAI: {e}")

def _responses_text(d):
    if d.get("output_text"):
        return d["output_text"]
    parts = []
    for item in d.get("output") or []:
        for c in item.get("content") or []:
            if c.get("text"):
                parts.append(c["text"])
    return "".join(parts)

def _parse_json(text):
    text = (text or "").strip()
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        raise ApiError("A resposta do modelo não veio em JSON.")
    return json.loads(m.group(0))

def chat_json(system, user, max_tokens=8000):
    key = api_key()
    if not key:
        raise ApiError("Chave da OpenAI não configurada. Defina OPENAI_API_KEY no arquivo .env (veja .env.example) ou como variável de ambiente e reinicie o app.")
    first_err = None
    try:
        d = _post("https://api.openai.com/v1/responses", {
            "model": MODEL, "instructions": system, "input": user,
            "max_output_tokens": max_tokens, "text": {"format": {"type": "json_object"}}}, key)
        return _parse_json(_responses_text(d))
    except Exception as e:
        first_err = e
        print("[aviso] Responses API falhou, tentando chat/completions:", e, flush=True)
    try:
        d = _post("https://api.openai.com/v1/chat/completions", {
            "model": MODEL, "response_format": {"type": "json_object"},
            "max_completion_tokens": max_tokens,
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]}, key)
        return _parse_json(d["choices"][0]["message"]["content"])
    except Exception as e:
        raise ApiError(f"Responses: {first_err} | chat/completions: {e}")

# ---------------- xAI (Cenas) ----------------
XAI = "https://api.x.ai/v1"
LOCK = threading.Lock()
SERVER_FIELDS = ("status", "file", "error", "cost_usd", "gen_seconds", "request_id", "media_duration", "generated_with")

def pricing():
    return json.loads((ROOT / "config" / "pricing.json").read_text(encoding="utf-8"))

def xai_key():
    return os.environ.get("XAI_API_KEY", "").strip()

def _xai(method, path, payload=None, timeout=120):
    key = xai_key()
    if not key:
        raise ApiError("Chave da xAI não configurada. Defina XAI_API_KEY no arquivo .env e reinicie o app.")
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(XAI + path, data=data, method=method,
                                 headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json", "User-Agent": "DarkStudio/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        raise ApiError(f"Erro da API xAI ({e.code}): {e.read().decode(errors='ignore')[:300]}")
    except ApiError:
        raise
    except Exception as e:
        raise ApiError(f"Falha ao chamar a xAI: {e}")

def _download(url, dest_noext, default_ext):
    req = urllib.request.Request(url, headers={"User-Agent": "DarkStudio/1.0"})
    with urllib.request.urlopen(req, timeout=300) as r:
        ct = r.headers.get("Content-Type", "")
        ext = ".jpg" if "jpeg" in ct else ".png" if "png" in ct else ".webp" if "webp" in ct else ".mp4" if "mp4" in ct else default_ext
        data = r.read()
    for old in dest_noext.parent.glob(dest_noext.name + ".*"):
        old.unlink()
    path = dest_noext.with_suffix(ext)
    path.write_bytes(data)
    return path

def proj_path(pid):
    return PROJECTS / (Path(pid).name + ".json")

GROK_STYLE = ("Style: dark cinematic documentary, moody low-key lighting with deep shadows and cold teal-and-amber contrast, "
              "volumetric haze, shallow depth of field, anamorphic lens look, subtle film grain, photorealistic, "
              "premium Netflix-style business documentary aesthetic.")
GROK_NEG = ("Avoid: no text, no captions, no watermark, no logos or trademarks, no real person likeness, "
            "no distorted faces or hands, no extra limbs, no cartoon look, no blur artifacts.")

def clean_subject(vp):
    t = (vp or "").strip()
    t = re.sub(r"(?i)\b(dark\s+)?cinematic\s+16:9\s*", "", t, count=1).strip()
    t = re.sub(r"(?i),?\s*no logos?,?\s*(no text,?)?\s*(no identifiable people\.?)?\s*$", "", t).strip(" ,.")
    t = t.split(" | ")[0]
    return (t[:1].upper() + t[1:]) if t else "Atmospheric establishing shot that illustrates the narration"

def build_grok_prompt(sc, cfg=None):
    subj = clean_subject(sc.get("visual_prompt"))
    narr = re.sub(r"\s+", " ", sc.get("narration") or "").strip()
    parts = [f"Subject: {subj}."]
    if narr:
        parts.append(f"Context (illustrate this narration, do not write it on screen): \"{narr[:240].rstrip('.')}\".")
    parts.append("Composition: wide cinematic framing, strong leading lines, clear focal subject, rule of thirds.")
    parts.append(GROK_STYLE)
    if sc.get("mode") == "video":
        dur = 8
        if cfg:
            dur = int(min(cfg["video_max_seconds"], max(cfg["video_min_seconds"], math.ceil(scene_seconds(sc, cfg)))))
        parts.append(f"Motion: slow cinematic camera movement (gentle dolly-in or slow parallax pan), subtle atmospheric motion "
                     f"(drifting haze, flickering lights), smooth and stable, no cuts. Duration: about {dur} seconds (max 15s), no audio.")
        parts.append("Format: video, aspect ratio 16:9, 1920x1080, high resolution, ultra detailed.")
    else:
        parts.append("Format: still image, aspect ratio 16:9, 1920x1080, high resolution, ultra detailed, sharp focus.")
    parts.append(GROK_NEG)
    return " ".join(parts)

def with_prompts(d):
    cfg = pricing()
    for sc in d.get("scenes") or []:
        sc["grok_prompt"] = build_grok_prompt(sc, cfg)
    return d

def export_prompts(d):
    out = PROJECTS / Path(d["id"]).name
    out.mkdir(parents=True, exist_ok=True)
    md = [f"# Prompts Grok Imagine - {d.get('title','')}", "", "Cole cada prompt em grok.com/imagine. Formato 16:9.", ""]
    tx = [f"Prompts Grok Imagine - {d.get('title','')}", ""]
    for i, sc in enumerate(d.get("scenes") or []):
        narr = re.sub(r"\s+", " ", sc.get("narration") or "").strip()
        ex = narr[:160] + ("..." if len(narr) > 160 else "")
        mode = "VIDEO" if sc.get("mode") == "video" else "IMAGEM"
        md += [f"## Cena {i+1:02d} - {mode}", "", f"> {ex}", "", "```", sc["grok_prompt"], "```", ""]
        tx += [f"=== Cena {i+1:02d} | {mode} ===", f"Narracao: {ex}", "", sc["grok_prompt"], "", ""]
    (out / "prompts-grok.md").write_text("\n".join(md), encoding="utf-8")
    (out / "prompts-grok.txt").write_text("\n".join(tx), encoding="utf-8")

def load_project(pid):
    return json.loads(proj_path(pid).read_text(encoding="utf-8"))

def update_scene(pid, i, **fields):
    with LOCK:
        d = load_project(pid)
        d["scenes"][i].update(fields)
        proj_path(pid).write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")

def scene_seconds(sc, cfg):
    w = len((sc.get("narration") or "").split())
    return max(1.0, w / cfg["words_per_minute"] * 60)

def generate_scene(pid, i):
    cfg = pricing()
    t0 = time.time()
    try:
        sc = load_project(pid)["scenes"][i]
        model = sc.get("model") or ("grok-imagine-video-1.5-lite" if sc.get("mode") == "video" else "grok-imagine-image")
        prompt = build_grok_prompt(sc, cfg)
        media = PROJECTS / Path(pid).name / "media"
        media.mkdir(parents=True, exist_ok=True)
        dest = media / f"scene-{i+1:02d}"
        if sc.get("mode") == "video":
            dur = int(min(cfg["video_max_seconds"], max(cfg["video_min_seconds"], math.ceil(scene_seconds(sc, cfg)))))
            r = _xai("POST", "/videos/generations", {"model": model, "prompt": prompt, "duration": dur,
                                                      "aspect_ratio": "16:9", "resolution": "720p", "generate_audio": False})
            rid = r.get("request_id")
            if not rid:
                raise ApiError(f"Resposta inesperada da xAI: {str(r)[:200]}")
            update_scene(pid, i, request_id=rid)
            deadline = time.time() + 900
            while True:
                if time.time() > deadline:
                    raise ApiError("Tempo esgotado esperando o vídeo (15 min).")
                time.sleep(5)
                d = _xai("GET", f"/videos/{rid}")
                st = d.get("status")
                if st == "done":
                    v = d.get("video") or {}
                    if v.get("respect_moderation") is False:
                        raise ApiError("Vídeo bloqueado pela moderação da xAI. Ajuste o prompt.")
                    path = _download(v["url"], dest, ".mp4")
                    real = float(v.get("duration") or dur)
                    cost = round(real * cfg["video_per_second"].get(model, 0), 4)
                    break
                if st == "failed":
                    e = d.get("error") or {}
                    raise ApiError(f"Geração falhou: {e.get('code')} {e.get('message')}")
            update_scene(pid, i, status="pronto", file=f"media/{path.name}", error=None, cost_usd=cost,
                         media_duration=real, gen_seconds=round(time.time() - t0, 1), generated_with=model)
        else:
            r = _xai("POST", "/images/generations", {"model": model, "prompt": prompt, "aspect_ratio": "16:9", "n": 1})
            url = ((r.get("data") or [{}])[0]).get("url")
            if not url:
                raise ApiError(f"Resposta inesperada da xAI: {str(r)[:200]}")
            path = _download(url, dest, ".jpg")
            cost = cfg["image"].get(model, 0)
            update_scene(pid, i, status="pronto", file=f"media/{path.name}", error=None, cost_usd=cost,
                         media_duration=None, gen_seconds=round(time.time() - t0, 1), generated_with=model)
    except Exception as e:
        update_scene(pid, i, status="erro", error=str(e)[:400], gen_seconds=round(time.time() - t0, 1))

SEM = None
def start_generation(pid, idxs):
    global SEM
    if not xai_key():
        raise ApiError("Chave da xAI não configurada. Defina XAI_API_KEY no arquivo .env e reinicie o app.")
    if SEM is None:
        SEM = threading.BoundedSemaphore(int(pricing().get("concurrency", 3)))
    d = load_project(pid)
    started = []
    for i in idxs:
        sc = d["scenes"][i]
        if sc.get("source", "api") != "api" or sc.get("status") == "gerando":
            continue
        started.append(i)
    for i in started:
        update_scene(pid, i, status="gerando", error=None)
        def run(i=i):
            with SEM:
                generate_scene(pid, i)
        threading.Thread(target=run, daemon=True).start()
    return {"started": started}

def save_upload(pid, i, filename, data):
    ext = Path(filename).suffix.lower()
    if ext not in (".mp4", ".mov", ".webm", ".png", ".jpg", ".jpeg", ".webp"):
        raise ApiError("Formato não suportado. Use MP4, MOV, WEBM, PNG, JPG ou WEBP.")
    media = PROJECTS / Path(pid).name / "media"
    media.mkdir(parents=True, exist_ok=True)
    for old in media.glob(f"scene-{i+1:02d}.*"):
        old.unlink()
    path = media / f"scene-{i+1:02d}{ext}"
    path.write_bytes(data)
    update_scene(pid, i, status="pronto", file=f"media/{path.name}", error=None, cost_usd=0,
                 generated_with="upload manual")
    return {"file": f"media/{path.name}"}

def slug(s):
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s.lower()).strip("-")
    return (s[:50] or "projeto") + "-" + time.strftime("%Y%m%d-%H%M%S")

def suggest_titles(p):
    sys = ("You are a YouTube strategist for faceless long-form documentary channels in the Business & Finance niche "
           "(fraud and scams, rise and fall of companies, the dark truth about empires, billionaires, history of money). Reply only in JSON.")
    u = (f"Niche: {p.get('niche')}\nLanguage of the titles: {p.get('language')}\nTheme/idea: {p.get('theme')}\n"
         "Suggest 8 titles for an 8-15 minute video, in that language, using proven formulas such as: "
         "'The Dark Truth About X', 'Why X Is Collapsing', 'Why X Owns EVERYTHING', 'Exposing $X ...', "
         "'The Rise and Fall of X', 'How X Turned Down $Y and Died'. Use specific dollar figures ONLY when they are factual and well known; "
         "never invent numbers. Titles must be honest about the content.\n"
         'JSON: {"titles":[{"title":"...","hook":"ângulo do vídeo em português (1 frase)","why":"por que retém, em português (1 frase)","formula":"formula used"}]}')
    return chat_json(sys, u, 3000)

def write_script(p):
    mins = int(p.get("minutes") or 10)
    words = mins * 150
    sys = ("You are a researcher and scriptwriter for a faceless Business & Finance documentary YouTube channel. "
           "Scripts will be reviewed by a human before production, so accuracy matters more than drama. "
           "NEVER invent sources, URLs, quotes or numbers. Only give a URL if you are confident it exists; otherwise set url to \"verificar\". "
           "Set needs_check=true on any scene whose claims (figures, dates, quotes, allegations) must be verified. Reply only in JSON.")
    u = (f"Title: {p.get('title')}\nNiche: {p.get('niche')}\nLanguage of the narration: {p.get('language')}\n"
         f"Target length: {mins} minutes (~{words} words of narration in total).\n"
         "Write a documentary narration split into scenes of 1-3 sentences (6-10 seconds each). "
         "Strong hook in the first 30 seconds, clear story arc, retention beats (open loops, reveals) spread through the video, ending with a call to subscribe. "
         "For each scene: narration in the narration language; visual_prompt IN ENGLISH: a concrete, detailed visual description (subject, setting, camera angle, lighting, mood; 25-50 words) faithful to that scene's narration "
         "(no real person likeness, no logos or trademarks, no on-screen text); key_facts (list of factual claims in the scene); "
         "sources (list of {title, url}); needs_check (boolean).\n"
         '{"title":"...","description":"resumo em português","hook":"first 30 seconds summary",'
         '"retention_beats":["..."],"scenes":[{"narration":"...","visual_prompt":"...","key_facts":["..."],'
         '"sources":[{"title":"...","url":"verificar"}],"needs_check":true}]}')
    return chat_json(sys, u, 32000)

def save_project(proj):
    pid = proj.get("id") or slug(proj.get("title", "projeto"))
    proj["id"] = pid
    proj["updated_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
    with LOCK:
        f = PROJECTS / f"{Path(pid).name}.json"
        if f.exists():
            old = json.loads(f.read_text(encoding="utf-8")).get("scenes") or []
            for i, sc in enumerate(proj.get("scenes") or []):
                if i < len(old):
                    for k in SERVER_FIELDS:
                        if k in old[i]:
                            sc[k] = old[i][k]
                        else:
                            sc.pop(k, None)
        with_prompts(proj)
        f.write_text(json.dumps(proj, ensure_ascii=False, indent=2), encoding="utf-8")
    try:
        export_prompts(proj)
    except Exception:
        pass
    return proj

# ---------- Gerar no Grok (automatico) - worker em subprocesso ----------
import subprocess, sys as _sys
AUTO = {}
def _venv_py():
    v = Path(__file__).resolve().parent / ".venv" / "Scripts" / "python.exe"
    return str(v) if v.is_file() else _sys.executable

def _auto_logs(pid):
    d = PROJECTS / Path(pid).name / "logs"; d.mkdir(parents=True, exist_ok=True); return d

def auto_status(pid):
    f = _auto_logs(pid) / "grok_auto.json"
    st = {}
    if f.is_file():
        try: st = json.loads(f.read_text(encoding="utf-8"))
        except Exception: st = {}
    pr = AUTO.get(Path(pid).name)
    st["running"] = bool(pr and pr.poll() is None)
    try: st["control"] = (_auto_logs(pid) / "grok_control.txt").read_text(encoding="utf-8").strip()
    except OSError: st["control"] = ""
    return st

def auto_start(pid, scenes=None, concurrency=None):
    pid = Path(pid).name
    pr = AUTO.get(pid)
    if pr and pr.poll() is None:
        raise ApiError("A geração automática já está rodando neste projeto.")
    conc = int(concurrency or pricing().get("grok_auto_concurrency", 2))
    args = [_venv_py(), str(Path(__file__).resolve().parent / "grok_worker.py"), pid, "--concurrency", str(conc)]
    if scenes:
        args += ["--scenes", ",".join(str(int(i)) for i in scenes)]
    logs = _auto_logs(pid)
    (logs / "grok_control.txt").write_text("run", encoding="utf-8")
    out = open(logs / "grok_worker.out", "a", encoding="utf-8")
    AUTO[pid] = subprocess.Popen(args, stdout=out, stderr=subprocess.STDOUT, cwd=str(Path(__file__).resolve().parent),
                                 creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    return {"started": True, "concurrency": conc}

def auto_control(pid, action):
    if action not in ("run", "pause", "stop"):
        raise ApiError("Ação inválida.")
    (_auto_logs(pid) / "grok_control.txt").write_text(action, encoding="utf-8")
    return auto_status(pid)

def auto_login():
    subprocess.Popen([_venv_py(), str(Path(__file__).resolve().parent / "grok_worker.py"), "_", "--login"],
                     cwd=str(Path(__file__).resolve().parent), creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    return {"opened": True}

class H(BaseHTTPRequestHandler):
    def _send(self, code, obj=None, raw=None, ctype="application/json; charset=utf-8"):
        b = raw if raw is not None else json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code); self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)

    def log_message(self, *a):
        pass

    def do_GET(self):
        p = self.path.split("?")[0]
        if p == "/api/status":
            return self._send(200, {"has_key": bool(api_key()), "model": MODEL, "has_xai": bool(xai_key())})
        if p == "/api/grok_auto":
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            return self._send(200, auto_status(q["id"][0]))
        if p == "/api/pricing":
            return self._send(200, pricing())
        if p.startswith("/media/"):
            parts = p.split("/")
            if len(parts) == 4:
                f = PROJECTS / Path(parts[2]).name / "media" / Path(urllib.parse.unquote(parts[3])).name
                if f.is_file():
                    ct = {".mp4": "video/mp4", ".webm": "video/webm", ".mov": "video/quicktime", ".png": "image/png",
                          ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}.get(f.suffix.lower(), "application/octet-stream")
                    return self._send(200, raw=f.read_bytes(), ctype=ct)
            return self._send(404, {"error": "não encontrado"})
        if p == "/api/projects":
            items = []
            for f in sorted(PROJECTS.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True):
                try:
                    d = json.loads(f.read_text(encoding="utf-8"))
                    items.append({"id": d["id"], "title": d.get("title"), "language": d.get("language"), "updated_at": d.get("updated_at")})
                except Exception:
                    pass
            return self._send(200, items)
        if p.startswith("/api/projects/"):
            f = PROJECTS / (Path(p).name + ".json")
            return self._send(200, raw=f.read_bytes()) if f.exists() else self._send(404, {"error": "não encontrado"})
        f = STATIC / ("index.html" if p == "/" else p.lstrip("/"))
        if f.is_file() and STATIC in f.resolve().parents:
            ct = {".html": "text/html", ".js": "application/javascript", ".css": "text/css"}.get(f.suffix, "application/octet-stream")
            return self._send(200, raw=f.read_bytes(), ctype=ct + "; charset=utf-8")
        self._send(404, {"error": "não encontrado"})

    def do_POST(self):
        n = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(n)
        if self.path.startswith("/api/upload"):
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            try:
                return self._send(200, save_upload(q["id"][0], int(q["i"][0]), q.get("name", ["x.mp4"])[0], raw))
            except ApiError as e:
                return self._send(400, {"error": str(e)})
            except Exception as e:
                return self._send(500, {"error": f"Erro interno: {e}"})
        body = json.loads(raw or b"{}")
        try:
            if self.path == "/api/generate":
                return self._send(200, start_generation(body["id"], [int(i) for i in body.get("scenes", [])]))
            if self.path == "/api/titles":
                return self._send(200, suggest_titles(body))
            if self.path == "/api/script":
                return self._send(200, write_script(body))
            if self.path == "/api/grok_auto/start":
                return self._send(200, auto_start(body["id"], body.get("scenes"), body.get("concurrency")))
            if self.path == "/api/grok_auto/control":
                return self._send(200, auto_control(body["id"], body["action"]))
            if self.path == "/api/grok_auto/login":
                return self._send(200, auto_login())
            if self.path == "/api/save":
                return self._send(200, save_project(body))
        except ApiError as e:
            return self._send(400, {"error": str(e)})
        except Exception as e:
            return self._send(500, {"error": f"Erro interno: {e}"})
        self._send(404, {"error": "não encontrado"})

if __name__ == "__main__":
    for f in PROJECTS.glob("*.json"):  # gerações interrompidas ao reiniciar
        try:
            d = json.loads(f.read_text(encoding="utf-8")); ch = False
            for sc in d.get("scenes") or []:
                if sc.get("status") == "gerando":
                    sc["status"] = "erro"; sc["error"] = "Interrompido (app reiniciado). Gere de novo."; ch = True
            if ch: f.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception:
            pass
    print(f"Dark YouTube rodando em http://127.0.0.1:{PORT}  (chave OpenAI: {'OK' if api_key() else 'NÃO configurada'})")
    ThreadingHTTPServer(("127.0.0.1", PORT), H).serve_forever()
