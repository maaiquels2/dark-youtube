# -*- coding: utf-8 -*-
"""Dark Studio - IA local para imagem e video (sem torch: ONNX no onnxruntime + executaveis ncnn-vulkan na GPU).
  inpaint  LaMa (Apache-2.0)                 apaga texto/logo/simbolo de uma imagem a partir de uma mascara
  depth    Depth Anything V2 Small (Apache)  mapa de profundidade (1 = perto) para parallax 2.5D
  ocr      RapidOCR (PP-OCR em ONNX, Apache) acha texto escrito nas cenas do Grok
  cutout   rembg + BiRefNet (MIT)            recorte de pessoa/objeto principal
  upscale  Real-ESRGAN ncnn (BSD-3)          aumenta fotos pequenas (nunca "restaura rosto": isso inventa tracos)
  rife     RIFE ncnn (MIT)                   cria quadros intermediarios (camera lenta suave)
Modelos e executaveis em %LOCALAPPDATA%/DarkStudio (models/, bin/).
Uso: python tools/media_ai.py clean <project_id> [--dry DIR]   apaga texto escrito pelo Grok nas imagens das cenas
"""
import argparse, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

BASE = Path(os.environ.get("LOCALAPPDATA", "")) / "DarkStudio"
MODELS, BIN = BASE / "models", BASE / "bin"
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import copy, projfile  # noqa: E402
_S = {}


def _sess(name):
    import onnxruntime as ort
    if name not in _S:
        _S[name] = ort.InferenceSession(str(MODELS / name), providers=["CPUExecutionProvider"])
    return _S[name]


