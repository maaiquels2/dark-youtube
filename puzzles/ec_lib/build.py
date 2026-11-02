"""Monta um video do EffectCraft a partir de <projeto>/scenes.json + <projeto>/assets/timing_raw.json (voz Kokoro).

Uso (da raiz do repo):
  python puzzles/ec_lib/build.py <projeto>                      # so monta o .ecproj (confere se o JSON esta certo)
  python puzzles/ec_lib/build.py <projeto> --frames             # + 1 quadro a cada 1.5 s -> ec_build/sheet.png
  python puzzles/ec_lib/build.py <projeto> --frames 1,7.5,20    # + quadros nesses segundos
  (longo, > 15 blocos: --frames sem lista = 2 quadros por bloco, uma folha por parte -> ec_build/sheet_partNN.png;
   --frames part3 = 1 quadro por segundo so da parte 3)
  python puzzles/ec_lib/build.py <projeto> --render             # + video (~12 min por minuto) + mixagem -> renders/<out>.mp4
                                                                #   (mais de uma parte: renderiza parte a parte, retoma de onde parou e junta)
  python puzzles/ec_lib/build.py <projeto> --render --part 3    # so a parte 3 (outra janela pode fazer outra parte)
  python puzzles/ec_lib/build.py <projeto> --mix                # so refaz a mixagem (usa o video ja renderizado)
  python puzzles/ec_lib/build.py <projeto> --sheet video.mp4    # folha de contato de um video a 2 quadros/s
Tudo que e gerado fica em <projeto>/ec_build/; o video final em <projeto>/renders/.
"""
import hashlib, json, re, subprocess, sys, time, wave
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

LIB = Path(__file__).parent
ROOT = LIB.parents[1]
CLI = Path.home() / "AppData/Local/DarkStudio/effectcraft/effectcraft-cli.exe"
SR = 48000


def clip_boxes(P):
    """caixa da manchete de cada print (assets/clips/<nome>.json, campo box): o web_clip corta nela quando nao ha crop"""
    out = {}
    for f in (P / "assets" / "clips").glob("*.json"):
        box = json.loads(f.read_text(encoding="utf-8")).get("box")
        if box: out[f.stem + ".png"] = box
    return out

US_CODES = dict(zip("Alabama Alaska Arizona Arkansas California Colorado Connecticut Delaware District_of_Columbia Florida Georgia Hawaii Idaho "
    "Illinois Indiana Iowa Kansas Kentucky Louisiana Maine Maryland Massachusetts Michigan Minnesota Mississippi Missouri Montana Nebraska Nevada "
    "New_Hampshire New_Jersey New_Mexico New_York North_Carolina North_Dakota Ohio Oklahoma Oregon Pennsylvania Rhode_Island South_Carolina "
    "South_Dakota Tennessee Texas Utah Vermont Virginia Washington West_Virginia Wisconsin Wyoming".replace("_", "~").split(),
    "AL AK AZ AR CA CO CT DE DC FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY".split()))


