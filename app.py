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

GROK_STYLE = ("Style: photorealistic cinematic documentary reconstruction, natural film look, subtle film grain, clear clean air, "
              "no letterbox bars, full-frame edge-to-edge image, premium business documentary aesthetic.")
GROK_NEG = ("Avoid: no text, no captions, no watermark, no logos, no emblems, no brand marks or trademarks, blank unbranded walls and screens, no real person likeness, "
            "no distorted faces or hands, no extra limbs, no cartoon look, no blur artifacts, no subtitles or quotes on screen, no letterbox or black bars.")
# texto garbado e o defeito mais comum do gerador: dizer o que fazer com papel/tela/placa, nao so "no text"
GROK_TEXT_GUARD = "Papers, screens and signs are blank, blurred or turned away; people only from behind or in silhouette."
# luz e cor seguem o arco emocional (pipeline.ARC); sem ato, mantem o visual escuro original
ACT_LOOK = {
    "act1": ("confident, prosperous momentum", "warm golden key light, rich amber tones with soft teal accents, lively but controlled contrast"),
    "act2": ("uneasy, investigative suspicion", "cool blue-grey light, low-key contrast, deepening shadows, restrained teal palette"),
    "act3": ("grave, heavy, human cost", "hard light and deep shadows, desaturated cold palette with small red accents"),
    "after": ("quiet, reflective aftermath", "soft dawn or overcast light, muted desaturated palette, calm stillness"),
}
DEFAULT_LOOK = ("tense, investigative business documentary atmosphere", "moody low-key lighting with deep shadows and cold teal-and-amber contrast")
# enquadramento coerente com o tipo de plano (antes todo prompt dizia "wide cinematic framing", ate em close-up)
SHOT_COMPOSITION = [
    ("over-the-shoulder", "over-the-shoulder framing from behind an anonymous figure toward what they are looking at, focus on the object of attention"),
    ("macro", "macro detail, one object filling the frame, very shallow depth of field"),
    ("close", "close-up, one subject filling most of the frame, shallow depth of field, soft background"),
    ("detail", "detail shot, one object filling the frame, shallow depth of field"),
    ("overhead", "top-down overhead composition, clean graphic arrangement of objects, even focus"),
    ("top-down", "top-down overhead composition, clean graphic arrangement of objects, even focus"),
    ("aerial", "high aerial composition, clear geography and scale, deep focus"),
    ("low-angle", "low-angle composition looking up, conveying authority and scale"),
    ("tracking", "tracking shot following one subject through the space, subject held on a third"),
    ("medium", "medium shot, one subject and its immediate surroundings, clean separation from the background"),
    ("wide", "wide establishing composition, clear focal subject on a rule-of-thirds line, deep focus"),
]
DEFAULT_COMPOSITION = "clear single focal subject, strong leading lines, rule of thirds"

def shot_composition(shot):
    t = (shot or "").lower()
    return next((c for k, c in SHOT_COMPOSITION if k in t), DEFAULT_COMPOSITION)

_NEG_HEAD = re.compile(r"(?i)^\s*(?:and\s+|with\s+|while\s+)?(?:no\b|without\b|never\b|nothing\b|keep(?:ing)?\b|all\s+\w+\s+(?:remain|are|is|stay)|"
                       r"every\s+\w+\s+(?:remains?|is|stays?)|not\s+(?:a\s+)?(?:depict|represent|recreat))")
_NEG_TOPIC = re.compile(r"(?i)logo|text|letter|label|sign|brand|readab|legib|likeness|identif|face|watermark|seal|flag|emblem|nameplate|placard|"
                        r"marking|caption|portrait|appearance|interface|numbers|figures|dates|recogni|trademark|badge|crest|inscription")

def strip_negations(t):
    """Tira do assunto as frases do tipo 'no logos / no readable text / keep faces hidden' (o bloco Avoid e o guard ja cobrem).
    Prompt mais curto = o gerador presta atencao na acao. Tudo depois de 'STRICT:' (correcao manual) fica intacto."""
    head, sep, tail = t.partition("STRICT:")
    sents = []
    for sent in re.split(r"(?<=[.!?])\s+", head.strip()):
        body = sent.rstrip(".!? ")
        cl, dropping = [], False
        for c in re.split(r"[,;]\s+", body):
            if _NEG_HEAD.search(c) and _NEG_TOPIC.search(c): dropping = True; continue
            # resto da mesma lista ("no X, readable text, or logos"): tambem sai, senao vira pedido positivo de texto/logo
            if dropping and len(c.split()) <= 5 and (_NEG_TOPIC.search(c) or re.match(r"(?i)\s*(or|nor)\b", c)): continue
            dropping = False; cl.append(c)
        if cl: sents.append(", ".join(cl).strip() + ".")
    out = " ".join(sents).strip()
    return (out + (" STRICT:" + tail if sep else "")).strip()

def clean_subject(vp):
    t = (vp or "").strip()
    t = re.sub(r"(?i)\b(dark\s+)?cinematic\s+16:9\s*", "", t, count=1).strip()
    t = re.sub(r"(?i),?\s*no logos?,?\s*(no text,?)?\s*(no identifiable people\.?)?\s*$", "", t).strip(" ,.")
    t = t.split(" | ")[0]
    t = strip_negations(t).strip(" ,.") if t else t
    return (t[:1].upper() + t[1:]) if t else "Atmospheric establishing shot that illustrates the narration"

