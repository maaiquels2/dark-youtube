"""Dark YouTube - protótipo local. Rode: python app.py  -> http://127.0.0.1:8765"""
import json, os, re, time, urllib.request, urllib.error
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
        print("[aviso] Responses API falhou, tentando chat/completions:", e)
    try:
        d = _post("https://api.openai.com/v1/chat/completions", {
            "model": MODEL, "response_format": {"type": "json_object"},
            "max_completion_tokens": max_tokens,
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]}, key)
        return _parse_json(d["choices"][0]["message"]["content"])
    except Exception as e:
        raise ApiError(f"Responses: {first_err} | chat/completions: {e}")

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
         "For each scene: narration in the narration language; visual_prompt IN ENGLISH for a short cinematic dark 16:9 AI clip "
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
    (PROJECTS / f"{pid}.json").write_text(json.dumps(proj, ensure_ascii=False, indent=2), encoding="utf-8")
    return proj

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
            return self._send(200, {"has_key": bool(api_key()), "model": MODEL})
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
        body = json.loads(self.rfile.read(n) or b"{}")
        try:
            if self.path == "/api/titles":
                return self._send(200, suggest_titles(body))
            if self.path == "/api/script":
                return self._send(200, write_script(body))
            if self.path == "/api/save":
                return self._send(200, save_project(body))
        except ApiError as e:
            return self._send(400, {"error": str(e)})
        except Exception as e:
            return self._send(500, {"error": f"Erro interno: {e}"})
        self._send(404, {"error": "não encontrado"})

if __name__ == "__main__":
    print(f"Dark YouTube rodando em http://127.0.0.1:{PORT}  (chave OpenAI: {'OK' if api_key() else 'NÃO configurada'})")
    ThreadingHTTPServer(("127.0.0.1", PORT), H).serve_forever()