def us_states():
    """Estados dos EUA projetados (Albers, Alasca a 35% e Havai em encarte embaixo a esquerda, como no padrao do Census),
    simplificados, largura 1000, y para baixo. Fonte: library/maps/us-states.json (fronteiras do US Census, dominio publico).
    Gerado uma vez em puzzles/ec_lib/assets/us_states.json: {"w", "h", "s": {UF: {"p": [aneis], "c": [x, y] (centro do maior anel)}}}"""
    out = LIB / "assets" / "us_states.json"
    if out.exists(): return json.loads(out.read_text(encoding="utf-8"))
    src = json.loads((ROOT / "library/maps/us-states.json").read_text(encoding="utf-8"))
    def conic(p1, p2, lat0, lon0):
        p1, p2, lat0 = np.radians(p1), np.radians(p2), np.radians(lat0); n = (np.sin(p1) + np.sin(p2)) / 2
        C = np.cos(p1) ** 2 + 2 * n * np.sin(p1); r0 = np.sqrt(C - 2 * n * np.sin(lat0)) / n
        def f(ll):
            lam, phi = np.radians(ll[:, 0] - lon0), np.radians(ll[:, 1]); r = np.sqrt(C - 2 * n * np.sin(phi)) / n
            return np.stack([r * np.sin(n * lam), -(r0 - r * np.cos(n * lam))], 1)
        return f
    proj = {"AK": conic(55, 65, 58.5, -154), "HI": conic(8, 18, 20, -157)}; main = conic(29.5, 45.5, 37.5, -96)
    def rdp(p, eps):  # Douglas-Peucker
        if len(p) < 4: return p
        a, b = p[0], p[-1]; u, v = b - a, p - a
        if np.allclose(a, b):  # anel fechado: corta no ponto mais longe do inicio
            i = int(np.argmax(np.hypot(v[:, 0], v[:, 1]))); return np.vstack([rdp(p[:i + 1], eps)[:-1], rdp(p[i:], eps)])
        d = np.abs(u[0] * v[:, 1] - u[1] * v[:, 0]) / np.hypot(u[0], u[1]); i = int(np.argmax(d))
        return np.vstack([rdp(p[:i + 1], eps)[:-1], rdp(p[i:], eps)]) if d[i] > eps else np.array([a, b])
    rings = {}
    for f in src["features"]:
        uf = US_CODES.get(f["properties"]["name"].replace(" ", "~"))
        if not uf: continue  # Porto Rico fica fora, como no mapa padrao
        g = f["geometry"]; polys = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
        rings[uf] = [proj.get(uf, main)(np.array(pl[0], float)) for pl in polys]  # so o contorno externo
    allp = np.vstack([r for uf, rs in rings.items() if uf not in proj for r in rs])
    lo, hi = allp.min(0), allp.max(0); k = 1000 / (hi[0] - lo[0])
    def place(uf, scale, x, ybot):  # encarte: canto inferior esquerdo em (x, ybot), unidades finais
        q = np.vstack(rings[uf]); qlo, qhi = q.min(0), q.max(0)
        rings[uf] = [(r - [qlo[0], qhi[1]]) * scale * k / k + [x / k + lo[0], ybot / k + lo[1]] for r in rings[uf]]
    H0 = (hi[1] - lo[1]) * k
    place("AK", 0.35, 0, H0); ak = np.vstack(rings["AK"]); place("HI", 1.0, (ak.max(0)[0] - lo[0]) * k + 20, H0)
    S = {}
    for uf, rs in rings.items():
        ps = []
        for r in rs:
            r = (r - lo) * k; ar = 0.5 * abs(np.dot(r[:-1, 0], r[1:, 1]) - np.dot(r[1:, 0], r[:-1, 1]))
            if ar < 3 and ps: continue  # ilhota
            s = rdp(r, 0.6); ps.append((ar, s))
        ps.sort(key=lambda t: -t[0]); big = ps[0][1]
        x, y = big[:, 0], big[:, 1]; cr = x[:-1] * y[1:] - x[1:] * y[:-1]; A = cr.sum() / 2
        c = [float(((x[:-1] + x[1:]) * cr).sum() / (6 * A)), float(((y[:-1] + y[1:]) * cr).sum() / (6 * A))]
        S[uf] = {"p": [np.round(s[:-1] if np.allclose(s[0], s[-1]) else s, 1).tolist() for _, s in ps], "c": np.round(c, 1).tolist()}
    allq = np.vstack([np.array(p) for v in S.values() for p in v["p"]])
    res = {"w": round(float(allq[:, 0].max()), 1), "h": round(float(allq[:, 1].max()), 1), "s": S}
    out.parent.mkdir(exist_ok=True); out.write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8")
    return res


def spec_checks(spec):
    """Avisos que nao param o build: mapa com vermelho e verde juntos (regra do canal: uma cor por grafico)."""
    for bi, blk in enumerate(spec["blocks"]):
        for sc in blk["scenes"]:
            if sc.get("t") == "us_map":
                tones = {s.get("tone", "neutral") for s in sc.get("states", [])}
                if {"scam", "rule"} <= tones: print(f"AVISO bloco {bi} (us_map): scam e rule no mesmo mapa; a regra do canal e uma cor por grafico")


def load_words(raw):
    """Palavras da voz; pontuacao gruda na palavra anterior."""
    words = []
    for w in raw["words"]:
        t = w["w"]
        if not any(c.isalnum() for c in t):
            if words: words[-1]["w"] += t; words[-1]["e"] = max(words[-1]["e"], w["e"])
            continue
        words.append({"w": t, "s": round(w["s"], 3), "e": round(w["e"], 3)})
    return words