def _sent(x):
    return re.sub(r"\s+", " ", str(x or "")).strip().rstrip(".") + "."

def build_grok_prompt(sc, cfg=None):
    subj = clean_subject(sc.get("visual_prompt"))
    narr = re.sub(r"\s+", " ", sc.get("narration") or "").strip()
    mood, look = ACT_LOOK.get(sc.get("act"), DEFAULT_LOOK)
    parts = [f"Subject: {_sent(subj)}"]
    if isinstance(sc.get("beat"), str) and sc["beat"].strip(): parts.append(f"Story beat: {_sent(sc['beat'])}")  # projetos antigos tem beat=true
    if sc.get("mood"): parts.append(f"Mood: {_sent(sc['mood'])}")
    elif narr: parts.append(f"Mood: {mood}.")
    if sc.get("camera") and sc.get("mode") != "video": parts.append(f"Camera: {_sent(sc['camera'])}")
    parts.append(f"Composition: {shot_composition(sc.get('shot'))}.")
    parts.append(GROK_STYLE + f" Light and color: {look}.")
    if sc.get("mode") == "video":
        dur = 8
        if cfg:
            dur = int(min(cfg["video_max_seconds"], max(cfg["video_min_seconds"], math.ceil(scene_seconds(sc, cfg)))))
        if sc.get("camera"):  # um movimento so: o da cena (antes vinha junto um "gentle dolly-in" generico que contradizia)
            parts.append(f"Camera move: one continuous move only: {_sent(sc['camera'])}")
            mv = "One simple, clearly visible subject action that completes within the clip, the rest of the scene stays still, realistic physics, no cuts, no morphing."
        else:
            mv = ("Motion: slow cinematic camera movement (gentle dolly-in or slow parallax pan), one simple subject action, the rest of the scene stays still, "
                  "smooth and stable, no cuts, no morphing.")
        parts.append(f"{mv} Duration: about {dur} seconds (max 15s), no audio.")
        parts.append("Format: video, aspect ratio 16:9, 1920x1080, high resolution, ultra detailed.")
    else:
        parts.append("Format: still image, aspect ratio 16:9, 1920x1080, high resolution, ultra detailed, sharp focus.")
    parts.append(GROK_TEXT_GUARD)
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

# Regras de clique (PADRAO_VIDEOS.md, secao Titulo/Escolha de tema), tiradas de ~2.000 videos do nicho (17/10/2026)
CLICK_RULES = (
    "CLICK RULES (from data on ~2,000 niche videos): the title sells a STORY, not a topic. "
    "NEVER use the news-headline format 'Company: How X happened' and do NOT start the title with the company name. "
    "Hide the company/person name in at least 6 of the 8 titles (the name goes in the description and on the thumbnail logo); curiosity about WHO it is drives the click. "
    "Use one of these proven formulas per title: "
    "(A) CHARACTER + EXACT AMOUNT + CONTRADICTION, e.g. 'The $63 BILLION Company That Sold Nothing', 'The Fake Genius: a $30 BILLION Fraud', 'The Homeless Teen Who Created Louis Vuitton', 'Hunting the $477,000,000 FTX Hacker'; "
    "(B) DIRECT, INFORMAL QUESTION with 'Actually', e.g. 'WTF Did Lehman Brothers Actually Do?', 'How Jeff Bezos Actually Built Amazon'; "
    "(C) PROMISE OF CLARITY, e.g. 'The 2008 Crisis Explained Simply'. "
    "Write big amounts in caps or full digits ($11.6 BILLION, $477,000,000) and ONLY when factual and well known; never invent numbers. "
    "Max 60 characters. The title must be honest: the video must pay off its promise in the first 15 seconds. ")

def suggest_titles(p):
    sys = ("You are a YouTube packaging strategist for faceless long-form documentary channels in the Business & Finance niche "
           "(fraud and scams, rise and fall of companies, the dark truth about empires, billionaires, history of money). Reply only in JSON.")
    u = (f"Niche: {p.get('niche')}\nLanguage of the titles: {p.get('language')}\nTheme/idea: {p.get('theme')}\n"
         "Suggest 8 titles for a 10-16 minute video, in that language.\n" + CLICK_RULES +
         "Also rate the topic's search DEMAND for a brand-new channel: 'alta' for famous evergreen stories people keep searching for years "
         "(Enron, Theranos, Madoff, 2008, FTX, Wolf of Wall Street), 'media' for known but niche stories, 'baixa' for little-known recent cases. "
         "For each title give a thumbnail text of 2-4 words that COMPLEMENTS the title without repeating its words (e.g. title 'The $63 BILLION Company That Sold Nothing' -> thumbnail 'ALL FAKE'). "
         "Suggest one recurring SERIES name the channel could use for this kind of video.\n"
         'JSON: {"demand":"alta|media|baixa","demand_why":"em português (1 frase)","series":"...","titles":[{"title":"...","thumb_text":"2-4 WORDS",'
         '"hook":"ângulo do vídeo em português (1 frase)","why":"por que gera clique, em português (1 frase)","formula":"A|B|C"}]}')
    return chat_json(sys, u, 3000)

