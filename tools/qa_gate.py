# -*- coding: utf-8 -*-
"""Dark Studio - portao de QA antes da montagem (so le o projeto; grava apenas logs/qa_gate.json e logs/qa_gate.md).
Cada regra vem do CHECKLIST_VIDEO_YOUTUBE.md. BLOQUEIA = nao monta; AVISO = olhar nos frames.
O portao confere o PLANO (JSON), nao os pixels: texto vazando, rotulo apagado e cena poluida de verdade so aparecem na folha de frames.
Uso: python tools/qa_gate.py <project_id>      (saida 1 se houver BLOQUEIA)"""
import argparse, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tools"))
import entities  # noqa: E402

DRAFT = re.compile(r"provided notes|no source url|user[- ]provided|\b(in|from|per) the notes\b|supplied verified facts|attributed (in|to) (the )?notes|\bdraft\b|placeholder|lorem ipsum|\bTODO\b", re.I)
# a narracao vira legenda e voz: pontuacao dobrada, espaco antes de sinal ou minuscula depois de ponto aparecem na tela
TEXT_SLIP = re.compile(r"[,;:]\s*[,;:]|(?<!\.)\.\.(?!\.)|\s[,.;:!?](?=\s|$)|(?<=\w{3})[.!?]\s+[a-z]")
SUFFIX = re.compile(r"(-(bw|raw|hq))+$")


def strings(o):
    if isinstance(o, str): yield o
    elif isinstance(o, dict):
        for v in o.values(): yield from strings(v)
    elif isinstance(o, list):
        for v in o: yield from strings(v)


def files(o):
    """Arquivos de imagem referenciados por um grafico (file, photo, files, items/nodes/sats)."""
    out = []
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ("file", "photo", "logo") and isinstance(v, str): out.append(v)
            elif k == "files" and isinstance(v, list): out += [x for x in v if isinstance(x, str)]
            elif isinstance(v, (dict, list)): out += files(v)
    elif isinstance(o, list):
        for v in o: out += files(v)
    return out


def norm(f): return SUFFIX.sub("", Path(f).stem.lower())


def stems(e):
    s = {norm(entities.slug(n)) for n in (e["name"], e.get("full_name")) if n}
    if e.get("photo"): s.add(norm(e["photo"]))
    return s


def portrait(pid, rel):
    """Foto vertical ou quase quadrada (altura >= 90% da largura): esticada em 16:9 vira zoom agressivo."""
    import subprocess
    p = ROOT / "projects" / pid / rel
    if not p.is_file(): return False
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout.strip()
    try: w, h = (int(x) for x in r.split(","))
    except ValueError: return False
    return h >= 0.9 * w


def run(pid):
    pj = json.loads((ROOT / "projects" / f"{pid}.json").read_text(encoding="utf-8"))
    starts = None
    try:
        import timeline
        starts = timeline.plan(ROOT / "projects" / pid, len(pj["scenes"]))
    except Exception: pass
    return findings(pj, pid, starts)


