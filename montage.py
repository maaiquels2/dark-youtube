# -*- coding: utf-8 -*-
"""Dark Studio - Montagem: narracao (OpenAI TTS) + ffmpeg -> output/final.mp4 + final.srt

Uso: python montage.py <project_id> [--step tts|render|all] [--force-tts]
Status: projects/<id>/logs/montage.json   Controle: logs/montage_control.txt (stop)
"""
import argparse, json, math, os, re, shutil, subprocess, sys, threading, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECTS = ROOT / "projects"
CFG_F = ROOT / "config" / "montage.json"
DEFAULTS = {
    "tts_model": "gpt-4o-mini-tts",
    "voice": "onyx",
    "instructions": ("Deep, calm, authoritative male documentary narrator. Measured pace, clear diction, "
                     "subtle gravitas and suspense; never theatrical or salesy. Natural pauses at commas and periods."),
    "tts_price_per_min_usd": 0.015,
    "pad_seconds": 0.3,
    "crossfade_seconds": 0.5,
    "fps": 30,
    "ken_burns_zoom": 0.12,
    "music_volume": 0.12,
    "loudness_lufs": -14,
    "burn_subtitles": False,
    "crf": 20,
    "preset": "medium",
    "parallel_clips": 3,
}


def cfg():
    c = dict(DEFAULTS)
    if CFG_F.is_file():
        try:
            c.update(json.loads(CFG_F.read_text(encoding="utf-8")))
        except Exception:
            pass
    return c


