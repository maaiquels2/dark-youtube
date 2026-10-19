# -*- coding: utf-8 -*-
"""Testes do timeline.py (duracao, inicio e ato de cada cena). Sem pytest: python tests/test_timeline.py"""
import json, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tools"))
import timeline  # noqa: E402

FALHAS = []


def caso(nome):
    def deco(fn):
        try: fn(); print("ok  ", nome)
        except Exception as e: FALHAS.append(nome); print("FALHA", nome, "->", repr(e))
        return fn
    return deco


def old_ec_act(i, n):  # a regra dos videos aprovados (antes em tools/ec_montage.py)
    x = i / n
    return "act1" if x < 0.32 else "act2" if x < 0.55 else "act3" if x < 0.84 else "after"


@caso("ato: igual ao dos videos ja aprovados, para qualquer tamanho")
def _():
    for n in range(1, 120):
        for i in range(n): assert timeline.act(i, n) == old_ec_act(i, n), (i, n)


@caso("ato gravado na cena vale mais")
def _():
    assert timeline.act_of({"act": "after"}, 0, 50) == "after"
    assert timeline.act_of({"act": "lixo"}, 0, 50) == "act1"
    assert timeline.act_of({}, 49, 50) == "after"


@caso("plan: narracao + pausa, crossfade em todas menos a ultima, inicios somados")
def _():
    with tempfile.TemporaryDirectory() as d:
        a = Path(d) / "audio"; a.mkdir()
        for i, s in enumerate((1.0, 2.0, 1.5), 1):
            subprocess.run([shutil.which("ffmpeg"), "-v", "error", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", str(s),
                            "-c:a", "libmp3lame", str(a / f"scene-{i:02d}.mp3")], check=True)
        tl = timeline.plan(d, 3, {"pad_seconds": 0.3, "crossfade_seconds": 0.5})
        assert [round(x, 1) for x in tl["D"]] == [1.3, 2.3, 1.8], tl
        assert [round(x, 1) for x in tl["L"]] == [1.8, 2.8, 1.8], tl
        assert [round(x, 1) for x in tl["starts"]] == [0.0, 1.3, 3.6] and round(tl["total"], 1) == 5.4, tl


@caso("plan: sem narracao para com erro (antes inventava 4 s)")
def _():
    with tempfile.TemporaryDirectory() as d:
        (Path(d) / "audio").mkdir()
        try: timeline.plan(d, 2, {"pad_seconds": 0.3, "crossfade_seconds": 0.5}); raise AssertionError("nao parou")
        except RuntimeError as e: assert "sem narracao" in str(e).lower()


@caso("projeto real: ec_gfx, ec_montage e shorts dao a mesma linha do tempo da montagem")
def _():
    import montage, ec_gfx, shorts
    pid = "the-rise-and-fall-of-wework-ec-20261017"; pd = ROOT / "projects" / pid
    if not (pd / "audio" / "scene-01.mp3").is_file(): print("     (projeto sem audio: pulado)"); return
    n = len(json.loads((ROOT / "projects" / f"{pid}.json").read_text(encoding="utf-8"))["scenes"])
    tl = timeline.plan(pd, n)
    assert ec_gfx.durations(pd, n) == tl["L"]
    D, st = shorts.timeline(pd, [None] * n); assert D == tl["D"] and st == tl["starts"]
    c = montage.cfg(); assert abs(tl["total"] - sum(timeline.probe(pd / "audio" / f"scene-{i + 1:02d}.mp3") + c["pad_seconds"] for i in range(n))) < 0.05


@caso("estimativa antes do audio: 150 palavras por minuto")
def _():
    assert timeline.estimate(" ".join(["w"] * 150)) == 60 and timeline.estimate("") == 1.0
    assert timeline.estimate(" ".join(["w"] * 150), wpm=180) == 50  # velocidade configuravel (app.scene_seconds)


print(f"\n{'TUDO OK' if not FALHAS else f'{len(FALHAS)} FALHA(S): ' + ', '.join(FALHAS)}")
sys.exit(1 if FALHAS else 0)
