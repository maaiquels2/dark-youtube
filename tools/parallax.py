# -*- coding: utf-8 -*-
"""Dark Studio - parallax 2.5D: foto real parada vira plano com movimento de camera (sem Grok/Flow).
Primeiro plano = recorte do assunto (BiRefNet) quando ha um assunto claro, senao o que esta perto pela profundidade
(Depth Anything V2); o fundo atras dele e preenchido pela LaMa; as duas camadas se movem em velocidades diferentes.
Uso: python tools/parallax.py <project_id> [--scenes 5,15] [--preview DIR]
     cenas: source == "real_photo" (foto inteira na tela) ou "parallax": true no plano da cena.
"""
import argparse, json, shutil, subprocess, sys, tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parent))
import media_ai as M  # noqa: E402

W, H, FPS = 1920, 1080, 30
MOVES = [  # (fundo: zoom ini/fim, deslocamento x px) (frente: idem) - alterna para nao repetir o mesmo movimento
    ((1.00, 1.05, 0), (1.00, 1.11, 0)),        # aproximacao
    ((1.04, 1.04, 30), (1.08, 1.08, -40)),     # travelling lateral
    ((1.05, 1.00, 0), (1.11, 1.00, 0)),        # recuo revelando
]


def layers(img):
    """(frente RGBA, fundo RGB, modo). Assunto claro (10-55% da foto) -> recorte; senao -> profundidade."""
    img = img.convert("RGB")
    m = np.asarray(M.cutout(img), np.float32) / 255; cov = (m > 0.5).mean()
    mode = "cutout"
    if not 0.10 <= cov <= 0.55:
        d = M.depth(img); thr = np.percentile(d, 70)  # o terco mais proximo vira primeiro plano
        m = np.clip((d - thr) / 0.08, 0, 1); mode = "depth"
    mask = Image.fromarray((m * 255).astype(np.uint8))
    hole = mask.point(lambda v: 255 if v > 40 else 0).filter(ImageFilter.MaxFilter(31))  # folga: borda do assunto nao vaza no fundo
    bg = M.inpaint(img, hole, pad=0.15)
    fg = img.copy(); fg.putalpha(mask.filter(ImageFilter.GaussianBlur(1.5)))
    return fg, bg, mode


def cover(im, scale):
    r = max(W / im.width, H / im.height) * scale
    return im.resize((max(W, round(im.width * r)), max(H, round(im.height * r))), Image.LANCZOS)


def render(src, out, dur, move=0):
    img = Image.open(src)
    if img.width < 1600:  # foto pequena: Real-ESRGAN antes (so nitidez geral; rosto nao e "restaurado")
        tmp = Path(tempfile.gettempdir()) / f"px_up_{Path(src).stem}.png"
        M.upscale(src, tmp, 2 if img.width >= 1000 else 4); img = Image.open(tmp)
    fg, bg, mode = layers(img)
    (b0, b1, bx), (f0, f1, fx) = MOVES[move % len(MOVES)]
    zmax = max(b0, b1, f0, f1) + 0.02
    BG, FG = cover(bg, zmax), cover(fg, zmax)  # uma vez em resolucao folgada; cada quadro so recorta e reduz
    n = max(2, int(round(dur * FPS)))
    ff = shutil.which("ffmpeg")
    p = subprocess.Popen([ff, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-crf", "16", "-preset", "veryfast", "-pix_fmt", "yuv420p", str(out)], stdin=subprocess.PIPE)
    def view(L, z, dx, k):
        s = z / zmax; cw, ch = W / s, H / s  # janela W x H no espaco da camada folgada, no zoom z
        x = (L.width - cw) / 2 - dx * k / s; y = (L.height - ch) / 2
        return L.crop((round(x), round(y), round(x + cw), round(y + ch))).resize((W, H), Image.BILINEAR)  # fora da borda: transparente
    for i in range(n):
        k = i / (n - 1); e = k * k * (3 - 2 * k)  # ease in-out
        frame = view(BG, b0 + (b1 - b0) * e, bx, e)
        f = view(FG, f0 + (f1 - f0) * e, fx, e); frame.paste(f, (0, 0), f.split()[3])
        p.stdin.write(np.asarray(frame.convert("RGB"), np.uint8).tobytes())
    p.stdin.close(); p.wait()
    return mode


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("project"); ap.add_argument("--scenes", default=""); ap.add_argument("--preview")
    a = ap.parse_args()
    root = Path(__file__).resolve().parents[1]
    pfile, pdir = root / "projects" / f"{a.project}.json", root / "projects" / a.project
    pj = json.loads(pfile.read_text(encoding="utf-8")); sc = pj["scenes"]
    import ec_gfx
    L = ec_gfx.durations(pdir, len(sc))
    only = {int(x) for x in a.scenes.split(",") if x.strip()}
    for i, s in enumerate(sc):
        if only and i + 1 not in only: continue
        photo = s.get("photo_file") or s.get("file") or ""
        if not (s.get("parallax") or s.get("source") in ("real_photo", "real_photo_parallax")) or not photo.lower().endswith((".jpg", ".jpeg", ".png")):
            continue
        out = (Path(a.preview) if a.preview else pdir / "media") / f"parallax-{i+1:02d}.mp4"; out.parent.mkdir(parents=True, exist_ok=True)
        mode = render(pdir / photo, out, L[i], move=i)
        print(f"cena {i+1}: {mode} -> {out.name}", flush=True)
        if not a.preview:
            real = s.get("source") in ("real_photo", "real_photo_parallax")  # imagem gerada (local/IA) nao vira "foto real"
            s["photo_file"] = photo; s.update(file=out.relative_to(pdir).as_posix(), mode="video", source="real_photo_parallax" if real else s.get("source"))
    if not a.preview:
        pfile.write_text(json.dumps(pj, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
