# -*- coding: utf-8 -*-
"""Dark Studio - linha do tempo do projeto: duracao, inicio e ato de cada cena (termos em GLOSSARY.md). Fonte unica:
montage, ec_gfx, ec_montage, parallax, shorts e o kit de capitulos leem daqui.
  plan(pasta, n)        -> {"D": cena (narracao + pausa), "L": clipe (D + crossfade, menos a ultima), "starts", "total"}
  act(i, n)             -> "act1" | "act2" | "act3" | "after"   (o ato gravado na cena, se houver, vale mais: act_of)
  act_of(cena, i, n)    -> ato gravado na cena ou act(i, n)
  estimate(narracao)    -> segundos estimados antes de existir audio (150 palavras por minuto)
Sem audio de uma cena, plan() para com erro (antes uma copia inventava 4 s e o clipe saia com a duracao errada).
"""
import shutil, subprocess
from pathlib import Path

ACTS = ("act1", "act2", "act3", "after")
CUTS = (0.32, 0.55, 0.84)  # os cortes dos videos ja aprovados (cor da montagem); o roteiro novo usa os mesmos


def probe(f):
    r = subprocess.run([shutil.which("ffprobe") or "ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)],
                       capture_output=True, text=True)
    return float(r.stdout.strip())


def plan(pdir, n, cfg=None):
    if cfg is None:
        import montage; cfg = montage.cfg()
    pad, xf = cfg["pad_seconds"], cfg["crossfade_seconds"]
    audio = [Path(pdir) / "audio" / f"scene-{i + 1:02d}.mp3" for i in range(n)]
    miss = [i + 1 for i, f in enumerate(audio) if not f.is_file()]
    if miss: raise RuntimeError(f"Cenas sem narracao: {miss[:10]} (gere a narracao primeiro)")
    D = [round(probe(f) + pad, 3) for f in audio]
    return {"D": D, "L": [round(d + (xf if k < n - 1 else 0), 3) for k, d in enumerate(D)],
            "starts": [round(sum(D[:k]), 3) for k in range(n)], "total": round(sum(D), 3)}


def act(i, n):
    x = i / max(1, n)
    return ACTS[sum(x >= c for c in CUTS)]


def act_of(s, i, n):
    return s["act"] if s.get("act") in ACTS else act(i, n)


def estimate(text):
    return max(1.0, len((text or "").split()) / 150 * 60)
