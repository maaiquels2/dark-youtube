"""Fase 3: últimos 50 uploads de cada canal escolhido (playlistItems = 1 unidade) + videos.list (1 unidade).
Salva raw/uploads.json {channelId: [video,...]}."""
import json, csv
from yt import call, OUT
from picks import PICKS
RAW = OUT / "raw"
cache = json.loads((RAW / "uploads.json").read_text(encoding="utf-8")) if (RAW / "uploads.json").exists() else {}
for n, names in PICKS.items():
    rows = list(csv.DictReader(open(OUT / f"dados_{n}.csv", encoding="utf-8")))
    for nm in names:
        cid = next(r["channelId"] for r in rows if r["channel"].startswith(nm[:20]))
        if cid in cache: continue
        pl = call("playlistItems", part="contentDetails", playlistId="UU" + cid[2:], maxResults=50)
        ids = [it["contentDetails"]["videoId"] for it in pl.get("items", [])]
        vs = call("videos", part="snippet,statistics,contentDetails", id=",".join(ids), maxResults=50) if ids else {"items": []}
        cache[cid] = {"niche": n, "name": nm, "items": vs.get("items", [])}
        print(n, nm, len(ids))
        (RAW / "uploads.json").write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
(RAW / "uploads.json").write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
print(json.loads((RAW / "quota.json").read_text()))
