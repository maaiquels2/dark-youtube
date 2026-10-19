# -*- coding: utf-8 -*-
"""Dark Studio - comando unico: do tema ao final.mp4, parando nos tres pontos que precisam do olhar humano.
  python tools/produce.py ideias "tema"                          titulos sugeridos (demanda, texto da thumbnail)
  python tools/produce.py novo "Titulo" --tema "angulo" --notas notas.txt [--minutos 11] [--motor local|grok|flow]
     notas = fatos com fonte (URL) que a pesquisa organiza; nada e inventado fora delas (podem ser coladas depois em
     projects/<id>/notas.txt ou no campo de pesquisa do app; o Claude pode juntar as notas pesquisando na web)
  python tools/produce.py <id>                                   continua de onde parou (retoma etapa que falhou)
  python tools/produce.py <id> --ok                              aprova a parada atual e segue
  python tools/produce.py <id> --refazer 12,30                   na parada das cenas: gera de novo essas cenas (outra semente)
  python tools/produce.py <id> --desde narracao                  refaz a partir de uma etapa
  python tools/produce.py <id> --status                          mostra em que etapa esta
Paradas: ROTEIRO (fatos, valores, acusacoes) -> LOGOS (o Commons ja trouxe logo errado) -> CENAS (revisao a 6 fps) -> FINAL
(assistir como espectador). Envio ao YouTube fica fora: e irreversivel e ja caiu num canal encerrado.
Motor das cenas que sobram depois de graficos e fotos reais: local (FLUX na placa + parallax, padrao, sem credito), grok ou flow.
Estado: projects/<id>/logs/produce.json.
"""
import argparse, json, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]; PY = sys.executable
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tools"))


def run(*args):
    r = subprocess.run([PY] + [str(a) for a in args], cwd=ROOT, env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8"})
    if r.returncode: raise RuntimeError(f"falhou: {' '.join(map(str, args))}")


def remake(pid, steps): run("tools/remake.py", pid, "--new", pid, "--steps", steps)


def validar(pid):
    import pipeline
    v = pipeline.validate(pid, autofix=False)
    if not v["ok"]:
        raise RuntimeError("validacao com lacunas: " + "; ".join(f"cena {g['scene']}: {', '.join(g['missing'])}" for g in v["gaps"][:10]))


def cenas(pid, st):
    if st["motor"] == "local": remake(pid, "local")
    else: run("grok_worker.py", pid, "--video-engine", st["motor"])


def revisao(pid):
    """Folha com um quadro por cena + tira a 6 fps de cada clipe de video do Grok/Flow (logica: gente que surge, carro na calcada)."""
    pdir = ROOT / "projects" / pid; out = pdir / "logs" / "revisao"; out.mkdir(parents=True, exist_ok=True)
    for f in out.glob("*.jpg"): f.unlink()
    run("tools/contact_sheet.py", pid, out)
    sc = json.loads((ROOT / "projects" / f"{pid}.json").read_text(encoding="utf-8"))["scenes"]
    for i, s in enumerate(sc):
        f = pdir / (s.get("file") or "")
        if s.get("source") in ("gfx", "local", "real_photo_parallax", "real_photo") or f.suffix.lower() != ".mp4" or not f.is_file(): continue
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(f), "-vf", "fps=6,scale=384:216,tile=6x6",
                        "-frames:v", "1", "-update", "1", str(out / f"cena-{i + 1:02d}-6fps.jpg")])
    return out


def resumo_roteiro(pid):
    d = json.loads((ROOT / "projects" / f"{pid}.json").read_text(encoding="utf-8")); sc = d["scenes"]
    import pipeline
    full = set(pipeline.FULL_GFX) - {"chapter"} | {"real_photo"}
    sem_ia = sum(any((g or {}).get("type") in full for g in (s.get("gfx") or []) + (s.get("gfx_legacy") or []))
                 or bool((s.get("ec") or {}).get("full")) or s.get("source") in ("real_photo", "real_photo_parallax") for s in sc)
    chk = [str(i + 1) for i, s in enumerate(sc) if s.get("needs_check")]
    return (f"{len(sc)} cenas, ~{sum(len((s.get('narration') or '').split()) for s in sc) / 150:.0f} min de narracao, {sem_ia} com grafico ou foto "
            f"({sem_ia / max(1, len(sc)):.0%}); a conferir (needs_check): {', '.join(chk) or 'nenhuma'}")


