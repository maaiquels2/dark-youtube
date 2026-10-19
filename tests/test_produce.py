# -*- coding: utf-8 -*-
"""Testes do tools/produce.py (comando unico) e do remake.run_steps. Nao chama API, placa nem EffectCraft:
as etapas pesadas sao trocadas por registradores. Sem pytest: python tests/test_produce.py"""
import contextlib, io, json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tools"))
import produce, remake, projfile  # noqa: E402

FALHAS = []
PID = "zz-teste-produce"


def caso(nome):
    def deco(fn):
        try: fn(); print("ok  ", nome)
        except Exception as e: FALHAS.append(nome); print("FALHA", nome, "->", repr(e))
        finally: limpar()
        return fn
    return deco


def limpar():
    shutil.rmtree(ROOT / "projects" / PID, ignore_errors=True)
    for f in (ROOT / "projects").glob(PID + ".json*"): f.unlink()


def projeto():
    limpar(); (ROOT / "projects" / PID / "logs").mkdir(parents=True)
    projfile.create(PID, {"id": PID, "title": "teste", "scenes": [{"narration": "uma cena", "needs_check": True}]})


def falso(log, falhar=None):
    """ETAPAS com as funcoes trocadas por registradores; `falhar` = nome da etapa que levanta erro."""
    out = []
    for e in produce.ETAPAS:
        if e[0] == "PARADA": out.append(e); continue
        def fn(pid, st, nome=e[0]):
            if nome == falhar: raise RuntimeError("falha simulada")
            log.append(nome)
        out.append((e[0], fn))
    return out


def rodar(**kw):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        try: produce.avancar(PID, **kw)
        except SystemExit as e: buf.write(f"\nSAIU: {e}")
    return buf.getvalue()


@caso("para em cada parada, na ordem, e --ok aprova so a atual")
def _():
    projeto(); log = []; orig = produce.ETAPAS
    try:
        produce.ETAPAS = falso(log); produce.NOMES[:] = [e[0] if e[0] != "PARADA" else "parada:" + e[1] for e in produce.ETAPAS]
        paradas = []
        for _ in range(4):
            out = rodar(ok=bool(paradas)); paradas.append(produce.estado(PID)[1].get("parada"))
        assert paradas == ["parada:roteiro", "parada:logos", "parada:cenas", "parada:final"], paradas
        assert log[:4] == ["notas", "pesquisa", "roteiro", "graficos"] and log[-1] == "montagem", log
        out = rodar(ok=True); assert "PRONTO" in out, out
    finally: produce.ETAPAS = orig


@caso("etapa que falha para, registra e retoma dali sem refazer as anteriores")
def _():
    projeto(); log = []; orig = produce.ETAPAS
    try:
        produce.ETAPAS = falso(log, falhar="pesquisa"); out = rodar()
        assert "SAIU" in out and "pesquisa" in out, out
        assert produce.estado(PID)[1]["feito"] == ["notas"]
        assert "ERRO" in produce.estado(PID)[1]["log"][-1]
        produce.ETAPAS = falso(log); rodar()
        assert log == ["notas", "pesquisa", "roteiro", "graficos"], log  # notas nao rodou de novo
    finally: produce.ETAPAS = orig


@caso("resumo do roteiro: cenas, minutos, sem IA e o que conferir")
def _():
    projeto()
    r = produce.resumo_roteiro(PID)
    assert r.startswith("1 cenas") and "a conferir (needs_check): 1" in r, r


@caso("remake.run_steps converte e poe deixas musicais no mesmo processo")
def _():
    limpar(); (ROOT / "projects" / PID).mkdir(parents=True)
    g = [[{"type": "chapter", "number": 1, "title": "Inicio"}, {"type": "chart", "series": [{"label": "Valor", "value": 47}], "unit": "$B", "source": "S"}],
         [{"type": "timeline", "title": "T", "events": [{"date": "2019", "label": "a"}, {"date": "2023", "label": "b"}], "source": "S"}],
         [{"type": "flow", "nodes": [{"name": "A"}, {"name": "B"}], "edges": [{"from": 0, "to": 1, "label": "X"}]}],
         [{"type": "takeaway", "text": "Curta e clara."}], [], [{"type": "chapter", "number": 2, "title": "Fim"}]]
    projfile.create(PID, {"id": PID, "entities": [], "scenes": [{"narration": f"cena {i} bankruptcy", "gfx": x, "sources": []} for i, x in enumerate(g)]})
    with contextlib.redirect_stdout(io.StringIO()): remake.run_steps(PID, ["convert", "cues"])
    d = projfile.read(PID)
    tipos = [((s.get("ec") or {}).get("full") or {}).get("type") for s in d["scenes"]]
    assert tipos == ["counter", "timeline", "flow", "statement", None, None], tipos
    assert all("gfx_legacy" in s for s in d["scenes"]) and d.get("music_cues"), d.get("music_cues")
    assert all((ROOT / "projects" / PID / c["file"]).is_file() for c in d["music_cues"])  # projeto novo tambem recebe as trilhas


print(f"\n{'TUDO OK' if not FALHAS else f'{len(FALHAS)} FALHA(S): ' + ', '.join(FALHAS)}")
sys.exit(1 if FALHAS else 0)
