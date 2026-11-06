"""Fase 1b: consultas extras (anexa a raw/search_<nicho>.json). 9 buscas = 900 unidades."""
import json
from yt import call, OUT
from discover import AFTER
EXTRA = {
    "A": [("rise and fall company documentary", "long")],
    "B": [("law explained", "medium"), ("scam tactics explained", "any"), ("legal loophole explained", "any")],
    "C": [("math riddle", "short"), ("how it works", "short")],
    "D": [("life lessons old age", "any"), ("old man story emotional", "any"), ("wisdom from elders", "any")],
}
for n, qs in EXTRA.items():
    f = OUT / "raw" / f"search_{n}.json"
    res = json.loads(f.read_text(encoding="utf-8"))
    for q, dur in qs:
        r = call("search", part="snippet", q=q, type="video", order="viewCount", publishedAfter=AFTER,
                 relevanceLanguage="en", regionCode="US", maxResults=50, videoDuration=dur)
        for it in r.get("items", []):
            res.append({"q": q, "videoId": it["id"]["videoId"], "channelId": it["snippet"]["channelId"],
                        "title": it["snippet"]["title"], "channelTitle": it["snippet"]["channelTitle"]})
        print(n, q, len(r.get("items", [])))
    f.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