def notas(pid):
    """A pesquisa so organiza fatos que vieram nas notas (com fonte): sem notas, para aqui e diz onde colocar."""
    import app
    d = app.load_project(pid); nf = ROOT / "projects" / pid / "notas.txt"
    if not (d.get("research_notes") or d.get("facts")):
        if not (nf.is_file() and nf.read_text(encoding="utf-8").strip()):
            raise RuntimeError(f"sem notas de pesquisa: cole os fatos com fonte (URL) em {nf} ou no campo de pesquisa do app")
        d["research_notes"] = nf.read_text(encoding="utf-8"); app.save_project(d)


ETAPAS = [  # (nome, funcao(pid, estado)) ou (PARADA, nome, mensagem(pid))
    ("notas", lambda pid, st: notas(pid)),
    ("pesquisa", lambda pid, st: __import__("pipeline").research(pid)),
    ("roteiro", lambda pid, st: __import__("pipeline").script_from_dossier(pid, gfx=False)),
    ("graficos", lambda pid, st: __import__("pipeline").plan_gfx(pid)),
    ("PARADA", "roteiro", lambda pid: "Revise o roteiro no app (fatos, valores, acusacoes, presuncao de inocencia). " + resumo_roteiro(pid)),
    ("entidades", lambda pid, st: __import__("pipeline").collect_images(pid)),
    ("prompts", lambda pid, st: __import__("pipeline").enrich_prompts(pid)),
    ("narracao", lambda pid, st: run("montage.py", pid, "--step", "tts")),
    ("palavras", lambda pid, st: run("tools/words.py", pid)),
    ("converter", lambda pid, st: remake(pid, "convert,cues,sheet")),
    ("PARADA", "logos", lambda pid: f"Confira logos, selos e fotos em projects/{pid}/logs/logos-sheet.jpg (troque o errado em entities/ antes de seguir)."),
    ("render_graficos", lambda pid, st: remake(pid, "gfx")),
    ("cenas", cenas),
    ("acabamento", lambda pid, st: remake(pid, "clean,parallax")),
    ("revisao", lambda pid, st: revisao(pid)),
    ("PARADA", "cenas", lambda pid: f"Revise as cenas em projects/{pid}/logs/revisao/ (folha geral + tiras a 6 fps dos clipes). "
                                    f"Para gerar de novo: python tools/produce.py {pid} --refazer 12,30"),
    ("validacao", lambda pid, st: validar(pid)),
    ("montagem", lambda pid, st: run("tools/ec_montage.py", pid)),
    ("PARADA", "final", lambda pid: f"Assista projects/{pid}/output/final.mp4 inteiro, como espectador. Depois: thumbnail, kit e envio "
                                    "(confira a conta do YouTube antes de enviar)."),
]
NOMES = [e[0] if e[0] != "PARADA" else "parada:" + e[1] for e in ETAPAS]


def estado(pid):
    f = ROOT / "projects" / pid / "logs" / "produce.json"
    return f, (json.loads(f.read_text(encoding="utf-8")) if f.is_file() else {"feito": [], "motor": "local", "log": []})


def salvar(f, st):
    f.parent.mkdir(parents=True, exist_ok=True); f.write_text(json.dumps(st, ensure_ascii=False, indent=1), encoding="utf-8")


