# -*- coding: utf-8 -*-
"""Dark Studio - montar um projeto: um caminho so para o botao "Montar" do app, o produce.py e o remake.py.
  python tools/montar.py <id> [--step tts|render|all] [--force-tts] [--sem-graficos]
O proprio projeto escolhe o caminho:
  EffectCraft (projeto convertido: alguma cena com ec ou gfx_legacy) -> gfx.py desenha o que sobrou sem equivalente,
      tools/ec_gfx.py, tools/ec_montage.py (cor por ato, SFX, deixas musicais)
  antigo (nunca convertido)                                          -> gfx.py + montage.py
A narracao (--step tts) e a mesma nos dois: montage.py. --sem-graficos: os graficos ja foram renderizados (produce.py).
Antes, o botao do app so conhecia o caminho antigo e o gfx.py desmarcava a midia das cenas EffectCraft.
"""
import argparse, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]; PY = sys.executable
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tools"))
import projfile  # noqa: E402


def is_ec(pj):
    return any(s.get("ec") or "gfx_legacy" in s for s in pj.get("scenes") or [])


def run(*args):
    r = subprocess.run([PY] + [str(a) for a in args], cwd=ROOT)
    if r.returncode: raise SystemExit(f"falhou: {' '.join(map(str, args))}")


def montar(pid, step="all", force_tts=False, graficos=True):
    ec = is_ec(projfile.read(pid))
    print(f"montar {pid}: caminho {'EffectCraft' if ec else 'antigo'}, etapa {step}", flush=True)
    if step in ("tts", "all"):
        run(ROOT / "montage.py", pid, "--step", "tts", *(["--force-tts"] if force_tts else []))
    if step == "tts": return
    if graficos:
        import gfx
        print("gfx.py:", gfx.render_project(projfile.path(pid), ROOT / "projects" / pid), flush=True)  # nao mexe em cena EffectCraft
        if ec: run(ROOT / "tools" / "ec_gfx.py", pid)
    run(*((ROOT / "tools" / "ec_montage.py", pid) if ec else (ROOT / "montage.py", pid, "--step", "render")))


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("project"); ap.add_argument("--step", default="all", choices=["tts", "render", "all"])
    ap.add_argument("--force-tts", action="store_true"); ap.add_argument("--sem-graficos", action="store_true")
    a = ap.parse_args()
    montar(a.project, a.step, a.force_tts, not a.sem_graficos)


if __name__ == "__main__":
    main()