def captions(words, n=3):
    """Legendas de ate n palavras (3 no vertical, 5 no horizontal); quebra em pontuacao ou pausa."""
    chunks, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        nxt = words[i + 1] if i + 1 < len(words) else None
        if len(cur) == n or w["w"][-1] in ".,:;!?" or not nxt or nxt["s"] - w["e"] > 0.35:
            chunks.append({"t": " ".join(x["w"] for x in cur).upper(), "s": cur[0]["s"],
                           "e": nxt["s"] if nxt and nxt["s"] - cur[-1]["e"] < 0.6 else cur[-1]["e"] + 0.25})
            cur = []
    assert all(c["e"] > c["s"] for c in chunks), "legenda com duracao zero"
    return chunks


def cli(*a, cwd):
    r = subprocess.run([str(CLI), *a], cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = (r.stdout + r.stderr).strip()
    if r.returncode: sys.exit(out)
    return out


# ---------------- efeitos sonoros sintetizados ----------------
rng = np.random.default_rng(1)
def env(n, a, d): t = np.arange(n) / SR; return np.minimum(t / a, 1) * np.exp(-t / d)
def boom(d=3.0, **_):
    n = int(d * SR); t = np.arange(n) / SR
    f = 30 + 70 * np.exp(-t * 3); s = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.005, 0.9)
    no = np.convolve(rng.standard_normal(n), np.ones(60) / 60, "same") * env(n, 0.002, 0.35)
    return s * 0.9 + no * 1.6
def whoosh(d=0.8, up=False, **_):
    n = int(d * SR); t = np.arange(n) / SR
    no = rng.standard_normal(n); k = 8 + 40 * (t / d if up else 1 - t / d)
    out = np.zeros(n); y = 0.0
    for i in range(n): y += (no[i] - y) / k[i]; out[i] = y  # passa-baixa que varre
    shape = np.sin(np.pi * t / d) ** (0.6 if up else 1.5)
    if up: shape *= (t / d) ** 2 + 0.1
    return out * shape * 3
def rise(d=1.0, **_): return whoosh(d, up=True)
def chime(d=2.5, f=880, **_):
    n = int(d * SR); t = np.arange(n) / SR
    return sum(np.sin(2 * np.pi * f * m * t) / m for m in (1, 2.01, 3.02)) * env(n, 0.004, 0.7) * 0.25
def thud(d=1.2, **_): n = int(d * SR); t = np.arange(n) / SR; return np.sin(2 * np.pi * (55 + 40 * np.exp(-t * 8)) * t) * env(n, 0.003, 0.25)
SFX = {"boom": boom, "whoosh": whoosh, "rise": rise, "chime": chime, "thud": thud}


def mix(P, B, spec, events, dur):
    sfx = np.zeros(int((dur + 1) * SR))
    for e in events:
        s = SFX[e["k"]](**{k: v for k, v in e.items() if k in ("d", "f")})
        i = int(max(0, e["t"]) * SR); s = s[: len(sfx) - i]
        sfx[i:i + len(s)] += s / (np.abs(s).max() + 1e-9) * e["g"]
    st = np.stack([np.clip(sfx * 0.5, -1, 1)] * 2, 1)
    with wave.open(str(B / "sfx.wav"), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype("<i2").tobytes())
    music = ROOT / spec.get("music", "library/music/incompetech/echoes-of-time-v2.mp3")
    out = P / "renders" / f"{spec['out']}.mp4"; out.parent.mkdir(exist_ok=True)
    # a trilha repete se o video for mais longo que ela (video longo de 10 min)
    # voz comprimida: silabas fortes da Kokoro saltavam 8-9 dB acima do resto
    fc = (f"[1:a]aresample={SR},acompressor=threshold=0.05:ratio=6:attack=2:release=100:makeup=3,asplit=2[v][vk];"
          f"[2:a]atrim=0:{dur:.2f},afade=t=in:d=1.5,afade=t=out:st={dur - 2.5:.2f}:d=2.5,volume={spec.get('music_gain', 0.22)}[m];"
          f"[m][vk]sidechaincompress=threshold=0.05:ratio=4:attack=20:release=400[md];"
          # efeitos bem abaixo da voz e limitados: antes passavam a voz em ate 10 dB
          f"[3:a]volume={spec.get('sfx_gain', 0.18)},alimiter=limit=0.08:attack=2:release=80:level=false[s];"
          f"[v][md][s]amix=inputs=3:normalize=0,loudnorm=I={spec.get('lufs', -16)}:TP=-1.5:LRA=7,alimiter=limit=0.84:attack=3:release=60:level=false[a]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(B / "visual.mp4"), "-i", str(P / "assets" / "voice.wav"),
                    "-stream_loop", "-1", "-i", str(music), "-i", str(B / "sfx.wav"), "-filter_complex", fc, "-map", "0:v", "-map", "[a]",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", str(out)], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(out), "-c:v", "libx264", "-crf", "25", "-preset", "slow",
                    "-c:a", "copy", str(out.with_name(out.stem + "_share.mp4"))], check=True)
    print("video:", out, f"| {len(events)} efeitos sonoros")