def avancar(pid, ok=False):
    f, st = estado(pid)
    for e, nome in zip(ETAPAS, NOMES):
        if nome in st["feito"]: continue
        if e[0] == "PARADA":
            if not ok:
                st["parada"] = nome; salvar(f, st)
                print(f"\n=== PARADA: {e[1].upper()} ===\n{e[2](pid)}\nQuando estiver bom: python tools/produce.py {pid} --ok\n", flush=True); return
            ok = False  # --ok aprova so a parada atual
        else:
            t = time.time(); print(f"--- {nome} ---", flush=True)
            try:
                e[1](pid, st)
            except Exception as x:
                st["log"].append(f"{time.strftime('%d/%m %H:%M')} {nome}: ERRO {x}"); salvar(f, st)
                sys.exit(f"etapa '{nome}' falhou: {x}\nCorrija e rode de novo: python tools/produce.py {pid}  (retoma desta etapa)")
            st["log"].append(f"{time.strftime('%d/%m %H:%M')} {nome}: ok em {time.time() - t:.0f}s")
        st["feito"].append(nome); st.pop("parada", None); salvar(f, st)
    print(f"\nPRONTO: projects/{pid}/output/final.mp4 aprovado. Falta thumbnail, kit e envio (manual).", flush=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("alvo", help="ideias | novo | <id do projeto>"); ap.add_argument("texto", nargs="?")
    ap.add_argument("--tema", default=""); ap.add_argument("--minutos", type=int, default=11)
    ap.add_argument("--motor", choices=["local", "grok", "flow"]); ap.add_argument("--ok", action="store_true")
    ap.add_argument("--refazer", default=""); ap.add_argument("--desde", choices=[n for n in NOMES if not n.startswith("parada:")])
    ap.add_argument("--status", action="store_true"); ap.add_argument("--notas", help="arquivo com os fatos e fontes (novo)")
    a = ap.parse_args()
    import app
    base = {"niche": "Business & Finance Documentary", "language": "English"}
    if a.alvo == "ideias":
        r = app.suggest_titles(dict(base, theme=a.texto or a.tema))
        print("demanda:", r.get("demand"), "-", r.get("demand_why"), "| serie:", r.get("series"))
        for t in r.get("titles") or []: print(f"  {t['title']}   [thumb: {t.get('thumb_text')}]  {t.get('hook', '')}")
        return
    if a.alvo == "novo":
        if not a.texto: sys.exit('informe o titulo: python tools/produce.py novo "Titulo" --tema "angulo"')
        notes = Path(a.notas).read_text(encoding="utf-8") if a.notas else ""
        pid = app.save_project(dict(base, title=a.texto, theme=a.tema or a.texto, minutes=a.minutos, status="draft", research_notes=notes))["id"]
        print("projeto criado:", pid)
    else:
        pid = a.alvo
        if not (ROOT / "projects" / f"{pid}.json").is_file(): sys.exit(f"projeto nao encontrado: {pid}")
    f, st = estado(pid)
    if a.motor: st["motor"] = a.motor
    if a.desde:
        k = NOMES.index(a.desde); st["feito"] = [n for n in st["feito"] if NOMES.index(n) < k]; st.pop("parada", None)
    salvar(f, st)
    if a.status:
        print(f"{pid} | motor: {st['motor']} | parada: {st.get('parada') or '-'}\nfeito: {', '.join(st['feito']) or '-'}"); print("\n".join(st["log"][-8:])); return
    if a.refazer:
        if st.get("parada") != "parada:cenas": sys.exit("--refazer so na parada das cenas")
        st["sementes"] = st.get("sementes", 1) + 1; salvar(f, st)
        run("tools/local_img.py", pid, "--scenes", a.refazer, "--redo", "--seed", st["sementes"])
        run("tools/media_ai.py", "clean", pid); run("tools/parallax.py", pid, "--scenes", a.refazer); revisao(pid)
        print(f"cenas {a.refazer} geradas de novo (semente {st['sementes']}). Revise logs/revisao/ e rode --ok ou --refazer de novo."); return
    if a.ok and not st.get("parada"):
        print("nenhuma parada esperando aprovacao: --ok ignorado (nao aprova paradas futuras)"); a.ok = False
    avancar(pid, ok=a.ok)


if __name__ == "__main__":
    main()
