# -*- coding: utf-8 -*-
"""Testes da escolha de estilo do gfx.py (draw): v2 do gfx2.py por padrao, v1 pelo ambiente, e a ordem de import nao importa.
Sem pytest: python tests/test_gfx_style.py"""
import os, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FALHAS = []


def caso(nome):
    def deco(fn):
        try: fn(); print("ok  ", nome)
        except Exception as e: FALHAS.append(nome); print("FALHA", nome, "->", repr(e))
        return fn
    return deco


def modulo(codigo, **env):
    r = subprocess.run([sys.executable, "-c", f"import sys; sys.path.insert(0, {str(ROOT)!r}); {codigo}"], capture_output=True, text=True,
                       env={**os.environ, **env}, cwd=ROOT)
    assert r.returncode == 0, r.stderr[-400:]
    return r.stdout.strip().splitlines()[-1]


@caso("padrao: desenhos do gfx2 (v2); os que ele nao tem vem do gfx")
def _():
    assert modulo("import gfx; print(gfx.draw('r_chart').__module__, gfx.draw('o_logo').__module__)") == "gfx2 gfx"


@caso("gfx2 importado antes do gfx tambem da o estilo v2 (antes caia no antigo em silencio)")
def _():
    assert modulo("import gfx2, gfx; print(gfx.draw('r_chart').__module__)") == "gfx2"


@caso("DS_GFX_STYLE=v1 usa os desenhos planos do gfx.py")
def _():
    assert modulo("import gfx; print(gfx.draw('r_chart').__module__)", DS_GFX_STYLE="v1") == "gfx"


@caso("o modulo gfx nao tem mais funcoes trocadas por baixo")
def _():
    assert modulo("import gfx; print(gfx.r_chart.__module__)") == "gfx"


print(f"\n{'TUDO OK' if not FALHAS else f'{len(FALHAS)} FALHA(S): ' + ', '.join(FALHAS)}")
sys.exit(1 if FALHAS else 0)
