# -*- coding: utf-8 -*-
"""Testes do projfile.py (dono do arquivo do projeto). Sem pytest: python tests/test_projfile.py"""
import copy, json, subprocess, sys, tempfile, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import projfile  # noqa: E402

FALHAS = []


def caso(nome):
    def deco(fn):
        try: fn(); print("ok  ", nome)
        except Exception as e: FALHAS.append(nome); print("FALHA", nome, "->", repr(e))
        return fn
    return deco


def novo(d, cenas):
    f = Path(d) / "p.json"; f.write_text(json.dumps({"id": "p", "scenes": cenas}), encoding="utf-8"); return f


@caso("corrida: ferramenta lenta nao apaga o que o worker gravou no meio tempo")
def _():
    with tempfile.TemporaryDirectory() as d:
        f = novo(d, [{"narration": "a"}, {"narration": "b", "status": "pendente"}])
        pj = projfile.read(f); before = copy.deepcopy(pj["scenes"])          # ec_gfx le e comeca a renderizar
        projfile.patch(f, {1: {"status": "pronto", "file": "media/scene-02.mp4"}})  # worker termina a cena 2
        pj["scenes"][0].update(file="gfx/ec-01.mp4", source="gfx", ec={"full": {"type": "flow"}})  # ec_gfx termina
        projfile.patch(f, projfile.changed(before, pj["scenes"], ("ec", "file", "source", "status", "orig_file")))
        s = projfile.read(f)["scenes"]
        assert s[0]["file"] == "gfx/ec-01.mp4" and s[0]["ec"]["full"]["type"] == "flow", s
        assert s[1]["status"] == "pronto" and s[1]["file"] == "media/scene-02.mp4", s


@caso("salvamento da tela com copia antiga nao desfaz plano EffectCraft, foto real nem midia")
def _():
    with tempfile.TemporaryDirectory() as d:
        f = novo(d, [{"narration": "a", "source": "real_photo_parallax", "file": "media/parallax-01.mp4", "photo_file": "entities/x.jpg"},
                     {"narration": "b", "source": "gfx", "file": "gfx/ec-02.mp4", "ec": {"full": {"type": "chart"}}, "gfx_legacy": []}])
        tela = {"id": "p", "title": "novo titulo", "scenes": [{"narration": "a (editada)", "source": "api"}, {"narration": "b", "source": "api"}]}
        projfile.save(dict(tela, id=str(f)))
        s = projfile.read(f)
        assert s["title"] == "novo titulo" and s["scenes"][0]["narration"] == "a (editada)", s
        assert s["scenes"][0]["source"] == "real_photo_parallax" and s["scenes"][0]["photo_file"] == "entities/x.jpg", s
        assert s["scenes"][1]["ec"]["full"]["type"] == "chart" and s["scenes"][1]["source"] == "gfx" and s["scenes"][1]["file"] == "gfx/ec-02.mp4", s


@caso("tela ainda escolhe o motor de uma cena de IA (source api/site nao e campo de ferramenta)")
def _():
    with tempfile.TemporaryDirectory() as d:
        f = novo(d, [{"narration": "a", "source": "api"}])
        projfile.save({"id": str(f), "scenes": [{"narration": "a", "source": "site"}]})
        assert projfile.read(f)["scenes"][0]["source"] == "site"


@caso("changed + DROP: campo removido em memoria some do disco")
def _():
    with tempfile.TemporaryDirectory() as d:
        f = novo(d, [{"narration": "a", "photo_file": "x.jpg", "file": "x.jpg"}])
        pj = projfile.read(f); before = copy.deepcopy(pj["scenes"]); pj["scenes"][0].pop("photo_file"); pj["scenes"][0]["file"] = "y.jpg"
        projfile.patch(f, projfile.changed(before, pj["scenes"], ("photo_file", "file")))
        s = projfile.read(f)["scenes"][0]; assert "photo_file" not in s and s["file"] == "y.jpg", s


@caso("edit com erro no meio nao grava nada")
def _():
    with tempfile.TemporaryDirectory() as d:
        f = novo(d, [{"narration": "a"}])
        try:
            with projfile.edit(f) as pj: pj["scenes"][0]["narration"] = "x"; raise ValueError("falhou")
        except ValueError: pass
        assert projfile.read(f)["scenes"][0]["narration"] == "a"


@caso("trava vale entre processos")
def _():
    with tempfile.TemporaryDirectory() as d:
        f = novo(d, [{"narration": "a"}])
        code = (f"import sys,time; sys.path.insert(0,{str(ROOT)!r}); import projfile\n"
                f"with projfile.lock({str(f)!r}):\n print('travado', flush=True); time.sleep(2)\n")
        p = subprocess.Popen([sys.executable, "-c", code], stdout=subprocess.PIPE, text=True)
        assert p.stdout.readline().strip() == "travado"
        t = time.time()
        with projfile.edit(f) as pj: pj["x"] = 1
        espera = time.time() - t; p.wait()
        assert espera > 1.0, f"nao esperou a outra trava ({espera:.2f}s)"
        assert projfile.read(f)["x"] == 1


print(f"\n{'TUDO OK' if not FALHAS else f'{len(FALHAS)} FALHA(S): ' + ', '.join(FALHAS)}")
sys.exit(1 if FALHAS else 0)
