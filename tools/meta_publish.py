# -*- coding: utf-8 -*-
"""Dark Studio - Reels no Facebook e no Instagram pela API oficial da Meta (sem automacao de navegador).
Contas FIXAS no .env: META_PAGE_ID (Pagina The Cracked Ledger) e META_IG_USER_ID (@thecrackedledger); o token de Pagina
(META_PAGE_TOKEN, nao expira) da acesso a outras Paginas do usuario, entao tudo confere o nome antes de enviar.
  Facebook: upload + agendamento nativo (video_state=SCHEDULED, 10 min a 29 dias) ou rascunho (DRAFT).
  Instagram: a API nao agenda; `run` publica os Reels que venceram (tarefa do Windows diaria) - upload, espera FINISHED, publica.
Fila: social/queue.json. Uso:
  python tools/meta_publish.py queue <project_id>    poe os Shorts do projeto na fila (mesmas datas do YouTube)
  python tools/meta_publish.py run                   agenda os do Facebook e publica os do Instagram que venceram
  python tools/meta_publish.py test <project_id>     Facebook em RASCUNHO + Instagram so ate FINISHED (nada publico)
"""
import json, re, sys, time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]; QUEUE = ROOT / "social" / "queue.json"
G, V = "https://graph.facebook.com", "v26.0"
BRT = timezone(timedelta(hours=-3))  # Brasil sem horario de verao desde 2019
EXPECT = {"page": "The Cracked Ledger", "ig": "thecrackedledger"}


def env():
    e = {m.group(1): m.group(2).strip().strip('"').strip("'") for m in re.finditer(r"(?m)^(META_[A-Z_]+)=(.*)$", (ROOT / ".env").read_text(encoding="utf-8"))}
    for k in ("META_PAGE_ID", "META_IG_USER_ID", "META_PAGE_TOKEN"):
        if not e.get(k): sys.exit(f"{k} faltando no .env")
    return e


def api(method, path, **params):
    r = requests.request(method, f"{G}/{V}/{path}", params=params, timeout=120); j = r.json()
    if "error" in j: raise RuntimeError(f"{path}: {j['error'].get('message')}")
    return j


def check(e):
    """Recusa enviar se os IDs do .env nao forem da Pagina/Instagram do canal."""
    p = api("GET", e["META_PAGE_ID"], fields="name,instagram_business_account{id,username}", access_token=e["META_PAGE_TOKEN"])
    ig = p.get("instagram_business_account") or {}
    assert p.get("name") == EXPECT["page"] and ig.get("username") == EXPECT["ig"] and ig.get("id") == e["META_IG_USER_ID"], \
        f"conta inesperada: {p.get('name')} / {ig.get('username')}"


def rupload(url, token, path, octet=True):
    """octet=False no Instagram (o teste sem Content-Type foi o que passou)."""
    data = Path(path).read_bytes(); h = {"Authorization": f"OAuth {token}", "offset": "0", "file_size": str(len(data))}
    if octet: h["Content-Type"] = "application/octet-stream"
    r = requests.post(url, data=data, timeout=600, headers=h)
    j = r.json()
    if not j.get("success"): raise RuntimeError(f"upload falhou: {j}")


def fb_reel(e, video, description, when=None, draft=False):
    """Sobe o Reel na Pagina e agenda (when=datetime) ou deixa em rascunho. Devolve o video_id."""
    tok, page = e["META_PAGE_TOKEN"], e["META_PAGE_ID"]
    vid = api("POST", f"{page}/video_reels", upload_phase="start", access_token=tok)["video_id"]
    rupload(f"https://rupload.facebook.com/video-upload/{V}/{vid}", tok, video)
    params = dict(video_id=vid, upload_phase="finish", description=description, access_token=tok)
    if draft: params["video_state"] = "DRAFT"
    else: params.update(video_state="SCHEDULED", scheduled_publish_time=int(when.timestamp()))
    api("POST", f"{page}/video_reels", **params)
    return vid


