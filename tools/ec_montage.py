# -*- coding: utf-8 -*-
"""Dark Studio - montagem com acabamento de editor (usa o montage.py sem altera-lo).
Por cima do montage.Job:
  - graficos do EffectCraft (tools/ec_gfx.py): tela cheia ja vem como midia da cena; sobreposicao gfx/ecov-NN.mov (alfa)
  - cor por ato (PADRAO_VIDEOS.md): ato 1 dourado, ato 2 azul acinzentado, ato 3 duro e dessaturado, final suave
  - vinheta e grao de filme; mergulho no preto antes de cada capitulo; flash nos numeros de impacto
  - design de som: whoosh nas entradas, impacto grave nos contadores/carimbo, tique nos marcos da linha do tempo
  - musica so onde faz sentido (pj["music_cues"]): abertura, capitulos e momentos de impacto
Uso: python tools/ec_montage.py <project_id> [--audio-only | --redo 5,46]   (a narracao ja precisa existir; nao chama o TTS)
"""
import json, math, shutil, subprocess, sys, time, wave
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import montage  # noqa: E402
import scenes  # noqa: E402

GRADE = {  # leve: as cenas do Grok ja vem com luz de cinema
    "act1": "colorbalance=rs=0.035:gs=0.01:bs=-0.04:rm=0.03:bm=-0.03,eq=saturation=1.04:contrast=1.04",
    "act2": "colorbalance=rs=-0.03:bs=0.04:rm=-0.02:bm=0.03,eq=saturation=0.86:contrast=1.05",
    "act3": "eq=saturation=0.68:contrast=1.12:brightness=-0.01,colorbalance=bs=0.02",
    "after": "eq=saturation=0.92:contrast=0.98:brightness=0.01,colorbalance=rh=0.02:bh=-0.01",
}
VIGNETTE, GRAIN, GRAIN_GFX = "vignette=angle=PI/5", "noise=alls=5:allf=t+u", "noise=alls=3:allf=t+u"
SR = 48000


from timeline import act_of  # noqa: E402  ato gravado na cena ou o corte unico (timeline.py)


