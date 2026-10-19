# -*- coding: utf-8 -*-
"""Dark Studio - tempo de cada palavra da narracao (Whisper da OpenAI, timestamp por palavra).
Guarda em audio/words.json: {"<cena>": {"sig": "<mtime do mp3>", "words": [{"w","s","e"}]}} (tempo relativo a cena).
Os graficos (tools/ec_gfx.py) e os Shorts (tools/shorts.py) usam isso para entrar na palavra certa.
Uso: python tools/words.py <project_id>
"""
import json, re, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import montage  # noqa: E402  (env_key le o .env)

NUM = {"zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
       "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18,
       "nineteen": 19, "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90}


def norm(w):
    """'Forty-seven,' -> '47'; 'SoftBank's' -> 'softbank'. Numeros por extenso viram digitos para casar com os graficos."""
    w = w.lower().strip(".,;:!?\"'()$%").replace("’s", "").removesuffix("'s")
    parts = w.split("-")
    if parts and all(p in NUM for p in parts): return str(sum(NUM[p] for p in parts))
    return w.replace(",", "")


def transcribe(path, key):
    with open(path, "rb") as f:
        r = requests.post("https://api.openai.com/v1/audio/transcriptions", headers={"Authorization": f"Bearer {key}"},
                          files={"file": (Path(path).name, f, "audio/mpeg")},
                          data={"model": "whisper-1", "response_format": "verbose_json", "timestamp_granularities[]": "word"}, timeout=180)
    r.raise_for_status()
    return [{"w": x["word"], "s": round(x["start"], 3), "e": round(x["end"], 3)} for x in r.json().get("words") or []]


def load(pdir):
    f = Path(pdir) / "audio" / "words.json"
    return json.loads(f.read_text(encoding="utf-8")) if f.is_file() else {}


def run(pid):
    pdir = ROOT / "projects" / pid; key = montage.env_key()
    if not key: sys.exit("OPENAI_API_KEY nao configurada no .env")
    data = load(pdir); mp3s = sorted((pdir / "audio").glob("scene-*.mp3"))
    todo = [p for p in mp3s if data.get(str(int(p.stem[6:])), {}).get("sig") != str(int(p.stat().st_mtime))]
    def work(p):
        return str(int(p.stem[6:])), {"sig": str(int(p.stat().st_mtime)), "words": transcribe(p, key)}
    with ThreadPoolExecutor(4) as ex:
        for n, v in ex.map(work, todo): data[n] = v
    (pdir / "audio" / "words.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return len(todo), len(mp3s)


STOP = set("the a an and or of to in on for by with from at as is was were be its this that not no than into over after before about "
           "per via new say said also more most once ever just".split())


def when(words, text, after=0.0):
    """Primeiro instante (s) em que a narracao diz algo distintivo de `text` (numero, nome, mes, sigla). None se nao achar."""
    toks = {norm(t) for t in re.findall(r"[A-Za-z][A-Za-z'’\-]+|\d[\d.,]*", text or "")}
    toks = {t for t in toks if t and t not in STOP and (t[0].isdigit() or len(t) >= 4)}
    if not toks: return None
    from difflib import SequenceMatcher
    def hit(w):  # nome proprio pode vir grafado diferente pelo Whisper (Neumann/Newman)
        return w in toks or (len(w) >= 5 and any(len(t) >= 5 and not t[0].isdigit() and SequenceMatcher(None, w, t).ratio() >= 0.8 for t in toks))
    for x in words:
        if x["s"] >= after and hit(norm(x["w"])): return x["s"]
    return None


if __name__ == "__main__":
    n, tot = run(sys.argv[1]); print(f"{n} cenas transcritas ({tot} no total)")
