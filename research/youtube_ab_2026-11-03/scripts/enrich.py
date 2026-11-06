"""Fase 2: videos.list + channels.list em lote (50 ids). Salva raw/videos.json, raw/channels.json e dados_<nicho>.csv."""
import json, csv, re, datetime as dt
from yt import call, OUT

NOW = dt.datetime(2026, 11, 3, 12, tzinfo=dt.timezone.utc)
RAW = OUT / "raw"


def chunks(xs, n=50):
    for i in range(0, len(xs), n):
        yield xs[i:i + n]


def dur_s(iso):
    m = re.match(r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso or "")
    if not m:
        return None
    d, h, mi, s = (int(x or 0) for x in m.groups())
    return d * 86400 + h * 3600 + mi * 60 + s


search = {n: json.loads((RAW / f"search_{n}.json").read_text(encoding="utf-8")) for n in "ABCD"}
vids = sorted({r["videoId"] for rs in search.values() for r in rs})
vcache = json.loads((RAW / "videos.json").read_text(encoding="utf-8")) if (RAW / "videos.json").exists() else {}
todo = [v for v in vids if v not in vcache]
for c in chunks(todo):
    r = call("videos", part="snippet,statistics,contentDetails", id=",".join(c), maxResults=50)
    for it in r.get("items", []):
        vcache[it["id"]] = it
(RAW / "videos.json").write_text(json.dumps(vcache, ensure_ascii=False), encoding="utf-8")

chs = sorted({v["snippet"]["channelId"] for v in vcache.values()})
ccache = json.loads((RAW / "channels.json").read_text(encoding="utf-8")) if (RAW / "channels.json").exists() else {}
todo = [c for c in chs if c not in ccache]
for c in chunks(todo):
    r = call("channels", part="snippet,statistics", id=",".join(c), maxResults=50)
    for it in r.get("items", []):
        ccache[it["id"]] = it
(RAW / "channels.json").write_text(json.dumps(ccache, ensure_ascii=False), encoding="utf-8")

for n, rs in search.items():
    rows, seen = [], set()
    for r in rs:
        vid = r["videoId"]
        if vid in seen or vid not in vcache:
            continue
        seen.add(vid)
        v = vcache[vid]; sn = v["snippet"]; st = v.get("statistics", {})
        ch = ccache.get(sn["channelId"], {}); cst = ch.get("statistics", {}); csn = ch.get("snippet", {})
        pub = dt.datetime.fromisoformat(sn["publishedAt"].replace("Z", "+00:00"))
        days = max((NOW - pub).total_seconds() / 86400, 1.0)
        views = int(st.get("viewCount", 0))
        subs = int(cst["subscriberCount"]) if cst.get("subscriberCount") and not cst.get("hiddenSubscriberCount") else None
        cpub = csn.get("publishedAt")
        cage = (NOW - dt.datetime.fromisoformat(cpub.replace("Z", "+00:00"))).days if cpub else None
        rows.append({
            "niche": n, "query": r["q"], "videoId": vid, "url": f"https://www.youtube.com/watch?v={vid}",
            "title": sn["title"], "lang": sn.get("defaultAudioLanguage") or sn.get("defaultLanguage") or "",
            "publishedAt": sn["publishedAt"][:10], "days": round(days, 1), "duration_s": dur_s(v["contentDetails"].get("duration")),
            "views": views, "views_per_day": round(views / days), "likes": st.get("likeCount", ""),
            "comments": st.get("commentCount", ""),
            "channelId": sn["channelId"], "channel": sn["channelTitle"], "subs": subs if subs is not None else "",
            "ratio_views_subs": round(views / subs, 2) if subs else "",
            "channel_created": cpub[:10] if cpub else "", "channel_age_days": cage,
            "channel_videos": cst.get("videoCount", ""), "channel_views": cst.get("viewCount", ""),
            "channel_country": csn.get("country", ""),
        })
    with open(OUT / f"dados_{n}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print(n, len(rows))
print(json.loads((RAW / "quota.json").read_text()))
