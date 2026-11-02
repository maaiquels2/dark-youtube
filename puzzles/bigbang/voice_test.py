import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT / "tools" / "kokoro_lib"))
import numpy as np, soundfile as sf
from kokoro import KPipeline
TEXT = "The Big Bang was not an explosion in space. It was the expansion of space itself. Thirteen point eight billion years ago, everything we can see was packed into something smaller than an atom."
pipe = KPipeline(lang_code="a", device="cuda")
for v in sys.argv[1:]:
    try:
        a = np.concatenate([r.audio.numpy() for r in pipe(TEXT, voice=v, speed=0.95)])
        sf.write(Path(__file__).parent / "voices" / f"{v}.wav", a, 24000); print(v, round(len(a) / 24000, 1), "s", flush=True)
    except Exception as e: print(v, "ERRO", str(e)[:80], flush=True)