def sheet(pngs, labels, dest, cols=8):
    ims = [Image.open(p).convert("RGB") for p in pngs]
    w, h = ims[0].size; rows = -(-len(ims) // cols)
    S = Image.new("RGB", (cols * w, rows * h)); d = ImageDraw.Draw(S)
    font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 22)
    for i, (im, lb) in enumerate(zip(ims, labels)):
        x, y = i % cols * w, i // cols * h; S.paste(im.resize((w, h)), (x, y)); d.text((x + 6, y + 4), lb, fill="yellow", font=font)
    S.save(dest); print("folha:", dest)


def video_sheet(video, dest, fps=2):
    tmp = Path(dest).with_suffix(""); tmp.mkdir(parents=True, exist_ok=True)
    for f in tmp.glob("*.png"): f.unlink()
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(video), "-vf", f"fps={fps},scale=-2:320", str(tmp / "%04d.png")], check=True)
    pngs = sorted(tmp.glob("*.png"))
    sheet(pngs, [f"{i / fps:.1f}" for i in range(len(pngs))], dest, cols=16)


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # o CLI imprime "→"; cp1252 quebrava o print
    a = sys.argv[1:]
    if not a or a[0].startswith("-"): sys.exit(__doc__)
    P = Path(a[0]).resolve(); B = P / "ec_build"; B.mkdir(exist_ok=True)
    if "--sheet" in a:
        v = Path(a[a.index("--sheet") + 1]); return video_sheet(v, B / f"sheet_{v.stem}.png")
    spec = json.loads((P / "scenes.json").read_text(encoding="utf-8"))
    raw = json.loads((P / "assets" / "timing_raw.json").read_text(encoding="utf-8"))
    words = load_words(raw)
    vend = max(w["e"] for w in words)
    blocks = raw["blocks"] + [round(vend + 0.3, 3)]
    if len(spec["blocks"]) != len(raw["blocks"]):
        sys.exit(f"scenes.json tem {len(spec['blocks'])} blocos, a voz tem {len(raw['blocks'])}")
    dur = round(vend + spec.get("tail", 3.0), 2)
    comp = spec.get("comp", "main")
    hz = spec.get("format", "vertical") == "horizontal"
    parts, starts = split_parts(spec, blocks, dur)
    head = (f"var PART_STARTS={json.dumps(starts)};\nvar WORDS={json.dumps(words)};\nvar BLOCKS={json.dumps(blocks)};\nvar DUR={dur};\nvar VEND={vend};\n"
            f"var CHUNKS={json.dumps(captions(words, spec.get('caption_words', 5 if hz else 3)))};\nvar IMG={json.dumps((P / 'assets' / 'img').as_posix())};\n"
            f"var SPEC={json.dumps(spec)};\nvar CLIPS={json.dumps(clip_boxes(P))};\n")
    if '"us_map"' in json.dumps(spec): head += f"var USMAP={json.dumps(us_states(), separators=(',', ':'))};\n"  # so quem usa o mapa
    spec_checks(spec)
    jsx = head + (LIB / "ec_lib.jsx").read_text(encoding="utf-8") + "\nbuildVideo();\n"
    # script igual ao da ultima montagem: reaproveita o projeto (e as partes ja renderizadas)
    same = (B / "video.jsx").exists() and (B / "video.jsx").read_text(encoding="utf-8") == jsx and (B / "video.ecproj").exists() and (B / "events.json").exists()
    (B / "video.jsx").write_text(jsx, encoding="utf-8")

    if "--mix" not in a and not same:
        t0 = time.time()
        out = cli("script", "video.jsx", "--empty", "--save-as", "video.ecproj", cwd=B)
        ev = next(l for l in out.splitlines() if l.startswith("EVENTS="))[7:]
        (B / "events.json").write_text(ev, encoding="utf-8")
        for l in out.splitlines():
            if l.startswith("AVISO"): print(l)
        ok = next((l for l in out.splitlines() if l.startswith("ok layers=")), "")
        print(out.splitlines()[-1], f"| {ok} | dur {dur}s | {len(parts)} parte(s) | montagem {time.time() - t0:.0f}s")
    elif same: print(f"scenes.json e biblioteca sem mudanca: video.ecproj reaproveitado | {len(parts)} parte(s)")
    events = json.loads((B / "events.json").read_text(encoding="utf-8"))

    if "--frames" in a:
        i = a.index("--frames")
        arg = a[i + 1] if i + 1 < len(a) and not a[i + 1].startswith("-") else None
        if arg and arg.startswith("part"):  # --frames part3: 1 quadro por segundo so dessa parte
            k = int(arg[4:]); s, e = parts[k - 1]
            frames(B, comp, [f"{t:.2f}" for t in np.arange(s + 0.5, e, 1.0)], B / f"sheet_part{k:02d}.png", hz)
        elif arg:
            frames(B, comp, arg.split(","), B / "sheet.png", hz)
        elif len(spec["blocks"]) <= 15:  # Short: 1 quadro a cada 1.5 s (como sempre)
            frames(B, comp, [f"{t:.2f}" for t in np.arange(0.5, dur, 1.5)], B / "sheet.png", hz)
        else:  # longo: 2 quadros por bloco (35% e 80% do bloco), uma folha por parte
            for k, (s, e) in enumerate(parts, 1):
                ts = [f"{blocks[j] + f * (blocks[j + 1] - blocks[j]):.2f}" for j in range(len(blocks) - 1) if s <= blocks[j] < e for f in (0.35, 0.8)]
                frames(B, comp, ts, B / f"sheet_part{k:02d}.png", hz)
    hz_parts = part_hashes(P, spec, blocks, words, (LIB / "ec_lib.jsx").read_text(encoding="utf-8"), dur, parts, hz)
    done = render_parts(B, comp, parts, a, hz_parts) if "--render" in a else False
    if done or "--mix" in a:
        mix(P, B, spec, events, dur)


