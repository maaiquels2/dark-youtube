# -*- coding: utf-8 -*-
"""Dark Studio - dono do arquivo do projeto (projects/<id>.json). Todo processo grava por aqui: o app (threads), o worker do
Grok/Flow e as ferramentas de linha de comando. Antes, cada um lia o projeto, trabalhava minutos e gravava a copia antiga
por cima do que o outro tinha gravado nesse meio tempo.
  read(pid)                   -> documento atual
  edit(pid)                   -> `with edit(pid) as d:` trava, le, entrega; grava atomico ao sair (mudanca curta)
  patch(pid, {i: {campo: v}}) -> ferramenta lenta: aplica so os campos dela sobre a versao mais nova (DROP apaga o campo)
  save(d)                     -> documento inteiro vindo da tela/pipeline; os campos das ferramentas ficam como estao no disco
A trava e um arquivo <id>.json.lock travado pelo sistema: vale entre processos e se solta sozinha se o processo morrer.
"""
import contextlib, json, os, threading, time
from pathlib import Path

PROJECTS = Path(__file__).resolve().parent / "projects"
DROP = object()
# campos que so o servidor/ferramentas escrevem: um salvamento da tela com copia antiga nao os desfaz
SERVER_FIELDS = ("status", "file", "error", "cost_usd", "gen_seconds", "request_id", "media_duration", "generated_with",
                 "ec", "gfx_legacy", "gfx_recusado", "orig_file", "photo_file", "photo_credit", "parallax", "cleaned_text")
TOOL_SOURCES = ("gfx", "real_photo", "real_photo_parallax", "local")  # source escrito por ferramenta: a tela nao volta para api
_THREAD = threading.RLock()


def path(pid):
    """id do projeto, ou o caminho do .json (gfx.render_project e os testes recebem o caminho)."""
    if str(pid).endswith(".json"): return Path(pid)
    return PROJECTS / f"{Path(str(pid)).name}.json"


def read(pid):
    return json.loads(path(pid).read_text(encoding="utf-8"))


@contextlib.contextmanager
def lock(pid, timeout=180):
    lf = path(pid).with_suffix(".json.lock"); lf.parent.mkdir(parents=True, exist_ok=True)
    with _THREAD:
        fh = open(lf, "a+b"); t0 = time.time()
        try:
            while True:
                try:
                    if os.name == "nt":
                        import msvcrt; fh.seek(0); msvcrt.locking(fh.fileno(), msvcrt.LK_NBLCK, 1)
                    else:
                        import fcntl; fcntl.flock(fh.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                    break
                except OSError:
                    if time.time() - t0 > timeout: raise TimeoutError(f"projeto {pid} travado por outro processo ha {timeout}s")
                    time.sleep(0.2)
            yield
        finally:
            try:
                if os.name == "nt":
                    import msvcrt; fh.seek(0); msvcrt.locking(fh.fileno(), msvcrt.LK_UNLCK, 1)
            except OSError:
                pass
            fh.close()


def _write(pid, d):
    f = path(pid); tmp = f.with_suffix(f".tmp{os.getpid()}")
    tmp.write_text(json.dumps({k: v for k, v in d.items() if not str(k).startswith("_")}, ensure_ascii=False, indent=2), encoding="utf-8")
    for k in range(20):  # no Windows o replace falha se outro processo estiver lendo naquele instante
        try: os.replace(tmp, f); return
        except PermissionError:
            if k == 19: raise
            time.sleep(0.1)


@contextlib.contextmanager
def edit(pid):
    with lock(pid):
        d = read(pid)
        yield d
        _write(pid, d)


def patch(pid, scenes=None, top=None):
    with edit(pid) as d:
        for i, fields in (scenes or {}).items():
            s = d["scenes"][i]
            for k, v in fields.items():
                if v is DROP: s.pop(k, None)
                else: s[k] = v
        for k, v in (top or {}).items():
            if v is DROP: d.pop(k, None)
            else: d[k] = v
    return d


def save(d, keep=SERVER_FIELDS, before_write=None):
    """Documento inteiro (tela, pipeline). Por cena, os campos em `keep` e o source de ferramenta valem como estao no disco.
    before_write(d): ultimo ajuste com o documento ja mesclado (o app recalcula os prompts aqui)."""
    pid = d["id"]
    with lock(pid):
        if path(pid).is_file():
            old = read(pid).get("scenes") or []
            for i, sc in enumerate(d.get("scenes") or []):
                if i >= len(old): break
                for k in keep:
                    if k in old[i]: sc[k] = old[i][k]
                    else: sc.pop(k, None)
                if old[i].get("source") in TOOL_SOURCES: sc["source"] = old[i]["source"]
        if before_write: before_write(d)
        _write(pid, d)
    return d


def changed(before, after, keys):
    """{i: {campo: valor novo ou DROP}} dos campos `keys` que a ferramenta mudou em memoria (para patch)."""
    out = {}
    for i, (b, a) in enumerate(zip(before, after)):
        ch = {k: (a[k] if k in a else DROP) for k in keys if b.get(k, DROP) != a.get(k, DROP)}
        if ch: out[i] = ch
    return out
