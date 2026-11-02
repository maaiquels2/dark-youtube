"""Kokoro TTS local: <projeto>/narration.json -> <projeto>/assets/voice.wav + timing_raw.json (tempo de cada palavra).
Rodar com: tools/ComfyUI/python_embeded/python.exe puzzles/ec_lib/voice.py <projeto> [voz=am_onyx] [velocidade=0.95]"""
import sys, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT / "tools" / "kokoro_lib"))
import numpy as np, soundfile as sf
from kokoro import KPipeline
D = Path(sys.argv[1]).resolve(); blocks = json.loads((D / "narration.json").read_text(encoding="utf-8"))["blocks"]
VOICE = sys.argv[2] if len(sys.argv) > 2 else "am_onyx"; SPEED = float(sys.argv[3]) if len(sys.argv) > 3 else 0.95
pipe = KPipeline(lang_code="a", device="cuda"); SR = 24000
audio, words, blk, t = [], [], [], 0.0
for text in blocks:
    blk.append(round(t, 3))
    for r in pipe(text, voice=VOICE, speed=SPEED, split_pattern=None):
        a = r.audio.numpy() if hasattr(r.audio, "numpy") else np.asarray(r.audio)
        for tk in (r.tokens or []):
            if tk.start_ts is None or not tk.text.strip(): continue
            words.append({"w": tk.text, "s": round(t + tk.start_ts, 3), "e": round(t + (tk.end_ts or tk.start_ts + .2), 3), "ws": tk.whitespace})
        audio.append(a); t += len(a) / SR
    audio.append(np.zeros(int(SR * 0.35))); t += 0.35
(D / "assets").mkdir(exist_ok=True)
sf.write(D / "assets" / "voice.wav", np.concatenate(audio), SR)
(D / "assets" / "timing_raw.json").write_text(json.dumps({"words": words, "blocks": blk, "end": round(t, 3)}), encoding="utf-8")
print("ok", len(words), "tokens", round(t, 1), "s")