def findings(pj, pid, starts=None):
    sc, ents = pj["scenes"], pj.get("entities") or []
    F = []

    def add(i, sev, rule, msg):
        t = starts["starts"][i] if starts else None
        F.append({"scene": i + 1, "time": f"{int(t // 60)}:{t % 60:04.1f}" if t is not None else "?", "sev": sev, "rule": rule, "msg": msg})

    for i, s in enumerate(sc):
        ec = s.get("ec") or {}; full = ec.get("full") or {}; ov = list(ec.get("overlay") or [])
        screen = {"ec": ec, "gfx": s.get("gfx")}
        shown = {norm(f) for f in files(ec)}
        for txt in strings(screen):
            if DRAFT.search(txt): add(i, "BLOQUEIA", "rascunho", f"texto de rascunho na tela: {txt[:70]!r}")
        m = TEXT_SLIP.search(s.get("narration", ""))
        if m: add(i, "AVISO", "texto_legenda", f"pontuacao suspeita na narracao: {s['narration'][max(0, m.start() - 15):m.end() + 15]!r}")
        for name in entities.mentions(s.get("narration", ""), ents):
            e = next(x for x in ents if x["name"] == name)
            if e.get("kind") == "person" and not (stems(e) & shown):
                add(i, "BLOQUEIA", "pessoa_sem_foto", f"{name} e citado e nao tem foto propria nesta cena")
            elif e.get("kind") in ("agency", "company") and not entities.has_real_asset(e):
                add(i, "AVISO", "sem_logo", f"{name} e citado e o cadastro nao tem logo, selo nem foto")
        for o in ov:
            if o.get("type") == "lower_third" and not o.get("file"):
                add(i, "BLOQUEIA", "lower_third_sem_foto", f"lower-third de {o.get('name')} sem foto em moldura")
        kinds = [o.get("type") for o in ov]
        shown_ov = [k for k in kinds if k != "chapter"]
        if full.get("type") == "timeline" and shown_ov: add(i, "BLOQUEIA", "foco_unico", f"timeline com {', '.join(shown_ov)} ao mesmo tempo")
        if full.get("type") == "person" and "lower_third" in kinds: add(i, "BLOQUEIA", "foco_unico", "card person com lower-third redundante")
        if "chapter" in kinds and full: add(i, "AVISO", "capitulo", "abertura de capitulo sobre grafico em tela cheia (PADRAO_VIDEOS e GEMINI.md divergem): conferir se nao sobrepoe")
        if len(shown_ov) > 2: add(i, "AVISO", "foco_unico", f"{len(shown_ov)} overlays na mesma cena")
        if full.get("type") == "flow":
            if len(full.get("nodes") or []) > 3: add(i, "AVISO", "fluxo", "fluxo com mais de 3 nos: simplificar")
            if any(abs(e.get("to", 0) - e.get("from", 0)) > 1 for e in full.get("edges") or []): add(i, "AVISO", "fluxo", "seta entre nos nao adjacentes passa por baixo de um cartao")
        if full.get("type") == "pair" and full.get("link") and len(full["link"]) > 22:
            add(i, "AVISO", "pair", "texto de ligacao longo entre os cartoes: conferir se invade as fotos")
        media = s.get("photo_file") or s.get("file") or ""
        if media.startswith("entities/") and full.get("type") != "person" and portrait(pid, media):
            add(i, "BLOQUEIA", "retrato_esticado", f"foto vertical de entidade como fundo da cena ({media})")

    last = sc[-1]; ecs = [(x.get("ec") or {}) for x in sc[-2:]]
    if not re.search(r"subscribe|inscrev", last.get("narration", ""), re.I): add(len(sc) - 1, "BLOQUEIA", "cta_falado", "a narracao da ultima cena nao pede a inscricao")
    if not (any((e.get("full") or {}).get("outro") for e in ecs) or re.search(r"subscribe", " ".join(strings(ecs)), re.I)):
        add(len(sc) - 1, "BLOQUEIA", "cta_escrito", "nenhum card final com SUBSCRIBE (outro) nas duas ultimas cenas")
    if starts and starts["D"][-1] < 6: add(len(sc) - 1, "AVISO", "cta_tempo", f"a cena final dura {starts['D'][-1]:.1f}s; o card precisa de 6 a 8 s")
    return F


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("project"); a = ap.parse_args()
    F = run(a.project); logs = ROOT / "projects" / a.project / "logs"; logs.mkdir(exist_ok=True)
    (logs / "qa_gate.json").write_text(json.dumps(F, ensure_ascii=False, indent=1), encoding="utf-8")
    nb = sum(f["sev"] == "BLOQUEIA" for f in F)
    md = [f"# QA gate - {a.project}", f"{nb} bloqueios, {len(F) - nb} avisos. O portao le o plano, nao os pixels: abra os frames dos avisos.", ""]
    md += [f"- **{f['sev']}** cena {f['scene']} ({f['time']}) `{f['rule']}`: {f['msg']}" for f in F]
    (logs / "qa_gate.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    for f in F: print(f"{f['sev']:8} cena {f['scene']:>3} {f['time']:>7} {f['rule']}: {f['msg']}")
    print(f"\n{nb} bloqueios, {len(F) - nb} avisos -> projects/{a.project}/logs/qa_gate.md")
    sys.exit(1 if nb else 0)


if __name__ == "__main__":
    main()
