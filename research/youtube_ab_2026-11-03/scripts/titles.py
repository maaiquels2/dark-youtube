"""Fase 5: estatística de títulos dos vencedores (raw/winners.json) -> raw/titles.json"""
import json, re, collections, statistics as s
from pathlib import Path
RAW = Path(r"D:\DarkYouTube\research\youtube_ab_2026-11-03\raw")
w = json.load(open(RAW / "winners.json", encoding="utf-8"))
STOP = set("the a an of to in is it and for on at by his her their its with this that you your are be was from who how why what our my me i they he she not just".split())
PAT = {"pergunta (?)": r"\?", "número/valor": r"\d", "How…": r"^how\b", "Why…": r"^why\b", "What Happened/What…": r"^what\b",
       "Rise and Fall / Collapse / Fall": r"rise and fall|collapse|fall of|bankrupt|gone|destroyed|lost everything",
       "consequência/stake (fine, illegal, jail, die…)": r"fine|illegal|jail|die|lose|lost|stolen|kill|fired|quit",
       "reviravolta (—, …, Then, Until)": r"—|…|\.\.\.|\bthen\b|\buntil\b",
       "personagem/adversário (CEO, judge, scammer, manager…)": r"ceo|judge|scammer|manager|boss|owner|doorman|government|fed|trump",
       "MAIÚSCULAS (palavra inteira ≥4 letras)": r"\b[A-Z]{4,}\b", "emoji": r"[\U0001F300-\U0001FAFF\u2600-\u27BF]", "hashtag": r"#"}
out = {}
for n, vs in w.items():
    ts = [v["title"] for v in vs]; clean = [re.sub(r"\s*#\S+", "", t).strip() for t in ts]
    L = [len(t) for t in clean]
    words = collections.Counter(x for t in clean for x in re.findall(r"[a-z']+", t.lower()) if x not in STOP and len(x) > 2)
    out[n] = {"n": len(ts), "len_min": min(L), "len_med": s.median(L), "len_max": max(L), "le60": sum(l <= 60 for l in L),
              "patterns": {k: sum(bool(re.search(p, t, 0 if "MAI" in k else re.I)) for t in clean) for k, p in PAT.items()},
              "top_words": words.most_common(12)}
json.dump(out, open(RAW / "titles.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for n, o in out.items(): print(n, o)
