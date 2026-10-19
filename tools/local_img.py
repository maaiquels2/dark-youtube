# -*- coding: utf-8 -*-
"""Dark Studio - imagens das cenas geradas na propria placa de video (FLUX.2 Klein 4B, Apache 2.0): sem Grok/Flow e sem credito.
Pega as cenas que ainda nao tem midia (as mesmas que o grok_worker pegaria: sem grafico, sem foto real), gera a imagem a partir
do visual_prompt e marca parallax: true, para tools/parallax.py transformar em plano com movimento de camera.
Uso: python tools/local_img.py <project_id> [--scenes 5,12] [--redo] [--seed 1]
  --redo  gera de novo cenas que ja tem midia (a anterior fica em orig_file)
Precisa de ~5 GB livres na placa: com jogo aberto ou EffectCraft/RIFE rodando, fica lento demais (o script avisa e para).
Ambiente do modelo: %LOCALAPPDATA%/DarkStudio/flux/.venv (torch cu128 + diffusers do GitHub + bitsandbytes).
"""
import argparse, json, os, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import scenes  # noqa: E402
import copy, projfile  # noqa: E402

FLUX_PY = Path(os.environ.get("LOCALAPPDATA", "")) / "DarkStudio" / "flux" / ".venv" / "Scripts" / "python.exe"
STYLE = ("Photorealistic documentary still of the real place and era, natural film look, subtle film grain, moody low-key light with readable "
         "shadows, cold teal and warm amber accents, 16:9. No text, no signage, no logos, no watermark; screens and papers blank or turned away. "
         "If the scene has people, they are seen only from behind, in silhouette or far away, with no faces; add no people the scene does not describe.")
MIN_FREE_MB = 5000


def todo(sc, pdir, only, redo):
    for i, s in enumerate(sc):
        if only and i + 1 not in only: continue
        if scenes.kind(s) not in ("ia", "local"): continue  # grafico e foto real nunca viram imagem gerada
        if not (redo or scenes.needs_media(s, pdir)): continue
        if s.get("visual_prompt"): yield i


def free_mb():
    r = subprocess.run(["nvidia-smi", "--query-gpu=memory.free", "--format=csv,noheader,nounits"], capture_output=True, text=True)
    return int(r.stdout.split()[0]) if r.returncode == 0 and r.stdout.strip() else 0


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("project"); ap.add_argument("--scenes", default="")
    ap.add_argument("--redo", action="store_true"); ap.add_argument("--seed", type=int, default=1)
    a = ap.parse_args()
    pfile, pdir = ROOT / "projects" / f"{a.project}.json", ROOT / "projects" / a.project
    if not FLUX_PY.is_file(): sys.exit(f"ambiente do FLUX nao encontrado: {FLUX_PY}")
    pj = json.loads(pfile.read_text(encoding="utf-8")); sc = pj["scenes"]; before = copy.deepcopy(sc)
    only = {int(x) for x in a.scenes.split(",") if x.strip()}
    idx = list(todo(sc, pdir, only, a.redo))
    if not idx: print("nenhuma cena para gerar"); return
    if free_mb() < MIN_FREE_MB:
        sys.exit(f"placa com {free_mb()} MB livres (precisa de {MIN_FREE_MB}): feche jogos e espere EffectCraft/RIFE terminarem")
    jobs = [{"out": str(pdir / "media" / f"local-{i + 1:02d}.jpg"), "prompt": sc[i]["visual_prompt"].strip() + " " + STYLE, "seed": a.seed} for i in idx]
    jf = pdir / "logs" / "local_img_jobs.json"; jf.parent.mkdir(exist_ok=True)
    jf.write_text(json.dumps(jobs, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(jobs)} cenas no FLUX local: {', '.join(str(i + 1) for i in idx)}", flush=True)
    r = subprocess.run([str(FLUX_PY), "-u", str(ROOT / "tools" / "flux_gen.py"), str(jf)], cwd=str(FLUX_PY.parents[2]))
    done = 0
    for i, j in zip(idx, jobs):
        out = Path(j["out"])
        if not out.is_file(): continue  # o gerador parou no meio: o que saiu fica, o resto continua pendente
        s = sc[i]
        if s.get("file") and s["file"] != out.relative_to(pdir).as_posix(): s.setdefault("orig_file", s["file"])
        s.update(file=out.relative_to(pdir).as_posix(), source="local", mode="image", status="pronto", parallax=True, error=None, cost_usd=0,
                 generated_with="FLUX.2 klein 4B (local)")
        s.pop("photo_file", None); done += 1
    projfile.patch(pfile, projfile.changed(before, sc, ("file", "source", "mode", "status", "parallax", "error", "cost_usd",
                                                       "generated_with", "orig_file", "photo_file")))
    print(f"{done}/{len(jobs)} imagens prontas; proximo passo: python tools/parallax.py {a.project}", flush=True)
    if r.returncode: sys.exit(f"gerador saiu com codigo {r.returncode}")


if __name__ == "__main__":
    main()
