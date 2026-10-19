# -*- coding: utf-8 -*-
"""Testes do tools/ec_gfx.py: preparo do spec, tempo dos graficos pela fala (timing, sync) e um quadro real no EffectCraft.
Sem pytest: python tests/test_ec_gfx.py"""
import sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tools"))
import ec_gfx  # noqa: E402

FALHAS = []


def caso(nome):
    def deco(fn):
        try: fn(); print("ok  ", nome)
        except Exception as e: FALHAS.append(nome); print("FALHA", nome, "->", repr(e))
        return fn
    return deco


def fala(texto, passo=0.4):  # uma palavra a cada 0,4 s (150 por minuto)
    return [{"w": w.strip(".,?"), "s": round(passo * k, 2)} for k, w in enumerate(texto.split())]


@caso("prep copia a imagem para a pasta do EffectCraft e quebra textos longos")
def _():
    with tempfile.TemporaryDirectory() as d:
        pd, wd = Path(d) / "p", Path(d) / "w"; (pd / "entities").mkdir(parents=True); wd.mkdir()
        (pd / "entities" / "x-logo.png").write_bytes(b"png")
        sp = ec_gfx.prep({"type": "flow", "nodes": [{"label": "X", "file": "entities/x-logo.png", "sub": "uma descricao bem mais longa que vinte e quatro"}]}, wd, pd)
        assert sp["nodes"][0]["file"] == "x-logo.png" and (wd / "x-logo.png").is_file()
        assert "\r" in sp["nodes"][0]["sub"], sp["nodes"][0]["sub"]
        st = ec_gfx.prep({"type": "statement", "text": "Uma frase que passa de trinta e quatro caracteres com folga"}, wd, pd)
        assert "\r" in st["text"]


@caso("flow: cartao entra quando e falado; fluxo para e alerta depois de comecar")
def _():
    f = {"type": "flow", "nodes": [{"label": "MEMBERS", "say": "members"}, {"label": "WEWORK", "say": "wework"}, {"label": "LANDLORDS", "say": "landlords"}],
         "edges": [{"from": 0, "to": 1, "label": "FEES", "stop_say": "empty desk"}, {"from": 1, "to": 2, "label": "RENT", "alert_say": "rent"}]}
    n = ec_gfx.timing(f, fala("Landlords wanted long leases and members wanted flexibility so WeWork stood between until an empty desk left the rent due"), 12.0)
    at = [x["at"] for x in f["nodes"]]
    assert n >= 4 and at[2] < at[0] < at[1], at  # na ordem em que sao ditos
    for e in f["edges"]: assert e["at"] >= max(f["nodes"][e["from"]]["at"], f["nodes"][e["to"]]["at"]), e
    assert f["edges"][0]["stop"] >= f["edges"][0]["at"] + 1.0 and f["edges"][1]["alert"] >= f["edges"][1]["at"] + 1.0, f["edges"]


@caso("plano feito a mao (at sem say) fica como esta")
def _():
    f = {"type": "flow", "nodes": [{"label": "A", "at": 5.2}, {"label": "B", "at": 7.3}], "edges": [{"from": 0, "to": 1, "label": "X", "at": 8.0}]}
    ec_gfx.timing(f, fala("qualquer coisa"), 13.0)
    assert [x["at"] for x in f["nodes"]] == [5.2, 7.3] and f["edges"][0]["at"] == 8.0


@caso("sem fala achada: ordem fixa dentro da cena; list sempre em ordem crescente")
def _():
    f = {"type": "list", "items": [{"text": "a", "say": "zzz"}, {"text": "b", "say": "yyy"}, {"text": "c", "say": "xxx"}]}
    assert ec_gfx.timing(f, [], 9.0) == 0
    at = [x["at"] for x in f["items"]]; assert at == sorted(at) and at[-1] <= 9.0 - 2.0, at
    f = {"type": "list", "items": [{"text": "Who controls the company?", "say": "Who controls the company?"},
                                   {"text": "Where does the cash go?", "say": "Where does the cash go?"}]}
    ec_gfx.timing(f, fala("Who controls the company Where does cash go"), 9.0)
    assert f["items"][0]["at"] < f["items"][1]["at"], f["items"]


@caso("stack e relmap: barra/alerta depois do rotulo; satelite depois do centro")
def _():
    s = {"type": "stack", "tiers": [{"label": "A", "say": "secured"}, {"label": "B", "say": "other"}], "highlight": 1, "highlight_say": "remains"}
    ec_gfx.timing(s, fala("secured first then other and only what remains"), 10.0)
    assert all(t["at"] >= 1.0 + 0.45 * k for k, t in enumerate(s["tiers"])) and s["highlight_at"] > s["tiers"][1]["at"], s
    r = {"type": "relmap", "center": {"label": "C"}, "sats": [{"label": "X", "say": "x"}, {"label": "Y", "alert_say": "losses"}]}
    ec_gfx.timing(r, fala("x then severe losses"), 10.0)
    assert all(x["at"] >= r["center"]["at"] for x in r["sats"]) and r["sats"][1]["alert_at"] >= r["sats"][1]["at"], r


@caso("sync: sobreposicao entra quando o assunto e falado; capitulo empurra para depois do titulo")
def _():
    sc = [{"narration": "x", "ec": {"overlay": [{"type": "callout", "label": "SOFTBANK", "text": "Rescue package", "start": 0.6}]}},
          {"narration": "y", "ec": {"overlay": [{"type": "chapter", "num": "II", "title": "The Money"},
                                                {"type": "logo", "file": "entities/softbank-logo.png", "label": "MAJOR INVESTOR"}]}}]
    wd = {"1": {"words": fala("then softbank arranged a rescue package")}, "2": {"words": fala("then came a backer softbank")}}
    ec_gfx.sync(sc, [10.0, 10.0], wd)
    c = sc[0]["ec"]["overlay"][0]; assert abs(c["start"] - (0.4 - 0.2)) < 0.01 or c["start"] == 0.3, c  # "softbank" em 0,4 s
    lg = sc[1]["ec"]["overlay"][1]; assert lg["start"] >= 3.6, lg  # depois do titulo de capitulo
    assert c.get("start_base") == 0.6  # o tempo do plano fica guardado


@caso("EffectCraft desenha um flow de verdade (se instalado)")
def _():
    if not Path(ec_gfx.CLI).is_file(): print("     (EffectCraft nao instalado: pulado)"); return
    with tempfile.TemporaryDirectory() as d:
        wd = Path(d)
        f = {"type": "flow", "label": "TESTE", "nodes": [{"label": "A", "sub": "x"}, {"label": "B"}], "edges": [{"from": 0, "to": 1, "label": "FEES"}]}
        ec_gfx.timing(f, [], 6.0)
        ec_gfx.render_one(("t", ec_gfx.prep(dict(f, dur=6.0), wd, wd), wd, None, None, [4.0]))
        from PIL import Image
        im = Image.open(wd / "t_t4.0.png"); assert im.size[0] >= 900 and im.convert("L").getextrema()[1] > 100  # tem conteudo claro


print(f"\n{'TUDO OK' if not FALHAS else f'{len(FALHAS)} FALHA(S): ' + ', '.join(FALHAS)}")
sys.exit(1 if FALHAS else 0)
