# -*- coding: utf-8 -*-
"""Testes do scenes.py (o que cada cena e) e de quem pergunta a ele. Sem pytest: python tests/test_scenes.py
Cobre o defeito de 18/10/2026: grafico recusado pelo convert voltava para gfx, o FLUX e o worker o pulavam e a cena ficava
sem midia. E o "Montar" do app, que desmarcava a midia de toda cena EffectCraft."""
import json, re, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tools"))
import scenes  # noqa: E402

FALHAS = []


def caso(nome):
    def deco(fn):
        try: fn(); print("ok  ", nome)
        except Exception as e: FALHAS.append(nome); print("FALHA", nome, "->", repr(e))
        return fn
    return deco


@caso("tipos basicos")
def _():
    assert scenes.kind({"ec": {"full": {"type": "flow"}}}) == "grafico"
    assert scenes.kind({"source": "gfx", "file": "gfx/full-03.png"}) == "grafico"
    assert scenes.kind({"source": "real_photo", "file": "entities/x.jpg"}) == "foto_real"
    assert scenes.kind({"source": "real_photo_parallax", "file": "media/parallax-05.mp4"}) == "foto_real"
    assert scenes.kind({"source": "local", "file": "media/local-07.jpg"}) == "local"
    assert scenes.kind({"source": "site", "file": "media/scene-08.mp4"}) == "ia"
    assert scenes.kind({}) == "ia"  # vazia: o motor e escolha de quem gera


@caso("capitulo e sobreposicao, nunca grafico")
def _():
    assert scenes.kind({"gfx": [{"type": "chapter", "number": 2, "title": "The Money"}]}) == "ia"
    assert scenes.kind({"gfx": [{"type": "chapter"}, {"type": "lower_third", "name": "X"}, {"type": "logo"}]}) == "ia"


@caso("roteiro ainda nao convertido")
def _():
    assert scenes.kind({"gfx": [{"type": "chart", "series": [{"label": "a", "value": 1}]}]}) == "grafico"
    assert scenes.kind({"gfx": [{"type": "flow", "nodes": []}]}) == "grafico"  # o convert ainda vai traduzir
    assert scenes.kind({"gfx": [{"type": "real_photo", "entity": "X"}]}) == "ia"  # vira foto so no convert


@caso("cena convertida: sobra do gfx.py e grafico, recusado nao conta")
def _():
    assert scenes.kind({"gfx_legacy": [{"type": "document"}], "gfx": [{"type": "document"}]}) == "grafico"
    assert scenes.kind({"gfx_legacy": [{"type": "flow"}], "gfx": [], "gfx_recusado": [{"type": "flow", "motivo": "x"}]}) == "ia"


@caso("needs_media")
def _():
    with tempfile.TemporaryDirectory() as d:
        (Path(d) / "media").mkdir(); (Path(d) / "media" / "a.jpg").write_bytes(b"x")
        assert not scenes.needs_media({"file": "media/a.jpg"}, d)
        assert scenes.needs_media({"file": "media/b.jpg"}, d)
        assert scenes.needs_media({"file": None}, d) and scenes.needs_media({}, d)


@caso("defeito: grafico recusado vira IA e o FLUX escolhe a cena")
def _():
    import remake, local_img
    flow = lambda: {"type": "flow", "nodes": [{"name": "A"}, {"name": "B"}], "edges": [{"from": 0, "to": 1, "label": "X"}]}
    pj = {"entities": [], "scenes": [{"narration": "a", "gfx": [flow()], "visual_prompt": "p"} for _ in range(3)]
          + [{"narration": "b", "gfx": [{"type": "takeaway", "text": " ".join(["palavra"] * 20)}], "visual_prompt": "p"},
             {"narration": "c", "gfx": [{"type": "stack", "tiers": [{"label": str(k), "fill": k / 6} for k in range(6)]}], "visual_prompt": "p"},
             {"narration": "d", "gfx": [{"type": "real_photo", "entity": "Ninguem"}], "visual_prompt": "p"}]}
    remake.convert(pj); sc = pj["scenes"]
    assert [scenes.kind(s) for s in sc[:2]] == ["grafico", "grafico"]
    for s in sc[2:]:  # 3a repeticao, frase longa, stack grande, foto que nao existe
        assert scenes.kind(s) == "ia", s
        assert s.get("gfx_recusado") and s["gfx_recusado"][0].get("motivo"), s
        assert not any(g["type"] in scenes.FULL for g in s.get("gfx") or []), s
    with tempfile.TemporaryDirectory() as d:
        assert list(local_img.todo(sc, Path(d), set(), False)) == [2, 3, 4, 5]


