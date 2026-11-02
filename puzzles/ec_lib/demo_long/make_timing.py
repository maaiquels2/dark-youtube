"""Tempo sintetico (sem voz) para testar o layout: narration.json -> assets/timing_raw.json, 0.36 s por palavra.
Uso: python puzzles/ec_lib_next/demo_long/make_timing.py"""
import json
from pathlib import Path

D = Path(__file__).parent
blocks, words, t = [], [], 0.0
for b in json.loads((D / "narration.json").read_text(encoding="utf-8"))["blocks"]:
    blocks.append(round(t, 3)); t += 0.3
    for w in b.split():
        words.append({"w": w, "s": round(t, 3), "e": round(t + 0.3, 3), "ws": " "}); t += 0.36
    t += 0.5
(D / "assets").mkdir(exist_ok=True)
(D / "assets" / "timing_raw.json").write_text(json.dumps({"words": words, "blocks": blocks, "end": round(t, 3)}), encoding="utf-8")
print(len(blocks), "blocos,", len(words), "palavras,", round(t, 1), "s")
