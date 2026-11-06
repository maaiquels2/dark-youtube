"""Fase 1: search.list por nicho (últimos 90 dias, ordem por views, inglês). Salva raw/search_<nicho>.json."""
import json, sys, datetime as dt
from yt import call, OUT

AFTER = (dt.datetime(2026, 11, 3) - dt.timedelta(days=90)).strftime("%Y-%m-%dT00:00:00Z")

# (consulta, duração) — duração: any/medium/long/short
QUERIES = {
    "A": [("corporate fraud documentary", "any"), ("company collapse explained", "any"),
          ("financial scandal documentary", "any"), ("how this company went bankrupt", "any"),
          ("biggest business fraud", "any"), ("ponzi scheme story", "any"),
          ("billionaire downfall", "any")],
    "B": [("new law explained", "any"), ("scam explained", "any"),
          ("consumer rights explained", "any"), ("why this law exists", "any"),
          ("law changed 2026", "any"), ("scammers exposed", "any"),
          ("illegal now new rule", "short")],
    "C": [("how it works engineering", "short"), ("math puzzle", "short"),
          ("how does it work animation", "short"), ("riddle can you solve", "short"),
          ("engineering explained", "short"), ("whiteboard explanation", "short"),
          ("logic puzzle", "short")],
    "D": [("grandpa advice", "any"), ("old man life advice", "any"),
          ("elderly wisdom life lessons", "any"), ("grandfather story", "any"),
          ("advice from a 90 year old", "any"), ("things I wish I knew when I was young", "any"),
          ("grandpa story", "short")],
}


def run(niche):
    res = []
    for q, dur in QUERIES[niche]:
        r = call("search", part="snippet", q=q, type="video", order="viewCount",
                 publishedAfter=AFTER, relevanceLanguage="en", regionCode="US",
                 maxResults=50, videoDuration=dur)
        for it in r.get("items", []):
            res.append({"q": q, "videoId": it["id"]["videoId"], "channelId": it["snippet"]["channelId"],
                        "title": it["snippet"]["title"], "channelTitle": it["snippet"]["channelTitle"]})
        print(niche, q, len(r.get("items", [])))
    (OUT / "raw" / f"search_{niche}.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    for n in sys.argv[1:]:
        run(n)