FPS = 30


def split_parts(spec, blocks, dur):
    """Partes para renderizar: corta no inicio de cada bloco com chapter_card (e a cada ~150 s se nao houver capitulo).
    Os cortes caem em quadro inteiro, para juntar sem emenda. Devolve ([(inicio, fim)], [bloco que abre cada parte])."""
    cuts, last, starts = [0.0], 0.0, [0]
    for j, blk in enumerate(spec["blocks"]):
        s = blocks[j]
        if j and (any(sc.get("t") == "chapter_card" for sc in blk["scenes"]) or s - last > spec.get("part_max", 150)):
            cuts.append(round(s * FPS) / FPS); last = s; starts.append(j)
    cuts.append(dur)
    return [(cuts[i], cuts[i + 1]) for i in range(len(cuts) - 1)], starts


def part_hashes(P, spec, blocks, words, lib, dur, parts, hz):
    """Impressao digital de cada parte: o que pode mudar os quadros dela. Biblioteca, tema e cabecalho do spec valem para
    todas; blocos, palavras, legendas e imagens so os da janela da parte (com 1 s de folga, por causa das sobras de 0,3 s
    e da parte que comeca 1 s antes). Bloco novo ou duracao diferente desloca os tempos e muda o hash das seguintes.
    shortcut: cena com "until" que passa de 1 s do proprio bloco nao entra no hash da parte seguinte; se usar, rode --part N."""
    glob_ = {k: v for k, v in spec.items() if k != "blocks"}
    clips = clip_boxes(P)
    out = []
    for s, e in parts:
        a, b = s - 1.0, e + 1.0
        blk = [[blocks[j], blocks[j + 1], spec["blocks"][j]] for j in range(len(spec["blocks"])) if blocks[j] < b and blocks[j + 1] > a]
        ws = [w for w in words if a < w["s"] < b]
        cap = [c for c in captions(words, spec.get("caption_words", 5 if hz else 3)) if a < c["s"] < b]
        files = sorted(set(re.findall(r'"([^"]+\.(?:png|jpg|jpeg|webp|mp4))"', json.dumps(blk))))
        st = []
        for f in files:
            for d in ("img", "clips"):
                q = P / "assets" / d / f
                if q.exists(): st.append([d, f, q.stat().st_size, q.stat().st_mtime_ns])
        h = hashlib.sha256(json.dumps([lib, glob_, dur, round(s, 4), round(e, 4), blk, ws, cap, st, clips], sort_keys=True).encode()).hexdigest()[:16]
        out.append(h)
    return out