STORY_STANDARD = (
    "STORYTELLING STANDARD: (1) open with a ~15-second hook built on the single most shocking verified moment; "
    "(2) a clear, humanized protagonist (who they are, what they wanted) without inventing private details; "
    "(3) rising conflict and tension with open loops ('but', 'what nobody knew yet', 'that was only the beginning'); "
    "(4) a clear 3-act structure (setup / unraveling / reckoning) mapped onto 6-10 chapters; "
    "(5) emotional authenticity through affected people (employees, creditors, investors, customers) based on reported facts, never sensational; "
    "(6) show-don't-tell: every visual_prompt must literally match and EXPLAIN its narration, varied shot types (wide, close-up, macro, aerial, tracking) so consecutive scenes never look alike; "
    "for abstract finance ideas (leverage, debt, funds moving, who owed whom, who gets paid first) use a gfx (flow, relmap, stack, chart), "
    "never a symbolic object standing for the idea (crates, keys, glass boxes, chess pieces) and never 'someone looking at screens or documents'. "
    "LEGAL: anyone charged but not convicted is presumed innocent: attribute every accusation ('prosecutors allege', 'according to the indictment', 'the company said'); never state guilt; "
    "include one explicit presumption-of-innocence line; report denials and not-guilty pleas. ")
GFX_SPEC = (
    "GRAPHICS (gfx) - motion-graphics specs rendered from real data. Use only facts given above, with their source. Types:\n"
    "VISUAL DECISION for every scene, in this order: a number -> chart/scale/collapse; money or obligations between parties, who owes whom, "
    "a conflict of interest -> flow/relmap/moneyflow; an order, priority or process -> stack/timeline; questions, lessons or a thesis -> list/takeaway; "
    "a real person or real building that is the subject -> real_photo; only a physical moment (people, streets, buildings, weather) is left to the AI visual. "
    "Aim for 55-70% of scenes with a full-screen item, never two identical types in a row, and never more than 3 full-screen graphics in a row "
    "without a real_photo or an AI scene between them. Write every \"say\" as 1-3 words copied from THIS scene's narration: the card appears when they are spoken. "
    "When the narration states an amount that is in the verified facts, that scene MUST get a chart. Arrow labels 1-2 words, list items <= 8 words. "
    "takeaway at most once per chapter: a short thesis in your own words, never a narration sentence copied onto the screen. "
    "Each real_photo (same person or building) at most once per video. stack only when the tiers recover different shares (a process or steps go in timeline or list). "
    "The same diagram (same parties) at most twice per video.\n"
    "FULL-SCREEN (replaces the AI visual for that scene):\n"
    '- {"type":"chapter","number":1,"title":"..."} on the first scene of each chapter (matches YouTube chapters).\n'
    '- {"type":"timeline","title":"...","events":[{"date":"Sep 28, 2025","label":"<=6 words"}],"highlight":index,"source":"..."} 3-6 events.\n'
    '- {"type":"chart","title":"... ($B)","unit":"$B","series":[{"label":"...","value":6.1}],"highlight":index,"source":"..."} only real sourced numbers.\n'
    '- {"type":"document","doc":"Indictment, US v. X, 26 Cr. 29","header":"...","excerpt":"exact or near-exact public wording (<=45 words)","highlight":"key phrase inside excerpt","source":"..."}.\n'
    '- {"type":"quote","text":"verbatim quote","speaker":"Name","role":"...","source":"outlet, date"} only real verbatim quotes from the facts.\n'
    '- {"type":"relmap","title":"Who owed whom","center":"Company","center_role":"...","nodes":[{"name":"Lender","relation":"$715M receivables","say":"lender","alert_say":"","alert_label":""}],"source":"..."} 2-4 nodes (more parties: use parties); alert_say/alert_label (e.g. "SEVERE LOSSES") only when the narration names that consequence.\n'
    '- {"type":"flow","label":"THE TIMING MISMATCH","nodes":[{"name":"Members","note":"wanted flexibility","say":"members"},{"name":"WeWork","say":"WeWork"},{"name":"Landlords","note":"wanted long leases","say":"landlords"}],'
    '"edges":[{"from":0,"to":1,"label":"FEES","stop_say":"empty desk","stop_label":"EMPTY DESK"},{"from":1,"to":2,"label":"RENT","alert_say":"rent","alert_label":"RENT STILL DUE"}],"note":"optional one-line takeaway","source":"..."} '
    '2-3 parties with money or obligations moving between them; stop_* only when the narration says a payment stops, alert_* when a payment becomes the problem.\n'
    '- {"type":"stack","label":"IN BANKRUPTCY","title":"Who gets paid first","tiers":[{"label":"Secured creditors","note":"","fill":1.0,"say":"..."}],"highlight":2,"highlight_label":"PAID ONLY FROM WHAT REMAINS","highlight_say":"...","illustrative":true,"source":"..."} '
    '2-4 tiers of an order or priority; fill = share recovered (0-1); illustrative:true unless every fill is a sourced number.\n'
    '- {"type":"list","label":"THE ORDINARY QUESTIONS","items":["Who controls the company?","Where does the cash go?"]} 2-4 short items the narration says one after another, in its own words.\n'
    '- {"type":"takeaway","label":"THE PATTERN","text":"<=12-word thesis taken from the narration","sub":"optional supporting line"} a scene that states a conclusion (not a quote).\n'
    '- {"type":"real_photo","entity":"Exact person or company name","place":"CITY"} full-screen REAL photo (Wikimedia Commons, animated with camera parallax) when that real person or headquarters is the subject.\n'
    '- {"type":"scale","title":"...","amount":"$11.6B","comparison":"plain-language comparison that is arithmetically true","blocks":0,"source":"..."}.\n'
    '- {"type":"headline","outlet":"Reuters","date":"Jan 29, 2026","headline":"real published headline"}.\n'
    '- {"type":"moneyflow","title":"Follow the money","flows":[{"from":{"name":"Fund, New York","lon":-74.0,"lat":40.7},"to":{"name":"Company, City","lon":-81.7,"lat":41.5},"amount":"$715M","date":"..."}],"source":"..."} ANIMATED map: ONLY for a sourced transfer/financing between two real places (use real city coordinates).\n'
    '- {"type":"collapse","title":"...","unit":"$B","mode":"line|bars","points":[{"label":"...","value":5.0,"display":"~$5B","tone":"loss|","event":""}],"final":{"label":"...","value":"$12M"},"source":"..."} ANIMATED value collapse (valuation, stock, assets vs liabilities) with sourced numbers only.\n'
    "OVERLAYS (drawn on top of the AI visual):\n"
    '- {"type":"lower_third","name":"Full Name","role":"role + legal status e.g. pleaded not guilty"} when a person is first named.\n'
    '- {"type":"logo","company":"Name"} when a company is named prominently.\n'
    '- {"type":"callout","text":"$12B liabilities","source":"short source"} for key amounts.\n'
    '- {"type":"parties","title":"Lenders exposed","items":["Jefferies","UBS"]} for involved parties (lenders, banks, regulators, courts).\n'
    '- {"type":"citation","text":"DOJ SDNY, Jan 29 2026"} small corner source when a key number appears without a callout.\n'
    "A scene may combine one full-screen item with nothing else, or several overlays. ")