def inpaint(img, mask, pad=0.35):
    """Preenche a area branca da mascara (L) com o que a LaMa imagina do entorno. Trabalha num recorte em volta
    da mascara (mais detalhe que reduzir a imagem inteira para 512) e cola de volta so a area mascarada."""
    img = img.convert("RGB"); m = np.array(mask.convert("L")) > 127
    if not m.any(): return img
    ys, xs = np.where(m); W, H = img.size
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    side = int(max(x1 - x0, y1 - y0) * (1 + 2 * pad)) + 16; side = min(max(side, 256), max(W, H))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    bx0 = int(min(max(0, cx - side // 2), max(0, W - side))); by0 = int(min(max(0, cy - side // 2), max(0, H - side)))
    box = (bx0, by0, min(W, bx0 + side), min(H, by0 + side))
    crop = img.crop(box); cm = Image.fromarray((m * 255).astype(np.uint8)).crop(box)
    a = np.asarray(crop.resize((512, 512), Image.LANCZOS), np.float32) / 255.0
    b = (np.asarray(cm.resize((512, 512), Image.NEAREST), np.float32) > 127).astype(np.float32)
    out = _sess("lama_fp32.onnx").run(None, {"image": a.transpose(2, 0, 1)[None], "mask": b[None, None]})[0][0]
    out = out.transpose(1, 2, 0); out = out if out.max() > 2 else out * 255  # o export devolve 0-255 (algumas versoes, 0-1)
    fill = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).resize(crop.size, Image.LANCZOS)
    soft = cm.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(3))
    res = img.copy(); res.paste(Image.composite(fill, crop, soft), box[:2])
    return res


def depth(img, size=518):
    """Profundidade relativa normalizada 0..1 (1 = mais perto), no tamanho da imagem."""
    img = img.convert("RGB"); W, H = img.size
    h = size; w = max(14, round(size * W / H / 14) * 14)
    a = (np.asarray(img.resize((w, h), Image.BICUBIC), np.float32) / 255.0 - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]
    d = _sess("depth_anything_v2_small.onnx").run(None, {"pixel_values": a.transpose(2, 0, 1)[None].astype(np.float32)})[0][0]
    d = (d - d.min()) / (d.max() - d.min() + 1e-6)
    return np.asarray(Image.fromarray((d * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC), np.float32) / 255.0


def ocr(img, min_score=0.75, min_len=2):
    """Textos na imagem: [(caixa 4x2, texto, confianca)]. Para avisar use o padrao; para apagar, min_score baixo:
    cena do Grok nao deve ter texto nenhum, e o resto de uma palavra lida pela metade tambem precisa sair."""
    from rapidocr import RapidOCR
    if "ocr" not in _S: _S["ocr"] = RapidOCR()
    r = _S["ocr"](np.asarray(img.convert("RGB"))[:, :, ::-1])
    if r.boxes is None: return []
    return [(np.asarray(b), t, float(s)) for b, t, s in zip(r.boxes, r.txts, r.scores) if s >= min_score and len(t.strip()) >= min_len]


def text_mask(img, boxes, grow=0.35):
    m = Image.new("L", img.size, 0); d = ImageDraw.Draw(m)
    for b, _, _ in boxes:
        c = b.mean(0); hgt = np.linalg.norm(b[3] - b[0])
        pts = [tuple(c + (p - c) * (1 + grow) + np.sign(p - c) * hgt * 0.15) for p in b]
        d.polygon(pts, fill=255)
    return m.filter(ImageFilter.MaxFilter(9))  # junta pedacos vizinhos da mesma palavra


def cutout(img, model="birefnet-general"):
    """Mascara (L) do assunto principal. BiRefNet recorta cabelo e bordas melhor que o u2net padrao do rembg."""
    from rembg import new_session, remove
    if model not in _S: _S[model] = new_session(model)
    return remove(img.convert("RGB"), session=_S[model], only_mask=True)


def upscale(src, dst, scale=4):
    exe = BIN / "realesrgan" / "realesrgan-ncnn-vulkan.exe"
    subprocess.run([str(exe), "-i", str(src), "-o", str(dst), "-n", "realesrgan-x4plus", "-s", str(scale)], check=True, capture_output=True)
    return Path(dst)


def rife(src, dst, factor=2):
    """Video com `factor`x quadros (RIFE v4.6) e fps multiplicado: a desaceleracao do montage usa quadros reais."""
    ff, fp = shutil.which("ffmpeg"), shutil.which("ffprobe")
    exe = next(BIN.glob("rife-ncnn-vulkan*/rife-ncnn-vulkan.exe"))
    fps = subprocess.run([fp, "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=r_frame_rate", "-of", "csv=p=0", str(src)],
                         capture_output=True, text=True).stdout.strip()
    num, den = (fps.split("/") + ["1"])[:2]; fps = float(num) / float(den or 1)
    with tempfile.TemporaryDirectory() as td:
        i, o = Path(td) / "in", Path(td) / "out"; i.mkdir(); o.mkdir()
        subprocess.run([ff, "-v", "error", "-i", str(src), str(i / "%06d.png")], check=True)
        n = len(list(i.glob("*.png")))
        subprocess.run([str(exe), "-i", str(i), "-o", str(o), "-m", str(exe.parent / "rife-v4.6"), "-n", str(n * factor)],
                       check=True, capture_output=True)
        subprocess.run([ff, "-v", "error", "-y", "-framerate", f"{fps * factor:.4f}", "-i", str(o / "%08d.png"), "-c:v", "libx264",
                        "-crf", "14", "-preset", "veryfast", "-pix_fmt", "yuv420p", str(dst)], check=True)
    return Path(dst)


def clean_project(pid, dry=None):
    """Cenas do Grok (media/): imagem com texto escrito -> apaga com LaMa e troca a midia (guarda a original);
    video com texto -> so avisa (apagar quadro a quadro tremula)."""
    pfile, pdir = ROOT / "projects" / f"{pid}.json", ROOT / "projects" / pid
    pj = json.loads(pfile.read_text(encoding="utf-8")); rep = []; before = copy.deepcopy(pj["scenes"])
    ff = shutil.which("ffmpeg")
    for i, s in enumerate(pj["scenes"]):
        f = s.get("file") or ""
        if not f.startswith("media/"): continue
        src = pdir / f
        if src.suffix.lower() in (".mp4", ".mov", ".webm"):
            found = []
            for t in (0.5, 2.5, 4.5):
                fr = Path(tempfile.gettempdir()) / f"ocr_{pid[:10]}_{i}.png"
                subprocess.run([ff, "-v", "error", "-y", "-ss", str(t), "-i", str(src), "-frames:v", "1", str(fr)])
                if fr.is_file(): found += [x[1] for x in ocr(Image.open(fr))]
            if found: rep.append({"scene": i + 1, "video": True, "text": sorted(set(found))})
            continue
        img = Image.open(src)
        if not ocr(img): continue  # so mexe se houver texto legivel de verdade
        boxes = ocr(img, min_score=0.2, min_len=1)
        out = inpaint(img, text_mask(img, boxes))
        rep.append({"scene": i + 1, "text": [b[1] for b in boxes]})
        if dry:
            Path(dry).mkdir(parents=True, exist_ok=True)
            w = img.width // 2; both = Image.new("RGB", (w * 2, img.height // 2))
            both.paste(img.convert("RGB").resize((w, img.height // 2)), (0, 0)); both.paste(out.resize((w, img.height // 2)), (w, 0))
            both.save(Path(dry) / f"clean-{i+1:02d}.jpg", quality=88)
        else:
            dst = src.with_name(src.stem + "-clean.jpg"); out.save(dst, quality=94)
            s.setdefault("orig_file", f); s["file"] = dst.relative_to(pdir).as_posix(); s["cleaned_text"] = [b[1] for b in boxes]
    if not dry:
        projfile.patch(pfile, projfile.changed(before, pj["scenes"], ("orig_file", "file", "cleaned_text")), top={"text_clean": rep})
    return rep


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); sp = ap.add_subparsers(dest="cmd", required=True)
    c = sp.add_parser("clean"); c.add_argument("project"); c.add_argument("--dry")
    a = ap.parse_args()
    if a.cmd == "clean":
        for r in clean_project(a.project, a.dry): print(json.dumps(r, ensure_ascii=False))
