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

MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

class ApiError(Exception):
    pass

def chat_json(system, user, max_tokens=8000):
    key = api_key()
    if not key:
        raise ApiError("Chave da OpenAI não configurada. Defina OPENAI_API_KEY no arquivo .env (veja .env.example) ou como variável de ambiente e reinicie o app.")
    body = json.dumps({"model": MODEL, "response_format": {"type": "json_object"},
                       "max_tokens": max_tokens,
                       "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]}).encode()
    req = urllib.request.Request("https://api.openai.com/v1/chat/completions", data=body,
                                 headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            data = json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise ApiError(f"Erro da API OpenAI ({e.code}): {e.read().decode(errors='ignore')[:400]}")
    except Exception as e:
        raise ApiError(f"Falha ao chamar a OpenAI: {e}")
    return json.loads(data["choices"][0]["message"]["content"])

def slug(s):
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s.lower()).strip("-")
    return (s[:50] or "projeto") + "-" + time.strftime("%Y%m%d-%H%M%S")

def suggest_titles(p):
    sys = "You are a YouTube strategist for faceless 'dark' channels (mystery, history, true crime, horror, curiosities). Reply in JSON."
    u = (f"Niche: {p.get('niche')}\nLanguage of the titles: {p.get('language')}\nTheme/idea: {p.get('theme')}\n"
         "Suggest 8 click-worthy but honest titles for an 8-15 minute video, written in that language. "
         'JSON: {"titles":[{"title":"...","hook":"one-sentence angle in Portuguese"}]}')
    return chat_json(sys, u, 1500)

def write_script(p):
    mins = int(p.get("minutes") or 10)
    words = mins * 145
    sys = "You write narration scripts for faceless dark YouTube documentaries and prompts for an AI video generator (Grok Imagine). Reply in JSON."
    u = (f"Title: {p.get('title')}\nNiche: {p.get('niche')}\nLanguage of the narration: {p.get('language')}\n"
         f"Target length: {mins} minutes (~{words} words of narration total).\n"
         "Split into scenes of 1-3 sentences (about 6-10 seconds each). Strong hook in the first scene, retention cues, satisfying ending with call to subscribe. "
         "For each scene give a visual prompt IN ENGLISH for a short cinematic, dark, 16:9 clip (no text, no faces of real people). "
         '{"title":"...","description":"short summary in Portuguese","scenes":[{"narration":"...","visual_prompt":"..."}]}')
    return chat_json(sys, u, 16000)

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