def frames(B, comp, ts, dest, batch=False):
    F = B / "frames"; F.mkdir(exist_ok=True)
    pngs = [F / f"f_{float(t):06.2f}.png" for t in ts]
    if batch:  # horizontal: varios quadros por processo (o projeto de um longo leva ~2 s para abrir)
        for i in range(0, len(ts), 40):
            cmds = [x for t, p in zip(ts[i:i + 40], pngs[i:i + 40]) for x in
                    ("comp.saveFrameAs", json.dumps({"comp": comp, "path": str(p), "time": float(t), "scale": 0.25}))]
            cli("run", *cmds, "--project", "video.ecproj", cwd=B)
    else:
        for t, p in zip(ts, pngs):
            cli("render-frame", "--project", "video.ecproj", "--comp", comp, "--time", t, "--max-side", "480", "--out", str(p), cwd=B)
    sheet(pngs, [f"{float(t):.2f}" for t in ts], dest)


def render_parts(B, comp, parts, a, hs):
    """Uma parte por vez; pula a parte cujo hash (part_hashes) nao mudou desde que foi renderizada (parts/hashes.json).
    --part N faz so a N. Junta com ffmpeg concat sem recodificar."""
    if len(parts) == 1:
        print(cli("render", "--project", "video.ecproj", "--comp", comp, "--out", "visual.mp4", "--format", "h264", "--audio", "off", cwd=B).splitlines()[-1])
        return True
    D = B / "parts"; D.mkdir(exist_ok=True)
    only = int(a[a.index("--part") + 1]) if "--part" in a else None
    HF = D / "hashes.json"
    old = json.loads(HF.read_text(encoding="utf-8")) if HF.exists() else {}
    if not HF.exists():  # partes de antes do hash: vale a regra antiga (mais nova que o projeto = em dia), uma vez so
        proj = (B / "video.ecproj").stat().st_mtime
        old = {f"{k:02d}": hs[k - 1] for k in range(1, len(parts) + 1) if (D / f"visual_{k:02d}.mp4").exists() and (D / f"visual_{k:02d}.mp4").stat().st_mtime > proj}
    for k, (s, e) in enumerate(parts, 1):
        f, key = D / f"visual_{k:02d}.mp4", f"{k:02d}"
        if only and k != only: continue
        if not only and f.exists() and old.get(key) == hs[k - 1]: print(f"parte {k}/{len(parts)} sem mudanca: pulada"); continue
        t0 = time.time()
        # --end e exclusivo: o ultimo quadro de uma parte e o anterior ao primeiro da seguinte
        cli("render", "--project", "video.ecproj", "--comp", comp, "--out", str(f), "--format", "h264", "--audio", "off",
            "--start", f"{s:.4f}", "--end", f"{e:.4f}", cwd=B)
        old[key] = hs[k - 1]; HF.write_text(json.dumps(old, indent=1), encoding="utf-8")
        print(f"parte {k}/{len(parts)} {s:.1f}-{e:.1f}s em {time.time() - t0:.0f}s")
    fs = [D / f"visual_{k:02d}.mp4" for k in range(1, len(parts) + 1)]
    for k in range(len(parts) + 1, 100):  # parte que sobrou de uma divisao antiga nao entra na juncao
        if not (D / f"visual_{k:02d}.mp4").exists(): break
        old.pop(f"{k:02d}", None)
    HF.write_text(json.dumps(old, indent=1), encoding="utf-8")
    if not all(f.exists() and old.get(f"{k:02d}") == hs[k - 1] for k, f in enumerate(fs, 1)):
        print("faltam partes; rode --render (sem --part) para terminar e juntar"); return False
    (D / "list.txt").write_text("".join(f"file '{f.name}'\n" for f in fs), encoding="utf-8")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(D / "list.txt"), "-c", "copy", str(B / "visual.mp4")], check=True)
    print("visual.mp4:", len(fs), "partes juntadas")
    return True


if __name__ == "__main__":
    main()