@caso("convert nao deixa sobreposicao no formato antigo (a montagem EC nao as desenha)")
def _():
    import remake
    ents = [{"name": "WeWork", "kind": "company", "aliases": ["The We Company"], "logo": "entities/wework-logo.png"}]
    tipos = [{"type": "logo", "company": "WeWork"}, {"type": "logo", "company": "Sem Logo Inc"}, {"type": "chapter", "number": 1, "title": "X"},
             {"type": "lower_third", "name": "A", "role": "B"}, {"type": "callout", "text": "$1B", "source": "x"},
             {"type": "parties", "items": ["WeWork"]}, {"type": "entity", "name": "WeWork"}, {"type": "citation", "text": "x"}]
    pj = {"entities": ents, "scenes": [{"narration": "a", "gfx": [g], "sources": []} for g in tipos]}
    remake.convert(pj)
    for s, g in zip(pj["scenes"], tipos):
        assert not s.get("gfx"), (g["type"], s.get("gfx"))
    ov = pj["scenes"][0]["ec"]["overlay"]; assert ov == [{"type": "chip", "files": ["entities/wework-logo.png"]}], ov
    assert any(o.get("text") == "Sem Logo Inc" for o in pj["scenes"][1]["ec"]["overlay"]), pj["scenes"][1]


@caso("worker do Grok/Flow pula grafico, foto real e local; pega IA")
def _():
    import grok_worker
    W = grok_worker.Worker
    assert W.is_gfx({"ec": {"full": {"type": "chart"}}}) and W.is_gfx({"source": "real_photo"}) and W.is_gfx({"source": "local"})
    assert not W.is_gfx({"gfx": [{"type": "chapter"}]}) and not W.is_gfx({"gfx_legacy": [], "gfx_recusado": [{"type": "flow"}]})


@caso("Montar antigo (gfx.render_project) nao desmarca cena EffectCraft")
def _():
    import gfx
    with tempfile.TemporaryDirectory() as d:
        pd = Path(d) / "p"; (pd / "gfx").mkdir(parents=True); (pd / "gfx" / "ec-01.mp4").write_bytes(b"x")
        pf = Path(d) / "p.json"
        s0 = {"narration": "x", "file": "gfx/ec-01.mp4", "source": "gfx", "status": "pronto", "gfx": [], "gfx_legacy": [{"type": "flow"}],
              "ec": {"full": {"type": "flow"}}}
        pf.write_text(json.dumps({"scenes": [s0, {"narration": "y", "gfx": []}]}), encoding="utf-8")
        gfx.render_project(pf, pd)
        s = json.loads(pf.read_text(encoding="utf-8"))["scenes"][0]
        assert s["file"] == "gfx/ec-01.mp4" and s["source"] == "gfx", s


@caso("capitulo desenhado como sobreposicao no gfx.py")
def _():
    import gfx
    assert "chapter" in gfx.OVER and "chapter" not in gfx.FULL
    im = gfx._draw_ov({"type": "chapter", "number": 3, "title": "The Filing"}, {}, {}, {}, {"kc": 0, "ey": 70})
    assert im.mode == "RGBA" and im.getchannel("A").getextrema()[1] > 0


@caso("todo tipo citado no prompt do roteiro esta na tabela do scenes.py")
def _():
    import app
    citados = set(re.findall(r'\{"type":"(\w+)"', app.GFX_SPEC))
    assert citados, "nenhum tipo achado no GFX_SPEC"
    faltam = citados - set(scenes.TYPES)
    assert not faltam, f"tipos no prompt sem regra em scenes.py: {sorted(faltam)}"


@caso("projetos reais: toda cena tem tipo; cena com grafico EC e grafico")
def _():
    n = 0
    for f in sorted((ROOT / "projects").glob("*.json")):
        for s in json.loads(f.read_text(encoding="utf-8")).get("scenes") or []:
            k = scenes.kind(s); n += 1
            assert k in ("grafico", "foto_real", "local", "ia"), (f.name, k)
            if (s.get("ec") or {}).get("full"): assert k == "grafico", f.name
    assert n > 100, n


print(f"\n{'TUDO OK' if not FALHAS else f'{len(FALHAS)} FALHA(S): ' + ', '.join(FALHAS)}")
sys.exit(1 if FALHAS else 0)