class ECJob(montage.Job):
    redo = None  # com --redo 5,46: so essas cenas sao refeitas; as outras reaproveitam work/clip-NN-fx.mp4

    def render_clip(self, i, sc, D, L):
        fx = self.pdir / "work" / f"clip-{i+1:02d}-fx.mp4"
        if self.redo is not None and i + 1 not in self.redo and fx.is_file():
            return fx, None, "reaproveitado"
        src = self.pdir / sc["file"]
        if src.suffix.lower() in (".mp4", ".mov", ".webm") and scenes.kind(sc) != "grafico" and montage.probe_dur(src) < L - 0.05:
            sc = dict(sc, file=self.smooth(i, src).relative_to(self.pdir).as_posix())  # sera desacelerado: quadros reais (RIFE)
        return super().render_clip(i, sc, D, L)

    def smooth(self, i, src):
        """Clipe com o dobro de quadros (RIFE na GPU), em cache por cena e data do arquivo. Sem GPU/RIFE: o original."""
        out = self.pdir / "work" / f"rife-{i+1:02d}-{int(src.stat().st_mtime)}.mp4"
        if out.is_file(): return out
        try:
            sys.path.insert(0, str(Path(__file__).resolve().parent)); import media_ai
            media_ai.rife(src, out, 2); self.log(f"cena {i+1}: camera lenta com RIFE"); return out
        except Exception as e:
            self.log(f"cena {i+1}: RIFE indisponivel ({str(e)[:120]}), desacelerando o original"); return src

    def render_gfx(self):
        self.log("graficos: EffectCraft (tools/ec_gfx.py), ja renderizados")
        return 0, 0

    def apply_overlay(self, i, clip, L):
        sc = self.scenes(); s = sc[i]; ec = s.get("ec") or {}
        full = (ec.get("full") or {}).get("type")
        vf = [GRAIN_GFX] if scenes.kind(s) == "grafico" else [GRADE[act_of(s, i, len(sc))], VIGNETTE, GRAIN]
        chapter = any(e.get("type") == "chapter" for e in ec.get("overlay") or [])
        if i == 0 or chapter:
            vf.append(f"fade=in:st=0:d={0.9 if i == 0 else 0.6}:color=black")   # mergulho no preto
        elif full in ("counter", "stamp"):
            vf.append("fade=in:st=0:d=0.35:color=white")                       # flash no numero de impacto
        if i == len(sc) - 1:
            vf.append(f"fade=out:st={max(0, L - 1.4):.2f}:d=1.4:color=black")
        ov = self.pdir / "gfx" / f"ecov-{i+1:02d}.mov"
        out = clip.with_name(clip.stem + "-fx.mp4")
        args = ["-i", str(clip)]
        if ov.is_file() and ec.get("overlay"):  # o plano manda: sobreposicao tirada do plano nao volta pelo .mov antigo
            args += ["-i", str(ov)]
            fc = f"[0:v]{','.join(vf[:-1] if vf[-1].startswith('fade') else vf)}[b];[1:v]format=rgba[o];[b][o]overlay=eof_action=pass"
            fc += (f",{vf[-1]}" if vf[-1].startswith("fade") else "") + ",format=yuv420p[v]"
        else:
            fc = f"[0:v]{','.join(vf)},format=yuv420p[v]"
        montage.ff(args + ["-filter_complex", fc, "-map", "[v]", "-t", f"{L:.3f}", "-c:v", "libx264", "-preset", "veryfast",
                           "-crf", "16", "-an", "-r", str(self.c["fps"]), str(out)])
        return out

    def timing(self):
        import timeline
        tl = timeline.plan(self.pdir, len(self.scenes()), self.c)
        return tl["D"], tl["starts"]

    # ---------------- design de som ----------------
    def sfx_events(self):
        sc = self.scenes()
        D, starts = self.timing()
        ev = []
        for i, s in enumerate(sc):
            ec, t = s.get("ec") or {}, starts[i]
            f = ec.get("full") or {}
            if f:
                ev.append((t - 0.25, "whoosh", 0.9))
                if f["type"] == "counter":
                    t1 = t + float(f.get("t1", 2.5))  # t1: numero falado (tools/words.py)
                    ev.append((t1 - 0.05, "impact", 0.7))
                    if "$" in f.get("prefix", ""): ev.append((t1 - 1.2, "coins", 0.35))
                if f["type"] == "stamp": ev += [(t + 1.0, "impact", 1.0), (t + 1.0, "stamp", 0.9), (t + 0.1, "paper", 0.5)]
                if f["type"] in ("person", "statement"): ev.append((t + 0.3, "paper", 0.45))
                if f["type"] == "versus": ev += [(t + 2.6, "tick", 0.8), (t + 3.7, "tick", 0.8)]
                if f["type"] == "timeline":
                    n = len(f["events"]); L = D[i] + self.c["crossfade_seconds"]; step = min(0.85, (L - 3.2) / n)
                    ev += [(t + 1.0 + k * step, "tick", 0.7) for k in range(n)]
                if f["type"] == "person": ev.append((t + 0.1, "whoosh", 0.6))
            for e in ec.get("overlay") or []:
                st = e.get("start")
                if e["type"] == "chapter": ev += [(t + 0.1, "impact", 0.45), (t + 0.15, "whoosh", 0.55)]
                elif e["type"] in ("lower_third", "callout", "logo"): ev.append((t + (0.4 if st is None else st), "whoosh", 0.4))
        return ev, sum(D)

    @staticmethod
    def sfx_library():
        """library/sfx/<tipo>/*.ogg|wav -> {tipo: [amostras estereo 48 kHz normalizadas]} (pico -6 dB)."""
        out = {}
        for d in sorted((ROOT / "library" / "sfx").glob("[!_]*")):
            arrs = []
            for f in sorted(d.glob("*")):
                if f.suffix.lower() not in (".ogg", ".wav", ".mp3", ".flac"): continue
                raw = subprocess.run([montage.FFMPEG or shutil.which("ffmpeg"), "-v", "error", "-i", str(f), "-ac", "2", "-ar", str(SR),
                                      "-f", "f32le", "-"], capture_output=True).stdout  # bytes: montage.ff le texto
                if raw: arrs.append(np.frombuffer(raw, np.float32).reshape(-1, 2).copy())
            if arrs: out[d.name] = arrs
        return {k: [a * (0.5 / (np.abs(a).max() + 1e-9)) for a in v] for k, v in out.items()}

    def write_sfx(self, path):
        ev, total = self.sfx_events()
        rng = np.random.default_rng(7)
        buf = np.zeros((int((total + 3) * SR), 2), np.float32)
        def whoosh(d=0.75):
            n = int(d * SR); x = rng.standard_normal(n).astype(np.float32)
            t = np.linspace(0, 1, n); fc = 300 + 2600 * np.sin(np.pi * t) ** 2  # filtro passa-baixa que abre e fecha
            a = 1 - np.exp(-2 * np.pi * fc / SR); y = np.empty(n, np.float32); acc = 0.0
            for k in range(n): acc += a[k] * (x[k] - acc); y[k] = acc
            y -= np.convolve(y, np.ones(64) / 64, "same")  # tira o grave (vira "ar")
            y *= np.sin(np.pi * t) ** 2 * 0.22 / (np.abs(y).max() + 1e-9)
            pan = t  # da esquerda para a direita
            return np.stack([y * (1 - 0.6 * pan), y * (0.4 + 0.6 * pan)], 1)
        def impact(d=1.6):
            n = int(d * SR); t = np.arange(n) / SR
            f = 38 + 60 * np.exp(-t * 9); ph = 2 * np.pi * np.cumsum(f) / SR
            y = np.sin(ph) * np.exp(-t * 3.2) * 0.55
            nz = rng.standard_normal(n) * np.exp(-t * 40) * 0.12
            y = (y + np.convolve(nz, np.ones(24) / 24, "same")).astype(np.float32)
            return np.stack([y, y], 1)
        def tick(d=0.09):
            n = int(d * SR); t = np.arange(n) / SR
            y = (np.sin(2 * np.pi * 1850 * t) * np.exp(-t * 70) * 0.10).astype(np.float32)
            return np.stack([y, y], 1)
        bank = {"whoosh": [whoosh()], "impact": [impact()], "tick": [tick()]}
        for kind, files in self.sfx_library().items(): bank[kind] = files  # sons reais (library/sfx) no lugar dos sintetizados
        for t, kind, g in ev:
            if kind not in bank: continue
            s = bank[kind][int(rng.integers(len(bank[kind])))] * g; a = max(0, int(t * SR)); b = min(len(buf), a + len(s))
            buf[a:b] += s[: b - a]
        pcm = (np.clip(buf, -1, 1) * 32767).astype("<i2")
        with wave.open(str(path), "wb") as w:
            w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
        self.log(f"sfx: {len(ev)} eventos")

    def add_sfx(self):
        final = self.pdir / "output" / "final.mp4"; dry = self.pdir / "output" / "final_nosfx.mp4"
        shutil.move(final, dry)
        sfx = self.pdir / "work" / "sfx.wav"; self.write_sfx(sfx)
        lufs = self.c["loudness_lufs"]
        montage.ff(["-i", str(dry), "-i", str(sfx), "-filter_complex",
                    f"[1:a]volume=0.55[s];[0:a][s]amix=inputs=2:duration=first:normalize=0,loudnorm=I={lufs}:TP=-1.5:LRA=11[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                    "-movflags", "+faststart", str(final)])
        self.log(f"final.mp4 com design de som: {montage.probe_dur(final):.1f}s")

    def mix_cues(self):
        """Musica so onde faz sentido: pj["music_cues"] = [{from_scene, to_scene, file, offset, volume}].
        Fora das deixas, silencio; dentro, a musica abaixa sob a voz (ducking) e sobe nas pausas.
        Refaz so o audio: video de output/final_nosfx.mp4 + work/narration.wav + work/sfx.wav."""
        pj = json.loads(self.pfile.read_text(encoding="utf-8")); cues = pj.get("music_cues") or []
        D, starts = self.timing(); total = sum(D)
        dry, narr, sfx = self.pdir / "output" / "final_nosfx.mp4", self.pdir / "work" / "narration.wav", self.pdir / "work" / "sfx.wav"
        if not sfx.is_file(): self.write_sfx(sfx)
        args = ["-i", str(dry), "-i", str(narr), "-i", str(sfx)]; parts = []
        for k, c in enumerate(cues):
            a = starts[c["from_scene"] - 1]; b = min(total, starts[c["to_scene"] - 1] + D[c["to_scene"] - 1] + float(c.get("tail", 2.5)))
            dur = b - a; fi, fo = float(c.get("fade_in", 1.8)), float(c.get("fade_out", 3.5))
            args += ["-ss", str(c.get("offset", 0)), "-stream_loop", "-1", "-i", str(self.pdir / c["file"])]
            parts.append(f"[{3+k}:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{dur:.3f},asetpts=PTS-STARTPTS,"
                         f"afade=t=in:d={fi},afade=t=out:st={max(0, dur-fo):.3f}:d={fo},volume={float(c.get('volume', 0.17))},"
                         f"adelay={int(a*1000)}|{int(a*1000)}[m{k}]")
        lufs = self.c["loudness_lufs"]
        mix = "".join(f"[m{k}]" for k in range(len(cues)))
        af = (";".join(parts) + f";{mix}amix=inputs={len(cues)}:duration=longest:normalize=0,apad,atrim=0:{total:.3f}[mus];"
              f"[1:a]asplit=2[nar][sc];[mus][sc]sidechaincompress=threshold=0.02:ratio=10:attack=15:release=450:makeup=1[duck];"
              f"[2:a]volume=0.55[s];[nar][duck][s]amix=inputs=3:duration=first:normalize=0,loudnorm=I={lufs}:TP=-1.5:LRA=11[a]")
        final = self.pdir / "output" / "final.mp4"
        montage.ff(args + ["-filter_complex", af, "-map", "0:v", "-map", "[a]", "-t", f"{total:.3f}", "-c:v", "copy",
                           "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", str(final)])
        self.log(f"audio refeito com {len(cues)} deixas musicais: {montage.probe_dur(final):.1f}s")


def main():
    montage.FFMPEG, montage.FFPROBE = montage.which("ffmpeg"), montage.which("ffprobe")
    j = ECJob(sys.argv[1]); t0 = time.time()
    if "--audio-only" in sys.argv:
        j.mix_cues(); return
    if "--redo" in sys.argv:
        j.redo = {int(x) for x in sys.argv[sys.argv.index("--redo") + 1].split(",")}
    j.ctrl_f.write_text("run", encoding="utf-8")
    try:
        j.run_render(); j.add_sfx()
        if json.loads(j.pfile.read_text(encoding="utf-8")).get("music_cues"): j.mix_cues()
        j.save(state="done", progress=100, step="", message=f"Concluido em {time.time()-t0:.0f}s")
    except Exception as e:
        j.save(state="error", message=str(e)[:500]); j.log(f"ERRO: {e}"); raise


if __name__ == "__main__":
    main()