def write_script(p, gfx=True):
    """gfx=False: so narracao e visual (os graficos vem depois em pipeline.plan_gfx, em lotes): o roteiro inteiro com as
    regras de grafico estourou os 600 s da API em 18/10/2026; em duas etapas levou ~3 min."""
    mins = int(p.get("minutes") or 10)
    words = mins * 150
    sys = ("You are a researcher and scriptwriter for a faceless Business & Finance documentary YouTube channel. "
           "Scripts will be reviewed by a human before production, so accuracy matters more than drama. "
           "NEVER invent sources, URLs, quotes or numbers. Only give a URL if you are confident it exists; otherwise set url to \"verificar\". "
           "Set needs_check=true on any scene whose claims (figures, dates, quotes, allegations) must be verified. Reply only in JSON (a single json object).")
    u = (f"Title: {p.get('title')}\nNiche: {p.get('niche')}\nLanguage of the narration: {p.get('language')}\n"
         "Keep the title EXACTLY as given (it was chosen for click-through); return it unchanged in the json. "
         "The first 15 seconds of narration must deliver on the title's curiosity promise (if the title hides who it is, reveal or tease it right away). "
         f"Target length: {mins} minutes (~{words} words of narration in total).\n"
         + (f"Angle / editorial brief: {p.get('theme')}\n" if p.get("theme") else "")
         + (f"Verified facts you may use (with sources). Prefer these; do not contradict them; cite the given URLs in sources:\n{p.get('facts')}\n" if p.get("facts") else "")
         + 
         "Write a documentary narration split into scenes of 1-3 sentences (6-10 seconds each). "
         + STORY_STANDARD +
         "Strong hook in the first 30 seconds, clear story arc, retention beats (open loops, reveals) spread through the video, ending with a call to subscribe. "
         "For each scene: narration in the narration language; visual_prompt IN ENGLISH: a concrete, detailed visual description (ONE clear subject doing ONE visible action, setting and era, camera angle, lighting, mood; 25-50 words) faithful to that scene's narration; "
         "the meaning must read from objects, action and light, never from readable text, charts on screens, calendars or documents "
         "(no real person likeness, no logos or trademarks, no on-screen text); key_facts (list of factual claims in the scene); "
         "sources (list of {title, url}); needs_check (boolean); chapter (short chapter title, set ONLY on the first scene of each chapter, else empty); "
         + ("gfx (list of on-screen graphics specs for this scene, see GRAPHICS below; [] when none).\n" + GFX_SPEC + "\n" if gfx else
            "gfx (always [] here: graphics are planned in a second pass).\n") +
         '{"title":"...","description":"resumo em português","hook":"first 30 seconds summary",'
         '"retention_beats":["..."],"scenes":[{"narration":"...","visual_prompt":"...","key_facts":["..."],'
         '"sources":[{"title":"...","url":"verificar"}],"needs_check":true,"chapter":"","gfx":[]}]}')
    return chat_json(sys, u, 32000)

def save_project(proj):
    for k in [k for k in proj if k.startswith("_")]:
        proj.pop(k, None)
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
    with LOCK:  # cenas ainda sem midia usam o modelo de prompt atual (as prontas guardam o prompt com que foram geradas)
        d = load_project(pid); cfg = pricing(); pdir = PROJECTS / pid
        for sc in d.get("scenes") or []:
            if not (sc.get("file") and (pdir / sc["file"]).is_file()):
                sc["grok_prompt"] = build_grok_prompt(sc, cfg)
        proj_path(pid).write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
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

