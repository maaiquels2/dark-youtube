# -*- coding: utf-8 -*-
"""Testes do tools/montar.py (um caminho so para montar). Nao monta de verdade: registra o que seria chamado.
Sem pytest: python tests/test_montar.py"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tools"))
import montar, gfx  # noqa: E402

FALHAS = []
EC = "the-rise-and-fall-of-wework-ec-20261017"
ANTIGO = "first-brands-the-11-6-billion-auto-parts-collapse-20261015-181116"


def caso(nome):
    def deco(fn):
        try: fn(); print("ok  ", nome)
        except Exception as e: FALHAS.append(nome); print("FALHA", nome, "->", repr(e))
        return fn
    return deco


def chamadas(pid, **kw):
    log = []
    montar.run, gfx.render_project = (lambda *a: log.append(" ".join(Path(str(x)).name if i == 0 else str(x) for i, x in enumerate(a)))), \
                                     (lambda pfile, pdir: log.append("gfx.render_project") or (0, 0))
    montar.montar(pid, **kw)
    return log


@caso("o projeto decide o caminho")
def _():
    assert montar.is_ec({"scenes": [{"ec": {"full": {"type": "chart"}}}]}) and montar.is_ec({"scenes": [{"gfx_legacy": []}]})
    assert not montar.is_ec({"scenes": [{"gfx": [{"type": "chart"}]}]}) and not montar.is_ec({"scenes": []})


@caso("EffectCraft: narracao, gfx.py (sobras), ec_gfx, ec_montage")
def _():
    if not (ROOT / "projects" / f"{EC}.json").is_file(): print("     (projeto ausente: pulado)"); return
    assert chamadas(EC) == ["montage.py " + EC + " --step tts", "gfx.render_project", "ec_gfx.py " + EC, "ec_montage.py " + EC]


@caso("EffectCraft sem graficos (produce/remake ja renderizaram)")
def _():
    if not (ROOT / "projects" / f"{EC}.json").is_file(): return
    assert chamadas(EC, step="render", graficos=False) == ["ec_montage.py " + EC]


@caso("antigo: gfx.py + montage.py render, nunca ec_gfx/ec_montage")
def _():
    if not (ROOT / "projects" / f"{ANTIGO}.json").is_file(): print("     (projeto ausente: pulado)"); return
    assert chamadas(ANTIGO, step="render") == ["gfx.render_project", "montage.py " + ANTIGO + " --step render"]


@caso("so narracao")
def _():
    if not (ROOT / "projects" / f"{EC}.json").is_file(): return
    assert chamadas(EC, step="tts", force_tts=True) == ["montage.py " + EC + " --step tts --force-tts"]


print(f"\n{'TUDO OK' if not FALHAS else f'{len(FALHAS)} FALHA(S): ' + ', '.join(FALHAS)}")
sys.exit(1 if FALHAS else 0)