def ig_container(e, video, caption):
    """Sobe o Reel no Instagram e espera o processamento (FINISHED). Ainda NAO publica. Devolve o id do container."""
    tok, ig = e["META_PAGE_TOKEN"], e["META_IG_USER_ID"]
    cid = api("POST", f"{ig}/media", media_type="REELS", upload_type="resumable", caption=caption, access_token=tok)["id"]  # share_to_feed quebra o upload resumable
    rupload(f"https://rupload.facebook.com/ig-api-upload/{V}/{cid}", tok, video, octet=False)
    for _ in range(20):  # a documentacao pede para consultar com calma
        st = api("GET", cid, fields="status_code,status", access_token=tok)
        if st.get("status_code") == "FINISHED": return cid
        if st.get("status_code") in ("ERROR", "EXPIRED"): raise RuntimeError(f"Instagram recusou o video: {st}")
        time.sleep(20)
    raise RuntimeError("Instagram nao terminou de processar em ~7 min")


def ig_publish(e, cid):
    return api("POST", f"{e['META_IG_USER_ID']}/media_publish", creation_id=cid, access_token=e["META_PAGE_TOKEN"])["id"]


def captions(k):
    """Mesmo texto do Short no YouTube. No Instagram link na legenda nao e clicavel: aponta para a bio."""
    base = (k.get("pick_description") or k["description"].split("\n\n")[0]).strip()
    yt = re.search(r"https?://\S+", k.get("description", "")); link = yt.group(0) if yt else "https://www.youtube.com/@thecrackedledger"
    return f"{base}\n\nFull documentary: {link}", f"{base}\n\nFull documentary on YouTube: link in bio."


def load():
    return json.loads(QUEUE.read_text(encoding="utf-8")) if QUEUE.is_file() else []


def save(q):
    QUEUE.parent.mkdir(exist_ok=True); QUEUE.write_text(json.dumps(q, ensure_ascii=False, indent=2), encoding="utf-8")


def queue(pid):
    od = ROOT / "projects" / pid / "output" / "shorts"; ks = json.loads((od / "shorts.json").read_text(encoding="utf-8"))
    q = load(); have = {(x["platform"], x["file"]) for x in q}; n = 0
    for k in ks:
        if not k.get("scheduled"): continue  # so o que ja tem data no YouTube
        fb, ig = captions(k); f = str((od / k["file"]).relative_to(ROOT))
        for plat, cap in (("facebook", fb), ("instagram", ig)):
            if (plat, f) in have: continue
            q.append({"platform": plat, "project": pid, "file": f, "title": k["title"], "caption": cap, "when": k["scheduled"], "status": "pendente"}); n += 1
    save(q); return n


def run(e):
    check(e); q = load(); now = datetime.now(BRT)
    print(now.strftime("%Y-%m-%d %H:%M"), "run:", sum(x["status"] == "pendente" for x in q), "pendentes", flush=True)  # prova no log que a tarefa rodou
    for x in q:
        if x["status"] != "pendente": continue
        when = datetime.strptime(x["when"], "%Y-%m-%d %H:%M").replace(tzinfo=BRT)
        try:
            if x["platform"] == "facebook" and when > now + timedelta(minutes=15) and when < now + timedelta(days=28):
                x["id"] = fb_reel(e, ROOT / x["file"], x["caption"], when=when); x["status"] = "agendado"
            elif x["platform"] == "instagram" and when <= now + timedelta(minutes=5):
                x["id"] = ig_publish(e, ig_container(e, ROOT / x["file"], x["caption"])); x["status"] = "publicado"
            else: continue
            print("ok", x["platform"], x["file"], x["when"], x["status"], flush=True)
        except Exception as err:
            x["error"] = str(err)[:300]; print("ERRO", x["platform"], x["file"], err, flush=True)
        save(q)


def test(e, pid):
    check(e); print("contas conferidas:", EXPECT)
    od = ROOT / "projects" / pid / "output" / "shorts"; k = json.loads((od / "shorts.json").read_text(encoding="utf-8"))[0]
    fb, ig = captions(k)
    if "--ig" not in sys.argv: print("facebook rascunho:", fb_reel(e, od / k["file"], fb, draft=True))
    print("instagram processado (nao publicado):", ig_container(e, od / k["file"], ig))


if __name__ == "__main__":
    assert captions({"description": "Hook.\n\nFull documentary: https://youtu.be/x"})[0].endswith("https://youtu.be/x")
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "queue": print(queue(sys.argv[2]), "itens na fila")
    elif cmd == "run": run(env())
    elif cmd == "test": test(env(), sys.argv[2])
    else: print(__doc__)