# ---------- Montagem (montage.py em subprocesso) ----------
MONT = {}
def mont_status(pid):
    pid = Path(pid).name; d = PROJECTS / pid
    st = {}
    f = d / "logs" / "montage.json"
    if f.is_file():
        try: st = json.loads(f.read_text(encoding="utf-8"))
        except Exception: st = {}
    pr = MONT.get(pid); st["running"] = bool(pr and pr.poll() is None)
    if st.get("state") == "running" and not st["running"] and not pr:
        st["state"] = "interrupted"
    sc = json.loads((PROJECTS / f"{pid}.json").read_text(encoding="utf-8")).get("scenes") or []
    st["scenes"] = len(sc)
    st["chars"] = sum(len(x.get("narration") or "") for x in sc)
    st["audio_done"] = sum(1 for i in range(len(sc)) if (d / "audio" / f"scene-{i+1:02d}.mp3").is_file())
    st["media_done"] = sum(1 for x in sc if x.get("file") and (d / x["file"]).is_file())
    fo = d / "output" / "final.mp4"
    st["final"] = fo.is_file(); st["final_mb"] = round(fo.stat().st_size / 1e6, 1) if fo.is_file() else 0
    st["srt"] = (d / "output" / "final.srt").is_file()
    st["music"] = next((m.name for m in sorted(d.glob("music.*"))), None)
    try:
        import montage as _m; st["config"] = _m.cfg()
    except Exception:
        st["config"] = {}
    return st

