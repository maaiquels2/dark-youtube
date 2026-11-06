"""Fase 4: métricas por canal e vencedores por nicho; baixa thumbs e monta folhas de contato."""
import json, re, statistics as stx, datetime as dt, urllib.request, csv
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
OUT = Path(r"D:\DarkYouTube\research\youtube_ab_2026-11-03"); RAW = OUT / "raw"; TH = OUT / "thumbs"
NOW = dt.datetime(2026, 11, 3, 12, tzinfo=dt.timezone.utc)
up = json.loads((RAW / "uploads.json").read_text(encoding="utf-8"))
chs = json.loads((RAW / "channels.json").read_text(encoding="utf-8"))

def dur_s(iso):
    m = re.match(r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso or "")
    d, h, mi, s = (int(x or 0) for x in m.groups()); return d*86400+h*3600+mi*60+s

channels, videos = [], []
for cid, c in up.items():
    ch = chs[cid]; st = ch["statistics"]; subs = int(st.get("subscriberCount", 0)) or None
    cpub = ch["snippet"]["publishedAt"]; age = (NOW - dt.datetime.fromisoformat(cpub.replace("Z", "+00:00"))).days
    vs = []
    for v in c["items"]:
        pub = dt.datetime.fromisoformat(v["snippet"]["publishedAt"].replace("Z", "+00:00"))
        days = max((NOW - pub).total_seconds()/86400, 1.0); views = int(v["statistics"].get("viewCount", 0))
        vs.append(dict(niche=c["niche"], channel=c["name"], channelId=cid, videoId=v["id"], title=v["snippet"]["title"],
                       publishedAt=v["snippet"]["publishedAt"][:10], days=round(days, 1), dur=dur_s(v["contentDetails"]["duration"]),
                       views=views, vpd=round(views/days), subs=subs, ratio=round(views/subs, 2) if subs else None,
                       thumbs=v["snippet"]["thumbnails"]))
    med = stx.median([x["views"] for x in vs]) if vs else 0
    for x in vs: x["x_median"] = round(x["views"]/med, 2) if med else None
    recent = [x for x in vs if x["days"] <= 90]
    best = max(recent, key=lambda x: x["vpd"]) if recent else None
    shorts = sum(1 for x in vs if x["dur"] <= 180)
    channels.append(dict(niche=c["niche"], channel=c["name"], channelId=cid, url=f"https://www.youtube.com/channel/{cid}",
        created=cpub[:10], age_days=age, subs=subs, total_videos=int(st.get("videoCount", 0)), total_views=int(st.get("viewCount", 0)),
        sample=len(vs), shorts_in_sample=shorts, median_views_sample=round(med), recent90=len(recent),
        recent90_views=sum(x["views"] for x in recent), outliers3x=sum(1 for x in recent if x["ratio"] and x["ratio"] >= 3),
        best_title=best["title"] if best else "", best_views=best["views"] if best else 0, best_vpd=best["vpd"] if best else 0,
        best_ratio=best["ratio"] if best else None))
    videos += recent
json.dump(channels, open(RAW / "channels_summary.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

import sys
if len(sys.argv) > 1 and sys.argv[1] == "pool":
    for n in "ABCD":
        print("=====", n)
        seen = {}
        for v in sorted([v for v in videos if v["niche"] == n], key=lambda v: -v["vpd"]):
            seen[v["channel"]] = seen.get(v["channel"], 0) + 1
            if seen[v["channel"]] > 4: continue
            print(v["videoId"], v["vpd"], v["dur"], v["channel"][:16], "|", v["title"][:70])
    raise SystemExit
WIN = {
 "A": "zhQVjly5Gos FVxmNVMSAhU XEMvG2vulKg 1-vw4UPDgU8 3Hp03-lSQRw Stz7bzbHRV4 zqFOMrzSr9g fycTftKbOTA PZ-DYHQMYsY hYSm3KuL5HE AtTZ2j9dWeg SIgfV-qz06o",
 "B": "eQR3pgMiUF0 LBwJ14rnS9E 1pTBLKdOijA ObrbEBbHX0k uQB9hVNXvLo 5SI7rzF8TII uuPrcgwt6xg zVaIaqRxEyw HhGThyikhxs PgSAg9HAoec gkqQe0qp3SM",
 "C": "qwwf2Dp-DTw w65jbQSq1io 1Ug_sjO1zrA --tDx15MD1k gmA6wSPwjSQ QiTdwT9mjpg ejh9GG17mA0 JakW-D2qSqw ahGr0xaEVUg YWbFyy6mHSY gyOZv_ckZQU",
 "D": "ZfayyZZ29Yc i1S7HJTPaY4 RWw_xsonAR4 DcLfSIcbeT8 b98ZBMjPkwE GsFAL6-2akA p32tBCJ2fGk Y1LbT8mR7ps 71sPZwVD3Fg wqcLSSa8C_M y-onkwEvqwA",
}
byid = {v["videoId"]: v for v in videos}
winners = {n: sorted([byid[i] for i in ids.split()], key=lambda v: -v["vpd"]) for n, ids in WIN.items()}
for n, sel in winners.items():
    for v in sel:
        t = v.pop("thumbs"); u = (t.get("maxres") or t.get("high") or t.get("medium"))["url"]
        v["thumb_url"] = u; f = TH / f"{n}_{v['videoId']}.jpg"; v["thumb_file"] = str(f)
        if not f.exists():
            urllib.request.urlretrieve(u, f)
for v in videos: v.pop("thumbs", None)
json.dump(winners, open(RAW / "winners.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

try: font = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 18)
except Exception: font = ImageFont.load_default()
W, H, cols = 640, 360, 2
for n, sel in winners.items():
    rows = (len(sel)+cols-1)//cols; sheet = Image.new("RGB", (cols*W, rows*(H+30)), "white"); d = ImageDraw.Draw(sheet)
    for i, v in enumerate(sel):
        im = Image.open(v["thumb_file"]).convert("RGB"); im = im.resize((W, H))
        x, y = (i % cols)*W, (i//cols)*(H+30); sheet.paste(im, (x, y))
        d.text((x+6, y+H+5), f"{i+1}. {v['channel'][:22]} | {v['vpd']:,}/dia | {v['title'][:40]}", fill="black", font=font)
    sheet.save(OUT / f"contato_{n}.jpg", quality=85)
print({n: len(s) for n, s in winners.items()})