def env_key():
    if os.environ.get("OPENAI_API_KEY"):
        return os.environ["OPENAI_API_KEY"]
    f = ROOT / ".env"
    if f.is_file():
        for line in f.read_text(encoding="utf-8").splitlines():
            if line.strip().startswith("OPENAI_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def which(name):
    p = shutil.which(name)
    if p:
        return p
    for cand in (ROOT / "tools").glob(f"**/{name}.exe"):
        return str(cand)
    raise RuntimeError(f"{name} nao encontrado. Instale com: winget install Gyan.FFmpeg")


FFMPEG, FFPROBE = None, None


def ff(args, **kw):
    r = subprocess.run([FFMPEG, "-hide_banner", "-nostdin", "-y"] + args, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", **kw)
    if r.returncode != 0:
        raise RuntimeError("ffmpeg falhou: " + r.stderr[-1500:])
    return r


def probe_dur(p):
    r = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                       capture_output=True, text=True)
    return float(r.stdout.strip() or 0)


class Job:
    def __init__(self, pid):
        self.pid = Path(pid).name
        self.pfile = PROJECTS / f"{self.pid}.json"
        self.pdir = PROJECTS / self.pid
        for d in ("audio", "output", "logs", "work"):
            (self.pdir / d).mkdir(parents=True, exist_ok=True)
        self.status_f = self.pdir / "logs" / "montage.json"
        self.ctrl_f = self.pdir / "logs" / "montage_control.txt"
        self.log_f = self.pdir / "logs" / "montage.log"
        self.c = cfg()
        self.st = {"state": "starting", "step": "", "progress": 0, "message": "", "pid": os.getpid(),
                   "started_at": time.strftime("%H:%M:%S")}
        self.lock = threading.Lock()

    def log(self, m):
        line = f"{time.strftime('%Y-%m-%d %H:%M:%S')} {m}"
        print(line, flush=True)
        with open(self.log_f, "a", encoding="utf-8") as f:
            f.write(line + "\n")

    def save(self, **kw):
        with self.lock:
            self.st.update(kw); self.st["updated_at"] = time.strftime("%H:%M:%S")
            tmp = self.status_f.with_suffix(".tmp")
            tmp.write_text(json.dumps(self.st, ensure_ascii=False, indent=1), encoding="utf-8")
            os.replace(tmp, self.status_f)

    def check_stop(self):
        try:
            if self.ctrl_f.read_text(encoding="utf-8").strip() == "stop":
                raise KeyboardInterrupt("parado")
        except OSError:
            pass

    def scenes(self):
        return json.loads(self.pfile.read_text(encoding="utf-8"))["scenes"]

    # ---------------- TTS ----------------
    def tts_one(self, i, text, key, force):
        out = self.pdir / "audio" / f"scene-{i+1:02d}.mp3"
        if out.is_file() and out.stat().st_size > 1000 and not force:
            return out
        body = {"model": self.c["tts_model"], "voice": self.c["voice"], "input": text, "response_format": "mp3"}
        if not self.c["tts_model"].startswith("tts-1"):
            body["instructions"] = self.c["instructions"]
        last = None
        for attempt in range(4):
            self.check_stop()
            req = urllib.request.Request("https://api.openai.com/v1/audio/speech", data=json.dumps(body).encode(),
                                         headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
            try:
                with urllib.request.urlopen(req, timeout=120) as r:
                    data = r.read()
                out.write_bytes(data)
                return out
            except urllib.error.HTTPError as e:
                msg = e.read().decode("utf-8", "replace")[:300]
                last = f"HTTP {e.code}: {msg}"
                if e.code in (400, 401, 403, 404):
                    break
            except Exception as e:
                last = str(e)
            time.sleep(2 + attempt * 3)
        raise RuntimeError(f"TTS cena {i+1}: {last}")

    def run_tts(self, force=False):
        key = env_key()
        if not key:
            raise RuntimeError("OPENAI_API_KEY nao configurada no .env")
        sc = self.scenes()
        chars = sum(len(s.get("narration") or "") for s in sc)
        self.save(state="running", step="narracao", progress=0, total=len(sc), chars=chars,
                  message=f"Gerando narracao ({self.c['tts_model']}, voz {self.c['voice']})")
        done = [0]
        def work(i):
            self.tts_one(i, (sc[i].get("narration") or "").strip() or "...", key, force)
            with self.lock:
                done[0] += 1
            self.save(progress=round(done[0] / len(sc) * 100))
        with ThreadPoolExecutor(4) as ex:
            list(ex.map(work, range(len(sc))))
        total = sum(probe_dur(self.pdir / "audio" / f"scene-{i+1:02d}.mp3") for i in range(len(sc)))
        est = total / 60 * self.c["tts_price_per_min_usd"]
        self.save(audio_seconds=round(total, 1), tts_cost_estimate_usd=round(est, 3))
        self.log(f"TTS ok: {len(sc)} cenas, {chars} chars, {total/60:.2f} min, ~US$ {est:.3f}")

    # ---------------- render ----------------
    def cropdetect(self, src, is_video):
        """Detecta barras pretas (letterbox) em cima/embaixo. cropdetect do ffmpeg erra em imagens escuras,
        entao analisamos as linhas: barra = linha quase toda preta (p98 do brilho muito baixo)."""
        r2 = subprocess.run([FFPROBE, "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                             "-of", "csv=p=0", str(src)], capture_output=True, text=True)
        W, H = map(int, r2.stdout.strip().split(",")[:2])
        w, h = 320, max(2, round(320 * H / W))
        args = (["-ss", "1"] if is_video else []) + ["-i", str(src), "-frames:v", "1", "-vf", f"scale={w}:{h}:flags=area,format=gray",
                "-f", "rawvideo", "-"]
        raw = subprocess.run([FFMPEG, "-hide_banner", "-nostdin", "-v", "error"] + args, capture_output=True).stdout
        if len(raw) < w * h:
            return None
        def is_bar(y):
            row = sorted(raw[y * w:(y + 1) * w])
            return row[int(w * 0.98)] <= 22
        top = 0
        while top < h // 3 and is_bar(top):
            top += 1
        bot = 0
        while bot < h // 3 and is_bar(h - 1 - bot):
            bot += 1
        if top + bot < h * 0.03 or min(top, bot) < 0.6 * max(top, bot):  # letterbox e simetrico
            return None
        y0 = math.ceil((top + 1) * H / h)          # margem de 1 linha para nao sobrar borda
        y1 = H - math.ceil((bot + 1) * H / h) if bot else H
        ch = (y1 - y0) // 2 * 2
        if ch < H * 0.55:
            return None
        return W, ch, 0, y0

    def render_clip(self, i, sc, D, L):
        fps = self.c["fps"]
        src = self.pdir / sc["file"]
        out = self.pdir / "work" / f"clip-{i+1:02d}.mp4"
        is_video = src.suffix.lower() in (".mp4", ".mov", ".webm")
        crop = self.cropdetect(src, is_video)
        cf = f"crop={crop[0]}:{crop[1]}:{crop[2]}:{crop[3]}," if crop else ""
        # preenche 16:9: escala para cobrir e corta o centro
        fill = "scale=1920:1080:force_original_aspect_ratio=increase:flags=lanczos,crop=1920:1080,setsar=1"
        enc = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", "-an", "-r", str(fps)]
        if is_video:
            sd = probe_dur(src) or L
            speed = 1.0
            if sd < L:
                speed = min(L / sd, 1.5)          # slow-mo ate 1.5x
            vf = f"{cf}{fill},setpts={speed:.4f}*PTS,fps={fps}"
            rem = L - sd * speed
            if rem > 0.05:
                vf += f",tpad=stop_mode=clone:stop_duration={rem + 0.2:.3f}"
            ff(["-i", str(src), "-vf", vf, "-t", f"{L:.3f}"] + enc + [str(out)])
            return out, crop, f"video x{speed:.2f}"
        frames = int(math.ceil(L * fps))
        z = self.c["ken_burns_zoom"]
        k = i % 4
        # 4 movimentos: zoom in, zoom out, pan esq->dir, pan dir->esq (com leve zoom)
        if k == 0:
            zexp, xexp, yexp = f"1+{z}*on/{frames}", "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"
        elif k == 1:
            zexp, xexp, yexp = f"1+{z}-{z}*on/{frames}", "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"
        elif k == 2:
            zexp, xexp, yexp = f"{1+z*0.8}", f"(iw-iw/zoom)*on/{frames}", "ih/2-(ih/zoom/2)"
        else:
            zexp, xexp, yexp = f"{1+z*0.8}", f"(iw-iw/zoom)*(1-on/{frames})", "ih/2-(ih/zoom/2)"
        vf = (f"{cf}scale=3840:2160:force_original_aspect_ratio=increase:flags=lanczos,crop=3840:2160,"
              f"zoompan=z='{zexp}':x='{xexp}':y='{yexp}':d={frames}:s=1920x1080:fps={fps},setsar=1")
        ff(["-i", str(src), "-vf", vf, "-frames:v", str(frames)] + enc + [str(out)])
        return out, crop, f"imagem kb{k}"

    def srt(self, sc, starts, durs):
        def ts(t):
            ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
            return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
        out, n = [], 1
        for s, t0, d in zip(sc, starts, durs):
            text = re.sub(r"\s+", " ", s.get("narration") or "").strip()
            if not text:
                continue
            parts = [p.strip() for p in re.split(r"(?<=[.!?;])\s+", text) if p.strip()]
            chunks = []
            for p in parts:  # quebra frases longas em ~84 chars
                words, cur = p.split(), ""
                for w in words:
                    if len(cur) + len(w) + 1 > 84 and cur:
                        chunks.append(cur); cur = w
                    else:
                        cur = (cur + " " + w).strip()
                if cur:
                    chunks.append(cur)
            speak = max(0.5, d - self.c["pad_seconds"])
            tot = sum(len(c) for c in chunks) or 1
            t = t0
            for c in chunks:
                dd = speak * len(c) / tot
                line = c if len(c) <= 42 else self._two_lines(c)
                out.append(f"{n}\n{ts(t)} --> {ts(t + dd - 0.05)}\n{line}\n"); n += 1
                t += dd
        return "\n".join(out)

    @staticmethod
    def _two_lines(c):
        mid = len(c) // 2
        sp = min((k for k in range(len(c)) if c[k] == " "), key=lambda k: abs(k - mid), default=mid)
        return c[:sp].strip() + "\n" + c[sp:].strip()

    def run_render(self):
        sc = self.scenes()
        missing = [i + 1 for i, s in enumerate(sc) if not s.get("file") or not (self.pdir / s["file"]).is_file()]
        if missing:
            raise RuntimeError(f"Cenas sem midia: {missing[:10]}")
        amiss = [i + 1 for i in range(len(sc)) if not (self.pdir / "audio" / f"scene-{i+1:02d}.mp3").is_file()]
        if amiss:
            raise RuntimeError(f"Cenas sem narracao: {amiss[:10]} (gere a narracao primeiro)")
        pad, XF, fps = self.c["pad_seconds"], self.c["crossfade_seconds"], self.c["fps"]
        adurs = [probe_dur(self.pdir / "audio" / f"scene-{i+1:02d}.mp3") for i in range(len(sc))]
        D = [round(a + pad, 3) for a in adurs]
        L = [d + (XF if k < len(D) - 1 else 0) for k, d in enumerate(D)]
        starts = [sum(D[:k]) for k in range(len(D))]
        total = sum(D)
        self.save(state="running", step="clipes", progress=0, total=len(sc), message="Renderizando clipes (Ken Burns / ajuste de video)",
                  duration_seconds=round(total, 1))
        t0 = time.time(); done = [0]; info = {}
        def work(k):
            self.check_stop()
            out, crop, how = self.render_clip(k, sc[k], D[k], L[k])
            info[k] = {"crop": crop, "how": how}
            with self.lock:
                done[0] += 1
            self.save(progress=round(done[0] / len(sc) * 100))
            return out
        with ThreadPoolExecutor(int(self.c["parallel_clips"])) as ex:
            clips = list(ex.map(work, range(len(sc))))
        self.log(f"clipes ok em {time.time()-t0:.0f}s; barras cortadas em {sum(1 for v in info.values() if v['crop'])} cenas")

        # narracao continua: cada cena preenchida ate D (alinha com o video)
        self.save(step="audio", progress=0, message="Montando narracao")
        alist = self.pdir / "work" / "narr.txt"
        parts = []
        for k in range(len(sc)):
            pa = self.pdir / "work" / f"a-{k+1:02d}.wav"
            ff(["-i", str(self.pdir / "audio" / f"scene-{k+1:02d}.mp3"), "-af", f"apad=whole_dur={D[k]:.3f}",
                "-t", f"{D[k]:.3f}", "-ar", "48000", "-ac", "2", str(pa)])
            parts.append(f"file '{pa.as_posix()}'")
        alist.write_text("\n".join(parts), encoding="utf-8")
        narr = self.pdir / "work" / "narration.wav"
        ff(["-f", "concat", "-safe", "0", "-i", str(alist), "-c", "copy", str(narr)])

        # junta clipes com crossfade, em blocos (evita grafo gigante)
        self.save(step="juncao", progress=0, message="Juntando cenas com crossfade")
        def xjoin(paths, lens, out):
            inp, fl, off, prev = [], [], 0.0, "0:v"
            for p in paths:
                inp += ["-i", str(p)]
            for k in range(1, len(paths)):
                off += lens[k - 1] - XF
                lab = f"v{k}"
                fl.append(f"[{prev}][{k}:v]xfade=transition=fade:duration={XF}:offset={off:.3f}[{lab}]")
                prev = lab
            if len(paths) == 1:
                shutil.copy(paths[0], out); return lens[0]
            ff(inp + ["-filter_complex", ";".join(fl), "-map", f"[{prev}]", "-c:v", "libx264", "-preset", "veryfast",
                      "-crf", "16", "-pix_fmt", "yuv420p", "-r", str(fps), str(out)])
            return off + lens[-1]
        B = 12
        blocks, blens = [], []
        for b in range(0, len(clips), B):
            ps, ls = clips[b:b + B], L[b:b + B]
            o = self.pdir / "work" / f"block-{b//B:02d}.mp4"
            bl = xjoin(ps, ls, o)
            # bloco termina com o overlap XF do ultimo clipe (exceto o ultimo bloco)
            blocks.append(o); blens.append(bl)
            self.save(progress=round((b + B) / len(clips) * 100))
            self.check_stop()
        video = self.pdir / "work" / "video.mp4"
        xjoin(blocks, blens, video)

        # audio final: narracao (+ musica opcional) + loudnorm
        self.save(step="final", progress=0, message="Mixando audio e codificando final.mp4")
        music = next((p for p in sorted(self.pdir.glob("music.*")) if p.suffix.lower() in (".mp3", ".wav", ".m4a", ".ogg")), None)
        srt_path = self.pdir / "output" / "final.srt"
        srt_path.write_text(self.srt(sc, starts, D), encoding="utf-8")
        out = self.pdir / "output" / "final.mp4"
        args = ["-i", str(video), "-i", str(narr)]
        lufs = self.c["loudness_lufs"]
        if music:
            args += ["-stream_loop", "-1", "-i", str(music)]
            af = (f"[2:a]volume={self.c['music_volume']},atrim=0:{total:.3f}[m];"
                  f"[1:a][m]amix=inputs=2:duration=first:normalize=0,loudnorm=I={lufs}:TP=-1.5:LRA=11[a]")
        else:
            af = f"[1:a]loudnorm=I={lufs}:TP=-1.5:LRA=11[a]"
        vf = "[0:v]null[v]"
        if self.c.get("burn_subtitles"):
            sp = srt_path.as_posix().replace(":", "\\:")
            vf = f"[0:v]subtitles='{sp}':force_style='FontName=Arial,FontSize=22,Outline=2,MarginV=40'[v]"
        ff(args + ["-filter_complex", vf + ";" + af, "-map", "[v]", "-map", "[a]", "-t", f"{total:.3f}",
                   "-c:v", "libx264", "-preset", self.c["preset"], "-crf", str(self.c["crf"]), "-pix_fmt", "yuv420p",
                   "-r", str(fps), "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", str(out)])
        el = time.time() - t0
        self.save(render_seconds=round(el), music=bool(music), output="output/final.mp4", srt="output/final.srt")
        self.log(f"final.mp4 ok: {probe_dur(out):.1f}s, render {el:.0f}s, musica={'sim' if music else 'nao'}")


def main():
    global FFMPEG, FFPROBE
    ap = argparse.ArgumentParser()
    ap.add_argument("project"); ap.add_argument("--step", default="all", choices=["tts", "render", "all"])
    ap.add_argument("--force-tts", action="store_true")
    a = ap.parse_args()
    j = Job(a.project)
    try:
        j.ctrl_f.write_text("run", encoding="utf-8")
        FFMPEG, FFPROBE = which("ffmpeg"), which("ffprobe")
        t0 = time.time()
        if a.step in ("tts", "all"):
            j.run_tts(a.force_tts)
        if a.step in ("render", "all"):
            j.run_render()
        j.save(state="done", progress=100, step="", message=f"Concluido em {time.time()-t0:.0f}s")
    except KeyboardInterrupt:
        j.save(state="stopped", message="Parado pelo usuario.")
    except Exception as e:
        import traceback
        j.log("ERRO: " + traceback.format_exc())
        j.save(state="error", message=str(e)[:500])
        sys.exit(1)


if __name__ == "__main__":
    main()