def mont_start(pid, step="all", force_tts=False):
    pid = Path(pid).name
    pr = MONT.get(pid)
    if pr and pr.poll() is None:
        raise ApiError("A montagem já está rodando.")
    if step != "tts":
        import pipeline
        v = pipeline.validate(pid, autofix=True)
        if not v["ok"]:
            g = "; ".join(f"cena {x['scene']}: {', '.join(x['missing'])}" for x in v["gaps"][:8])
            raise ApiError(f"Render bloqueado pela Validação: {len(v['gaps'])} cena(s) com lacunas. {g}")
        gfx_render(pid)
    logs = PROJECTS / pid / "logs"; logs.mkdir(parents=True, exist_ok=True)
    args = [_venv_py(), str(Path(__file__).resolve().parent / "montage.py"), pid, "--step", step]
    if force_tts: args.append("--force-tts")
    out = open(logs / "montage.out", "a", encoding="utf-8")
    MONT[pid] = subprocess.Popen(args, stdout=out, stderr=subprocess.STDOUT, cwd=str(Path(__file__).resolve().parent),
                                 creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    return {"started": True}

def mont_stop(pid):
    (PROJECTS / Path(pid).name / "logs" / "montage_control.txt").write_text("stop", encoding="utf-8")
    return {"ok": True}

def mont_config(c):
    f = Path(__file__).resolve().parent / "config" / "montage.json"
    cur = json.loads(f.read_text(encoding="utf-8")) if f.is_file() else {}
    for k in ("tts_model", "voice", "instructions", "music_volume", "burn_subtitles", "crossfade_seconds", "ken_burns_zoom"):
        if k in c: cur[k] = c[k]
    f.write_text(json.dumps(cur, ensure_ascii=False, indent=2), encoding="utf-8")
    return cur

def gfx_render(pid):
    import gfx
    pdir = PROJECTS / Path(pid).name
    nf, no = gfx.render_project(proj_path(pid), pdir)
    return {"full": nf, "overlays": no}

def save_music(pid, name, data):
    ext = Path(name).suffix.lower()
    if ext not in (".mp3", ".wav", ".m4a", ".ogg"):
        raise ApiError("Use MP3, WAV, M4A ou OGG.")
    d = PROJECTS / Path(pid).name
    for m in d.glob("music.*"): m.unlink()
    (d / f"music{ext}").write_bytes(data)
    return {"music": f"music{ext}"}

def save_logo(pid, name, data):
    if not data.startswith(b"\x89PNG"):
        raise ApiError("Envie um arquivo PNG.")
    d = PROJECTS / Path(pid).name / "assets"; d.mkdir(parents=True, exist_ok=True)
    (d / "logo.png").write_bytes(data)
    return {"logo": "assets/logo.png"}

# ---------- YouTube stats ----------
YT_CHANNEL = "UCvmyoFV8fg5fMtoejd82CRA"
def yt_key():
    f = ROOT / ".env"
    if f.is_file():
        for line in f.read_text(encoding="utf-8", errors="ignore").splitlines():
            if line.strip().startswith("YOUTUBE_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return os.environ.get("YOUTUBE_API_KEY", "").strip()
def yt_vid(url):
    m = re.search(r"(?:v=|youtu\.be/|shorts/|embed/)([A-Za-z0-9_-]{11})", url or "")
    return m.group(1) if m else None
def yt_stats(pid, force=False):
    d = load_project(pid); vid = yt_vid(d.get("published_url"))
    sf = PROJECTS / Path(pid).name / "yt_stats.json"
    cur = json.loads(sf.read_text(encoding="utf-8")) if sf.is_file() else {"history": []}
    cur["video_id"] = vid; cur["has_key"] = bool(yt_key())
    if not vid:
        cur["error"] = "Projeto sem link do YouTube publicado."; return cur
    today = time.strftime("%Y-%m-%d")
    if not force and cur.get("fetched_at", "")[:10] == today and cur.get("video_id_fetched") == vid:
        return cur
    if not cur["has_key"]:
        cur["error"] = "no_key"; return cur
    q = urllib.parse.urlencode({"part": "statistics,snippet", "id": vid, "key": yt_key()})
    try:
        with urllib.request.urlopen("https://www.googleapis.com/youtube/v3/videos?" + q, timeout=20) as r:
            j = json.loads(r.read())
    except urllib.error.HTTPError as e:
        try: msg = json.loads(e.read())["error"]["message"]
        except Exception: msg = f"HTTP {e.code}"
        cur["error"] = "YouTube API: " + re.sub(r"key=[^&\s]+", "key=***", msg); return cur
    except Exception as e:
        cur["error"] = "Falha de rede: " + type(e).__name__; return cur
    it = (j.get("items") or [None])[0]
    if not it:
        cur["error"] = "Vídeo não encontrado (privado ou removido?)."; return cur
    stt, sn = it.get("statistics", {}), it.get("snippet", {})
    cur.update(error=None, views=int(stt.get("viewCount", 0)), likes=int(stt.get("likeCount", 0)) if "likeCount" in stt else None,
               comments=int(stt.get("commentCount", 0)) if "commentCount" in stt else None, yt_title=sn.get("title"),
               channel_ok=sn.get("channelId") == YT_CHANNEL, published_at=sn.get("publishedAt"),
               fetched_at=time.strftime("%Y-%m-%d %H:%M"), video_id_fetched=vid)
    h = [x for x in cur.get("history", []) if x.get("date") != today]
    h.append({"date": today, "views": cur["views"], "likes": cur["likes"], "comments": cur["comments"]})
    cur["history"] = h[-120:]
    sf.write_text(json.dumps(cur, ensure_ascii=False, indent=2), encoding="utf-8")
    return cur
def yt_cached(pid):
    sf = PROJECTS / Path(pid).name / "yt_stats.json"
    try: return json.loads(sf.read_text(encoding="utf-8"))
    except Exception: return None
def yt_daily_loop():
    while True:
        try:
            if yt_key():
                for f in PROJECTS.glob("*.json"):
                    try:
                        d = json.loads(f.read_text(encoding="utf-8"))
                        if d.get("status") in ("publicado", "agendado") and d.get("published_url"):
                            yt_stats(d["id"])
                    except Exception:
                        pass
        except Exception:
            pass
        time.sleep(3600)

# ---------- etapas / publicacao ----------
COVER_CANDIDATES = ("PUBLICAR/3-thumbnail.jpg", "PUBLICAR/thumbnail.jpg", "output/thumbnail.jpg")
def set_fair_use(b):
    """Per-person 'Uso justo' (fair use): news/agency photo of a verified person, shown only inside the person card,
    briefly, with transformative polaroid treatment and on-card credit. Requires image URL + article URL naming the person."""
    with LOCK:
        d = load_project(b["id"]); pdir = PROJECTS / Path(d["id"]).name
        e = next((x for x in d.get("entities") or [] if x["name"] == b["name"]), None)
        if not e or e.get("kind") != "person": raise ApiError("Pessoa não encontrada.")
        cr = e.setdefault("credits", {})
        if not b.get("enabled"):
            if e.get("photo_license") == "fair_use":
                e.pop("photo", None); e.pop("photo_license", None)
                for k in ("photo", "photo_source", "photo_short", "photo_image_url"): cr.pop(k, None)
        else:
            if not (b.get("source_url") and b.get("outlet")): raise ApiError("Informe a URL da matéria (que nomeia a pessoa) e o veículo.")
            if b.get("image_url"):
                req = urllib.request.Request(b["image_url"], headers={"User-Agent": "Mozilla/5.0"})
                data = urllib.request.urlopen(req, timeout=60).read()
                from PIL import Image
                import io
                rel = f"entities/{re.sub(r'[^a-z0-9]+', '-', e['name'].lower()).strip('-')}-photo.jpg"
                Image.open(io.BytesIO(data)).convert("RGB").save(pdir / rel, quality=95); e["photo"] = rel
            if not e.get("photo"): raise ApiError("Informe a URL da imagem.")
            e["photo_license"] = "fair_use"
            cr.update(photo=f"{b['outlet']} (fair use, news photo)", photo_short=b["outlet"], photo_source=b["source_url"])
            if b.get("image_url"): cr["photo_image_url"] = b["image_url"]
            if b.get("role"): e["role"] = b["role"]
        proj_path(d["id"]).write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"ok": True, "entity": e}

def project_cover(d):
    pdir = PROJECTS / Path(d["id"]).name
    # chosen/uploaded thumbnail wins over generated candidates and scene frames
    for rel in [d.get(k) for k in ("thumbnail", "cover") if d.get(k)] + list(COVER_CANDIDATES):
        if (pdir / rel).is_file():
            return rel
    if (pdir / "output" / "final.mp4").is_file():
        th = sorted(p for p in (pdir / "output" / "thumbs").rglob("*") if p.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp")) if (pdir / "output" / "thumbs").is_dir() else []
        th += sorted(p for p in (pdir / "PUBLICAR").glob("*thumb*")) if (pdir / "PUBLICAR").is_dir() else []
        th += sorted(p for p in (pdir / "output").glob("thumb*") if p.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp"))
        if th:
            return th[-1].relative_to(pdir).as_posix()
    for sc in d.get("scenes") or []:
        f = sc.get("file") or ""
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")) and (pdir / f).is_file():
            return f
    return None

def project_stages(d):
    pdir = PROJECTS / Path(d["id"]).name
    sc = d.get("scenes") or []
    leg = bool(d.get("legacy_complete"))  # produced before the 9-stage flow; all stages done
    return {
        "ideia": bool(d.get("title")),
        "pesquisa": leg or bool(d.get("dossier")),
        "roteiro": len(sc) > 0,
        "imagens": leg or bool(d.get("images_done")),
        "prompts": leg or bool(d.get("prompts_enriched")),
        "validacao": leg or bool((d.get("validation") or {}).get("ok")),
        "cenas": len(sc) > 0 and all(x.get("file") and (pdir / x["file"]).is_file() for x in sc),
        "montagem": (pdir / "output" / "final.mp4").is_file(),
        "publicacao": d.get("status") in ("publicado", "agendado") and bool(d.get("published_url")),
    }

def decorate(d):
    if d.get("status") == "agendado" and d.get("scheduled_at") and time.strftime("%Y-%m-%d %H:%M") >= d["scheduled_at"]:
        d["status"] = "publicado"; d.setdefault("published_at", d["scheduled_at"] + ":00")
    d["_stages"] = project_stages(d); d["_cover"] = project_cover(d)
    if isinstance(d.get("logo"), dict):
        d["logo"]["has"] = (PROJECTS / Path(d["id"]).name / (d["logo"].get("file") or "assets/logo.png")).is_file()
    return d

def publish(pid, url, unpublish=False, scheduled_at=None):
    url = (url or "").strip()
    with LOCK:
        d = load_project(pid)
        if unpublish:
            d["status"] = "rascunho"
        else:
            if not re.match(r"^https?://", url):
                raise ApiError("Cole o link completo do vídeo (https://...).")
            if scheduled_at:
                d.update(published_url=url, status="agendado", scheduled_at=scheduled_at.replace("T", " ")[:16])
            else:
                d.update(published_url=url, status="publicado", published_at=time.strftime("%Y-%m-%d %H:%M:%S"))
        proj_path(pid).write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    return decorate(d)

class H(BaseHTTPRequestHandler):
    def _send(self, code, obj=None, raw=None, ctype="application/json; charset=utf-8"):
        b = raw if raw is not None else json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code); self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)

    def _send_file(self, f):
        ct = {".mp4": "video/mp4", ".srt": "application/x-subrip; charset=utf-8", ".mp3": "audio/mpeg"}.get(f.suffix.lower(), "application/octet-stream")
        size = f.stat().st_size
        rng = self.headers.get("Range")
        start, end = 0, size - 1
        if rng and rng.startswith("bytes="):
            a, _, b = rng[6:].partition("-")
            start = int(a) if a else max(0, size - int(b)); end = int(b) if (a and b) else size - 1
            end = min(end, size - 1, start + 8 * 1024 * 1024 - 1)
            self.send_response(206); self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        else:
            self.send_response(200)
        n = end - start + 1
        self.send_header("Content-Type", ct); self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Length", str(n))
        if f.suffix.lower() == ".srt" or "dl=1" in self.path:
            self.send_header("Content-Disposition", f'attachment; filename="{f.name}"')
        self.end_headers()
        with open(f, "rb") as fh:
            fh.seek(start); left = n
            while left > 0:
                chunk = fh.read(min(1 << 20, left))
                if not chunk: break
                try: self.wfile.write(chunk)
                except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError): return
                left -= len(chunk)

    def log_message(self, *a):
        pass

    def do_GET(self):
        p = self.path.split("?")[0]
        if p == "/api/status":
            return self._send(200, {"has_key": bool(api_key()), "model": MODEL, "has_xai": bool(xai_key())})
        if p == "/api/grok_auto":
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            return self._send(200, auto_status(q["id"][0]))
        if p == "/api/montage":
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            return self._send(200, mont_status(q["id"][0]))
        if p == "/api/ytstats":
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            try:
                return self._send(200, yt_stats(q["id"][0], q.get("force", ["0"])[0] == "1"))
            except Exception as e:
                return self._send(400, {"error": str(e)})
        if p.startswith("/files/"):
            parts = [urllib.parse.unquote(x) for x in p.split("/")[2:]]
            if len(parts) == 2 and parts[1] == "cover":
                d = json.loads((PROJECTS / f"{Path(parts[0]).name}.json").read_text(encoding="utf-8"))
                c = project_cover(d)
                if c:
                    f = PROJECTS / Path(parts[0]).name / c
                    ct = {".png": "image/png", ".webp": "image/webp"}.get(f.suffix.lower(), "image/jpeg")
                    return self._send(200, raw=f.read_bytes(), ctype=ct)
            if len(parts) == 3 and parts[1] in ("output", "audio", "assets", "entities", "gfx"):
                f = PROJECTS / Path(parts[0]).name / parts[1] / Path(parts[2]).name
                if f.is_file():
                    return self._send_file(f)
            if len(parts) == 3 and parts[1] == "shorts":
                f = PROJECTS / Path(parts[0]).name / "output" / "shorts" / Path(parts[2]).name
                if f.is_file():
                    return self._send_file(f)
            return self._send(404, {"error": "não encontrado"})
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
                    st = project_stages(d)
                    items.append({"id": d["id"], "title": d.get("title"), "language": d.get("language"), "updated_at": d.get("updated_at"),
                                  "status": decorate(dict(d)).get("status") or "rascunho", "scheduled_at": d.get("scheduled_at"), "published_url": d.get("published_url"), "cover": project_cover(d),
                                  "stages_done": sum(st.values()), "stages": st, "yt": {k: (yt_cached(d["id"]) or {}).get(k) for k in ("views", "likes", "comments", "fetched_at")},
                                  "pub_at": d.get("scheduled_at") or (d.get("published_at") or "")[:16] or None})
                except Exception:
                    pass
            # ordem de publicacao: com data primeiro (mais antigo -> mais novo), depois rascunhos por edicao recente
            items.sort(key=lambda x: (0, x["pub_at"]) if x["pub_at"] else (1, ""))
            return self._send(200, items)
        if p == "/api/shorts":
            items, now = [], time.strftime("%Y-%m-%d %H:%M")
            social = {}  # (projeto, arquivo) -> {facebook: status, instagram: status}, da fila do tools/meta_publish.py
            try:
                for x in json.loads((ROOT / "social" / "queue.json").read_text(encoding="utf-8")):
                    social.setdefault((x["project"], Path(x["file"].replace("\\", "/")).name), {})[x["platform"]] = "erro" if x.get("error") and x["status"] == "pendente" else x["status"]
            except FileNotFoundError:
                pass
            for f in PROJECTS.glob("*/output/shorts/shorts.json"):
                try:
                    pid = f.parents[2].name; pj = json.loads((PROJECTS / f"{pid}.json").read_text(encoding="utf-8"))
                    for s in json.loads(f.read_text(encoding="utf-8")):
                        sch = s.get("scheduled"); url = s.get("youtube")
                        stt = "publicado" if url and sch and sch <= now else "agendado" if url and sch else "publicado" if url else "rascunho"
                        items.append({"project": pid, "project_title": pj.get("title"), "file": s.get("file"), "title": s.get("title"),
                                      "seconds": s.get("seconds"), "published_url": url, "pub_at": sch, "status": stt,
                                      "social": social.get((pid, s.get("file")), {})})
                except Exception:
                    pass
            items.sort(key=lambda x: (0, x["pub_at"]) if x["pub_at"] else (1, x["project"], x["file"] or ""))
            return self._send(200, items)
        if p.startswith("/api/projects/"):
            f = PROJECTS / (Path(p).name + ".json")
            if not f.exists():
                return self._send(404, {"error": "não encontrado"})
            return self._send(200, decorate(json.loads(f.read_text(encoding="utf-8"))))
        f = STATIC / ("index.html" if p == "/" else p.lstrip("/"))
        if f.is_file() and STATIC in f.resolve().parents:
            ct = {".html": "text/html", ".js": "application/javascript", ".css": "text/css"}.get(f.suffix, "application/octet-stream")
            return self._send(200, raw=f.read_bytes(), ctype=ct + "; charset=utf-8")
        self._send(404, {"error": "não encontrado"})

    def do_POST(self):
        n = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(n)
        if self.path.startswith("/api/montage/logo"):
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            try:
                return self._send(200, save_logo(q["id"][0], q.get("name", ["logo.png"])[0], raw))
            except ApiError as e:
                return self._send(400, {"error": str(e)})
        if self.path.startswith("/api/montage/music"):
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            try:
                return self._send(200, save_music(q["id"][0], q.get("name", ["m.mp3"])[0], raw))
            except ApiError as e:
                return self._send(400, {"error": str(e)})
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
            if self.path == "/api/montage/start":
                return self._send(200, mont_start(body["id"], body.get("step", "all"), body.get("force_tts", False)))
            if self.path == "/api/montage/stop":
                return self._send(200, mont_stop(body["id"]))
            if self.path == "/api/montage/config":
                return self._send(200, mont_config(body))
            if self.path == "/api/gfx/render":
                return self._send(200, gfx_render(body["id"]))
            if self.path.startswith("/api/pipeline/"):
                import pipeline
                st = self.path.rsplit("/", 1)[-1]
                if st == "notes":
                    with LOCK:
                        d = load_project(body["id"]); d["research_notes"] = body.get("notes", ""); proj_path(body["id"]).write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
                    return self._send(200, {"ok": True})
                if st == "fairuse":
                    return self._send(200, set_fair_use(body))
                fn = {"research": lambda: pipeline.research(body["id"]), "script": lambda: pipeline.script_from_dossier(body["id"]),
                      "images": lambda: pipeline.collect_images(body["id"], body.get("curated")),
                      "prompts": lambda: pipeline.enrich_prompts(body["id"]), "validate": lambda: pipeline.validate(body["id"], body.get("autofix", True))}[st]
                r = fn()
                if st == "validate" and r.get("ok"): gfx_render(body["id"])
                return self._send(200, r)
            if self.path == "/api/publish":
                return self._send(200, publish(body["id"], body.get("url"), body.get("unpublish", False), body.get("scheduled_at")))
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
    threading.Thread(target=yt_daily_loop, daemon=True).start()
    ThreadingHTTPServer(("127.0.0.1", PORT), H).serve_forever()
